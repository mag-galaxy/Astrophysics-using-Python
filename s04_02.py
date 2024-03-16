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
