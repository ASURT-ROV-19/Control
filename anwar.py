from __future__ import division
from anwar import PID
from UDP import UDP_Server
import sys
import time
import Adafruit_PCA9685
from VideoStream import *
import logging
from Adafruit_BNO055 import BNO055


pipline = "v4l2src device=/dev/video0 ! image/jpeg,width=1920,height=1080,framerate=30/1 ! rtpjpegpay ! udpsink host=10.1.1.14 port=5000"
camera  = Gstreamer(pipline)

cony_f   = PID(1,0 ,0 , 340, 250)
cony_b   = PID(1,0 ,0 , 340, 250)

conyaw_f = PID(0.3,0 ,0 , 340, 250)
conyaw_b = PID(0.3,0 ,0 , 340, 250)

conz     = PID(130,80 ,0.1 , 370, 220)

print("yallaaaaaaa")

toss=UDP_Server("10.1.1.15",9020)
helali=UDP_Client("192.168.43.190",9921)

bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)

# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status, self_test, error = bno.get_system_status()

# Pressure sensor
sensor = ms5837.MS5837_30BA()
# We must initialize the sensor before reading it
if not sensor.init():
        exit(1)

# We have to read values from sensor to update pressure and temperature
if not sensor.read():
    exit(1)

sensor.setFluidDensity(1000) # kg/m^3

# Sensor data, desired set value, errors, and PWMs 
sensor_yaw = 0.0
set_yaw    = 0.0
sensor_z   = 0.0
set_z      = 0.0
errory     = 0.0
errorz     = 0.0  
erroryaw   = 0.0

set_yawz   = 0.0

valy_f, valy_b, valyaw_f, valyaw_b,valz = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0


sensor_yaw, roll, pitch = bno.read_euler()
print (sensor_yaw)

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

pwm.set_pwm(3, 0, 305)
pwm.set_pwm(5, 0, 305)
pwm.set_pwm(9, 0, 305)
pwm.set_pwm(8, 0, 305)
pwm.set_pwm(13, 0, 305)
pwm.set_pwm(15, 0, 305)
pwm.set_pwm(11, 0, 305)

time.sleep(0.01)

motors = [0,0,0,0,0,0]

set_pointyaw  = False
ack           = False
set_pointz    = False
set_pointyawz = False

read    = 0.0
factorz = 0.0003

input("Enter.....")
set_yaw, roll, pitch = bno.read_euler()

try:
    while True:

            data=toss.recieve()
            data=data.split(",")

            errory   = float(data[0])
            errorz   = float(data[1])
            
            sensor_yaw, roll, pitch = bno.read_euler()
            erroryaw =  set_yaw - sensor_yaw
            
            # Read the Euler angles for heading, roll, pitch (all in degrees).
            if erroryaw > 5 or erroryaw < -5:
                
                if not ack:
                    helali.send("halt")
                    print ("halt")
                    ack = True
                
                if not set_pointyawz:
                    set_yawz = sensor.depth()
                    set_pointyawz = True

                else :
                    read = sensor.depth()
                    errorz = set_yawz - read
                    conz.update(errorz)
                    valz   = conz.output
                    #pwm.set_pwm(11, 0, valz)
                    #pwm.set_pwm(9,  0, valz)

                conyaw_f.update(erroryaw)
                conyaw_b.update(-1.0*erroryaw)
                valyaw_f = conyaw_f.output
                valyaw_b = conyaw_b.output
                if erroryaw > 5:
                    print ("right")
                    print ("valyaw_b : " + str(valyaw_b))
                    print ("valyaw_f : " + str(valyaw_f))
                    pwm.set_pwm(13, 0, valyaw_b)
                    pwm.set_pwm(5, 0, valyaw_f)
                    pwm.set_pwm(15, 0, 305)

                elif erroryaw < -5:
                    print ("left")
                    print ("valyaw_b : " + str(valyaw_b))
                    print ("valyaw_f : " + str(valyaw_f))
                    pwm.set_pwm(5, 0, valyaw_f)
                    pwm.set_pwm(13, 0, valyaw_b)
                    pwm.set_pwm(15, 0, 305)

            else :
                set_pointyawz = False

            if (errorz > 33 or errorz < -33) and (not set_pointyawz):
                errorz = errorz * factorz
                conz.update(errorz)
                
                valz   = conz.output

                pwm.set_pwm(11, 0, valz)
                pwm.set_pwm(9,  0, valz)
            
            elif errory > 33 or errory < -33:

                cony_f.update(errory)
                cony_b.update(-1.0*errory)
                valy_f = cony_f.output
                valy_b = cony_b.output
                
                if not set_pointz :
                    set_z = sensor.depth()
                    set_z = float(set_pointz)
                    set_pointz = True

                elif set_pointz :
                    read = sensor.depth()
                    errorz = set_z - read
                    conz.update(errorz)
                    valz   = conz.output
                    pwm.set_pwm(11, 0, valz)
                    pwm.set_pwm(9,  0, valz)
                
                if errory > 33:
                    print("right")
                    pwm.set_pwm(5, 0, valy_b)
                    pwm.set_pwm(15,  0, valy_f)
                    pwm.set_pwm(13, 0, 305)
                
                elif errory < -33:
                    print("left")
                    pwm.set_pwm(5, 0, valy_b)
                    pwm.set_pwm(15,  0, valy_f)
                    pwm.set_pwm(13, 0, 305)

            else :
                print("end of track.... :D")

            time.sleep(0.01)

except KeyboardInterrupt:
    time.sleep(0.1)
    pwm.set_pwm(5, 0, 305)
    pwm.set_pwm(7, 0, 305)
    pwm.set_pwm(13, 0, 305)
    pwm.set_pwm(15, 0, 305)
    pwm.set_pwm(11, 0, 305)
    pwm.set_pwm(9, 0, 305)
    print("no")


sys.exit()

