# visual-follow

This is a developer preview of visual based follow-me enhancements.   When combined with conventional GPS based follow-me, this module will attempt to usethe gimbal to keep the target centered in frame.

# Limitations

The blob detector depends on color - in particular a red hat or shirt.  Future releases will be smarter about selecting the target.

# Usage

* Install the [DroneAPI](http://dev.ardupilot.com/wiki/droneapi-tutorial/).
* cd src
* Run mavproxy to connect to vehicle (i.e. mavproxy.py --master=/dev/ttyACM0,115000).
* Run "api start src/drone_script.py"
* These steps can be combined into a single init script as necessary
