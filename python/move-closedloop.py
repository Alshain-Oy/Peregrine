#!/usr/bin/env python


import serial, sys
import libPeregrine
import time

com = serial.Serial( sys.argv[1], 460800, timeout = 0.1 )

ctrl = libPeregrine.Controller( com, int(sys.argv[2]) )


ctrl.write( libPeregrine.PARAM_MOTOR_DIRECTION, 1 )
ctrl.write( libPeregrine.PARAM_OPERATING_MODE, libPeregrine.MODE_CLOSEDLOOP )

ctrl.move( pos = int(sys.argv[3]), speed = 20000, accel = 200 )
		
t0 = time.time()
try:
    while True:
        pos, speed, flags = ctrl.status()
        print( time.time() - t0, pos, speed, flags )
except KeyboardInterrupt:
    pass

com.close()
