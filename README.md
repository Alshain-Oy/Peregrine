# Peregrine
Alshain Peregrine Motion Controller scripts & user guide

## Quickstart

1) Connect RS485<->usb cable to _RS485_ port
2) Connect motor and incremental encoder to their respective ports ( _Motor_ and _Encoder_ )
3) Connect power supply (9..30V) to _VM_ port

```python
import serial
import libPeregrine

# replace "COM3" with corresponding port on your computer
com = serial.Serial( "COM3", 460800, timeout = 0.1 )

# Connect to controller with address = 1 
ctrl = libPeregrine.Controller( com, 1 )

# Put controller into closed loop mode
ctrl.write( libPeregrine.PARAM_OPERATING_MODE, libPeregrine.MODE_CLOSEDLOOP )

# Issue a movement command 
ctrl.move( pos = 1500, speed = 1000, accel = 100)

# Query current position and status
pos, speed, flags = ctrl.status()

print( pos, speed, flags)
```

## Snippets

### Parameters

```python

# Open & closed loop control
ctrl.write( libPeregrine.PARAM_OPERATING_MODE, libPeregrine.MODE_OPENLOOP )
ctrl.write( libPeregrine.PARAM_OPERATING_MODE, libPeregrine.MODE_CLOSEDLOOP )

# Motor rotation direction vs encoder
ctrl.write( libPeregrine.PARAM_MOTOR_DIRECTION, 1 )
ctrl.write( libPeregrine.PARAM_MOTOR_DIRECTION, -1 )

# Limit switch mode
ctrl.write( libPeregrine.PARAM_LIMIT_SWITCH, libPeregrine.LIMIT_SWITCH_DISABLED )
ctrl.write( libPeregrine.PARAM_LIMIT_SWITCH, libPeregrine.LIMIT_SWITCH_ENABLED )
ctrl.write( libPeregrine.PARAM_LIMIT_SWITCH, libPeregrine.LIMIT_SWITCH_INVERTED )

# Power saving mode
ctrl.write( libPeregrine.PARAM_POWER_MODE, libPeregrine.POWER_SAVE )
ctrl.write( libPeregrine.PARAM_POWER_MODE, libPeregrine.POWER_ALWAYS_ON )

# Servo control parameters (advanced users only)
ctrl.write( libPeregrine.PARAM_SERVO_DEADZONE, 5 )  # Servo deadzone in encoder steps
ctrl.write( libPeregrine.PARAM_ERROR_GAIN, 4 )  # 1 .. 10
ctrl.write( libPeregrine.PARAM_LQR_K0, 4633 )  # LQR K0 term, multiplied by 10^4
ctrl.write( libPeregrine.PARAM_LQR_K1, 12278 )  # LQR K1 term, multiplied by 10^4

```
