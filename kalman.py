import numpy
import pylab
import ms5837
import time

# intial parameters
iteration_count = 50
empty_iteration_tuple = (iteration_count,)  # size of array
actual_value = -0.37727  # truth value
#noisy_measurement = numpy.random.normal(actual_value, 0.1, size=empty_iteration_tuple)  # observations (normal about x, sigma=0.1)
sensor = ms5837.MS5837_30BA()
if not sensor.init():
        print "Sensor could not be initialized"
        exit(1)

# We have to read values from sensor to update pressure and temperature
if not sensor.read():
    print "Sensor read failed!"
    exit(1)

print("Pressure: %.2f atm  %.2f Torr  %.2f psi") % (
sensor.pressure(ms5837.UNITS_atm),
sensor.pressure(ms5837.UNITS_Torr),
sensor.pressure(ms5837.UNITS_psi))

print("Temperature: %.2f C  %.2f F  %.2f K") % (
sensor.temperature(ms5837.UNITS_Centigrade),
sensor.temperature(ms5837.UNITS_Farenheit),
sensor.temperature(ms5837.UNITS_Kelvin))

freshwaterDepth = sensor.depth() # default is freshwater
sensor.setFluidDensity(ms5837.DENSITY_SALTWATER)
saltwaterDepth = sensor.depth() # No nead to read() again
sensor.setFluidDensity(1000) # kg/m^3
print("Depth: %.3f m (freshwater)  %.3f m (saltwater)") % (freshwaterDepth, saltwaterDepth)

# fluidDensity doesn't matter for altitude() (always MSL air density)
print("MSL Relative Altitude: %.2f m") % sensor.altitude() # relative to Mean Sea Level pressure in air

process_variance = 1e-5  # process variance

# allocate space for arrays
posteri_estimate = numpy.zeros(empty_iteration_tuple)
posteri_error_estimate = numpy.zeros(empty_iteration_tuple)
priori_estimate = numpy.zeros(empty_iteration_tuple)
priori_error_estimate = numpy.zeros(empty_iteration_tuple)
blending_factor = numpy.zeros(empty_iteration_tuple)
data = numpy.zeros(empty_iteration_tuple)

estimated_measurement_variance = 0.1 ** 2  # estimate of measurement variance, change to see effect

# intial guesses
posteri_estimate[0] = 0.0
posteri_error_estimate[0] = 1.0

for iteration in range(1, iteration_count):
    # time update
    priori_estimate[iteration] = posteri_estimate[iteration - 1]
    priori_error_estimate[iteration] = posteri_error_estimate[iteration - 1] + process_variance

    # measurement update
    blending_factor[iteration] = priori_error_estimate[iteration] / (priori_error_estimate[iteration] + estimated_measurement_variance)
    # noisy measurement is the only thing where we need the entire list
    posteri_estimate[iteration] = priori_estimate[iteration] + blending_factor[iteration] * (sensor.pressure() - priori_estimate[iteration])
    posteri_error_estimate[iteration] = (1 - blending_factor[iteration]) * priori_error_estimate[iteration]
    print(posteri_estimate[iteration])

#pylab.figure()
#pylab.plot(data, 'k+', label='noisy measurements')
#pylab.plot(posteri_estimate, 'b-', label='a posteri estimate')
#pylab.axhline(actual_value, color='g', label='truth value')
#pylab.legend()
#pylab.xlabel('Iteration')
#pylab.ylabel('Voltage')
#pylab.show()
#pylab.plot(data)
