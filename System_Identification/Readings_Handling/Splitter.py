import matlab.engine

f = open("readings1.txt").readlines()
F_PWM = open("PWM.csv","w")
F_Pressure = open("Pressure.csv","w")

for line in f:
    pwm=line.split()[0]
    pressure=line.split()[1]
    F_PWM.write(pwm)
    F_PWM.write("\n")
    F_Pressure.write(pressure)
    F_Pressure.write("\n")

#Connect with MATlab    
eng = matlab.engine.connect_matlab()
#Makes MatLab recieve the .csv files we created above
eng.eval("pwms = csvread('C:\Users\Helaly\Desktop\Readings_Handling\PWM.csv');",nargout=0)
eng.eval("pressure = csvread('C:\Users\Helaly\Desktop\Readings_Handling\Pressure.csv');",nargout=0)

