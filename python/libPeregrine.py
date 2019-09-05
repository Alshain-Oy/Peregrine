#!/usr/bin/env python

import serial
import struct

# Opcodes for operating the controller
OP_MOVE   = 0x00
OP_WRITE  = 0x01
OP_READ   = 0x02
OP_STATUS = 0x03
OP_MOVES  = 0x04
OP_ERROR   = 0xff
OP_HALT = 0x11
OP_SET_POS   = 0x30
OP_HIRES = 0x31

# Opcodes for I2C extension
OP_I2C_TEMP  = 0x13
OP_I2C_IO_W  = 0x14
OP_I2C_IO_R  = 0x15
#OP_I2C_ADC   = 0x16
#OP_I2C_DAC   = 0x17
#OP_I2C_PWM   = 0x18
OP_I2C_MEM_W = 0x19
OP_I2C_MEM_R = 0x20

# Params for functionality of the controller
PARAM_ENCODER_VALUE = 0
PARAM_OPERATING_MODE = 1
PARAM_PLANNING_MODE = 2
PARAM_ENCODER_MODE = 3
PARAM_DRIVER_CONFIG = 4
PARAM_LIMIT_SWITCH = 5
PARAM_CONTROL_MODE = 6
PARAM_POWER_MODE = 7

# Params for the servo feedback loop
PARAM_SERVO_DEADZONE = 10
PARAM_POS_TARGET_GAIN = 11
PARAM_POS_TARGET_P = 12
PARAM_POS_TARGET_D = 13
PARAM_V_TARGET_P = 14
PARAM_V_TARGET_D = 15
PARAM_FREQ_SLEW = 16
PARAM_MOTOR_DIRECTION = 17
PARAM_ERROR_GAIN = 18
PARAM_LQR_K0 = 19
PARAM_LQR_K1 = 20
PARAM_LQR_B1 = 21
PARAM_ENCODER_DIV = 22


# Params for housekeeping etc
PARAM_FDIR_STEPRATE = 23
PARAM_PROBE_POSITION = 25

PARAM_FIRMWARE_VER = 60
PARAM_UPTIME = 61


# Values for operating mode
MODE_OPENLOOP = 1
MODE_CLOSEDLOOP = 2

# Values for path planning 
PLANNING_NONE = 1
PLANNING_PATH = 2

# Values for encoder mode
ENCODER_INCREMENTAL = 1
ENCODER_ABSOLUTE = 2
ENCODER_ABSOLUTE_MULTITURN = 3

# Values for driver config
DRIVER_8_STEP  = 0
DRIVER_2_STEP  = 1
DRIVER_4_STEP  = 2
DRIVER_16_STEP = 3

# Values for limit switch config
LIMIT_SWITCH_ENABLED = 1
LIMIT_SWITCH_DISABLED = 2
LIMIT_SWITCH_INVERTED = 3

# Values for control mode
MODE_PID = 1
MODE_LQR = 2

# Values for power saving mode
POWER_SAVE = 0
POWER_ALWAYS_ON = 1



# Functions to encode messages
def gen_move_msg( addr, target, speed, accel ):
	return struct.pack( ">BBihH", addr, OP_MOVE, target, speed, accel )

def gen_write_msg( addr, key, value ):
	return struct.pack( ">BBIi", addr, OP_WRITE, key, value )

def gen_read_msg( addr, key):
	return struct.pack( ">BBIi", addr, OP_READ, key, 0 )

def gen_status_msg( addr ):
	return struct.pack( ">BBihH", addr, OP_STATUS, 0, 0, 0 )

def gen_action_msg( addr, action, key, value ):
	return struct.pack( ">BBIi", addr, action, key, value )

def gen_action_msg( addr, action, key, value ):
	return struct.pack( ">BBIi", addr, action, key, value )
	
def gen_action_msg_mem( addr, action, key, value ):
	return struct.pack( ">BBII", addr, action, key, value )


# Functions to decode message
def decode_flags( flags ):
	out = {}
	out["RUNNING"] = ((flags >> 0) & 0x01) > 0
	out["EMG_STOP"] = ((flags >> 1) & 0x01) > 0
	out["LIMIT+"] = ((flags >> 2) & 0x01) > 0
	out["LIMIT-"] = ((flags >> 3) & 0x01) > 0
	out["FDIR"] = ((flags >> 4) & 0x01) > 0
	out["CL"] = ((flags >> 5) & 0x01) > 0
	
	return out

def decode_error( msg ):
	(addr, op, error, extra) = struct.unpack( ">BBIi", msg )
	return error, extra

def decode_read( msg ):
	(addr, op, key, value) = struct.unpack( ">BBIi", msg )
	return key, value

def decode_status( msg ):
	(addr, op, position, speed, flags) = struct.unpack( ">BBihH", msg )
	return position, speed*32, decode_flags( flags )

def decode_action( msg ):
	(addr, op, key, value) = struct.unpack( ">BBIi", msg )
	return key, value

def decode_action_mem( msg ):
	(addr, op, key, value) = struct.unpack( ">BBII", msg )
	return key, value

def decode_header( msg ):
	(addr, op) = struct.unpack_from( ">BB", msg )
	
	return addr, op 







class Controller( object ):
	def __init__( self, com, address ):
		self.com = com
		self.address = address
	
	
	def status( self ):
		self.com.write( gen_status_msg( self.address ) )
		response = self.com.read( 10 )
		
		return decode_status( response ) 
	
	def move( self, pos, speed, accel ):
		self.com.write( gen_move_msg( self.address, int(pos), int(speed/32), int(accel)  ) )
		response = self.com.read( 10 )
	
	def move_with_status( self, pos, speed, accel ):
		self.com.write( gen_move_msg( self.address, int(pos), int(speed/32), int(accel)  ) )
		response = self.com.read( 10 )
		return decode_status( response ) 
	
	def write( self, key, value ):
		self.com.write( gen_write_msg( self.address, int(key), int(value) ) )
		response = self.com.read( 10 )
		addr, op = decode_header( response )
		if op == OP_ERROR:
			raise IndexError
		
	def read( self, key ):
		self.com.write( gen_read_msg( self.address, int( key ) ) )
		response = self.com.read( 10 )
		addr, op = decode_header( response )
		if op == OP_ERROR:
			raise IndexError
		
		key, value = decode_read( response )
		return value
		
	
	def halt( self ):
		self.com.write( gen_action_msg( self.address, OP_HALT, 0, 0 ) )
		response = self.com.read( 10 )
		key, value = decode_action( response )
		return value 
	
	def set_position( self, value ):
		self.com.write( gen_action_msg( self.address, OP_SET_POS, 0, value ) )
		response = self.com.read( 10 )
		key, value = decode_action( response )
		return value 
	
	
	def i2c_read_temperature( self, addr ):
		self.com.write( gen_action_msg( self.address, OP_I2C_TEMP, addr, 0 ) )
		response = self.com.read( 10 )
		key, value = decode_action( response )
		t = (value >>5) * 0.125
		return t 
	
	def i2c_read_ioexpander( self, addr ):
		self.com.write( gen_action_msg( self.address, OP_I2C_IO_R, addr, 0 ) )
		response = self.com.read( 10 )
		key, value = decode_action( response )
		return value 
	
	def i2c_write_ioexpander( self, addr, value ):
		self.com.write( gen_action_msg( self.address, OP_I2C_IO_W, addr, value ) )
		response = self.com.read( 10 )
		key, value = decode_action( response )
		return value 
	
#	def i2c_read_adc( self, addr, channel ):
#		self.com.write( gen_action_msg( self.address, OP_I2C_ADC, addr, channel ) )
#		response = self.com.read( 10 )
#		key, value = decode_action( response )
#		return value 
	
#	def i2c_write_dac( self, addr, channel, value ):
#		self.com.write( gen_action_msg( self.address, OP_I2C_DAC, (addr << 8) | channel, value ) )
#		response = self.com.read( 10 )
#		key, value = decode_action( response )
#		return value 
	
#	def i2c_write_pwm( self, addr, channel, value ):
#		self.com.write( gen_action_msg( self.address, OP_I2C_PWM, (addr << 8) | channel, value ) )
#		response = self.com.read( 10 )
#		key, value = decode_action( response )
#		return value 
	
	def mem_write( self, addr, value ):
		self.com.write( gen_action_msg_mem( self.address, OP_I2C_MEM_W, addr, value ) )
		response = self.com.read( 10 )
		key, value = decode_action( response )
		return value 
	
	def mem_read( self, addr ):
		self.com.write( gen_action_msg( self.address, OP_I2C_MEM_R, addr, 0 ) )
		response = self.com.read( 10 )
		key, value = decode_action_mem( response )
		return value 
	
	def set_hires( self ):
		self.com.write( gen_action_msg( self.address, OP_HIRES, 0, 0 ) )
		response = self.com.read( 10 )
		key, value = decode_action( response )
		return value 
	
