import os

import numpy as np

from pyccapt.calibration.calibration_tools import share_variables
from pyccapt.calibration.data_tools import data_tools
from pyccapt.calibration.mc import tof_tools


def load_data(dataset_path, max_mc, flightPathLength, pulse_mode, tdc):
	# Calculate the maximum possible time of flight (TOF)
	max_tof = int(tof_tools.mc2tof(max_mc, 1000, 0, 0, flightPathLength))
	print('The maximum possible TOF is:', max_tof, 'ns')
	print('=============================')
	# create an instance of the Variables opject
	variables = share_variables.Variables()
	variables.pulse_mode = pulse_mode
	dataset_main_path = os.path.dirname(dataset_path)
	dataset_name_with_extention = os.path.basename(dataset_path)
	variables.dataset_name = os.path.splitext(dataset_name_with_extention)[0]
	variables.result_data_path = dataset_main_path + '/' + variables.dataset_name + '/data_processing/'
	variables.result_data_name = variables.dataset_name
	variables.result_path = dataset_main_path + '/' + variables.dataset_name + '/data_processing/'

	if not os.path.isdir(variables.result_path):
		os.makedirs(variables.result_path, mode=0o777, exist_ok=True)

	print('The data will be saved on the path:', variables.result_data_path)
	print('=============================')
	print('The dataset name after saving is:', variables.result_data_name)
	print('=============================')
	print('The figures will be saved on the path:', variables.result_path)
	print('=============================')

	# Create data farame out of hdf5 file dataset
	dld_group_storage = data_tools.load_data(dataset_path, tdc, mode='raw')

	# Remove the data with tof greater thatn Max TOF or below 0 ns
	data = data_tools.remove_invalid_data(dld_group_storage, max_tof)
	print('Total number of Ions:', len(data))

	variables.data = data
	variables.data_backup = data.copy()
	variables.max_mc = max_mc
	variables.max_tof = max_tof
	variables.flight_path_length = flightPathLength
	variables.pulse_mode = pulse_mode

	return variables


def add_columns(variables, max_mc):
	variables.data.drop(['x (nm)', 'y (nm)', 'z (nm)', 'mc (Da)', 'mc_c (Da)', 't_c (ns)'], axis=1, errors='ignore',
	                    inplace=True)

	variables.data.insert(0, 'x (nm)', np.zeros(len(variables.dld_t)))
	variables.data.insert(1, 'y (nm)', np.zeros(len(variables.dld_t)))
	variables.data.insert(2, 'z (nm)', np.zeros(len(variables.dld_t)))
	variables.data.insert(3, 'mc_c (Da)', np.zeros(len(variables.dld_t)))
	variables.data.insert(4, 'mc (Da)', variables.mc)
	variables.data.insert(8, 't_c (ns)', np.zeros(len(variables.dld_t)))

	# Remove the data with mc biger than max mc
	mask = (variables.data['mc (Da)'].to_numpy() > max_mc.value)
	print('The number of data over max_mc:', len(mask[mask == True]))
	variables.data.drop(np.where(mask)[0], inplace=True)
	variables.data.reset_index(inplace=True, drop=True)

	# Remove the data with x,y,t = 0
	mask1 = (variables.data['x (nm)'].to_numpy() == 0)
	mask2 = (variables.data['y (nm)'].to_numpy() == 0)
	mask3 = (variables.data['t (ns)'].to_numpy() == 0)
	mask = np.logical_and(mask1, mask2)
	mask = np.logical_and(mask, mask3)
	print('The number of data with having t, x, and y equal to zero is:', len(mask[mask == True]))
	variables.data.drop(np.where(mask)[0], inplace=True)
	variables.data.reset_index(inplace=True, drop=True)
	variables.data_backup = variables.data.copy()
