# read csv file and plot
import astropy.io.ascii
import astropy.units
import astropy.constants
import numpy
import matplotlib.figure
import matplotlib.backends.backend_agg
import scipy.optimize
import scipy.constants

# file names
file_csv = 'Leda_data_1.txt'
file_fig = 'Leda_data.png'
resolution_dpi = 150

# units
u_km  = astropy.units.km
u_Mpc = astropy.units.Mpc
u_sec = astropy.units.s
u_yr  = astropy.units.yr

# store data
data_d = []
data_v = []

with open(file_csv, 'r') as f_read:
  for line in f_read:
    if("#" in line):
       continue
    data = line.split(',')
    if(data[0] == 'objname'):
      continue
    name = data[0]
    dis_pc = 10 ** (float(data[1])/5.0 + 1.0)  # distance in parsecs = 10^(distance modulus/5+1)
    dis_Mpc = dis_pc * 10**-6
    vel = float(data[2])  # km/s
    data_d.append(dis_Mpc)
    data_v.append(vel)

# change lists into numpy array
arr_data_d = numpy.array(data_d)
arr_data_v = numpy.array(data_v)
print('finish reading data')

# initial values of coefficient
H0 = 100.0
init = [H0]

# function (a line go through O(0,0))
def func (x, H0):
    y = H0 * x
    return(y)

# using least-squares method
popt, pcov = scipy.optimize.curve_fit(func, data_d, data_v, p0=init)

# result of fitting
H0_bestfit = popt[0]
print(f'popt: {popt}')
print(f'pcov: {pcov}')

# Hubble constant
H0_err = numpy.sqrt(pcov[0][0])
print(f"H0 = {H0_bestfit} +/- {H0_err} ({H0_err / H0_bestfit * 100.0} %)")

# fitted curve
fitted_x = numpy.linspace(0.0, 5000.0, 10000)
fitted_y = func(fitted_x, H0_bestfit)

# figure, canvas, axes object for plotting
fig = matplotlib.figure.Figure()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
ax = fig.add_subplot(111)

ax.set_xlabel('Distance [Mpc]')
ax.set_ylabel('Velocity [km/s]')
ax.grid ()
ax.plot(data_d, data_v, linestyle='None', marker='o', markersize=2, \
        color='blue', zorder=0.2, label='LEDA')
label_fitting = f"best-fit line (H0={H0_bestfit:4.1f} km/sec/Mpc)"
ax.plot(fitted_x, fitted_y, linestyle='--', linewidth=3, color='red', \
         zorder=0.1, label=label_fitting)
ax.legend()
fig.savefig(file_fig, dpi = resolution_dpi)

hubble_constant_with_units = H0_bestfit * u_km / u_sec / u_Mpc
hubble_time = 1.0 / hubble_constant_with_units

print (f'Hubble constant = {hubble_constant_with_units}')
print (f'Estimation of age of Universe = {hubble_time.to (u_yr):g}')
