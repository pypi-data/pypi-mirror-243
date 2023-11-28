import datetime
import multiprocessing
import os
import time

import serial.tools.list_ports

from pyccapt.control.control_tools import experiment_statistics, hdf5_creator, loggi
from pyccapt.control.devices import email_send, initialize_devices, signal_generator
from pyccapt.control.drs import drs
from pyccapt.control.tdc_roentdek import tdc_roentdek
from pyccapt.control.tdc_surface_concept import tdc_surface_consept


class APT_Exp_Control:
    """
    This class is responsible for controlling the experiment.
    """

    def __init__(self, variables, conf, experiment_finished_event, x_plot, y_plot, t_plot, main_v_dc_plot):

        self.variables = variables
        self.conf = conf
        self.experiment_finished_event = experiment_finished_event
        self.x_plot = x_plot
        self.y_plot = y_plot
        self.t_plot = t_plot
        self.main_v_dc_plot = main_v_dc_plot

        self.com_port_v_p = None
        self.log_apt = None
        self.variables.start_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        self.sleep_time = 1 / self.variables.ex_freq

        self.detection_rate = 0
        self.specimen_voltage = 0
        self.pulse_voltage = 0
        self.count_last = 0
        self.vdc_max = 0
        self.pulse_frequency = 0
        self.pulse_fraction = 0
        self.pulse_amp_per_supply_voltage = 0
        self.pulse_voltage_max = 0
        self.pulse_voltage_min = 0
        self.total_ions = 0
        self.ex_freq = 0

        self.main_v_dc = []
        self.main_v_p = []
        self.main_counter = []
        self.main_temperature = []
        self.main_chamber_vacuum = []

        self.initialization_error = False

    def initialize_detector_process(self):
        """
        Initialize the detector process based on the configured settings.

        This method initializes the necessary queues and processes for data acquisition based on the configured settings.

        Args:
           None

        Returns:
           None
        """
        if self.conf['tdc'] == "on" and self.conf['tdc_model'] == 'Surface_Consept' \
                and self.variables.counter_source == 'TDC':

            # Initialize and initiate a process(Refer to imported file 'tdc_new' for process function declaration )
            # Module used: multiprocessing
            self.tdc_process = multiprocessing.Process(target=tdc_surface_consept.experiment_measure,
                                                       args=(self.variables, self.x_plot, self.y_plot, self.t_plot,
                                                             self.main_v_dc_plot,))

            self.tdc_process.start()

        elif self.conf['tdc'] == "on" and self.conf[
            'tdc_model'] == 'RoentDek' and self.variables.counter_source == 'TDC':

            self.tdc_process = multiprocessing.Process(target=tdc_roentdek.experiment_measure,
                                                       args=(self.variables,))
            self.tdc_process.start()

        elif self.conf['tdc'] == "on" and self.conf['tdc_model'] == 'HSD' and self.variables.counter_source == 'HSD':

            # Initialize and initiate a process(Refer to imported file 'drs' for process function declaration)
            # Module used: multiprocessing
            self.hsd_process = multiprocessing.Process(target=drs.experiment_measure,
                                                       args=(self.variables,))
            self.hsd_process.start()

        else:
            print("No counter source selected")

    def initialize_v_dc(self):
        """
        Initialize the V_dc source.

        This function initializes the V_dc source by configuring the COM port settings and sending commands to set
        the parameters.

        Args:
            None

        Returns:
            None
        """
        self.com_port_v_dc = serial.Serial(
            port=self.variables.COM_PORT_V_dc,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )

        if self.com_port_v_dc.is_open:
            self.com_port_v_dc.flushInput()
            self.com_port_v_dc.flushOutput()

            cmd_list = [">S1 3.0e-4", ">S0B 0", ">S0 %s" % self.variables.vdc_min, "F0", ">S0?", ">DON?", ">S0A?"]
            for cmd in range(len(cmd_list)):
                self.command_v_dc(cmd_list[cmd])
        else:
            print("Couldn't open Port!")
            exit()

    def initialize_v_p(self):
        """
        Initialize the Pulser device.

        This method initializes the Pulser device using the Visa library.

        Args:
            None

        Returns:
            None
        """
        self.com_port_v_p = serial.Serial(self.variables.COM_PORT_V_p, baudrate=115200, timeout=0.01)

        self.command_v_p('*RST')

    def command_v_p(self, cmd):
        """
        Send commands to the pulser.

        This method sends commands to the pulser over the COM port and reads the response.

        Args:
            cmd (str): The command to send.

        Returns:
            str: The response received from the device.
        """
        cmd = cmd + '\r\n'
        self.com_port_v_p.write(cmd.encode())
        # response = self.com_port_v_p.readline().decode().strip()
        # return response

    def command_v_dc(self, cmd):
        """
        Send commands to the high voltage parameter: v_dc.

        This method sends commands to the V_dc source over the COM port and reads the response.

        Args:
            cmd (str): The command to send.

        Returns:
            str: The response received from the device.
        """
        self.com_port_v_dc.write((cmd + '\r\n').encode())
        # response = ''
        # try:
        #     while self.com_port_v_dc.in_waiting > 0:
        #         response = self.com_port_v_dc.readline()
        # except Exception as error:
        #     print(error)
        #
        # if isinstance(response, bytes):
        #     response = response.decode("utf-8")

        # return response

    def main_ex_loop(self, ):
        """
        Execute main experiment loop.

        This method contains all methods that iteratively run to control the experiment. It reads the number of detected
        ions, calculates the error of the desired rate, and regulates the high voltage and pulser accordingly.

        Args:
            None

        Returns:
            None
        """
        # Update total_ions based on the counter_source...
        # Calculate count_temp and update variables...
        # Save high voltage, pulse, and current iteration ions...
        # Calculate counts_measured and counts_error...
        # Perform proportional control with averaging...
        # Update v_dc and v_p...
        # Update other experiment variables...

        # with self.variables.lock_statistics:
        count_temp = self.total_ions - self.count_last
        self.count_last = self.total_ions

        # saving the values of high dc voltage, pulse, and current iteration ions
        # with self.variables.lock_experiment_variables:
        self.main_v_dc.extend([self.specimen_voltage])
        self.main_v_p.extend([self.pulse_voltage])
        self.main_counter.extend([count_temp])
        self.main_temperature.extend([self.variables.temperature])
        self.main_chamber_vacuum.extend([self.variables.vacuum_main])

        error = self.detection_rate - self.variables.detection_rate_current
        # simple proportional control with averaging
        if error > 0.05:
            voltage_step = error * self.variables.vdc_step_up * 10
        elif error < -0.05:
            voltage_step = error * self.variables.vdc_step_down * 10
        else:
            voltage_step = 0

        if voltage_step > 40:
            print('voltage step is too high: %s' % voltage_step)
            voltage_step = 40

        # update v_dc
        if not self.variables.vdc_hold and voltage_step != 0:
            specimen_voltage_temp = min(self.specimen_voltage + voltage_step, self.vdc_max)
            if specimen_voltage_temp != self.specimen_voltage:
                if self.conf['v_dc'] != "off":
                    self.command_v_dc(">S0 %s" % specimen_voltage_temp)
                    self.specimen_voltage = specimen_voltage_temp
                    self.variables.specimen_voltage = self.specimen_voltage
                    self.variables.specimen_voltage_plot = self.specimen_voltage

                new_vp = self.specimen_voltage * self.pulse_fraction * (1 / self.pulse_amp_per_supply_voltage)
                if self.pulse_voltage_max > new_vp > self.pulse_voltage_min and self.conf['v_p'] != "off":
                    self.command_v_p('VOLT %s' % new_vp)
                    self.pulse_voltage = new_vp * self.pulse_amp_per_supply_voltage
                    self.variables.pulse_voltage = self.pulse_voltage

    def precise_sleep(self, seconds):
        """
        Precise sleep function.

        Args:
            seconds:    Seconds to sleep

        Returns:
            None
        """
        start_time = time.perf_counter()
        while time.perf_counter() - start_time < seconds:
            pass

    def run_experiment(self):
        """
        Run the main experiment.

        This method initializes devices, starts the experiment loop, monitors various criteria, and manages experiment
        stop conditions and data storage.

        Returns:
            None
        """
        self.variables.flag_visualization_start = True

        if os.path.exists("./files/counter_experiments.txt"):
            # Read the experiment counter
            with open('./files/counter_experiments.txt') as f:
                self.variables.counter = int(f.readlines()[0])
        else:
            # create a new txt file
            with open('./files/counter_experiments.txt', 'w') as f:
                f.write(str(1))  # Current time and date
        now = datetime.datetime.now()
        self.variables.exp_name = "%s_" % self.variables.counter + \
                                  now.strftime("%b-%d-%Y_%H-%M") + "_%s" % self.variables.hdf5_data_name
        p = os.path.abspath(os.path.join(__file__, "../../.."))
        self.variables.path = os.path.join(p, 'data\\%s' % self.variables.exp_name)
        self.variables.path_meta = self.variables.path + '\\meta_data\\'

        self.variables.log_path = self.variables.path_meta
        # Create folder to save the data
        if not os.path.isdir(self.variables.path):
            try:
                os.makedirs(self.variables.path, mode=0o777, exist_ok=True)
            except Exception as e:
                print('Can not create the directory for saving the data')
                print(e)
                self.variables.stop_flag = True
                self.initialization_error = True
                self.log_apt.info('Experiment is terminated')
        if not os.path.isdir(self.variables.path_meta):
            try:
                os.makedirs(self.variables.path_meta, mode=0o777, exist_ok=True)
            except:
                print('Can not create the directory for saving the data')
                self.variables.stop_flag = True
                self.initialization_error = True
                self.log_apt.info('Experiment is terminated')

        if self.conf['tdc'] == 'on':
            self.initialize_detector_process()

        self.log_apt = loggi.logger_creator('apt', self.variables, 'apt.log', path=self.variables.log_path)
        if self.conf['signal_generator'] == 'on':
            # Initialize the signal generator
            try:
                signal_generator.initialize_signal_generator(self.variables, self.variables.pulse_frequency)
                self.log_apt.info('Signal generator is initialized')
            except Exception as e:
                self.log_apt.info('Signal generator is not initialized')
                print('Can not initialize the signal generator')
                print('Make the signal_generator off in the config file or fix the error below')
                print(e)
                self.variables.stop_flag = True
                self.initialization_error = True
                self.log_apt.info('Experiment is terminated')

        if self.conf['v_dc'] == 'on':
            try:
                # Initialize high voltage
                self.initialize_v_dc()
                self.log_apt.info('High voltage is initialized')
            except Exception as e:
                self.log_apt.info('High voltage is  not initialized')
                print('Can not initialize the high voltage')
                print('Make the v_dc off in the config file or fix the error below')
                print(e)
                self.variables.stop_flag = True
                self.initialization_error = True
                self.log_apt.info('Experiment is terminated')

        if self.conf['v_p'] == 'on':
            try:
                # Initialize pulser
                self.initialize_v_p()
                self.log_apt.info('Pulser is initialized')
            except Exception as e:
                self.log_apt.info('Pulser is not initialized')
                print('Can not initialize the pulser')
                print('Make the v_p off in the config file or fix the error below')
                print(e)
                self.variables.stop_flag = True
                self.initialization_error = True
                self.log_apt.info('Experiment is terminated')

        self.variables.specimen_voltage = self.variables.vdc_min
        self.variables.pulse_voltage_min = self.variables.v_p_min * (1 / self.variables.pulse_amp_per_supply_voltage)
        self.variables.pulse_voltage_max = self.variables.v_p_max * (1 / self.variables.pulse_amp_per_supply_voltage)
        self.variables.pulse_voltage = self.variables.v_p_min

        time_ex = []
        time_counter = []

        steps = 0
        flag_achieved_high_voltage = 0
        index_time = 0

        desired_rate = self.variables.ex_freq  # Hz
        desired_period = 1.0 / desired_rate  # seconds
        self.counts_target = self.variables.pulse_frequency * 1000 * self.variables.detection_rate / 100

        # Turn on the v_dc and v_p
        if not self.initialization_error:
            if self.conf['v_p'] == "on":
                self.command_v_p('OUTPut ON')
                vol = self.variables.v_p_min / self.variables.pulse_amp_per_supply_voltage
                cmd = 'VOLT %s' % vol
                self.command_v_p(cmd)
                self.com_port_v_p.write(cmd.encode())
                time.sleep(0.1)
            if self.conf['v_dc'] == "on":
                self.command_v_dc("F1")
                time.sleep(0.1)

        self.pulse_frequency = self.variables.pulse_frequency * 1000
        self.pulse_fraction = self.variables.pulse_fraction
        self.pulse_amp_per_supply_voltage = self.variables.pulse_amp_per_supply_voltage
        self.specimen_voltage = self.variables.specimen_voltage
        self.pulse_voltage = self.variables.pulse_voltage
        counter_source = self.variables.counter_source
        self.ex_freq = self.variables.ex_freq

        # Wait for 8 second to all devices get ready specially tdc
        time.sleep(8)
        self.log_apt.info('Experiment is started')
        # Main loop of experiment
        remaining_time_list = []

        if self.initialization_error:
            pass
        else:
            while True:
                start_time = time.perf_counter()
                self.vdc_max = self.variables.vdc_max
                self.vdc_min = self.variables.vdc_min
                self.pulse_voltage_min = self.variables.v_p_min / self.pulse_amp_per_supply_voltage
                self.pulse_voltage_max = self.variables.v_p_max / self.pulse_amp_per_supply_voltage
                self.total_ions = self.variables.total_ions
                self.detection_rate = self.variables.detection_rate

                if self.variables.flag_new_min_voltage:
                    if self.variables.vdc_hold:
                        decrement_vol = (self.specimen_voltage - self.vdc_min) / 10
                        for _ in range(10):
                            self.specimen_voltage -= decrement_vol
                            if self.conf['v_dc'] != "off":
                                self.command_v_dc(">S0 %s" % self.specimen_voltage)
                            time.sleep(0.3)

                        new_vp = self.specimen_voltage * self.pulse_fraction / self.pulse_amp_per_supply_voltage
                        if self.pulse_voltage_max > new_vp > self.pulse_voltage_min and self.conf['v_p'] != "off":
                            self.command_v_p('VOLT %s' % new_vp)
                        self.pulse_voltage = new_vp * self.pulse_amp_per_supply_voltage

                        self.variables.specimen_voltage = self.specimen_voltage
                        self.variables.specimen_voltage_plot = self.specimen_voltage
                        self.variables.pulse_voltage = self.pulse_voltage
                        self.variables.flag_new_min_voltage = False

                # main loop function
                self.main_ex_loop()

                # Counter of iteration
                time_counter.append(steps)

                # Measure time
                current_time = datetime.datetime.now()
                current_time_with_microseconds = current_time.strftime(
                    "%Y-%m-%d %H:%M:%S.%f")  # Format with microseconds
                current_time_unix = datetime.datetime.strptime(current_time_with_microseconds,
                                                               "%Y-%m-%d %H:%M:%S.%f").timestamp()
                time_ex.append(current_time_unix)

                if self.variables.stop_flag:
                    self.log_apt.info('Experiment is stopped')
                    if self.conf['tdc'] != "off":
                        if self.variables.counter_source == 'TDC':
                            self.variables.flag_stop_tdc = True
                    time.sleep(1)
                    break

                if self.variables.flag_tdc_failure:
                    self.log_apt.info('Experiment is stopped because of tdc failure')
                    if self.conf['tdc'] == "on":
                        if self.variables.counter_source == 'TDC':
                            self.variables.stop_flag = True  # Set the STOP flag
                    time.sleep(1)
                    break

                if self.variables.criteria_ions:
                    if self.variables.max_ions <= self.total_ions:
                        self.log_apt.info('Experiment is stopped because total number of ions is achieved')
                        if self.conf['tdc'] == "on":
                            if self.variables.counter_source == 'TDC':
                                self.variables.flag_stop_tdc = True
                                self.variables.stop_flag = True  # Set the STOP flag
                        time.sleep(1)
                        break
                if self.variables.criteria_vdc:
                    if self.vdc_max <= self.specimen_voltage:
                        if flag_achieved_high_voltage > self.ex_freq * 10:
                            self.log_apt.info('Experiment is stopped because dc voltage Max. is achieved')
                            if self.conf['tdc'] != "off":
                                if self.variables.counter_source == 'TDC':
                                    self.variables.flag_stop_tdc = True
                                    self.variables.stop_flag = True  # Set the STOP flag
                            time.sleep(1)
                            break
                        flag_achieved_high_voltage += 1

                if self.variables.criteria_time:
                    if self.variables.elapsed_time >= self.variables.ex_time:
                        self.log_apt.info('Experiment is stopped because experiment time Max. is achieved')
                        if self.conf['tdc'] == "on":
                            if self.variables.counter_source == 'TDC':
                                self.variables.flag_stop_tdc = True
                                self.variables.stop_flag = True

                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                remaining_time = desired_period - elapsed_time

                if remaining_time > 0:
                    self.precise_sleep(remaining_time)
                elif remaining_time < 0:
                    index_time += 1
                    remaining_time_list.append(elapsed_time)

                steps += 1

        self.variables.start_flag = False  # Set the START flag
        time.sleep(1)

        self.log_apt.info('Experiment is finished')
        print("Experiment loop took longer than %s Millisecond for %s times out of %s "
              "iteration" % (int(1000 / self.variables.ex_freq), index_time, steps))
        self.log_apt.warning(
            'Experiment loop took longer than %s (ms) for %s times out of %s iteration.'
            % (int(1000 / self.variables.ex_freq), index_time, steps))

        print('Waiting for TDC process to be finished for maximum 60 seconds...')
        for i in range(60):
            if self.variables.flag_finished_tdc:
                print('TDC process is finished')
                break
            print(i)
            time.sleep(1)

        if self.conf['tdc'] == "on":
            # Stop the TDC process
            try:
                if self.variables.counter_source == 'TDC':
                    self.tdc_process.join(2)
                    if self.tdc_process.is_alive():
                        self.tdc_process.join(1)
                elif self.variables.counter_source == 'HSD':
                    self.hsd_process.join(2)
                    if self.hsd_process.is_alive():
                        self.hsd_process.join(1)

            except Exception as e:
                print(
                    f"{initialize_devices.bcolors.WARNING}Warning: The TDC or HSD process cannot be terminated "
                    f"properly{initialize_devices.bcolors.ENDC}")
                print(e)

        self.variables.extend_to('main_v_dc', self.main_v_dc)
        self.variables.extend_to('main_v_p', self.main_v_p)
        self.variables.extend_to('main_counter', self.main_counter)
        self.variables.extend_to('main_temperature', self.main_temperature)
        self.variables.extend_to('main_chamber_vacuum', self.main_chamber_vacuum)

        time.sleep(1)
        if self.conf['tdc'] != "off":
            # Stop the TDC process
            try:
                if self.variables.counter_source == 'TDC':
                    self.tdc_process.join(3)
                    if self.tdc_process.is_alive():
                        self.tdc_process.join(2)
                        # Release all the resources of the TDC process
                elif self.variables.counter_source == 'HSD':
                    self.hsd_process.join(3)
                    if self.hsd_process.is_alive():
                        self.hsd_process.join(2)
                        # Release all the resources of the TDC process
                print('TDC process is joined')
            except Exception as e:
                print(
                    f"{initialize_devices.bcolors.WARNING}Warning: The TDC or HSD process cannot be terminated "
                    f"properly{initialize_devices.bcolors.ENDC}")
                print(e)

        if self.conf['tdc'] == "off":
            if self.variables.counter_source == 'TDC':
                self.variables.total_ions = len(self.variables.x)
        elif self.variables.counter_source == 'HSD':
            pass

        # Check the length of arrays to be equal
        if self.variables.counter_source == 'TDC':
            if all(len(lst) == len(self.variables.x) for lst in [self.variables.x, self.variables.y,
                                                                 self.variables.t, self.variables.dld_start_counter,
                                                                 self.variables.main_v_dc_dld,
                                                                 self.variables.main_p_dld]):
                self.log_apt.warning('dld data have not same length')

            if all(len(lst) == len(self.variables.channel) for lst in [self.variables.channel, self.variables.time_data,
                                                                       self.variables.tdc_start_counter,
                                                                       self.variables.main_v_dc_tdc,
                                                                       self.variables.main_p_tdc]):
                self.log_apt.warning('tdc data have not same length')
        elif self.variables.counter_source == 'DRS':
            if all(len(lst) == len(self.variables.ch0_time) for lst in
                   [self.variables.ch0_wave, self.variables.ch1_time,
                    self.variables.ch1_wave, self.variables.ch2_time,
                    self.variables.ch2_wave, self.variables.ch3_time,
                    self.variables.ch3_wave,
                    self.variables.main_v_dc_drs, self.variables.main_v_p_drs]):
                self.log_apt.warning('tdc data have not same length')

        self.variables.end_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        # save data in hdf5 file
        hdf5_creator.hdf_creator(self.variables, self.conf, time_counter, time_ex)
        # Adding results of the experiment to the log file
        self.log_apt.info('Total number of Ions is: %s' % self.variables.total_ions)
        self.log_apt.info('HDF5 file is created')

        # Save new value of experiment counter
        if os.path.exists("./files/counter_experiments.txt"):
            with open('./files/counter_experiments.txt', 'w') as f:
                f.write(str(self.variables.counter + 1))
                self.log_apt.info('Experiment counter is increased')

        # save setup parameters and run statistics in a txt file
        experiment_statistics.save_statistics_apt(self.variables, self.conf)

        # send an email
        if len(self.variables.email) > 3:
            subject = 'Experiment {} Report on {}'.format(self.variables.hdf5_data_name, self.variables.start_time)
            elapsed_time_temp = float("{:.3f}".format(self.variables.elapsed_time))
            message = 'The experiment was started at: {}\n' \
                      'The experiment was ended at: {}\n' \
                      'Experiment duration: {}\n' \
                      'Total number of ions: {}\n\n'.format(self.variables.start_time,
                                                            self.variables.end_time, elapsed_time_temp,
                                                            self.variables.total_ions)

            additional_info = 'Username: {}\n'.format(self.variables.user_name)
            additional_info += 'Experiment Name: {}\n'.format(self.variables.ex_name)
            additional_info += 'Detection Rate (%): {}\n'.format(self.variables.detection_rate)
            additional_info += 'Maximum Number of Ions: {}\n'.format(self.variables.max_ions)
            additional_info += 'Counter source: {}\n'.format(self.variables.counter_source)
            additional_info += 'Pulse Fraction (%): {}\n'.format(self.variables.pulse_fraction)
            additional_info += 'Pulse Frequency (kHz): {}\n'.format(self.variables.pulse_frequency)
            additional_info += 'Control Algorithm: {}\n'.format(self.variables.control_algorithm)
            additional_info += 'pulse_mode: {}\n'.format(self.variables.pulse_mode)
            additional_info += 'Experiment Control Refresh freq. (Hz): {}\n'.format(self.variables.ex_freq)
            additional_info += 'K_p Upwards: {}\n'.format(self.variables.vdc_step_up)
            additional_info += 'K_p Downwards: {}\n'.format(self.variables.vdc_step_down)
            additional_info += 'Specimen start Voltage (V): {}\n'.format(self.variables.vdc_min)
            additional_info += 'Specimen Stop Voltage (V): {}\n'.format(self.variables.vdc_max)
            additional_info += 'Temperature (C): {}\n'.format(self.variables.temperature)
            additional_info += 'Vacuum (mbar): {}\n'.format(self.variables.vacuum_main)

            if self.variables.pulse_mode == 'Voltage':
                additional_info += 'Pulse start Voltage (V): {}\n'.format(self.variables.v_p_min)
                additional_info += 'Pulse Stop Voltage (V): {}\n'.format(self.variables.v_p_max)
                additional_info += 'Specimen Max Achieved Pulse Voltage (V): {:.3f}\n\n'.format(
                    self.variables.pulse_voltage)
            additional_info += 'StopCriteria:\n'
            additional_info += 'Criteria Time:: {}\n'.format(self.variables.criteria_time)
            additional_info += 'Criteria DC Voltage:: {}\n'.format(self.variables.criteria_vdc)
            additional_info += 'Criteria Ions:: {}\n'.format(self.variables.criteria_ions)


            additional_info += 'Specimen Max Achieved dc Voltage (V): {:.3f}\n'.format(self.variables.specimen_voltage)
            additional_info += 'Experiment Elapsed Time (Sec): {:.3f}\n'.format(self.variables.elapsed_time)
            additional_info += 'Experiment Total Ions: {}\n\n'.format(self.variables.total_ions)

            additional_info += 'Email: {}\n'.format(self.variables.email)

            additional_info += 'The experiment was conducted using PyCCAPT Python package.'

            message += additional_info
            email_send.send_email(self.variables.email, subject, message)
            self.log_apt.info('Email is sent')

        self.experiment_finished_event.set()
        # Clear up all the variables and deinitialize devices
        self.clear_up()
        self.log_apt.info('Variables and devices are cleared and deinitialized')
        self.variables.flag_end_experiment = True

    def clear_up(self):
        """
        Clear class variables, deinitialize high voltage and pulser, and reset variables.

        This method performs the cleanup operations at the end of the experiment. It turns off the high voltage,
        pulser, and signal generator, resets global variables, and performs other cleanup tasks.

        Args:
            None

        Returns:
            None
        """

        def cleanup_variables():
            """
            Reset all the global variables.
            """
            self.variables.vdc_hold = False
            self.variables.flag_finished_tdc = False
            self.variables.detection_rate_current = 0.0
            self.variables.count = 0
            self.variables.index_plot = 0
            self.variables.index_save_image = 0
            self.variables.index_wait_on_plot_start = 0
            self.variables.index_plot_save = 0
            self.variables.index_plot = 0
            self.variables.specimen_voltage = 0
            self.variables.specimen_voltage_plot = 0
            self.variables.pulse_voltage = 0

            while not self.x_plot.empty() or not self.y_plot.empty() or not self.t_plot.empty() or \
                    not self.main_v_dc_plot.empty():
                dumy = self.x_plot.get()
                dumy = self.y_plot.get()
                dumy = self.t_plot.get()
                dumy = self.main_v_dc_plot.get()

            self.variables.clear_to('x')
            self.variables.clear_to('y')
            self.variables.clear_to('t')

            self.variables.clear_to('channel')
            self.variables.clear_to('time_data')
            self.variables.clear_to('tdc_start_counter')
            self.variables.clear_to('dld_start_counter')

            self.variables.clear_to('time_stamp')
            self.variables.clear_to('ch0')
            self.variables.clear_to('ch1')
            self.variables.clear_to('ch2')
            self.variables.clear_to('ch3')
            self.variables.clear_to('ch4')
            self.variables.clear_to('ch5')
            self.variables.clear_to('ch6')
            self.variables.clear_to('ch7')
            self.variables.clear_to('laser_intensity')

            self.variables.clear_to('ch0_time')
            self.variables.clear_to('ch0_wave')
            self.variables.clear_to('ch1_time')
            self.variables.clear_to('ch1_wave')
            self.variables.clear_to('ch2_time')
            self.variables.clear_to('ch2_wave')
            self.variables.clear_to('ch3_time')
            self.variables.clear_to('ch3_wave')

            self.variables.clear_to('main_v_dc')
            self.variables.clear_to('main_v_p')
            self.variables.clear_to('main_counter')
            self.variables.clear_to('main_temperature')
            self.variables.clear_to('main_chamber_vacuum')
            self.variables.clear_to('main_v_dc_dld')
            self.variables.clear_to('main_p_dld')
            self.variables.clear_to('main_v_dc_tdc')
            self.variables.clear_to('main_p_tdc')
            self.variables.clear_to('main_v_dc_drs')
            self.variables.clear_to('main_v_p_drs')

        self.log_apt.info('Starting cleanup')

        try:
            if self.conf['v_dc'] != "off":
                # Turn off the v_dc
                self.command_v_dc('F0')
                self.com_port_v_dc.close()
        except:
            pass

        try:
            if self.conf['v_p'] == "on":
                # Turn off the v_p
                self.command_v_p('VOLT 0')
                self.command_v_p('OUTPut OFF')
                self.com_port_v_p.close()
        except:
            pass

        try:
            if self.conf['signal_generator'] != "off":
                # Turn off the signal generator
                signal_generator.turn_off_signal_generator()

        except:
            pass

        # Reset variables
        cleanup_variables()
        self.log_apt.info('Cleanup is finished')


def run_experiment(variables, conf, experiment_finished_event, x_plot, y_plot, t_plot, main_v_dc_plot):
    """
    Run the main experiment.

    Args:
        variables:                  Global variables
        conf:                       Configuration dictionary
        experiment_finished_event:  Event to signal the end of the experiment
        x_plot:                     Array to store x data
        y_plot:                     Array to store y data
        t_plot:                     Array to store t data
        main_v_dc_plot:             Array to store main_v_dc data

    Returns:
        None

    """

    # from line_profiler import LineProfiler
    #
    # lp1 = LineProfiler()
    #
    # # Run the experiment
    # apt_exp_control = APT_Exp_Control(variables, conf, experiment_finished_event, x_plot, y_plot, t_plot,
    #                                   main_v_dc_plot, counter_plot, lock)
    #
    # lp1.add_function(apt_exp_control.run_experiment)
    #
    # lp1.add_function(apt_exp_control.main_ex_loop)
    #
    # # Run the profiler
    # lp1(apt_exp_control.run_experiment)()
    # # Save the profiling result to a file
    # lp1.dump_stats('run_experiment.lprof')

    apt_exp_control = APT_Exp_Control(variables, conf, experiment_finished_event, x_plot, y_plot, t_plot,
                                      main_v_dc_plot)

    apt_exp_control.run_experiment()
