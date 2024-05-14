import argparse
import numpy
import matplotlib.figure
import matplotlib.backends.backend_agg

# using argparse
descr = 'plotting Kepler data'
parser = argparse.ArgumentParser (description=descr)
parser.add_argument('-i', type=str, default="in.data", help='input file name (data)')
parser.add_argument('-o', type=str, default="out.png", help='output file name (png)')
args = parser.parse_args()

# get value from argument
file_data = args.i
file_png = args.o

# store data
data_mjd = numpy.array([])
data_flux = numpy.array([])
data_err = numpy.array([])

# read data
with open (file_data, 'r') as fh:
    for line in fh:
        if (line[0] == '#'):
            continue
        line = line.strip()
        all_data = line.split()
        mjd = float(all_data[1])
        flux = float(all_data[2]) / 10**6
        err = float(all_data[3]) / 10**6
        data_mjd = numpy.append(data_mjd, mjd)
        data_flux = numpy.append(data_flux, flux)
        data_err = numpy.append(data_err, err)
 
# objects for plotting
fig = matplotlib.figure.Figure()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
ax = fig.add_subplot(111)
ax.set_xlabel('MJD [day]')
ax.set_ylabel('Flux [10^6 e-/sec]')
ax.errorbar(data_mjd, data_flux, yerr=data_err, \
             linestyle='None', marker='.', markersize=1, color='blue', \
             ecolor='black', capsize=1, label='photometry of Kepler-2')
ax.legend()
fig.savefig(file_png, dpi=150)
