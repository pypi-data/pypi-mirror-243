import multiprocessing
import os
import re
import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt

# Local module and scripts
from pyccapt.control.apt import apt_exp_control
from pyccapt.control.control_tools import share_variables, read_files
from pyccapt.control.gui import gui_baking, gui_cameras, gui_gates, gui_laser_control, gui_pumps_vacuum, \
	gui_stage_control, gui_visualization


class Ui_PyCCAPT(object):

	def __init__(self, variables, conf, x_plot, y_plot, t_plot, main_v_dc_plot):
		"""
		Constructor for the PyCCAPT UI class.

		Args:
				variables (object): Global experiment variables.
				conf (dict): Configuration settings.
				parent: Parent widget (optional).

		Returns:
				None
		"""
		self.conf = conf
		self.variables = variables
		self.emitter = SignalEmitter()
		self.x_plot = x_plot
		self.y_plot = y_plot
		self.t_plot = t_plot
		self.main_v_dc_plot = main_v_dc_plot
		self.experiment_running = False
		self.experimetn_finished_event = multiprocessing.Event()
		self.camera_closed_event = multiprocessing.Event()
		self.visualization_closed_event = multiprocessing.Event()
		self.camera_win_front = multiprocessing.Event()
		self.visualization_win_front = multiprocessing.Event()

	def setupUi(self, PyCCAPT):
		PyCCAPT.setObjectName("PyCCAPT")
		PyCCAPT.resize(905, 873)
		self.centralwidget = QtWidgets.QWidget(PyCCAPT)
		self.centralwidget.setObjectName("centralwidget")
		self.gridLayout_5 = QtWidgets.QGridLayout(self.centralwidget)
		self.gridLayout_5.setObjectName("gridLayout_5")
		self.gridLayout_4 = QtWidgets.QGridLayout()
		self.gridLayout_4.setObjectName("gridLayout_4")
		self.horizontalLayout = QtWidgets.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.gates_control = QtWidgets.QPushButton(self.centralwidget)
		self.gates_control.setMinimumSize(QtCore.QSize(0, 40))
		self.gates_control.setStyleSheet("QPushButton{\n"
		                                 "                                                background: rgb(85, 170, 255)\n"
		                                 "                                                }\n"
		                                 "                                            ")
		self.gates_control.setObjectName("gates_control")
		self.horizontalLayout.addWidget(self.gates_control)
		self.pumps_vaccum = QtWidgets.QPushButton(self.centralwidget)
		self.pumps_vaccum.setMinimumSize(QtCore.QSize(0, 40))
		self.pumps_vaccum.setStyleSheet("QPushButton{\n"
		                                "                                                background: rgb(85, 170, 255)\n"
		                                "                                                }\n"
		                                "                                            ")
		self.pumps_vaccum.setObjectName("pumps_vaccum")
		self.horizontalLayout.addWidget(self.pumps_vaccum)
		self.camears = QtWidgets.QPushButton(self.centralwidget)
		self.camears.setMinimumSize(QtCore.QSize(0, 40))
		self.camears.setStyleSheet("QPushButton{\n"
		                           "                                                background: rgb(85, 170, 255)\n"
		                           "                                                }\n"
		                           "                                            ")
		self.camears.setObjectName("camears")
		self.horizontalLayout.addWidget(self.camears)
		self.laser_control = QtWidgets.QPushButton(self.centralwidget)
		self.laser_control.setMinimumSize(QtCore.QSize(0, 40))
		self.laser_control.setSizeIncrement(QtCore.QSize(0, 0))
		self.laser_control.setStyleSheet("QPushButton{\n"
		                                 "                                                background: rgb(85, 170, 255)\n"
		                                 "                                                }\n"
		                                 "                                            ")
		self.laser_control.setObjectName("laser_control")
		self.horizontalLayout.addWidget(self.laser_control)
		self.stage_control = QtWidgets.QPushButton(self.centralwidget)
		self.stage_control.setMinimumSize(QtCore.QSize(0, 40))
		self.stage_control.setSizeIncrement(QtCore.QSize(0, 0))
		self.stage_control.setStyleSheet("QPushButton{\n"
		                                 "                                                background: rgb(85, 170, 255)\n"
		                                 "                                                }\n"
		                                 "                                            ")
		self.stage_control.setObjectName("stage_control")
		self.horizontalLayout.addWidget(self.stage_control)
		self.visualization = QtWidgets.QPushButton(self.centralwidget)
		self.visualization.setMinimumSize(QtCore.QSize(0, 40))
		self.visualization.setSizeIncrement(QtCore.QSize(0, 0))
		self.visualization.setStyleSheet("QPushButton{\n"
		                                 "                                                background: rgb(85, 170, 255)\n"
		                                 "                                                }\n"
		                                 "                                            ")
		self.visualization.setObjectName("visualization")
		self.horizontalLayout.addWidget(self.visualization)
		self.baking = QtWidgets.QPushButton(self.centralwidget)
		self.baking.setMinimumSize(QtCore.QSize(0, 40))
		self.baking.setSizeIncrement(QtCore.QSize(0, 0))
		self.baking.setStyleSheet("QPushButton{\n"
		                          "                                                background: rgb(85, 170, 255)\n"
		                          "                                                }\n"
		                          "                                            ")
		self.baking.setObjectName("baking")
		self.horizontalLayout.addWidget(self.baking)
		self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 2)
		self.text_line = QtWidgets.QTextEdit(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
		                                   QtWidgets.QSizePolicy.Policy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.text_line.sizePolicy().hasHeightForWidth())
		self.text_line.setSizePolicy(sizePolicy)
		self.text_line.setMinimumSize(QtCore.QSize(0, 100))
		self.text_line.setStyleSheet("QWidget{\n"
		                             "                                        border: 2px solid gray;\n"
		                             "                                        border-radius: 10px;\n"
		                             "                                        padding: 0 8px;\n"
		                             "                                        background: rgb(223,223,233)\n"
		                             "                                        }\n"
		                             "                                    ")
		self.text_line.setObjectName("text_line")
		self.gridLayout_4.addWidget(self.text_line, 1, 1, 1, 1)
		self.gridLayout_3 = QtWidgets.QGridLayout()
		self.gridLayout_3.setObjectName("gridLayout_3")
		self.gridLayout_2 = QtWidgets.QGridLayout()
		self.gridLayout_2.setObjectName("gridLayout_2")
		self.Error = QtWidgets.QLabel(self.centralwidget)
		self.Error.setMinimumSize(QtCore.QSize(800, 30))
		font = QtGui.QFont()
		font.setPointSize(13)
		font.setBold(True)
		font.setStrikeOut(False)
		self.Error.setFont(font)
		self.Error.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		self.Error.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse)
		self.Error.setObjectName("Error")
		self.gridLayout_2.addWidget(self.Error, 0, 0, 1, 2)
		self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 2, 1)
		self.start_button = QtWidgets.QPushButton(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.start_button.sizePolicy().hasHeightForWidth())
		self.start_button.setSizePolicy(sizePolicy)
		self.start_button.setMinimumSize(QtCore.QSize(0, 25))
		self.start_button.setStyleSheet("QPushButton{\n"
		                                "                                                background: rgb(193, 193, 193)\n"
		                                "                                                }\n"
		                                "                                            ")
		self.start_button.setObjectName("start_button")
		self.gridLayout_3.addWidget(self.start_button, 0, 1, 1, 1)
		self.stop_button = QtWidgets.QPushButton(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.stop_button.sizePolicy().hasHeightForWidth())
		self.stop_button.setSizePolicy(sizePolicy)
		self.stop_button.setMinimumSize(QtCore.QSize(0, 25))
		self.stop_button.setStyleSheet("QPushButton{\n"
		                               "                                                background: rgb(193, 193, 193)\n"
		                               "                                                }\n"
		                               "                                            ")
		self.stop_button.setObjectName("stop_button")
		self.gridLayout_3.addWidget(self.stop_button, 1, 1, 1, 1)
		self.gridLayout_4.addLayout(self.gridLayout_3, 2, 0, 1, 2)
		self.gridLayout = QtWidgets.QGridLayout()
		self.gridLayout.setObjectName("gridLayout")
		self.detection_rate = QtWidgets.QLineEdit(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.detection_rate.sizePolicy().hasHeightForWidth())
		self.detection_rate.setSizePolicy(sizePolicy)
		self.detection_rate.setMinimumSize(QtCore.QSize(0, 20))
		self.detection_rate.setStyleSheet("QLineEdit{\n"
		                                  "                                                background: rgb(223,223,233)\n"
		                                  "                                                }\n"
		                                  "                                            ")
		self.detection_rate.setText("")
		self.detection_rate.setObjectName("detection_rate")
		self.gridLayout.addWidget(self.detection_rate, 25, 5, 1, 2)
		self.criteria_time = QtWidgets.QCheckBox(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.criteria_time.sizePolicy().hasHeightForWidth())
		self.criteria_time.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setItalic(False)
		self.criteria_time.setFont(font)
		self.criteria_time.setMouseTracking(True)
		self.criteria_time.setStyleSheet("")
		self.criteria_time.setText("")
		self.criteria_time.setChecked(True)
		self.criteria_time.setObjectName("criteria_time")
		self.gridLayout.addWidget(self.criteria_time, 3, 5, 1, 1)
		self.vp_max = QtWidgets.QLineEdit(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.vp_max.sizePolicy().hasHeightForWidth())
		self.vp_max.setSizePolicy(sizePolicy)
		self.vp_max.setMinimumSize(QtCore.QSize(0, 20))
		self.vp_max.setStyleSheet("QLineEdit{\n"
		                          "                                                background: rgb(223,223,233)\n"
		                          "                                                }\n"
		                          "                                            ")
		self.vp_max.setObjectName("vp_max")
		self.gridLayout.addWidget(self.vp_max, 13, 6, 1, 1)
		self.label_179 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_179.sizePolicy().hasHeightForWidth())
		self.label_179.setSizePolicy(sizePolicy)
		self.label_179.setObjectName("label_179")
		self.gridLayout.addWidget(self.label_179, 6, 0, 1, 3)
		self.label_189 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_189.sizePolicy().hasHeightForWidth())
		self.label_189.setSizePolicy(sizePolicy)
		self.label_189.setObjectName("label_189")
		self.gridLayout.addWidget(self.label_189, 17, 0, 1, 1)
		self.label_181 = QtWidgets.QLabel(self.centralwidget)
		self.label_181.setObjectName("label_181")
		self.gridLayout.addWidget(self.label_181, 8, 0, 1, 1)
		self.vdc_min = QtWidgets.QLineEdit(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.vdc_min.sizePolicy().hasHeightForWidth())
		self.vdc_min.setSizePolicy(sizePolicy)
		self.vdc_min.setMinimumSize(QtCore.QSize(0, 20))
		self.vdc_min.setStyleSheet("QLineEdit{\n"
		                           "                                                background: rgb(223,223,233)\n"
		                           "                                                }\n"
		                           "                                            ")
		self.vdc_min.setObjectName("vdc_min")
		self.gridLayout.addWidget(self.vdc_min, 6, 6, 1, 1)
		self.label_180 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_180.sizePolicy().hasHeightForWidth())
		self.label_180.setSizePolicy(sizePolicy)
		self.label_180.setObjectName("label_180")
		self.gridLayout.addWidget(self.label_180, 7, 0, 1, 3)
		self.dc_hold = QtWidgets.QPushButton(self.centralwidget)
		self.dc_hold.setMinimumSize(QtCore.QSize(0, 20))
		self.dc_hold.setObjectName("dc_hold")
		self.gridLayout.addWidget(self.dc_hold, 23, 2, 1, 3)
		self.label_193 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_193.sizePolicy().hasHeightForWidth())
		self.label_193.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setBold(True)
		self.label_193.setFont(font)
		self.label_193.setObjectName("label_193")
		self.gridLayout.addWidget(self.label_193, 20, 0, 1, 1)
		self.hit_displayed = QtWidgets.QLineEdit(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.hit_displayed.sizePolicy().hasHeightForWidth())
		self.hit_displayed.setSizePolicy(sizePolicy)
		self.hit_displayed.setMinimumSize(QtCore.QSize(0, 20))
		self.hit_displayed.setStyleSheet("QLineEdit{\n"
		                                 "                                                background: rgb(223,223,233)\n"
		                                 "                                                }\n"
		                                 "                                            ")
		self.hit_displayed.setObjectName("hit_displayed")
		self.gridLayout.addWidget(self.hit_displayed, 17, 6, 1, 1)
		self.control_algorithm = QtWidgets.QComboBox(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.control_algorithm.sizePolicy().hasHeightForWidth())
		self.control_algorithm.setSizePolicy(sizePolicy)
		self.control_algorithm.setMinimumSize(QtCore.QSize(0, 20))
		self.control_algorithm.setStyleSheet("QComboBox{\n"
		                                     "                                                background: rgb(223,223,233)\n"
		                                     "                                                }\n"
		                                     "                                            ")
		self.control_algorithm.setObjectName("control_algorithm")
		self.control_algorithm.addItem("")
		self.control_algorithm.addItem("")
		self.gridLayout.addWidget(self.control_algorithm, 10, 6, 1, 1)
		self.pulse_voltage = QtWidgets.QLineEdit(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.pulse_voltage.sizePolicy().hasHeightForWidth())
		self.pulse_voltage.setSizePolicy(sizePolicy)
		self.pulse_voltage.setMinimumSize(QtCore.QSize(0, 20))
		self.pulse_voltage.setStyleSheet("QLineEdit{\n"
		                                 "                                                background: rgb(223,223,233)\n"
		                                 "                                                }\n"
		                                 "                                            ")
		self.pulse_voltage.setText("")
		self.pulse_voltage.setObjectName("pulse_voltage")
		self.gridLayout.addWidget(self.pulse_voltage, 24, 5, 1, 2)
		self.label_196 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_196.sizePolicy().hasHeightForWidth())
		self.label_196.setSizePolicy(sizePolicy)
		self.label_196.setObjectName("label_196")
		self.gridLayout.addWidget(self.label_196, 23, 0, 1, 1)
		self.ex_name = QtWidgets.QLineEdit(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.ex_name.sizePolicy().hasHeightForWidth())
		self.ex_name.setSizePolicy(sizePolicy)
		self.ex_name.setMinimumSize(QtCore.QSize(0, 20))
		self.ex_name.setMaximumSize(QtCore.QSize(16777215, 100))
		self.ex_name.setStyleSheet("QLineEdit{\n"
		                           "                                                background: rgb(223,223,233)\n"
		                           "                                                }\n"
		                           "                                            ")
		self.ex_name.setObjectName("ex_name")
		self.gridLayout.addWidget(self.ex_name, 2, 6, 1, 1)
		self.email = QtWidgets.QLineEdit(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.email.sizePolicy().hasHeightForWidth())
		self.email.setSizePolicy(sizePolicy)
		self.email.setMinimumSize(QtCore.QSize(0, 20))
		self.email.setStyleSheet("QLineEdit{\n"
		                         "                                                background: rgb(223,223,233)\n"
		                         "                                                }\n"
		                         "                                            ")
		self.email.setText("")
		self.email.setObjectName("email")
		self.gridLayout.addWidget(self.email, 18, 6, 1, 1)
		self.label_190 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_190.sizePolicy().hasHeightForWidth())
		self.label_190.setSizePolicy(sizePolicy)
		self.label_190.setObjectName("label_190")
		self.gridLayout.addWidget(self.label_190, 18, 0, 1, 1)
		self.vp_min = QtWidgets.QLineEdit(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.vp_min.sizePolicy().hasHeightForWidth())
		self.vp_min.setSizePolicy(sizePolicy)
		self.vp_min.setMinimumSize(QtCore.QSize(0, 20))
		self.vp_min.setStyleSheet("QLineEdit{\n"
		                          "                                                background: rgb(223,223,233)\n"
		                          "                                                }\n"
		                          "                                            ")
		self.vp_min.setObjectName("vp_min")
		self.gridLayout.addWidget(self.vp_min, 12, 6, 1, 1)
		self.criteria_vdc = QtWidgets.QCheckBox(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.criteria_vdc.sizePolicy().hasHeightForWidth())
		self.criteria_vdc.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setItalic(False)
		self.criteria_vdc.setFont(font)
		self.criteria_vdc.setMouseTracking(True)
		self.criteria_vdc.setStyleSheet("")
		self.criteria_vdc.setText("")
		self.criteria_vdc.setChecked(True)
		self.criteria_vdc.setObjectName("criteria_vdc")
		self.gridLayout.addWidget(self.criteria_vdc, 7, 5, 1, 1)
		self.label_199 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_199.sizePolicy().hasHeightForWidth())
		self.label_199.setSizePolicy(sizePolicy)
		self.label_199.setObjectName("label_199")
		self.gridLayout.addWidget(self.label_199, 11, 0, 1, 1)
		self.elapsed_time = QtWidgets.QLineEdit(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.elapsed_time.sizePolicy().hasHeightForWidth())
		self.elapsed_time.setSizePolicy(sizePolicy)
		self.elapsed_time.setMinimumSize(QtCore.QSize(0, 20))
		self.elapsed_time.setStyleSheet("QLineEdit{\n"
		                                "                                                background: rgb(223,223,233)\n"
		                                "                                                }\n"
		                                "                                            ")
		self.elapsed_time.setText("")
		self.elapsed_time.setObjectName("elapsed_time")
		self.gridLayout.addWidget(self.elapsed_time, 21, 5, 1, 2)
		self.label_186 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_186.sizePolicy().hasHeightForWidth())
		self.label_186.setSizePolicy(sizePolicy)
		self.label_186.setObjectName("label_186")
		self.gridLayout.addWidget(self.label_186, 14, 0, 1, 1)
		self.pulse_fraction = QtWidgets.QLineEdit(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.pulse_fraction.sizePolicy().hasHeightForWidth())
		self.pulse_fraction.setSizePolicy(sizePolicy)
		self.pulse_fraction.setMinimumSize(QtCore.QSize(0, 20))
		self.pulse_fraction.setStyleSheet("QLineEdit{\n"
		                                  "                                                background: rgb(223,223,233)\n"
		                                  "                                                }\n"
		                                  "                                            ")
		self.pulse_fraction.setObjectName("pulse_fraction")
		self.gridLayout.addWidget(self.pulse_fraction, 14, 6, 1, 1)
		self.label_177 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_177.sizePolicy().hasHeightForWidth())
		self.label_177.setSizePolicy(sizePolicy)
		self.label_177.setObjectName("label_177")
		self.gridLayout.addWidget(self.label_177, 4, 0, 1, 1)
		self.pulse_frequency = QtWidgets.QLineEdit(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.pulse_frequency.sizePolicy().hasHeightForWidth())
		self.pulse_frequency.setSizePolicy(sizePolicy)
		self.pulse_frequency.setMinimumSize(QtCore.QSize(0, 20))
		self.pulse_frequency.setStyleSheet("QLineEdit{\n"
		                                   "                                                background: rgb(223,223,233)\n"
		                                   "                                                }\n"
		                                   "                                            ")
		self.pulse_frequency.setObjectName("pulse_frequency")
		self.gridLayout.addWidget(self.pulse_frequency, 15, 6, 1, 1)
		self.vdc_steps_down = QtWidgets.QLineEdit(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.vdc_steps_down.sizePolicy().hasHeightForWidth())
		self.vdc_steps_down.setSizePolicy(sizePolicy)
		self.vdc_steps_down.setMinimumSize(QtCore.QSize(0, 20))
		self.vdc_steps_down.setStyleSheet("QLineEdit{\n"
		                                  "                                                background: rgb(223,223,233)\n"
		                                  "                                                }\n"
		                                  "                                            ")
		self.vdc_steps_down.setObjectName("vdc_steps_down")
		self.gridLayout.addWidget(self.vdc_steps_down, 9, 6, 1, 1)
		self.label_2 = QtWidgets.QLabel(self.centralwidget)
		self.label_2.setObjectName("label_2")
		self.gridLayout.addWidget(self.label_2, 4, 4, 1, 1)
		self.label_184 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_184.sizePolicy().hasHeightForWidth())
		self.label_184.setSizePolicy(sizePolicy)
		self.label_184.setObjectName("label_184")
		self.gridLayout.addWidget(self.label_184, 12, 0, 1, 1)
		self.label_174 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_174.sizePolicy().hasHeightForWidth())
		self.label_174.setSizePolicy(sizePolicy)
		self.label_174.setObjectName("label_174")
		self.gridLayout.addWidget(self.label_174, 1, 0, 1, 1)
		self.counter_source = QtWidgets.QComboBox(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.counter_source.sizePolicy().hasHeightForWidth())
		self.counter_source.setSizePolicy(sizePolicy)
		self.counter_source.setMinimumSize(QtCore.QSize(0, 20))
		self.counter_source.setStyleSheet("QComboBox{\n"
		                                  "                                                background: rgb(223,223,233)\n"
		                                  "                                                }\n"
		                                  "                                            ")
		self.counter_source.setObjectName("counter_source")
		self.counter_source.addItem("")
		self.counter_source.addItem("")
		self.gridLayout.addWidget(self.counter_source, 19, 6, 1, 1)
		self.speciemen_voltage = QtWidgets.QLineEdit(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.speciemen_voltage.sizePolicy().hasHeightForWidth())
		self.speciemen_voltage.setSizePolicy(sizePolicy)
		self.speciemen_voltage.setMinimumSize(QtCore.QSize(0, 20))
		self.speciemen_voltage.setStyleSheet("QLineEdit{\n"
		                                     "                                                background: rgb(223,223,233)\n"
		                                     "                                                }\n"
		                                     "                                            ")
		self.speciemen_voltage.setText("")
		self.speciemen_voltage.setObjectName("speciemen_voltage")
		self.gridLayout.addWidget(self.speciemen_voltage, 23, 5, 1, 2)
		self.label_187 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_187.sizePolicy().hasHeightForWidth())
		self.label_187.setSizePolicy(sizePolicy)
		self.label_187.setObjectName("label_187")
		self.gridLayout.addWidget(self.label_187, 15, 0, 1, 1)
		self.ex_time = QtWidgets.QLineEdit(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.ex_time.sizePolicy().hasHeightForWidth())
		self.ex_time.setSizePolicy(sizePolicy)
		self.ex_time.setMinimumSize(QtCore.QSize(0, 20))
		self.ex_time.setStyleSheet("QLineEdit{\n"
		                           "                                                background: rgb(223,223,233)\n"
		                           "                                                }\n"
		                           "                                            ")
		self.ex_time.setObjectName("ex_time")
		self.gridLayout.addWidget(self.ex_time, 3, 6, 1, 1)
		self.total_ions = QtWidgets.QLineEdit(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.total_ions.sizePolicy().hasHeightForWidth())
		self.total_ions.setSizePolicy(sizePolicy)
		self.total_ions.setMinimumSize(QtCore.QSize(0, 20))
		self.total_ions.setStyleSheet("QLineEdit{\n"
		                              "                                                background: rgb(223,223,233)\n"
		                              "                                                }\n"
		                              "                                            ")
		self.total_ions.setText("")
		self.total_ions.setObjectName("total_ions")
		self.gridLayout.addWidget(self.total_ions, 22, 5, 1, 2)
		self.pulse_mode = QtWidgets.QComboBox(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.pulse_mode.sizePolicy().hasHeightForWidth())
		self.pulse_mode.setSizePolicy(sizePolicy)
		self.pulse_mode.setMinimumSize(QtCore.QSize(0, 20))
		self.pulse_mode.setStyleSheet("QComboBox{\n"
		                              "                                                background: rgb(223,223,233)\n"
		                              "                                                }\n"
		                              "                                            ")
		self.pulse_mode.setObjectName("pulse_mode")
		self.pulse_mode.addItem("")
		self.pulse_mode.addItem("")
		self.gridLayout.addWidget(self.pulse_mode, 11, 6, 1, 1)
		self.ex_freq = QtWidgets.QLineEdit(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.ex_freq.sizePolicy().hasHeightForWidth())
		self.ex_freq.setSizePolicy(sizePolicy)
		self.ex_freq.setMinimumSize(QtCore.QSize(0, 20))
		self.ex_freq.setStyleSheet("QLineEdit{\n"
		                           "                                                background: rgb(223,223,233)\n"
		                           "                                                }\n"
		                           "                                            ")
		self.ex_freq.setObjectName("ex_freq")
		self.gridLayout.addWidget(self.ex_freq, 5, 6, 1, 1)
		self.label_194 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_194.sizePolicy().hasHeightForWidth())
		self.label_194.setSizePolicy(sizePolicy)
		self.label_194.setObjectName("label_194")
		self.gridLayout.addWidget(self.label_194, 21, 0, 1, 1)
		self.criteria_ions = QtWidgets.QCheckBox(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.criteria_ions.sizePolicy().hasHeightForWidth())
		self.criteria_ions.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setItalic(False)
		self.criteria_ions.setFont(font)
		self.criteria_ions.setMouseTracking(True)
		self.criteria_ions.setStyleSheet("")
		self.criteria_ions.setText("")
		self.criteria_ions.setChecked(True)
		self.criteria_ions.setObjectName("criteria_ions")
		self.gridLayout.addWidget(self.criteria_ions, 4, 5, 1, 1)
		self.label_176 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_176.sizePolicy().hasHeightForWidth())
		self.label_176.setSizePolicy(sizePolicy)
		self.label_176.setObjectName("label_176")
		self.gridLayout.addWidget(self.label_176, 3, 0, 1, 2)
		self.label_3 = QtWidgets.QLabel(self.centralwidget)
		self.label_3.setObjectName("label_3")
		self.gridLayout.addWidget(self.label_3, 7, 4, 1, 1)
		self.hitmap_plot_size = QtWidgets.QDoubleSpinBox(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.hitmap_plot_size.sizePolicy().hasHeightForWidth())
		self.hitmap_plot_size.setSizePolicy(sizePolicy)
		self.hitmap_plot_size.setMinimumSize(QtCore.QSize(0, 20))
		self.hitmap_plot_size.setStyleSheet("QDoubleSpinBox{\n"
		                                    "                                                background: rgb(223,223,233)\n"
		                                    "                                                }\n"
		                                    "                                            ")
		self.hitmap_plot_size.setObjectName("hitmap_plot_size")
		self.gridLayout.addWidget(self.hitmap_plot_size, 17, 1, 1, 3)
		self.label_188 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_188.sizePolicy().hasHeightForWidth())
		self.label_188.setSizePolicy(sizePolicy)
		self.label_188.setObjectName("label_188")
		self.gridLayout.addWidget(self.label_188, 16, 0, 1, 1)
		self.label_185 = QtWidgets.QLabel(self.centralwidget)
		self.label_185.setObjectName("label_185")
		self.gridLayout.addWidget(self.label_185, 13, 0, 1, 2)
		self.ex_user = QtWidgets.QLineEdit(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.ex_user.sizePolicy().hasHeightForWidth())
		self.ex_user.setSizePolicy(sizePolicy)
		self.ex_user.setMinimumSize(QtCore.QSize(0, 20))
		self.ex_user.setStyleSheet("QLineEdit{\n"
		                           "                                                background: rgb(223,223,233)\n"
		                           "                                                }\n"
		                           "                                            ")
		self.ex_user.setObjectName("ex_user")
		self.gridLayout.addWidget(self.ex_user, 1, 6, 1, 1)
		self.reset_heatmap = QtWidgets.QPushButton(self.centralwidget)
		self.reset_heatmap.setMinimumSize(QtCore.QSize(0, 20))
		self.reset_heatmap.setObjectName("reset_heatmap")
		self.gridLayout.addWidget(self.reset_heatmap, 17, 4, 1, 2)
		self.label_192 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_192.sizePolicy().hasHeightForWidth())
		self.label_192.setSizePolicy(sizePolicy)
		self.label_192.setObjectName("label_192")
		self.gridLayout.addWidget(self.label_192, 19, 0, 1, 1)
		self.label_173 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_173.sizePolicy().hasHeightForWidth())
		self.label_173.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setBold(True)
		self.label_173.setFont(font)
		self.label_173.setObjectName("label_173")
		self.gridLayout.addWidget(self.label_173, 0, 0, 1, 1)
		self.label_191 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_191.sizePolicy().hasHeightForWidth())
		self.label_191.setSizePolicy(sizePolicy)
		self.label_191.setObjectName("label_191")
		self.gridLayout.addWidget(self.label_191, 10, 0, 1, 1)
		self.label_175 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_175.sizePolicy().hasHeightForWidth())
		self.label_175.setSizePolicy(sizePolicy)
		self.label_175.setObjectName("label_175")
		self.gridLayout.addWidget(self.label_175, 2, 0, 1, 1)
		self.label = QtWidgets.QLabel(self.centralwidget)
		self.label.setObjectName("label")
		self.gridLayout.addWidget(self.label, 3, 4, 1, 1)
		self.parameters_source = QtWidgets.QComboBox(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.parameters_source.sizePolicy().hasHeightForWidth())
		self.parameters_source.setSizePolicy(sizePolicy)
		self.parameters_source.setMinimumSize(QtCore.QSize(0, 20))
		self.parameters_source.setStyleSheet("QComboBox{\n"
		                                     "                                                background: rgb(223,223,233)\n"
		                                     "                                                }\n"
		                                     "                                            ")
		self.parameters_source.setObjectName("parameters_source")
		self.parameters_source.addItem("")
		self.parameters_source.addItem("")
		self.gridLayout.addWidget(self.parameters_source, 0, 6, 1, 1)
		self.max_ions = QtWidgets.QLineEdit(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.max_ions.sizePolicy().hasHeightForWidth())
		self.max_ions.setSizePolicy(sizePolicy)
		self.max_ions.setMinimumSize(QtCore.QSize(0, 20))
		self.max_ions.setStyleSheet("QLineEdit{\n"
		                            "                                                background: rgb(223,223,233)\n"
		                            "                                                }\n"
		                            "                                            ")
		self.max_ions.setObjectName("max_ions")
		self.gridLayout.addWidget(self.max_ions, 4, 6, 1, 1)
		self.vdc_max = QtWidgets.QLineEdit(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.vdc_max.sizePolicy().hasHeightForWidth())
		self.vdc_max.setSizePolicy(sizePolicy)
		self.vdc_max.setMinimumSize(QtCore.QSize(0, 20))
		self.vdc_max.setStyleSheet("QLineEdit{\n"
		                           "                                                background: rgb(223,223,233)\n"
		                           "                                                }\n"
		                           "                                            ")
		self.vdc_max.setObjectName("vdc_max")
		self.gridLayout.addWidget(self.vdc_max, 7, 6, 1, 1)
		self.label_198 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_198.sizePolicy().hasHeightForWidth())
		self.label_198.setSizePolicy(sizePolicy)
		self.label_198.setObjectName("label_198")
		self.gridLayout.addWidget(self.label_198, 25, 0, 1, 1)
		self.label_182 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_182.sizePolicy().hasHeightForWidth())
		self.label_182.setSizePolicy(sizePolicy)
		self.label_182.setObjectName("label_182")
		self.gridLayout.addWidget(self.label_182, 9, 0, 1, 1)
		self.vdc_steps_up = QtWidgets.QLineEdit(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.vdc_steps_up.sizePolicy().hasHeightForWidth())
		self.vdc_steps_up.setSizePolicy(sizePolicy)
		self.vdc_steps_up.setMinimumSize(QtCore.QSize(0, 20))
		self.vdc_steps_up.setStyleSheet("QLineEdit{\n"
		                                "                                                background: rgb(223,223,233)\n"
		                                "                                                }\n"
		                                "                                            ")
		self.vdc_steps_up.setObjectName("vdc_steps_up")
		self.gridLayout.addWidget(self.vdc_steps_up, 8, 6, 1, 1)
		self.label_197 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_197.sizePolicy().hasHeightForWidth())
		self.label_197.setSizePolicy(sizePolicy)
		self.label_197.setObjectName("label_197")
		self.gridLayout.addWidget(self.label_197, 24, 0, 1, 1)
		self.label_178 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_178.sizePolicy().hasHeightForWidth())
		self.label_178.setSizePolicy(sizePolicy)
		self.label_178.setObjectName("label_178")
		self.gridLayout.addWidget(self.label_178, 5, 0, 1, 2)
		self.detection_rate_init = QtWidgets.QLineEdit(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.detection_rate_init.sizePolicy().hasHeightForWidth())
		self.detection_rate_init.setSizePolicy(sizePolicy)
		self.detection_rate_init.setMinimumSize(QtCore.QSize(0, 20))
		self.detection_rate_init.setStyleSheet("QLineEdit{\n"
		                                       "                                                background: rgb(223,223,233)\n"
		                                       "                                                }\n"
		                                       "                                            ")
		self.detection_rate_init.setObjectName("detection_rate_init")
		self.gridLayout.addWidget(self.detection_rate_init, 16, 6, 1, 1)
		self.label_195 = QtWidgets.QLabel(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_195.sizePolicy().hasHeightForWidth())
		self.label_195.setSizePolicy(sizePolicy)
		self.label_195.setObjectName("label_195")
		self.gridLayout.addWidget(self.label_195, 22, 0, 1, 1)
		self.set_min_voltage = QtWidgets.QPushButton(self.centralwidget)
		self.set_min_voltage.setMinimumSize(QtCore.QSize(0, 20))
		self.set_min_voltage.setObjectName("set_min_voltage")
		self.gridLayout.addWidget(self.set_min_voltage, 6, 3, 1, 1)
		self.gridLayout_4.addLayout(self.gridLayout, 1, 0, 1, 1)
		self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 1)
		PyCCAPT.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(PyCCAPT)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 905, 22))
		self.menubar.setObjectName("menubar")
		self.menuFile = QtWidgets.QMenu(self.menubar)
		self.menuFile.setObjectName("menuFile")
		self.menuEdit = QtWidgets.QMenu(self.menubar)
		self.menuEdit.setObjectName("menuEdit")
		self.menuHelp = QtWidgets.QMenu(self.menubar)
		self.menuHelp.setObjectName("menuHelp")
		self.menuSettings = QtWidgets.QMenu(self.menubar)
		self.menuSettings.setObjectName("menuSettings")
		self.menuView = QtWidgets.QMenu(self.menubar)
		self.menuView.setObjectName("menuView")
		PyCCAPT.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(PyCCAPT)
		self.statusbar.setObjectName("statusbar")
		PyCCAPT.setStatusBar(self.statusbar)
		self.actionExit = QtGui.QAction(PyCCAPT)
		self.actionExit.setObjectName("actionExit")
		self.actiontake_sceernshot = QtGui.QAction(PyCCAPT)
		self.actiontake_sceernshot.setObjectName("actiontake_sceernshot")
		self.actionAbout = QtGui.QAction(PyCCAPT)
		self.actionAbout.setObjectName("actionAbout")
		self.menuFile.addAction(self.actionExit)
		self.menuEdit.addAction(self.actiontake_sceernshot)
		self.menuHelp.addAction(self.actionAbout)
		self.menubar.addAction(self.menuFile.menuAction())
		self.menubar.addAction(self.menuEdit.menuAction())
		self.menubar.addAction(self.menuView.menuAction())
		self.menubar.addAction(self.menuSettings.menuAction())
		self.menubar.addAction(self.menuHelp.menuAction())

		self.retranslateUi(PyCCAPT)
		QtCore.QMetaObject.connectSlotsByName(PyCCAPT)
		PyCCAPT.setTabOrder(self.gates_control, self.pumps_vaccum)
		PyCCAPT.setTabOrder(self.pumps_vaccum, self.camears)
		PyCCAPT.setTabOrder(self.camears, self.laser_control)
		PyCCAPT.setTabOrder(self.laser_control, self.stage_control)
		PyCCAPT.setTabOrder(self.stage_control, self.visualization)
		PyCCAPT.setTabOrder(self.visualization, self.baking)
		PyCCAPT.setTabOrder(self.baking, self.start_button)
		PyCCAPT.setTabOrder(self.start_button, self.stop_button)
		PyCCAPT.setTabOrder(self.stop_button, self.parameters_source)
		PyCCAPT.setTabOrder(self.parameters_source, self.ex_user)
		PyCCAPT.setTabOrder(self.ex_user, self.ex_name)
		PyCCAPT.setTabOrder(self.ex_name, self.ex_time)
		PyCCAPT.setTabOrder(self.ex_time, self.criteria_time)
		PyCCAPT.setTabOrder(self.criteria_time, self.max_ions)
		PyCCAPT.setTabOrder(self.max_ions, self.criteria_ions)
		PyCCAPT.setTabOrder(self.criteria_ions, self.ex_freq)
		PyCCAPT.setTabOrder(self.ex_freq, self.vdc_min)
		PyCCAPT.setTabOrder(self.vdc_min, self.vdc_max)
		PyCCAPT.setTabOrder(self.vdc_max, self.criteria_vdc)
		PyCCAPT.setTabOrder(self.criteria_vdc, self.vdc_steps_up)
		PyCCAPT.setTabOrder(self.vdc_steps_up, self.vdc_steps_down)
		PyCCAPT.setTabOrder(self.vdc_steps_down, self.control_algorithm)
		PyCCAPT.setTabOrder(self.control_algorithm, self.pulse_mode)
		PyCCAPT.setTabOrder(self.pulse_mode, self.vp_min)
		PyCCAPT.setTabOrder(self.vp_min, self.vp_max)
		PyCCAPT.setTabOrder(self.vp_max, self.pulse_fraction)
		PyCCAPT.setTabOrder(self.pulse_fraction, self.pulse_frequency)
		PyCCAPT.setTabOrder(self.pulse_frequency, self.detection_rate_init)
		PyCCAPT.setTabOrder(self.detection_rate_init, self.hitmap_plot_size)
		PyCCAPT.setTabOrder(self.hitmap_plot_size, self.reset_heatmap)
		PyCCAPT.setTabOrder(self.reset_heatmap, self.hit_displayed)
		PyCCAPT.setTabOrder(self.hit_displayed, self.email)
		PyCCAPT.setTabOrder(self.email, self.counter_source)
		PyCCAPT.setTabOrder(self.counter_source, self.text_line)
		PyCCAPT.setTabOrder(self.text_line, self.dc_hold)
		PyCCAPT.setTabOrder(self.dc_hold, self.elapsed_time)
		PyCCAPT.setTabOrder(self.elapsed_time, self.total_ions)
		PyCCAPT.setTabOrder(self.total_ions, self.speciemen_voltage)
		PyCCAPT.setTabOrder(self.speciemen_voltage, self.pulse_voltage)
		PyCCAPT.setTabOrder(self.pulse_voltage, self.detection_rate)

		###
		self.camears.clicked.connect(self.open_cameras_win)
		self.gates_control.clicked.connect(self.open_gates_win)
		self.laser_control.clicked.connect(self.open_laser_control_win)
		self.stage_control.clicked.connect(self.open_stage_control_win)
		self.pumps_vaccum.clicked.connect(self.open_pumps_vacuum_win)
		self.visualization.clicked.connect(self.open_visualization_win)
		self.baking.clicked.connect(self.open_baking_win)
		# Create a QTimer to hide the warning message after 8 seconds
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.hideMessage)
		self.camera_close_check_timer = QtCore.QTimer()
		self.camera_close_check_timer.timeout.connect(self.check_closed_events)
		QtWidgets.QApplication.instance().aboutToQuit.connect(self.cleanup)
		self.statistics_timer = QtCore.QTimer()
		self.statistics_timer.timeout.connect(self.statistics_update)
		self.timer_stop_exp = QtCore.QTimer()
		self.timer_stop_exp.timeout.connect(self.on_stop_experiment_worker)  # timer to stop the experiment

		###
		self.setup_parameters_changes()
		self.parameters_source.currentIndexChanged.connect(self.setup_parameters_changes)
		self.ex_user.editingFinished.connect(self.setup_parameters_changes)
		self.ex_name.editingFinished.connect(self.setup_parameters_changes)
		self.ex_time.editingFinished.connect(self.setup_parameters_changes)
		self.max_ions.editingFinished.connect(self.setup_parameters_changes)
		self.ex_freq.editingFinished.connect(self.setup_parameters_changes)
		self.vdc_min.editingFinished.connect(self.setup_parameters_changes)
		self.vdc_max.editingFinished.connect(self.setup_parameters_changes)
		self.vdc_steps_up.editingFinished.connect(self.setup_parameters_changes)
		self.vdc_steps_down.editingFinished.connect(self.setup_parameters_changes)
		self.vp_min.editingFinished.connect(self.setup_parameters_changes)
		self.vp_max.editingFinished.connect(self.setup_parameters_changes)
		self.pulse_fraction.editingFinished.connect(self.setup_parameters_changes)
		self.pulse_frequency.editingFinished.connect(self.setup_parameters_changes)
		self.detection_rate_init.editingFinished.connect(self.setup_parameters_changes)
		self.hit_displayed.editingFinished.connect(self.setup_parameters_changes)
		self.email.editingFinished.connect(self.setup_parameters_changes)
		self.counter_source.currentIndexChanged.connect(self.setup_parameters_changes)
		self.hitmap_plot_size.valueChanged.connect(self.setup_parameters_changes)
		self.control_algorithm.currentIndexChanged.connect(self.setup_parameters_changes)
		self.pulse_mode.currentIndexChanged.connect(self.setup_parameters_changes)
		self.parameters_source.currentIndexChanged.connect(self.setup_parameters_changes)
		self.criteria_vdc.stateChanged.connect(self.setup_parameters_changes)
		self.criteria_time.stateChanged.connect(self.setup_parameters_changes)
		self.criteria_ions.stateChanged.connect(self.setup_parameters_changes)
		###
		self.start_button.clicked.connect(self.start_experiment_clicked)
		self.stop_button.clicked.connect(self.stop_experiment_clicked)
		self.reset_heatmap.clicked.connect(self.reset_heatmap_clicked)
		self.dc_hold.clicked.connect(self.dc_hold_clicked)
		self.set_min_voltage.clicked.connect(self.set_min_voltage_clicked)

		self.hitmap_plot_size.setValue(1.0)
		self.hitmap_plot_size.setSingleStep(0.1)
		self.hitmap_plot_size.setDecimals(1)

		self.emitter.elapsed_time.connect(self.update_elapsed_time)
		self.emitter.total_ions.connect(self.update_total_ions)
		self.emitter.speciemen_voltage.connect(self.update_speciemen_voltage)
		self.emitter.pulse_voltage.connect(self.update_pulse_voltage)
		self.emitter.detection_rate.connect(self.update_detection_rate)

		self.result_list = []

		self.camera_close_check_timer.start(500)  # check every 500 ms
		self.statistics_timer.start(333)  # check every 333 ms

		# initialize the wins

		self.wins_init()

		self.original_button_style = self.dc_hold.styleSheet()

	def retranslateUi(self, PyCCAPT):
		"""
				Retranslate the UI with the selected language

				Args:
					PyCCAPT: Main window

				Return:
					None
			"""
		_translate = QtCore.QCoreApplication.translate
		###
		# PyCCAPT.setWindowTitle(_translate("PyCCAPT", "OXCART"))
		_translate = QtCore.QCoreApplication.translate
		PyCCAPT.setWindowTitle(_translate("PyCCAPT", "PyCCAPT APT Experiment Control"))
		PyCCAPT.setWindowIcon(QtGui.QIcon('./files/logo.png'))
		###
		self.gates_control.setText(_translate("PyCCAPT", "Gates Control"))
		self.pumps_vaccum.setText(_translate("PyCCAPT", "Pumps & Vacuum"))
		self.camears.setText(_translate("PyCCAPT", "Cameras & Alingment"))
		self.laser_control.setText(_translate("PyCCAPT", "Laser Control"))
		self.stage_control.setText(_translate("PyCCAPT", "Stage Control"))
		self.visualization.setText(_translate("PyCCAPT", "Visualization"))
		self.baking.setText(_translate("PyCCAPT", "Baking"))
		self.text_line.setHtml(_translate("PyCCAPT",
		                                  "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
		                                  "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
		                                  "p, li { white-space: pre-wrap; }\n"
		                                  "</style></head><body style=\" font-family:\'Segoe UI\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">{ex_user=user1;</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.875pt; color:#000000\">ex_name=test1;</span>                                                                                </p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; color:#000000\">ex_time=90;max_ions=2000;ex_freq=10;</span>                                                                                </p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; color:#000000\">vdc_min=500;vdc_max=4000;vdc_steps_up=1;</span>                                                                                </p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; color:#000000\">vdc_steps_down=1;</span><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">control_algorithm=PID;</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; color:#000000\">vp_min=328;</span>                                                                                </p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; color:#000000\">vp_max=3281;pulse_fraction=20;pulse_frequency=200;</span>                                                                                </p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; color:#000000\">detection_rate_init=1;hit_displayed=20000;email=;counter_source=TDC</span><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">;</span>                                         </p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">criteria_time=True;criteria_ions=False;</span>                                                                                </p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">criteria_vdc=False}</span>                                                                                </p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">{ex_user=user2;ex_name=test2;ex_time=100;</span>                                                                                </p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">max_ions=3000;ex_freq=5;vdc_min=1000;</span>                                                                                </p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">vdc_max=3000;vdc_steps_up=0.5;vdc_steps_down=0.5;</span>                                                                                </p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">control_algorithm=proportional;vp_min=400;vp_max=2000;</span>                                                                                </p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">pulse_fraction=15;pulse_frequency=200;detection_rate_init=2;</span>                                                                                </p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">hit_displayed=40000;email=;counter_source=DRS;</span>                                                                                </p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">criteria_time=False;criteria_ions=False;criteria_vdc=True}</span>                                                                            </p></body></html>"))
		self.Error.setText(_translate("PyCCAPT", "<html><head/><body><p><br/></p></body></html>"))
		self.start_button.setText(_translate("PyCCAPT", "Start"))
		self.stop_button.setText(_translate("PyCCAPT", "Stop"))
		self.vp_max.setText(_translate("PyCCAPT", "3281"))
		self.label_179.setText(_translate("PyCCAPT", "DC Min. Voltage (V)"))
		self.label_189.setText(_translate("PyCCAPT", "# Hits Displayed"))
		self.label_181.setText(_translate("PyCCAPT", "K_p Upwards"))
		self.vdc_min.setText(_translate("PyCCAPT", "500"))
		self.label_180.setText(_translate("PyCCAPT", "DC Max. Voltage (V)"))
		self.dc_hold.setText(_translate("PyCCAPT", "Hold"))
		self.label_193.setText(_translate("PyCCAPT", "Run Statistics"))
		self.hit_displayed.setText(_translate("PyCCAPT", "20000"))
		self.control_algorithm.setItemText(0, _translate("PyCCAPT", "Proportional"))
		self.control_algorithm.setItemText(1, _translate("PyCCAPT", "PID"))
		self.label_196.setText(_translate("PyCCAPT", "DC Voltage (V)"))
		self.ex_name.setText(_translate("PyCCAPT", "test"))
		self.label_190.setText(_translate("PyCCAPT", "Email"))
		self.vp_min.setText(_translate("PyCCAPT", "328"))
		self.label_199.setText(_translate("PyCCAPT", "Pulse Mode"))
		self.label_186.setText(_translate("PyCCAPT", "Pulse Fraction (%)"))
		self.pulse_fraction.setText(_translate("PyCCAPT", "20"))
		self.label_177.setText(_translate("PyCCAPT", "Max. Number of Ions"))
		self.pulse_frequency.setText(_translate("PyCCAPT", "200"))
		self.vdc_steps_down.setText(_translate("PyCCAPT", "1"))
		self.label_2.setText(_translate("PyCCAPT", "Stop at"))
		self.label_184.setText(_translate("PyCCAPT", "Pulse Min. Voltage (V)"))
		self.label_174.setText(_translate("PyCCAPT", "Experiment User"))
		self.counter_source.setItemText(0, _translate("PyCCAPT", "TDC"))
		self.counter_source.setItemText(1, _translate("PyCCAPT", "Digitizer"))
		self.label_187.setText(_translate("PyCCAPT", "Pulse Frequency (KHz)"))
		self.ex_time.setText(_translate("PyCCAPT", "900"))
		self.pulse_mode.setItemText(0, _translate("PyCCAPT", "Voltage"))
		self.pulse_mode.setItemText(1, _translate("PyCCAPT", "Laser"))
		self.ex_freq.setText(_translate("PyCCAPT", "5"))
		self.label_194.setText(_translate("PyCCAPT", "Elapsed Time (sec)"))
		self.label_176.setText(_translate("PyCCAPT", "Max. Experiment Time (sec)"))
		self.label_3.setText(_translate("PyCCAPT", "Stop at"))
		self.label_188.setText(_translate("PyCCAPT", "Detection Rate (%)"))
		self.label_185.setText(_translate("PyCCAPT", "Pulse Max. Voltage (V)"))
		self.ex_user.setText(_translate("PyCCAPT", "user"))
		self.reset_heatmap.setText(_translate("PyCCAPT", "Reset"))
		self.label_192.setText(_translate("PyCCAPT", "Detection Mode"))
		self.label_173.setText(_translate("PyCCAPT", "Setup Parameters"))
		self.label_191.setText(_translate("PyCCAPT", "Control Algorithm"))
		self.label_175.setText(_translate("PyCCAPT", "Experiment Name"))
		self.label.setText(_translate("PyCCAPT", "Stop at"))
		self.parameters_source.setItemText(0, _translate("PyCCAPT", "TextBox"))
		self.parameters_source.setItemText(1, _translate("PyCCAPT", "TextLine"))
		self.max_ions.setText(_translate("PyCCAPT", "40000"))
		self.vdc_max.setText(_translate("PyCCAPT", "4000"))
		self.label_198.setText(_translate("PyCCAPT", "Detection Rate (%)"))
		self.label_182.setText(_translate("PyCCAPT", "K_p Downwards"))
		self.vdc_steps_up.setText(_translate("PyCCAPT", "1"))
		self.label_197.setText(_translate("PyCCAPT", "Pulse Voltage (V)"))
		self.label_178.setText(_translate("PyCCAPT", "Control refresh Freq.(Hz)"))
		self.detection_rate_init.setText(_translate("PyCCAPT", "1"))
		self.label_195.setText(_translate("PyCCAPT", "Total Ions"))
		self.set_min_voltage.setText(_translate("PyCCAPT", "Set Volatge"))
		self.menuFile.setTitle(_translate("PyCCAPT", "File"))
		self.menuEdit.setTitle(_translate("PyCCAPT", "Edit"))
		self.menuHelp.setTitle(_translate("PyCCAPT", "Help"))
		self.menuSettings.setTitle(_translate("PyCCAPT", "Settings"))
		self.menuView.setTitle(_translate("PyCCAPT", "View"))
		self.actionExit.setText(_translate("PyCCAPT", "Exit"))
		self.actiontake_sceernshot.setText(_translate("PyCCAPT", "take sceernshot"))
		self.actionAbout.setText(_translate("PyCCAPT", "About PyCCAPT"))

	def update_elapsed_time(self, value):
		"""
		Update the speciemen voltage

		Args:
			value (float): The speciemen voltage

		Return:
			None
		"""
		self.elapsed_time.setText(str("{:.3f}".format(value)))

	def update_total_ions(self, value):
		"""
		Update the speciemen voltage

		Args:
			value (float): The speciemen voltage

		Return:
			None
		"""
		self.total_ions.setText(str(value))

	def update_speciemen_voltage(self, value):
		"""
		Update the speciemen voltage

		Args:
			value (float): The speciemen voltage

		Return:
			None
		"""
		self.speciemen_voltage.setText(str("{:.3f}".format(value)))

	def update_pulse_voltage(self, value):
		"""
		Update the pulse voltage

		Args:
			value (float): The pulse voltage

		Return:
			None
		"""
		self.pulse_voltage.setText(str("{:.3f}".format(value)))

	def update_detection_rate(self, value):
		"""
		Update the detection rate

		Args:
			value (float): The detection rate

		Return:
			None
		"""
		self.detection_rate.setText(str("{:.3f}".format(value)))

	def read_text_lines(self, ):
		"""
		Read the text lines and convert them to a dictionary

		Args:
			None

		Return:
			None
		"""

		def convert_value(value):
			"""
			Convert the value to the correct type

			Args:
				value (str): The value to convert

			Return:
				None
			"""
			# Try to convert to integer
			try:
				return int(value)
			except ValueError:
				# If not an integer, check if it's a boolean value
				if value.lower() == 'true':
					return True
				elif value.lower() == 'false':
					return False
				else:
					# If not a boolean, return the original value as string
					return value

		lines = self.text_line.toPlainText()
		pattern = r"{(.*?)}"
		matches = re.findall(pattern, lines, re.DOTALL)

		# Define the required keys for each dictionary
		required_keys = [
			'ex_user', 'ex_name', 'ex_time', 'max_ions', 'ex_freq', 'vdc_min', 'vdc_max',
			'vdc_steps_up', 'vdc_steps_down', 'control_algorithm', 'pulse_mode', 'vp_min', 'vp_max',
			'pulse_fraction', 'pulse_frequency', 'detection_rate_init', 'hit_displayed',
			'email', 'counter_source', 'criteria_time', 'criteria_ions', 'criteria_vdc'
		]

		# Process each match and create a dictionary for each item
		for match in matches:
			item_dict = {}
			elements = match.split(";")
			for element in elements:
				key, value = element.split("=")
				item_dict[key.strip()] = convert_value(value.strip())

			# Check if all the required keys are present in the dictionary
			assert all(
				key in item_dict for key in required_keys), f"Missing keys in dictionary: {item_dict}"
			self.result_list.append(item_dict)
		self.variables.number_of_experiment_in_text_line = len(self.result_list)
		if self.variables.index_experiment_in_text_line < len(self.result_list):
			index_line = self.variables.index_experiment_in_text_line
			self.variables.ex_user = self.result_list[index_line]['ex_user']
			self.variables.ex_name = self.result_list[index_line]['ex_name']
			self.variables.ex_time = self.result_list[index_line]['ex_time']
			self.variables.max_ions = self.result_list[index_line]['max_ions']
			self.variables.ex_freq = self.result_list[index_line]['ex_freq']
			self.variables.vdc_min = self.result_list[index_line]['vdc_min']
			if self.result_list[index_line]['vdc_max'] < self.conf['max_vdc']:
				self.variables.vdc_max = self.result_list[index_line]['vdc_max']
			elif self.result_list[index_line]['vdc_max'] > self.conf['max_vdc']:
				self.error_message("Maximum possible Vdc is " + str(self.conf['max_vdc']))
			self.variables.vdc_steps_up = self.result_list[index_line]['vdc_steps_up']
			self.variables.vdc_steps_down = self.result_list[index_line]['vdc_steps_down']
			self.variables.control_algorithm = self.result_list[index_line]['control_algorithm']
			self.variables.pulse_mode = self.result_list[index_line]['pulse_mode']
			self.variables.vp_min = self.result_list[index_line]['vp_min']
			if self.result_list[index_line]['vp_max'] < self.conf['max_vp']:
				self.variables.vp_max = self.result_list[index_line]['vp_max']
			elif self.result_list[index_line]['vp_max'] > self.conf['max_vp']:
				self.error_message("Maximum possible V_p is " + str(self.conf['max_vp']))
			self.variables.pulse_fraction = self.result_list[index_line]['pulse_fraction']
			self.variables.pulse_frequency = self.result_list[index_line]['pulse_frequency']
			self.variables.detection_rate_init = self.result_list[index_line]['detection_rate_init']
			self.variables.hit_displayed = self.result_list[index_line]['hit_displayed']
			self.variables.email = self.result_list[index_line]['email']
			self.variables.counter_source = self.result_list[index_line]['counter_source']
			self.variables.criteria_time = self.result_list[index_line]['criteria_time']
			self.variables.criteria_ions = self.result_list[index_line]['criteria_ions']
			self.variables.criteria_vdc = self.result_list[index_line]['criteria_vdc']

	def setup_parameters_changes(self):
		"""
        Function to setup parameters changes

        Args:
            None

        Return:
            None
        """
		# with self.variables.lock_setup_parameters:
		if self.parameters_source.currentText() == 'TextLine':
			self.read_text_lines()
		else:
			self.variables.user_name = self.ex_user.text()
			self.variables.ex_name = self.ex_name.text()
			self.variables.ex_time = int(float(self.ex_time.text()))
			self.variables.ex_freq = int(float(self.ex_freq.text()))
			self.variables.max_ions = int(float(self.max_ions.text()))
			self.variables.vdc_min = int(float(self.vdc_min.text()))
			self.variables.detection_rate = float(self.detection_rate_init.text())
			self.variables.hit_display = int(float(self.hit_displayed.text()))
			self.variables.pulse_fraction = int(float(self.pulse_fraction.text())) / 100
			self.variables.pulse_frequency = float(self.pulse_frequency.text())
			self.variables.hdf5_data_name = self.ex_name.text()
			self.variables.email = self.email.text()
			self.variables.vdc_step_up = float(self.vdc_steps_up.text())
			self.variables.vdc_step_down = float(self.vdc_steps_down.text())
			self.variables.control_algorithm = str(self.control_algorithm.currentText())
			self.variables.pulse_mode = str(self.pulse_mode.currentText())
			self.variables.v_p_min = int(float(self.vp_min.text()))
			self.variables.v_p_max = int(float(self.vp_max.text()))
			self.variables.counter_source = str(self.counter_source.currentText())
			self.variables.hitmap_plot_size = self.hitmap_plot_size.value()

			if float(self.vp_max.text()) > self.conf['max_vp']:
				self.error_message.setText("Maximum possible number is " + str(self.conf['max_vp']))
				_translate = QtCore.QCoreApplication.translate
				self.vp_max.setText(_translate("PyCCAPT", self.conf['max_vp']))
			else:
				self.variables.v_p_max = int(float(self.vp_max.text()))

			if int(float(self.vdc_max.text())) > self.conf['max_vdc']:
				self.error_message("Maximum possible number is " + str(self.conf['max_vdc']))
				_translate = QtCore.QCoreApplication.translate
				self.vdc_max.setText(_translate("PyCCAPT", str(self.conf['max_vdc'])))
			else:
				self.variables.vdc_max = int(float(self.vdc_max.text()))

			if self.criteria_time.isChecked():
				self.variables.criteria_time = True
			elif not self.criteria_time.isChecked():
				self.variables.criteria_time = False
			if self.criteria_ions.isChecked():
				self.variables.criteria_ions = True
			elif not self.criteria_ions.isChecked():
				self.variables.criteria_ions = False
			if self.criteria_vdc.isChecked():
				self.variables.criteria_vdc = True
			elif not self.criteria_vdc.isChecked():
				self.variables.criteria_vdc = False

	def start_experiment_clicked(self):
		"""
        Start the experiment worker thread

        Args:
            None

        Return:
            None
        """
		# with self.variables.lock_statistics:
		self.variables.start_flag = True  # Set the start flag
		self.variables.stop_flag = False  # Set the stop flag
		self.variables.plot_clear_flag = True  # Change the flag to clear the plots in GUI
		self.variables.clear_index_save_image = True
		self.start_button.setEnabled(False)  # Disable the star button
		self.counter_source.setEnabled(False)  # Disable the counter source
		self.pulse_mode.setEnabled(False)  # Disable the pulse mode
		self.parameters_source.setEnabled(False)  # Disable the parameters source
		self.pulse_fraction.setEnabled(False)  # Disable the pulse fraction
		self.pulse_frequency.setEnabled(False)  # Disable the pulse frequency
		self.ex_freq.setEnabled(False)
		self.ex_name.setEnabled(False)
		self.start_experiment_worker()

		self.variables.elapsed_time = 0.0
		self.variables.total_ions = 0
		self.variables.specimen_voltage = 0.0
		self.variables.pulse_voltage = 0.0
		self.variables.detection_rate_current = 0.0

	def statistics_update(self):
		"""
            Update the statistics

            Args:
                None

            Return:
                None
        """
		self.emitter.elapsed_time.emit(self.variables.elapsed_time)
		self.emitter.total_ions.emit(self.variables.total_ions)
		self.emitter.speciemen_voltage.emit(self.variables.specimen_voltage)
		self.emitter.pulse_voltage.emit(self.variables.pulse_voltage)
		self.emitter.detection_rate.emit(self.variables.detection_rate_current)

		if not self.variables.start_flag and self.variables.stop_flag:
			self.stop_experiment_clicked()

	def stop_experiment_clicked(self):
		"""
			Stop the experiment worker thread

            Args:
                None

            Return:
                None
        """
		self.statistics_timer.stop()
		self.variables.stop_flag = True  # Set the STOP flag
		self.stop_button.setEnabled(False)  # Disable the stop button
		self.timer_stop_exp.start(1000)  # Start the timer to run stop actions after 8 seconds

	def start_experiment_worker(self):
		"""
			Start the experiment worker thread

			Args:
				None

			Return:
                None
        """
		self.experiment_process = multiprocessing.Process(target=apt_exp_control.run_experiment,
		                                                  args=(self.variables, self.conf,
		                                                        self.experimetn_finished_event, self.x_plot,
		                                                        self.y_plot, self.t_plot, self.main_v_dc_plot,))
		self.experiment_process.start()
		self.statistics_timer.start()

	def on_stop_experiment_worker(self):
		"""
			Enable the start and stop buttons after experiment is finished

			Args:
				None

			Return:
				None
		"""
		self.emitter.total_ions.emit(self.variables.total_ions)  # Update the total ions
		if self.variables.flag_end_experiment:
			self.start_button.setEnabled(True)
			self.stop_button.setEnabled(True)
			self.counter_source.setEnabled(True)  # Enable the counter source
			self.pulse_mode.setEnabled(True)  # Enable the pulse mode
			self.parameters_source.setEnabled(True)  # Enable the parameters source
			self.pulse_fraction.setEnabled(True)  # Enable the pulse fraction
			self.pulse_frequency.setEnabled(True)  # Enable the pulse frequency
			self.ex_freq.setEnabled(True)
			self.variables.vdc_hold = False
			self.ex_name.setEnabled(True)
			self.dc_hold.setStyleSheet(self.original_button_style)

			self.experiment_process.join(1)
			print('experiment_process joined')

			# for getting screenshot of GUI
			screen = QtWidgets.QApplication.primaryScreen()
			w = self.centralwidget
			screenshot = screen.grabWindow(w.winId())
			# with self.variables.lock_setup_parameters:
			screenshot.save(self.variables.path + '\screenshot.png', 'png')

			self.variables.flag_cameras_take_screenshot = True

			# with self.variables.lock_statistics:
			if self.variables.index_experiment_in_text_line < len(
					self.result_list):  # Do next experiment in case of TextLine
				self.variables.index_experiment_in_text_line += 1
				self.start_experiment_worker()
			else:
				self.variables.index_line = 0

			self.variables.flag_end_experiment = False
			self.variables.flag_stop_tdc = False
			self.timer_stop_exp.stop()

	def reset_heatmap_clicked(self):
		"""
            Reset the heatmap
            Args:
                None

            Return:
                None
        """
		# with self.variables.lock_setup_parameters:
		if not self.variables.reset_heatmap:
			self.variables.reset_heatmap = True

	def dc_hold_clicked(self):
		"""
            Hold the DC voltage

            Args:
                None

            Return:
                None
        """
		# with self.variables.lock_setup_parameters:
		if not self.variables.vdc_hold:
			self.variables.vdc_hold = True
			self.dc_hold.setStyleSheet("QPushButton{\n"
			                           "background: rgb(0, 255, 26)\n"
			                           "}")
		elif self.variables.vdc_hold:
			self.variables.vdc_hold = False
			self.dc_hold.setStyleSheet(self.original_button_style)

	def set_min_voltage_clicked(self):
		"""
			Set the minimum voltage

			Args:
				None

			Return:
				None
		"""

		if self.variables.vdc_hold:
			self.variables.flag_new_min_voltage = True
		else:
			self.error_message("Hold the DC voltage first")

	def wins_init(self):
		# GUI Cameras
		self.camera_process = multiprocessing.Process(target=gui_cameras.run_camera_window,
		                                              args=(self.variables, self.conf,
		                                                    self.camera_closed_event,
		                                                    self.camera_win_front))
		self.camera_process.start()
		# GUI gate
		self.gui_gates = gui_gates.Ui_Gates(self.variables, self.conf)
		self.Gates = gui_gates.GatesWindow(self.gui_gates, flags=QtCore.Qt.WindowType.Tool)
		self.Gates.setWindowStyleFusion()
		self.gui_gates.setupUi(self.Gates)
		# GUI Pumps and Vacuum
		self.SignalEmitter_Pumps_Vacuum = gui_pumps_vacuum.SignalEmitter()
		self.gui_pumps_vacuum = gui_pumps_vacuum.Ui_Pumps_Vacuum(self.variables, self.conf,
		                                                         self.SignalEmitter_Pumps_Vacuum)
		self.Pumps_vacuum = gui_pumps_vacuum.PumpsVacuumWindow(self.gui_pumps_vacuum,
		                                                       self.SignalEmitter_Pumps_Vacuum,
		                                                       flags=Qt.WindowType.Tool)
		self.Pumps_vacuum.setWindowStyleFusion()
		self.gui_pumps_vacuum.setupUi(self.Pumps_vacuum)
		self.variables.flag_pumps_vacuum_start = True

		# GUI Laser Control
		self.gui_laser_control = gui_laser_control.Ui_Laser_Control(self.variables, self.conf)
		self.Laser_control = gui_laser_control.LaserControlWindow(self.gui_laser_control,
		                                                          flags=Qt.WindowType.Tool)
		self.gui_laser_control.setupUi(self.Laser_control)

		# GUI Stage Control
		self.gui_stage_control = gui_stage_control.Ui_Stage_Control(self.variables, self.conf)
		self.Stage_control = gui_stage_control.StageControlWindow(self.gui_stage_control,
		                                                          flags=Qt.WindowType.Tool)
		self.Stage_control.setWindowStyleFusion()
		self.gui_stage_control.setupUi(self.Stage_control)

		# GUI Visualization
		self.visualization_process = multiprocessing.Process(target=gui_visualization.run_visualization_window,
		                                                     args=(self.variables, self.conf,
		                                                           self.visualization_closed_event,
		                                                           self.visualization_win_front, self.x_plot,
		                                                           self.y_plot,
		                                                           self.t_plot, self.main_v_dc_plot))
		self.visualization_process.start()

	def open_cameras_win(self):
		"""
        Open the Cameras window

        Args:
            None

        Return:
            None
        """
		self.variables.flag_camera_win_show = True
		self.camera_win_front.set()
		self.camears.setStyleSheet("background-color: green")

	def check_closed_events(self):
		"""
		Check if the camera window is closed

		Args:
		    None

		Return:
			None
		"""
		if self.camera_closed_event.is_set():
			# Change the color of the push button when the camera window is closed
			self.reset_button_color(self.camears)
			self.camera_closed_event.clear()
		if self.experimetn_finished_event.is_set():
			self.experimetn_finished_event.clear()
			self.on_stop_experiment_worker()
		if self.visualization_closed_event.is_set():
			# Change the color of the push button when the camera window is closed
			self.reset_button_color(self.visualization)
			self.visualization_closed_event.clear()

	def open_gates_win(self):
		"""
		Open the Gates window

		Args:
		    None

		Return:
		    None
		"""
		if hasattr(self, 'Gates') and self.Gates.isVisible():
			self.Gates.raise_()
			self.Gates.activateWindow()
		else:
			self.Gates.show()
			self.gates_control.setStyleSheet("background-color: green")
			self.Gates.closed.connect(lambda: self.reset_button_color(self.gates_control))

	def open_pumps_vacuum_win(self, ):
		"""
		Open the Pumps and Vacuum window

		Args:
            None

        Return:
            None
        """
		if hasattr(self, 'Pumps_vacuum') and self.Pumps_vacuum.isVisible():
			self.Pumps_vacuum.raise_()
			self.Pumps_vacuum.activateWindow()
		else:
			self.Pumps_vacuum.show()
			self.pumps_vaccum.setStyleSheet("background-color: green")
			self.Pumps_vacuum.closed.connect(lambda: self.reset_button_color(self.pumps_vaccum))

	def open_laser_control_win(self):
		"""
		Open laser control window

        Args:
            None

        Return:
            None
        """
		if hasattr(self, 'Laser_control') and self.Laser_control.isVisible():
			self.Laser_control.raise_()
			self.Laser_control.activateWindow()
		else:
			self.Laser_control.show()
			self.laser_control.setStyleSheet("background-color: green")
			self.Laser_control.closed.connect(lambda: self.reset_button_color(self.laser_control))

	def open_stage_control_win(self):
		"""
		Open stage control window

        Args:
            None

        Return:
            None
        """
		if hasattr(self, 'Stage_control') and self.Stage_control.isVisible():
			self.Stage_control.raise_()
			self.Stage_control.activateWindow()
		else:
			self.Stage_control.show()
			self.stage_control.setStyleSheet("background-color: green")
			self.Stage_control.closed.connect(lambda: self.reset_button_color(self.stage_control))

	def open_visualization_win(self, ):
		"""
		Open visualization window

        Args:
            None

        Return:
            None
        """
		self.variables.flag_visualization_win_show = True
		self.visualization_win_front.set()
		self.visualization.setStyleSheet("background-color: green")
	def open_baking_win(self):
		"""
		Open baking window

		Args:
            None

        Return:
            None
        """

		if hasattr(self, 'Baking') and self.Baking.isVisible():
			self.Baking.raise_()
			self.Baking.activateWindow()
		else:
			self.gui_baking = gui_baking.Ui_Baking(self.variables, self.conf)
			self.Baking = gui_baking.BakingWindow(self.gui_baking, flags=Qt.WindowType.Tool)
			self.gui_baking.setupUi(self.Baking)
			self.Baking.show()
			self.baking.setStyleSheet("background-color: green")
			self.Baking.closed.connect(lambda: self.reset_button_color(self.baking))

	def reset_button_color(self, button):
		"""
		Reset the button color to the original color

		Args:
			button (QPushButton): The button to reset the color

		Return:
			None
		"""
		button.setStyleSheet("QPushButton{ background: rgb(85, 170, 255) }")

	def error_message(self, message):
		"""
        Display an error message and start a timer to hide it after 8 seconds

        Args:
            message (str): Error message to display

        Return:
            None
        """
		_translate = QtCore.QCoreApplication.translate
		self.Error.setText(_translate("OXCART",
		                              "<html><head/><body><p><span style=\" color:#ff0000;\">"
		                              + message + "</span></p></body></html>"))

		self.timer.start(8000)

	def hideMessage(self, ):
		"""
		Hide the message and stop the timer
        Args:
            None

        Return:
            None
        """
		# Hide the message and stop the timer
		_translate = QtCore.QCoreApplication.translate
		self.Error.setText(_translate("OXCART",
		                              "<html><head/><body><p><span style=\" "
		                              "color:#ff0000;\"></span></p></body></html>"))

		self.timer.stop()

	def cleanup(self, ):
		"""
		Cleanup function to terminate the camera process

		Args:
			None

		Return:
			None
		"""
		if hasattr(self, 'camera_process') and self.camera_process.is_alive():
			self.camera_process.terminate()
			self.visualization_process.terminate()
			self.gui_pumps_vacuum.gauges_thread.join(2)

class SignalEmitter(QtCore.QObject):
	elapsed_time = QtCore.pyqtSignal(float)
	total_ions = QtCore.pyqtSignal(int)
	speciemen_voltage = QtCore.pyqtSignal(float)
	pulse_voltage = QtCore.pyqtSignal(float)
	detection_rate = QtCore.pyqtSignal(float)


if __name__ == "__main__":
	try:
		# Load the JSON file
		configFile = 'config.json'
		p = os.path.abspath(os.path.join(__file__, "../../.."))
		os.chdir(p)
		conf = read_files.read_json_file(configFile)
	except Exception as e:
		print('Can not load the configuration file')
		print(e)
		sys.exit()

	# Initialize global experiment variables
	manager = multiprocessing.Manager()
	ns = manager.Namespace()
	variables = share_variables.Variables(conf, ns)
	x_plot = multiprocessing.Queue()
	y_plot = multiprocessing.Queue()
	t_plot = multiprocessing.Queue()
	main_v_dc_plot = multiprocessing.Queue()

	# variables = share_variables.Variables(conf)
	variables.log_path = p

	app = QtWidgets.QApplication(sys.argv)
	app.setStyle('Fusion')
	PyCCAPT = QtWidgets.QMainWindow()
	ui = Ui_PyCCAPT(variables, conf, x_plot, y_plot, t_plot, main_v_dc_plot)
	ui.setupUi(PyCCAPT)
	PyCCAPT.show()
	sys.exit(app.exec())
