import argparse
import numpy
import astropy.io.votable
import matplotlib.figure
import matplotlib.backends.backend_agg

# using argparse
descr = 'distribution of distance of stars'
parser = argparse.ArgumentParser(description=descr)
parser.add_argument('-i', '--input', help='input file name (gzip)')
parser.add_argument('-o', '--output', help='output file name (png)')
parser.add_argument('-a', '--min', type=float, help='minimum data value')
parser.add_argument('-b', '--max', type=float, help='maximum data value')
parser.add_argument('-n', '--nbins', type=int, help='number of bins')
args = parser.parse_args ()

# get value from argument
file_votable = args.input
file_fig = args.output
x_min = args.min
x_max = args.max
n_bins = args.nbins

# read input file
table = astropy.io.votable.parse_single_table(file_votable).to_table()

# data
data_ra        = numpy.array(table['ra'])
data_dec       = numpy.array(table['dec'])
data_parallax  = numpy.array(table['parallax'])
data_p_snr     = numpy.array(table['parallax_over_error'])

# distance
data_distance = numpy.array([])
for i in range(len(data_parallax)):
    # rejecting stars of negative parallax, no measurement of parallax,
    # and parallax SNR less than 10.0
    if ((data_parallax[i] <= 0.0) or (numpy.isnan(data_parallax[i]) ) \
         or (data_p_snr[i] < 10.0)):
        data_distance.append(-1.0)
    else:
        data_distance.append(1000.0 / data_parallax[i])

# objects for plotting
fig = matplotlib.figure.Figure()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
ax = fig.add_subplot(111)
bin_range = (x_min, x_max)      # set range of bins
ax.set_xlabel('Distance [pc]')
ax.set_ylabel('Number of Stars')
ax.set_xlim(bin_range)
ax.grid()
ax.hist(data_distance, bins=n_bins, range=bin_range, histtype='bar', align='mid')
fig.savefig (file_fig, dpi=150)
