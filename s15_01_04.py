# visualize result of clustering
import argparse
import numpy
import matplotlib.backends.backend_agg
import matplotlib.figure

# use argparse
descr = f'plotting result of DBSCAN using parallax, rv, pmra, and pmdec'
parser = argparse.ArgumentParser(description=descr)
parser.add_argument('-i', '--input', help='input file name (data)')
parser.add_argument('-o', '--output', help='output file name (png)')
parser.add_argument('-t', '--target', help='target object name')
args = parser.parse_args()

# get value from argument
file_input = args.input
file_output = args.output
target_name = args.target

list_clusters = []

# read input data file
with open (file_input, 'r') as fh:
    for line in fh:
        if (line[0] == '#'):
            continue
        (source_id, ra, dec, parallax, dist_pc, dist_norm, pmra, pmdec, rv, rv_norm, label) = line.split()
        list_clusters.append(label)
set_clusters = set(list_clusters)

# 2-D list for storing data
data = []
for i in range(len(set_clusters)):
    data.append([])

# opening file for reading
with open (file_input, 'r') as fh:
    for line in fh:
        if (line[0] == '#'):
            continue
        (source_id, ra, dec, parallax, dist_pc, dist_norm, pmra, pmdec, rv, rv_norm, label) = line.split()
        source_id = int(source_id)
        label = int(label)
        ra = float(ra)
        dec = float(dec)
        parallax = float(parallax)
        dist_pc = float(dist_pc)
        dist_norm = float(dist_norm)
        pmra = float(pmra)
        pmdec = float(pmdec)
        rv = float(rv)
        rv_norm = float(rv_norm)
        data[label].append([source_id, ra, dec, parallax, dist_pc, dist_norm, pmra, pmdec, rv, rv_norm])

# objects for plotting
fig = matplotlib.figure.Figure()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)

# figure 1
ax1 = fig.add_subplot(221)
ax1.set_xlabel('Proper motion in RA [mas/yr]')
ax1.set_ylabel('Proper motion in Dec [mas/yr]')
ax1.set_xlim(-30, +30)
ax1.set_ylim(-30, +30)
ax1.grid()
for i in range(len(data)):
    source_id, ra, dec, parallax, dist_pc, dist_norm, pmra, pmdec, rv, rv_norm = numpy.array(data[i]).T
    if (i < len(data) - 1):
        ax1.plot(pmra, pmdec, linestyle='None', marker='o', markersize=1, zorder=0.2, label=f'cluster {i}')
    else:
        ax1.plot(pmra, pmdec, linestyle='None', marker='.', markersize=1, zorder=0.1, label=f'field stars')
ax1.legend()

#  figure 2
ax2 = fig.add_subplot(222)
ax2.set_xlabel('Distance [pc]')
ax2.set_ylabel('Radial velocity [km/s]')
ax2.set_xlim(0, 4000)
ax2.set_ylim(-100, +100)
ax2.grid()
for i in range(len(data)):
    source_id, ra, dec, parallax, dist_pc, dist_norm, pmra, pmdec, rv, rv_norm = numpy.array(data[i]).T
    if (i < len(data) - 1):
        ax2.plot(dist_pc, rv, linestyle='None', marker='o', markersize=1, zorder=0.2, label=f'cluster {i}')
    else:
        ax2.plot(dist_pc, rv, linestyle='None', marker='.', markersize=1, zorder=0.1, label=f'field stars')
ax2.legend()

# figure 3
ax3 = fig.add_subplot(223)
ax3.set_xlabel('Proper motion in RA [mas/yr]')
ax3.set_ylabel('Distance [pc]')
ax3.set_xlim(-30, +30)
ax3.set_ylim(0, 4000)
ax3.grid()
for i in range(len(data)):
    source_id, ra, dec, parallax, dist_pc, dist_norm, pmra, pmdec, rv, rv_norm = numpy.array(data[i]).T
    if (i < len(data) - 1):
        ax3.plot(pmra, dist_pc, linestyle='None', marker='o', markersize=1, zorder=0.2, label=f'cluster {i}')
    else:
        ax3.plot(pmra, dist_pc, linestyle='None', marker='.', markersize=1, zorder=0.1, label=f'field stars')
ax3.legend()

# figure 4
ax4 = fig.add_subplot(224)
ax4.set_xlabel('Proper motion in Dec [mas/yr]')
ax4.set_ylabel('Radial velocity [km/s]')
ax4.set_xlim(-30, +30)
ax4.set_ylim(-100, +100)
ax4.grid()
for i in range(len(data)):
    source_id, ra, dec, parallax, dist_pc, dist_norm, pmra, pmdec, rv, rv_norm = numpy.array(data[i]).T
    # plotting data
    if (i < len(data) - 1):
        ax4.plot(pmdec, rv, linestyle='None', marker='o', markersize=1, zorder=0.2, label=f'cluster {i}')
    else:
        ax4.plot(pmdec, rv, linestyle='None', marker='.', markersize=1, zorder=0.1, label=f'field stars')
ax4.legend()
        
fig.suptitle(target_name)
fig.tight_layout()
fig.savefig(file_output, dpi=150.0)
