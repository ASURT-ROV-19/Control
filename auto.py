# -*- coding: utf-8 -*-

"""
    Based on Arduino PID Library (Version 1.0.1) by Brett Beauregard <br3ttb@gmail.com> brettbeauregard.com
"""

from __future__ import division
from UDP import UDP_Server
import sys
import time
import Adafruit_PCA9685

#kp = 130 , ki = 80 , kp = 0.1

out_max = 400
out_min = 230
zero_offset = 305
direct = True
sample_time = 0.01  # seconds


kpx = 0.7
kix = 0.1
kdx = 0.001
output_valuex = 0.0
last_inputx = 0.0
i_termx = 0.0
windup_guardx = 5.0
out_maxx = 330
out_minx = 270
last_timex=0.0
errorx=0.0

kpy = 1.0
kiy = 0.2
kdy = 0.001
output_valuey = 0.0
last_inputy = 0.0
i_termy = 0.0
windup_guardy = 5.0
out_maxy = 350
out_miny = 250
last_timey=0.0
errory=0.0

kpyaw = 0.7
kiyaw =  0.1
kdyaw = 0.001
output_value_yaw = 0.0
last_input_yaw = 0.0
i_term_yaw = 0.0
windup_guard_yaw = 5.0
out_max_yaw = 330
out_min_yaw = 270
last_time_yaw = 0.0
error_yaw = 0.0

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

last_time = time.time() - sample_time

#sensor.setFluidDensity(1000) # kg/m^3

def computex(kpx,kix,kdx,direct,errorx,
            sample_time,last_timex,windup_guardx,i_termx,
            output_valuex,last_inputx,out_minx,out_maxx):
    
    
    now = time.time()
    time_change = now - last_timex
    
    #error = setpoint - input_value
    
    i_termx += kix * errorx * sample_time
    if i_termx > windup_guardx:
         i_termx = out_maxx
    elif i_termx < -windup_guardx:
         i_termx = out_minx

    delta_input = errorx - last_inputx
    output = (kpx * errorx) + i_termx + (kdx * (delta_input / sample_time))
    print(output)
    #output += zero_offset
    if output > out_maxx:
        output = out_maxx
    elif output < out_minx:
        output = out_minx

    output_valuex = output

    last_inputx = errorx
    last_timex = now
    return output_valuex

def computeyaw(kpyaw,kiyaw,kdyaw,direct,error_yaw,
            sample_time,last_time_yaw,windup_guard_yaw,i_term_yaw,
            output_value_yaw,last_input_yaw,out_min_yaw,out_max_yaw):
    
    
    now = time.time()
    time_change = now - last_time_yaw
    
    #error = setpoint - input_value
    
    i_term_yaw += kiyaw * error_yaw * sample_time
    if i_term_yaw > windup_guard_yaw:
         i_term_yaw = out_max_yaw
    elif i_term_yaw < -windup_guard_yaw:
         i_term_yaw = out_min_yaw

    delta_input = error_yaw - last_input_yaw
    output = (kpyaw * error_yaw) + i_term_yaw + (kdyaw * (delta_input / sample_time))
    print(output)
    #output += zero_offset
    if output > out_max_yaw:
        output = out_max_yaw
    elif output < out_min_yaw:
        output = out_min_yaw

    output_value_yaw = output

    last_input_yaw = error_yaw
    last_time_yaw = now
    return output_value_yaw

def computey(kpy,kiy,kdy,direct,errory,
            sample_time,last_timey,windup_guardy,i_termy,
            output_valuey,last_inputy,out_miny,out_maxy):
    
    
    now = time.time()
    time_change = now - last_timey
    
    #error = setpoint - input_value
    
    i_termy += kiy * errory * sample_time
    if i_termy > windup_guardy:
         i_termy = out_maxy
    elif i_termy < -windup_guardy:
         i_termy = out_miny

    delta_input = errory - last_inputy
    output = (kpy * errory) + i_termy + (kdy * (delta_input / sample_time))
    print(output)
    output += zero_offset
    if output > out_maxy:
        output = out_maxy
    elif output < out_miny:
        output = out_miny

    output_valuey = output

    last_inputy = errory
    last_timey = now
    return output_valuey

if __name__ == '__main__':
    print("yallaaaaaaa")
    #setpoint = input("enter height : ")
    #freshwaterDepth = input("enter depth : ")
    
    anwar=UDP_Server("10.1.1.15",9020)
    
    #setpoint = float(setpoint)
    #nput_value = input("enter current point : ")
    #input_value=float(input_value)
    #freshwaterDepth = float(freshwaterDepth)
    
    pwm.set_pwm(5, 0, 305)
    pwm.set_pwm(7, 0, 305)
    pwm.set_pwm(13, 0, 305)
    pwm.set_pwm(15, 0, 305)
    pwm.set_pwm(11, 0, 305)
    pwm.set_pwm(9, 0, 305)
    pwm.set_pwm(9, 0, 305)
    pwm.set_pwm(8, 0, 305)

    time.sleep(0.1)
    try:
        while True:
            data=anwar.recieve()
            #print(data)
            data=data.split(",")
            #print(data)
            #print(data[0])
            errorx=int(data[0])
            errory=int(data[1])
            print("error in x: "+str(errorx))
            print("error in y: "+str(errory))
            val  = computex(kpx,kix,kdx,direct,errorx,
                            sample_time,last_timex,windup_guardx,i_termx,
                            output_valuex,last_inputx,out_minx,out_maxx)
            val1 = computey(kpy,kiy,kdy,direct,errory,
                            sample_time,last_timey,windup_guardy,i_termy,
                            output_valuey,last_inputy,out_miny,out_maxy)
            val2 = computeyaw(kpyaw,kiyaw,kdyaw,direct,error_yaw,
                            sample_time,last_time_yaw,windup_guard_yaw,i_term_yaw,
                            output_value_yaw,last_input_yaw,out_min_yaw,out_max_yaw)
            print("pwm: " + str(val))

            if val:
                
                val = int(val)
                val1= int(val1)

                pwm.set_pwm(7, 0,  zero_offset+val)
                pwm.set_pwm(5, 0,  zero_offset-val)
                pwm.set_pwm(13, 0, zero_offset+val)
                pwm.set_pwm(15, 0, zero_offset-val)
                pwm.set_pwm(11, 0, val1)
                pwm.set_pwm(9, 0,  val1)

                last_time = time.time()
            else :
                print("\n")

            time.sleep(0.01)

    except KeyboardInterrupt:
        time.sleep(0.1)
        print("no")
        pwm.set_pwm(5, 0, 305)
        pwm.set_pwm(7, 0, 305)
        pwm.set_pwm(13, 0, 305)
        pwm.set_pwm(15, 0, 305)
        pwm.set_pwm(11, 0, 305)
        pwm.set_pwm(9, 0, 305)

    sys.exit()
