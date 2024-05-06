import argparse
import numpy
import matplotlib.figure
import matplotlib.backends.backend_agg

# using argparse
descr  = 'visualisation of proper motion of stars'
parser = argparse.ArgumentParser(description=descr)
parser.add_argument('-i', '--input', help='input file name')
parser.add_argument('-o', '--output', help='output file name')
args = parser.parse_args ()

# get value from argument
file_input = args.input
file_output = args.output

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
        # splitting the line
        data = line.split()
        list_pmra.append(float(data[4]))    # only need pmra and pmdec
        list_pmdec.append(float(data[5]))


# change into numpy arrays
data_pmra = numpy.array(list_pmra)
data_pmdec = numpy.array(list_pmdec)

# # clearing lists
# list_pmra.clear()
# list_pmdec.clear()

# objects for plotting
fig = matplotlib.figure.Figure()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
ax = fig.add_subplot(111)
ax.set_xlabel('Proper motion in RA [mas/yr]')
ax.set_ylabel('Proper motion in Dec [mas/yr]')
ax.set_aspect('equal')
ax.grid()
ax.plot (data_pmra, data_pmdec, \
         linestyle='None', marker='o', markersize=1, color='blue', alpha=0.5, \
         label='Stars in Gaia DR3')
ax.legend (bbox_to_anchor=(1.05, 0.95), loc='upper left')
fig.savefig (file_output, dpi=150, bbox_inches="tight")
