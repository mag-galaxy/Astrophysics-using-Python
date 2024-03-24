import numpy as np
import scipy
import matplotlib.backends.backend_agg
import matplotlib.figure
import argparse
import pathlib
import sys

parser = argparse.ArgumentParser(description='ball throwing motion')

# add argument
parser.add_argument ('-o1', '--output1', default='vt_relation.png',\
          help='output file name (default: vt_relation.png)')
parser.add_argument ('-o2', '--output2', default='xt_relation.png',\
          help='output file name (default: xt_relation.png)')
parser.add_argument ('-r', '--resolution', type=float, default=250.0,\
          help='resolution of plot in DPI (default: 250.0)')
args = parser.parse_args()
file_output1 = args.output1
file_output2 = args.output2
g_resolution = args.resolution

# output
path_output1 = pathlib.Path(file_output1)
path_output2 = pathlib.Path(file_output2)

# check of existence of output file 1, file 2
if(path_output1.exists()):
    print (f'ERROR: output file "{file_output1}" exists!')
    sys.exit(0)
if not((path_output1.suffix == '.eps')\
       or(path_output1.suffix == '.pdf')\
       or(path_output1.suffix == '.png')\
       or(path_output1.suffix == '.ps')):
    print (f'ERROR: output file must be either \
    EPS or PDF or PNG or PS file.')
    sys.exit(0)
if(path_output2.exists()):
    print (f'ERROR: output file "{file_output2}" exists!')
    sys.exit(0)
if not((path_output2.suffix == '.eps')\
       or(path_output2.suffix == '.pdf')\
       or(path_output2.suffix == '.png')\
       or(path_output2.suffix == '.ps')):
    print (f'ERROR: output file must be either \
    EPS or PDF or PNG or PS file.')
    sys.exit(0)

# information given by the question
mass = 0.3  # kg
initial_velocity = 30  # m/s
g = scipy.constants.g  # m/s^2

# variable for calculating
dt = 0.01  # very very short time (s)
total_time = 0  # initial total time (s)
velocity = initial_velocity  # initial v (m/s)
position = 0  # initial position (m)

# store data for plotting
t = []
v = []
x = []

# numerical integration
while velocity > 0:
    acceleration = -g # go up is positive, go down is negative

    # update velocity and position
    velocity += acceleration * dt # delta v = a*t
    position += velocity * dt #delta x = v*t

    # Update total time
    total_time += dt

    # add data to list
    t.append(total_time) 
    v.append(velocity)
    x.append(position)

# Calculate velocity change
velocity_change = initial_velocity - v[-1]

# figure, canvas, axes objects
fig1 = matplotlib.figure.Figure()
canvas1 = matplotlib.backends.backend_agg.FigureCanvasAgg(fig1)
ax1 = fig1.add_subplot(111)
fig2 = matplotlib.figure.Figure()
canvas2 = matplotlib.backends.backend_agg.FigureCanvasAgg(fig2)
ax2 = fig2.add_subplot(111)

# plot v-t graph
ax1.plot(t, v)
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Velocity (m/s)')
ax1.grid()
ax1.legend()
fig1.savefig(file_output1, dpi = g_resolution)

# plot x-t graph
ax2.plot(t, x)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Position (m)')
ax2.grid()
ax2.legend()
fig2.savefig(file_output2, dpi = g_resolution)

print(f'Velocity change of the ball: {velocity_change:.2f} m/s')
print(f'Time to reach highest position: {total_time:.2f} seconds')
