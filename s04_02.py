import matplotlib.backends.backend_agg
import matplotlib.figure
import numpy
import argparse
import pathlib
import sys

parser = argparse.ArgumentParser(description='plotting normal distribution')
# add argument
parser.add_argument ('-o', '--output', default='normal_dis.png',\
                     help='output file name (default: normal_dis.png)')
parser.add_argument ('-r', '--resolution', type=float, default=250.0,\
                     help='resolution of plot in DPI (default: 250.0)')
args = parser.parse_args()
file_output = args.output
g_resolution = args.resolution

# output
path_output = pathlib.Path(file_output)

# check of existence of output file
if(path_output.exists()):
    print (f'ERROR: output file "{file_output}" exists!')
    sys.exit(0)

if not((path_output.suffix == '.eps')\
       or(path_output.suffix == '.pdf')\
       or(path_output.suffix == '.png')\
       or(path_output.suffix == '.ps')):
    print (f'ERROR: output file must be either EPS or PDF or PNG or PS file.')
    sys.exit(0)

# data
mu = 0 # mean
sigma = 1 # standard deviation
data_x = numpy.linspace(-5, 5, 10000)
data_y = 1 / ((2*numpy.pi)**(1/2) * sigma) * numpy.exp((-1/2)*(((data_x-mu)/sigma)**2))

# figure,anvas,axes object
fig = matplotlib.figure.Figure()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
ax = fig.add_subplot(111)

# plot
ax.plot(data_x, data_y, color = 'green', linestyle = '--',\
        linewidth = 5, label = 'normal distribution')
ax.set_xlim(-5, 5)
ax.set_ylim(0.0, 1.0)
ax.set_xlabel('$z-score$')
ax.set_ylabel('$probability density$')
ax.set_xticks(numpy.linspace(-5, 5, 11))
# ax.set_yticks(numpy.linspace(0.0, 1.0, 11))
ax.grid()
ax.legend()

fig.savefig(file_output, dpi = g_resolution)
