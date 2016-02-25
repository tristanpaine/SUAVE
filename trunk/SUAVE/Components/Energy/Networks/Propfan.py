# Propfan.py
#
# Created: Feb 2016, T. Paine
# Modified Feb 2016, T. Paine

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# suave imports
import SUAVE

# package imports
import numpy as np
from SUAVE.Components.Propulsors.Propulsor import Propulsor

from SUAVE.Core import Data

# ----------------------------------------------------------------------
#  Network
# ----------------------------------------------------------------------

class Propfan(Propulsor):
	def __defaults__(self):
		self.propeller_front      = None
		self.propeller_rear       = None
		self.motor_front          = None
		self.motor_rear           = None
		self.esc_front            = None
		self.esc_rear             = None
		self.voltage              = None
		self.battery              = None
		self.tag                  = 'network'

	# manage process with a driver function
	def evalulate_thrust(self,state):

		#unpack
		condition			= state.conditions
		numerics			= state.numerics
		propeller_front		= self.propeller_front
		propeller_rear		= self.propeller_rear
		motor_front			= self.motor_front
		motor_rear			= self.motor_rear
		esc_front			= self.esc_front
		esc_rear			= self.esc_rear
		battery				= self.battery

		#set battery energy
		battery.current_energy = condition.propulsion.battery_energy

		#link battery to front esc
		esc_front.inputs.voltagein = self.voltage
		esc_front.voltageout(conditions)
		#link front esc to front motor
		motor_front.inputs.voltage = esc_front.outputs.voltageout
		motor_front.omega(conditions)
		#link front motor to front propeller
		propeller_front.inputs.omega  = motor_front.outputs.omega
		propeller_front.inputs.torque = motor_front.outputs.torque
		#
		F_front, Q_front, P_front, Cplast_front = front_propeller.spin(conditions)

		#link battery to rear esc
		esc_rear.inputs.voltagein = self.voltage
		esc_rear.voltageout(conditions)
		#link rear esc to rear motor
		motor_rear.inputs.voltage = esc_rear.outputs.voltageout
		motor_rear.omega(conditions)
		#link rear motor to rear propeller
		propeller_rear.inputs.omega  = motor_rear.outputs.omega
		propeller_rear.inputs.torque = motor_rear.output.torque
		#
		F_rear, Q_front, P_front, Cplast_rear = rear_propeller.spin(conditions)





























