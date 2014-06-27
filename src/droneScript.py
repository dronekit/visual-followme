from droneapi.lib import VehicleMode
from pymavlink import mavutil


# First get an instance of the API endpoint
api = local_connect()

# get our vehicle - when running with mavproxy it only knows about one vehicle (for now)
v = api.get_vehicles()[0]

# Print out some interesting stats about the vehicle
print "Mode: %s" % v.mode
print "Location: %s" % v.location
print "Attitude: %s" % v.attitude
print "GPS: %s" % v.gps_0
print "Armed: %s" % v.armed