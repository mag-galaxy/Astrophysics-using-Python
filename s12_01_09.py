import argparse
import numpy
import matplotlib.figure
import matplotlib.backends.backend_agg

# using argparse
descr = 'making folded lightcurve'
parser = argparse.ArgumentParser(description=descr)
parser.add_argument('-i', type=str, default="in.data", help='input file name (data)')
parser.add_argument('-o', type=str, default="out.png", help='output figure file name (png)')
parser.add_argument('-p', type=float, default=1.0, help='period in day')
args = parser.parse_args()

# get value from argument
file_data = args.i
file_fig = args.o
p_best = args.p

# store data
data_mjd = numpy.array([])
data_mag = numpy.array([])
data_err = numpy.array([])
data_phase = numpy.array([])

# read data file
with open (file_data, 'r') as fh:
    for line in fh:
        if (line[0] == '#'):
            continue
        line = line.strip()
        all_data = line.split()
        mjd = float(all_data[1])
        mag = float(all_data[2])
        err = float(all_data[3])
        data_mjd = numpy.append(data_mjd, mjd)
        data_mag = numpy.append(data_mag, mag)
        data_err = numpy.append(data_err, err)
        # calculation of phase using assumed period
        phase = (mjd - data_mjd[0]) / p_best
        phase -= int(phase)
        data_phase = numpy.append(data_phase, phase)

# objects for plotting
fig = matplotlib.figure.Figure()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
ax = fig.add_subplot(111)
ax.set_xlabel('Phase')
ax.set_ylabel('Relative Brightness')
ax.errorbar(data_phase, data_mag, yerr=data_err, \
             linestyle='None', marker='.', markersize=1, color='blue', \
             ecolor='black', capsize=1, \
             label=f'folded lightcurve of Kepler-2 using {p_best:8.6f} hr')
ax.errorbar(data_phase + 1.0, data_mag, yerr=data_err, \
             linestyle='None', marker='.', markersize=1, color='blue', \
             ecolor='black', capsize=1)
ax.legend(bbox_to_anchor=(1.0, 1.12), loc='upper right')
fig.savefig(file_fig, dpi=150)
