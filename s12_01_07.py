import argparse
import numpy
import matplotlib.figure
import matplotlib.backends.backend_agg

# using argparse
descr = 'plotting power spectrum'
parser = argparse.ArgumentParser(description=descr)
parser.add_argument('-i', type=str, default="in.data", help='input file name (data)')
parser.add_argument('-o', type=str, default="out.png", help='output file name (png)')
parser.add_argument('-a', type=float, default=0.0, help='min. period plotted in day')
parser.add_argument('-b', type=float, default=100.0, help='max. period plotted in day')
args = parser.parse_args()

# get value from argument
file_data = args.i
file_png = args.o
per_min_day = args.a
per_max_day = args.b

# store data
data_freq = numpy.array([])
data_per_day = numpy.array([])
data_per_hr = numpy.array([])
data_per_min = numpy.array([])
data_power = numpy.array([])

# read data
with open (file_data, 'r') as fh:
    for line in fh:
        if (line[0] == '#'):
            continue
        line = line.strip()
        all_data = line.split()
        freq = float(all_data[0])
        per_day = float(all_data[1])
        per_hr = float(all_data[2])
        per_min = float(all_data[3])
        power = float(all_data[4])
        if (per_day >= per_min_day and per_day <= per_max_day):
            data_freq = numpy.append(data_freq, freq)
            data_per_day = numpy.append(data_per_day, per_day)
            data_per_hr = numpy.append(data_per_hr, per_hr)
            data_per_min = numpy.append(data_per_min, per_min)
            data_power = numpy.append(data_power, power)
            
# objects for plotting
fig = matplotlib.figure.Figure()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
ax = fig.add_subplot(111)
ax.set_xlabel('Period [day]')
ax.set_ylabel('Power')
ax.set_xlim(per_min_day, per_max_day)
ax.plot(data_per_day, data_power, \
         linestyle='-', linewidth=3, color='blue', \
         label='result of Lomb-Scargle periodogram')
ax.legend(bbox_to_anchor=(1.0, 1.12), loc='upper right')
fig.savefig(file_png, dpi=150)
