import numpy as np
import scipy
import matplotlib.backends.backend_agg
import matplotlib.figure
import argparse
import pathlib
import sys

parser = argparse.ArgumentParser(description='ball throwing motion')

# add argument
parser.add_argument ('-o', '--output', default='vt_relation.png',\
          help='output file name (default: vt_relation.png)')
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
    print (f'ERROR: output file must be either \
    EPS or PDF or PNG or PS file.')
    sys.exit(0)
         
# information given by the question
mass = 0.3  # kg
initial_velocity = 30  # m/s
g = scipy.constants.g  # m/s^2
a = -g  # go up is positive, go down is negative

# variable for calculating
dt = 0.0001  # very very short time (s)
total_time = 0  # initial total time (s)
velocity = initial_velocity  # initial v (m/s)

# store data for plotting
t = []
v = []

# calculate velocity each 0.0001 sec
while velocity > 0:
    # when v == 0, the ball is at the highest point
    # update velocity and total time
    velocity += a * dt  # delta v = a*dt
    total_time += dt

    # add data to list
    t.append(total_time) 
    v.append(velocity)

# Calculate velocity change
velocity_change = initial_velocity - v[-1]

# figure, canvas, axes objects
fig = matplotlib.figure.Figure()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
ax = fig.add_subplot(111)

# plot v-t graph
ax.plot(t, v)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Velocity (m/s)')
ax.set_title('v-t relation')
ax.grid()
fig.savefig(file_output, dpi = g_resolution)

print(f'Velocity change of the ball: {velocity_change:.2f} m/s')
print(f'Time for ball to reach the highest position: {total_time:.3f} s')
