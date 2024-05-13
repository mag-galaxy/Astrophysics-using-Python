import argparse
import numpy
import scipy.optimize
import matplotlib.figure
import matplotlib.backends.backend_agg

# using argparse
descr = 'baseline fitting'
parser = argparse.ArgumentParser(description=descr)
parser.add_argument ('-i', type=str, default="in.data", help='input file name (data)')
parser.add_argument ('-o', type=str, default="out.eps", help='output file name (png)')
args = parser.parse_args()

# get value from argument
file_data = args.i
file_fig = args.o

# store data
data_mjd = numpy.array([])
data_flux = numpy.array([])
data_err = numpy.array([])

mjd_min = +9999999.0
mjd_max = -9999999.0

# read data file
with open (file_data, 'r') as fh:
    for line in fh:
        if (line[0] == '#'):
            continue
        line = line.strip()
        all_data = line.split()
        # (datetime_str, mjd_str, flux_str, err_str) = line.split()
        if (all_data[2] == 'nan'):
            continue
        mjd = float(all_data[1])
        flux = float(all_data[2])
        err = float(all_data[3])
        data_mjd = numpy.append(data_mjd, mjd)
        data_flux = numpy.append(data_flux, flux)
        data_err = numpy.append(data_err, err)

        # get range of data
        if (mjd < mjd_min):
            mjd_min = mjd
        if (mjd > mjd_max):
            mjd_max = mjd

# coefficients and function of fitting line
a = 1.0
b = 1.0 * 10**6
def func(x, a, b):
    y = -a * x + b
    return y

# least-squares fitting
popt, pcov = scipy.optimize.curve_fit(func, data_mjd, data_flux, \
                                       sigma=data_err, p0=[a, b])

# print fitted result
a_fitted = popt[0]
b_fitted = popt[1]
a_err = numpy.sqrt(pcov[0][0])
b_err = numpy.sqrt(pcov[1][1])
print(f"a = {a_fitted} +/- {a_err} ({a_err / a_fitted * 100.0} %)")
print(f"b = {b_fitted} +/- {b_err} ({b_err / b_fitted * 100.0} %)")

# generate fitted line
fitted_x = numpy.linspace(mjd_min, mjd_max, 10**3)
fitted_y = func (fitted_x, a_fitted, b_fitted)

# objects for plotting
fig = matplotlib.figure.Figure()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
ax = fig.add_subplot(111)
ax.set_xlabel('MJD [day]')
ax.set_ylabel('Flux [10^6 e-/sec]')
ax.plot(data_mjd, data_flux, linestyle='-', linewidth=3, \
        color='blue', label='Photometry of Kepler-2')
ax.plot(fitted_x, fitted_y, linestyle=':', linewidth=5, \
        color='red', label='Baseline')
ax.legend()
fig.savefig(file_fig, dpi=150)
