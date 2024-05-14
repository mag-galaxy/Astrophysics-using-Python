import argparse
import matplotlib.figure
import matplotlib.backends.backend_agg
import numpy
import scipy.optimize

# using argparse
descr = 'finding peak of power spectrum'
parser = argparse.ArgumentParser(description=descr)
parser.add_argument('-i', type=str, default="in.data", help='input file name (data)')
parser.add_argument('-o', type=str, default="out.eps", help='output file name (png)')
parser.add_argument('-x1', type=float, default=0.0, help='min. period plotted in day')
parser.add_argument('-x2', type=float, default=100.0, help='max. period plotted in day')
parser.add_argument('-f1', type=float, default=1.0, help='min. period fitted in day')
parser.add_argument('-f2', type=float, default=10.0, help='max. period fitted in day')
parser.add_argument('-a', type=float, default=1.0, help='coe a')
parser.add_argument('-b', type=float, default=1.0, help='coe b')
parser.add_argument('-c', type=float, default=1.0, help='coe c')
args = parser.parse_args()

# get value from argument
input_data = args.i
output_png = args.o
per_min_day = args.x1
per_max_day = args.x2
fitting_min_day = args.f1
fitting_max_day = args.f2
a = args.a
b = args.b
c = args.c

# store data
data_freq = numpy.array([])
data_per_day = numpy.array([])
data_per_hr = numpy.array([])
data_per_min = numpy.array([])
data_power = numpy.array([])
fit_freq = numpy.array([])
fit_per_day = numpy.array([])
fit_per_hr = numpy.array([])
fit_per_min = numpy.array([])
fit_power = numpy.array([])

# read data file
with open (input_data, 'r') as fh:
    for line in fh:
        if (line[0] == '#'):
            continue
        line = line.strip()
        all_data = line.split()
        freq = float(all_data[0])
        per_day = float(all_data[1])
        per_hr = float(all_data[2])
        per_min = float(all_data[3])
        power = float(all_data[5])
        if (per_day >= per_min_day and per_day <= per_max_day):
            data_freq = numpy.append(data_freq, freq)
            data_per_day = numpy.append(data_per_day, per_day)
            data_per_hr = numpy.append(data_per_hr, per_hr)
            data_per_min = numpy.append(data_per_min, per_min)
            data_power = numpy.append(data_power, power)
        if (per_day >= fitting_min_day and per_day <= fitting_max_day):
            fit_freq = numpy.append(fit_freq, freq)
            fit_per_day = numpy.append(fit_per_day, per_day)
            fit_per_hr = numpy.append(fit_per_hr, per_hr)
            fit_per_min = numpy.append(fit_per_min, per_min)
            fit_power = numpy.append(fit_power, power)

# function for fitting
def func(x, a, b, c):
    y = -a * (x - b)**2 + c
    return y

# least-squares fitting using scipy.optimize.curve_fit
popt, pcov = scipy.optimize.curve_fit(func, fit_per_day, fit_power, \
                                p0=[a, b, c], maxfev=3000, method='lm')

# result of fitting
a_fitted = popt[0]
b_fitted = popt[1]
c_fitted = popt[2]
a_err = numpy.sqrt(pcov[0][0])
b_err = numpy.sqrt(pcov[1][1])
c_err = numpy.sqrt(pcov[2][2])
print(f"a = {a_fitted:15.8f} +/- {a_err:15.8f} ({a_err/a_fitted*100:8.4f} %)")
print(f"b = {b_fitted:15.8f} +/- {b_err:15.8f} ({b_err/b_fitted*100:8.4f} %)")
print(f"c = {c_fitted:15.8f} +/- {c_err:15.8f} ({c_err/c_fitted*100:8.4f} %)")

# generate fitted line
fitted_x = numpy.linspace(fitting_min_day, fitting_max_day, 10**3)
fitted_y = func(fitted_x, a_fitted, b_fitted, c_fitted)

# objects for plotting
fig = matplotlib.figure.Figure()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
ax = fig.add_subplot(111)
ax.set_xlabel('Period [day]')
ax.set_ylabel('Power')
ax.set_xlim(per_min_day, per_max_day)
ax.plot(data_per_day, data_power, \
         linestyle='-', linewidth=5, color='blue', \
         label='result of Lomb-Scargle periodogram')
ax.plot(fitted_x, fitted_y, \
         linestyle=':', linewidth=3, color='red', \
         label='result of least-squares fitting')
ax.legend(bbox_to_anchor=(1.0, 1.16), loc='upper right')
fig.savefig(output_png, dpi=150)
