#!/usr/bin/env python

import sys
import serial
import libPeregrine
import struct 

com = serial.Serial( sys.argv[1], 460800, timeout = .1 )


for i in range( 1, 9 ):
    ctrl = libPeregrine.Controller( com, i )
    try:
        serial = ctrl.read( libPeregrine.PARAM_FIRMWARE_VER )
        print( "Peregrine[%i] = %x" %(i, serial))
    except struct.error:
        print( "Peregrine[%i] = Not present" %(i))
