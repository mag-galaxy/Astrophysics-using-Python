import argparse
import sys
import pathlib
import astropy.table
import astropy.visualization
import matplotlib.figure
import matplotlib.backends.backend_agg

# using argparse
descr = 'reading .cat file and showing locations of sources'
parser = argparse.ArgumentParser(description=descr)
parser.add_argument('-c', '--catalogue-file', default='', help='input file name (cat)')
parser.add_argument('-f', '--input-file', default='', help='input file name (fits)')
parser.add_argument('-o', '--output-file', default='', help='output file name (png)')
parser.add_argument('-r', '--radius', type=float, default=10.0, help='radius of aperture in pixel')
args = parser.parse_args()

# get value from argument
file_cat = args.catalogue_file
file_fits = args.input_file
file_output = args.output_file
radius = args.radius

# making pathlib objects
path_input = pathlib.Path(file_fits)
path_catalogue = pathlib.Path(file_cat)
path_output = pathlib.Path(file_output)

if (!path_input.exists()):
    print (f'Fits file "{file_fits}" does not exist!!')
    sys.exit()
if not (path_catalogue.exists()):
    print (f'Catalogue file "{file_cat}" does not exist!!')
    sys.exit()
if (path_output.exists()):
    print (f'Output file "{file_output}" has existed!!')
    sys.exit()

# read catalogue file
table_source = astropy.table.Table.read(file_cat, format='ascii.commented_header')

# positions of detected sources
list_x = list(table_source['xcentroid'])
list_y = list(table_source['ycentroid'])

# read FITS file
with astropy.io.fits.open(file_fits) as hdu:
    header = hdu[0].header
    image  = hdu[0].data
    if (header['NAXIS'] == 0):    #read next one
        header = hdu[1].header
        image = hdu[1].data

# making objects for plotting
fig = matplotlib.figure.Figure()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
ax = fig.add_subplot(111)
ax.set_xlabel('X [pixel]')
ax.set_ylabel('Y [pixel]')

# normalisation
norm = astropy.visualization.mpl_normalize.ImageNormalize(stretch=astropy.visualization.HistEqStretch(image))

im = ax.imshow(image, origin='lower', cmap='viridis', norm=norm)    # show image
for i in range(len(list_x)):    # plot circle on sky objects
    source = matplotlib.patches.Circle(xy=(list_x[i], list_y[i]), \
                radius=radius, fill=False, color="red", linewidth=1)
    ax.add_patch(source)
fig.savefig(file_output, dpi=150) # save as png file
