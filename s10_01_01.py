import astropy.io.ascii
import numpy
import matplotlib.figure
import matplotlib.backends.backend_agg

# file names
file_csv = 'Leda_data_1.txt'
file_fig = 'Leda_data.png'
resolution_dpi = 150

# dictionary to store data
data_d = numpy.array([])
data_v = numpy.array([])

with open(file_csv, 'r') as f_read:
  for line in f_read:
    if(line.contain('#')
       continue
    data = line.split(',')
    if(data[0] == 'objname'):
      continue
    name = data[0]
    dis_pc = 10 ** (float(data[1])/5.0 + 1.0)  # distance in parsecs = 10^(distance modulus/5+1)
    dis_Mpc = dis_pc * 10**-6
    vel = float(data[2])  # km/s
    data_d.append(dis_Mpc)
    data_v.append(vel)
    
# figure, canvas, axes object for plotting
fig = matplotlib.figure.Figure()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
ax = fig.add_subplot(111)

ax.set_xlabel('Distance [Mpc]')
ax.set_ylabel('Velocity [km/s]')
ax.grid ()
ax.plot(data_d, data_v, linestyle='None', marker='o', markersize=3, color='blue',label='LEDA')
ax.legend()
fig.savefig(file_fig, dpi = resolution_dpi)
