import astropy.io.ascii
import numpy
import matplotlib.figure
import matplotlib.backends.backend_agg

file_csv = 'earthquack.csv'
file_output = 'earthquack_April.png'
resolution = 150
all_mag = []

with open(file_csv, 'r') as f_read:
  for line in f_read:
    data = line.split(',')
    try:
      mag = float(data[4])
      print(mag)
      all_mag.append(mag)
    except:
      continue

mag_array = numpy.array(all_mag)
print(mag_array)

hist_x = numpy.linspace(3, 7, 5)
hist_y = numpy.zeros(5, dtype='int64')

for i in range(len(all_mag)):
  if(mag_array[i] < 3 or mag_array[i] > 7):
    continue
  hist_y[int(float(mag_array[i])-3)] += 1

for i in range(4):
  bin0 = 3 + i
  bin1 = 3 + i + 1
  print(f'{bin0}~{bin1} {hist_y}')

fig = matplotlib.figure.Figure()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
ax = fig.add_subplot(111)
ax.set_xlabel('madnitude')
ax.set_ylabel('number of cases')
ax.set_xlim(3, 7)
ax.bar(hist_x, hist_y, 1, edgecolor='black', linewidth=0.3, align='edge',\
      label = 'magnitude of earthquack in April 2024 in Taiwan')
ax.legend()
fig.savefig(file_output, dpi=resolution)
