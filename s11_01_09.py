import argparse
import numpy
import matplotlib.figure
import matplotlib.backends.backend_agg

# using  argparse
descr  = 'making HR diagram and superimposing location of main-sequence'
parser = argparse.ArgumentParser(description=descr)
parser.add_argument('-i', '--input', help='input file name')
parser.add_argument('-o', '--output', help='output file name')
parser.add_argument('-m', '--mainsequence', default='ms.data', help='main-sequence data')
parser.add_argument('-t', '--title', help='title of plot')
args = parser.parse_args()

# input parameters
file_input = args.input
file_output = args.output
file_ms = args.mainsequence
title = args.title

# lists to store data
list_parallax = []
list_g = []
list_br = []


# opening file
with open (file_input, 'r') as fh:
    for line in fh:
        if (line[0] == '#'):
            continue
        # removing new line at the end of the line
        line = line.strip()
        data = line.split()
        list_parallax.append(float(data[3]))
        list_g.append(float(data[8]))
        list_br.append(float(data[10]))

# making numpy arrays
data_parallax = numpy.array(list_parallax)
data_g = numpy.array(list_g)
data_br = numpy.array(list_br)

# calculation of g-band absolute magnitude
data_g_abs = data_g + 5.0 * numpy.log10 (data_parallax / 1000.0) + 5.0

# making empty lists for storing data
list_ms_colour = []
list_ms_absmag = []

# opening data file
with open (file_ms, 'r') as fh_ms:
    for line in fh_ms:
        line = line.strip()
        if (line == ''):
            break
        if (line[0] == '#'):
            continue
        fields = line.split ()
        # spectral type
        sptype = fields[0]
        # effective temperature
        teff = float (fields[1])
        # Gaia (b-r) colour index
        try:
            colour_br = float (fields[11])
        except:
            colour_br = 999.999
        # Gaia g-band absolute magnitude
        try:
            absmag_g = float (fields[13])
        except:
            absmag_g = 999.999
        # appending data to lists
        if ((colour_br < 100.0) and (absmag_g < 100.0)):
            list_ms_colour.append (colour_br)
            list_ms_absmag.append (absmag_g)

# making numpy arrays
data_ms_colour = numpy.array (list_ms_colour)
data_ms_absmag = numpy.array (list_ms_absmag)

# objects for plotting
fig = matplotlib.figure.Figure ()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax = fig.add_subplot (111)
ax.set_xlabel('(b-r) colour index')
ax.set_ylabel('g absolute magnitude [mag]')
ax.grid()
ax.set_title(title)
ax.set_box_aspect(aspect=1.0)
ax.set_xlim(-1.0, 6.0)
ax.set_ylim(18.0, -3.0)
ax.plot(data_br, data_g_abs, \
         linestyle='None', marker='o', markersize=3, color='blue', \
         zorder=0.2, label='Gaia DR3 stars')
ax.plot(data_ms_colour, data_ms_absmag, \
         linestyle='-', linewidth=10, color='orange', alpha=0.5, \
         zorder=0.1, label='Typical main-sequence stars')
ax.legend (bbox_to_anchor=(1.05, 0.95), loc='upper left')
fig.savefig (file_output, dpi=150, bbox_inches="tight")
