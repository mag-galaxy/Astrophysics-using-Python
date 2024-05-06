import argparse
import numpy
import matplotlib.figure
import matplotlib.backends.backend_agg

# using argparse
descr = 'visualisation of proper motion of stars'
parser = argparse.ArgumentParser(description=descr)
parser.add_argument('-i', '--input', help='input file name')
parser.add_argument('-o', '--output', help='output file name')
parser.add_argument('-a1', type=float, default=0.0,help='minimum RA')
parser.add_argument('-a2', type=float, default=0.0, help='maximum RA')
parser.add_argument('-d1', type=float, default=0.0, help='minimum Dec')
parser.add_argument('-d2', type=float, default=0.0, help='maximum Dec')
parser.add_argument('radii', type=float, nargs='+', help='radii in mas/yr')
args = parser.parse_args()

# input parameters
file_input     = args.input
file_output    = args.output
pmra_min       = args.a1
pmra_max       = args.a2
pmdec_min      = args.d1
pmdec_max      = args.d2
list_radii     = args.radii

# lists to store data
list_pmra     = []
list_pmdec    = []

# opening file
with open (file_input, 'r') as fh:
    # read by line
    for line in fh:
        if (line[0] == '#'):
            continue
        # removing new line at the end of the line
        line = line.strip ()
        data = line.split ()
        list_pmra.append (float (data[4]) )
        list_pmdec.append (float (data[5]) )

# making numpy arrays
data_pmra     = numpy.array (list_pmra)
data_pmdec    = numpy.array (list_pmdec)

# # clearing lists
# list_pmra.clear ()
# list_pmdec.clear ()

# making empty lists
list_pmra_selected  = []
list_pmdec_selected = []

# finding candidate stars
for i in range (len (data_pmra)):
    # rejecting star if pmra is smaller than pmra_min
    if (data_pmra[i] < pmra_min):
        continue
    # rejecting star if pmra is larger than pmra_max
    if (data_pmra[i] > pmra_max):
        continue
    # rejecting star if pmdec is smaller than pmdec_min
    if (data_pmdec[i] < pmdec_min):
        continue
    # rejecting star if pmdec is larger than pmdec_max
    if (data_pmdec[i] > pmdec_max):
        continue
    # appending data to lists
    list_pmra_selected.append(data_pmra[i])
    list_pmdec_selected.append(data_pmdec[i])

# calculating mean proper motion of candidate stars
data_pmra_selected  = numpy.array(list_pmra_selected)
data_pmdec_selected = numpy.array(list_pmdec_selected)
mean_pmra           = numpy.mean(data_pmra_selected)
mean_pmdec          = numpy.mean(data_pmdec_selected)

print (f'mean pmra and pmdec of star cluster member candidates:')
print (f'  mean pmra  = {mean_pmra:+6.2f} [mas/yr]')
print (f'  mean pmdec = {mean_pmdec:+6.2f} [mas/yr]')

# objects for plotting
fig    = matplotlib.figure.Figure ()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax     = fig.add_subplot (111)
ax.set_xlabel ('Proper motion in RA [mas/yr]')
ax.set_ylabel ('Proper motion in Dec [mas/yr]')
ax.set_aspect ('equal')
ax.grid ()
ax.set_xlim (pmra_min, pmra_max)
ax.set_ylim (pmdec_min, pmdec_max)
ax.plot (data_pmra, data_pmdec, \
         linestyle='None', marker='o', markersize=1, color='blue', alpha=0.5, \
         zorder=0.1, label='Stars in Gaia DR3')
ax.plot (mean_pmra, mean_pmdec, \
         linestyle='None', marker='+', markersize=10, color='red', \
         zorder=0.2, label='mean proper motion')
for r in list_radii:
    n = 1000
    data_theta = numpy.linspace (0.0, 2.0 * numpy.pi, n)
    data_x     = r * numpy.cos (data_theta) + mean_pmra
    data_y     = r * numpy.sin (data_theta) + mean_pmdec
    ax.plot (data_x, data_y, linestyle='-', linewidth=1, \
             label=f'radius = {r:4.2f}')
ax.legend (bbox_to_anchor=(1.05, 0.95), loc='upper left')
fig.savefig (file_output, dpi=150, bbox_inches="tight")
