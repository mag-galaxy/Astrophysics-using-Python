import matplotlib.backends.backend_agg
import matplotlib.figure
import numpy
import argparse
import pathlib
import sys

parser = argparse.ArgumentParser(description='plotting f(x)')
# add argument
parser.add_argument ('-o', '--output', default='output.png',\
                     help='output file name (default: output.png)')
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
data_x = numpy.linspace (-0.5, 0.5, 20000)
data_y = data_x * numpy.sin(1/data_x)

# figure,anvas,axes object
fig = matplotlib.figure.Figure()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
ax = fig.add_subplot(111)

ax.plot(data_x, data_y, label = r'$f(x) = x*sin(1/x)$')
ax.set_xlim(-0.5, 0.5)
ax.set_ylim(-0.5, 0.5)
ax.set_xlabel('$x$')
ax.set_ylabel('$f(x)$')
ax.set_xticks(numpy.linspace(-0.5, 0.5, 11))
ax.set_yticks(numpy.linspace(-0.5, 0.5, 11))
ax.grid()
ax.legend()

fig.savefig(file_output, dpi = g_resolution)
