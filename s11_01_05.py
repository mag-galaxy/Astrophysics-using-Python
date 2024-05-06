import argparse
import numpy
import matplotlib.figure
import matplotlib.backends.backend_agg

# using argparse
descr = 'visualisation of proper motion of stars'
parser = argparse.ArgumentParser(description=descr)
parser.add_argument('-i', '--input', help='input file name (list)')
parser.add_argument('-o', '--output', help='output file name (png)')
parser.add_argument('-a1', type=float, default=0.0, help='minimum RA')
parser.add_argument('-a2', type=float, default=0.0, help='maximum RA')
parser.add_argument('-d1', type=float, default=0.0, help='minimum Dec')
parser.add_argument('-d2', type=float, default=0.0, help='maximum Dec')
args = parser.parse_args()

# get value from argument
file_input = args.input
file_output = args.output
pmra_min = args.a1
pmra_max = args.a2
pmdec_min = args.d1
pmdec_max = args.d2

# empty lists
list_pmra = []
list_pmdec = []

# opening file
with open (file_input, 'r') as fh:
    # read by line
    for line in fh:
        if (line[0] == '#'):
            continue
        # removing new line at the end of the line
        line = line.strip()
        data = line.split()
        # fields
        list_pmra.append(float (data[4]) )
        list_pmdec.append(float (data[5]) )

# making numpy arrays
data_pmra = numpy.array(list_pmra)
data_pmdec = numpy.array(list_pmdec)

# # clearing lists
# list_pmra.clear ()
# list_pmdec.clear ()

# making objects "fig", "canvas", and "ax"
fig = matplotlib.figure.Figure()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
ax = fig.add_subplot(111)
ax.set_xlabel('Proper motion in RA [mas/yr]')
ax.set_ylabel('Proper motion in Dec [mas/yr]')
ax.set_aspect('equal')
ax.grid()
ax.set_xlim(pmra_min, pmra_max)
ax.set_ylim(pmdec_min, pmdec_max)
ax.plot(data_pmra, data_pmdec, \
         linestyle='None', marker='o', markersize=1, color='blue', alpha=0.5, \
         label='Stars in Gaia DR3')
ax.legend(bbox_to_anchor=(1.05, 0.95), loc='upper left')
fig.savefig (file_output, dpi=150, bbox_inches="tight")
