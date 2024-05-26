import pathlib
import matplotlib.figure
import matplotlib.backends.backend_agg

file_data = 'sirius.data'  # input file name (data)
dir_png = 'sirius'  # name of directory for storing PNG files

# make directory
path_dir_png = pathlib.Path(dir_png)
if not (path_dir_png.exists()):
    path_dir_png.mkdir()
prefix_fig = 'sirius'

# counter
i = 0

# read input file
with open (file_data, 'r') as fh:
    for line in fh:
        if (line[0] == '#'):
            continue
        (time, sirA_x, sirA_y, sirA_z, sirB_x, sirB_y, sirB_z) = line.split()  # split data
        file_fig = f"{dir_png}/{prefix_fig}_{i:08d}.png"  # output file name (png)

        # objects for plotting
        fig = matplotlib.figure.Figure()
        canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
        ax = fig.add_subplot(111)
        ax.set_xlabel('X [au]')
        ax.set_ylabel('Y [au]')
        ax.set_xlim(-25.0, +25.0)
        ax.set_ylim(-25.0, +25.0)
        ax.set_aspect('equal')
        ax.grid()
        ax.plot(float(sirA_x), float(sirA_y), linestyle='None', \
                 marker='o', markersize=10, color='red', label='Sirius A')
        ax.plot (float(sirB_x), float(sirB_y), linestyle='None', \
                 marker='o', markersize=5, color='blue', label='Sirius B')
        ax.set_title (f"Sirius A and B binary system at {float(time):6.2f} yr")
        ax.legend (loc='upper right')
        
        fig.savefig (file_fig, dpi=225)
        i += 1
