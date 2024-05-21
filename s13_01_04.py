# star-to-star matching and image alignment
import argparse
import sys
import pathlib
import datetime
import numpy
import astropy.table
import astropy.visualization
import skimage.transform
import astroalign
import matplotlib.figure
import matplotlib.backends.backend_agg

# time
now = datetime.datetime.now()

# using argparse
descr = 'star-to-star matching and image alignment'
parser = argparse.ArgumentParser(description=descr)

# adding arguments
parser.add_argument('-o', '--file-output', default='', help='output file (png)')
parser.add_argument('-n', '--number', type=int, default=50, help='max number of control sources')
parser.add_argument('catalogue1', nargs=1, help='.cat file 1')
parser.add_argument('catalogue2', nargs=1, help='.cat file 2')
parser.add_argument('fits1', nargs=1, help='.fits file 1')
parser.add_argument('fits2', nargs=1, help='.fits file 2')
args = parser.parse_args()

# get value from argument
file_cat1 = args.catalogue1[0]
file_cat2 = args.catalogue2[0]
file_fits1 = args.fits1[0]
file_fits2 = args.fits2[0]
file_png = args.file_output
n_controlpoints = args.number

# making pathlib objects
path_cat1 = pathlib.Path(file_cat1)
path_cat2 = pathlib.Path(file_cat2)
path_fits1 = pathlib.Path(file_fits1)
path_fits2 = pathlib.Path(file_fits2)
path_png = pathlib.Path(file_png)

# check files exsistence
if (!path_cat1.exists()):
    print(f'Catalogue file "{file_cat1}" does not exist!!')
    sys.exit()
if (!path_cat2.exists()):
    print(f'Catalogue file "{file_cat2}" does not exist!!')
    sys.exit()
if (!path_fits1.exists()):
    print(f'Fits file "{file_fits1}" does not exist!!')
    sys.exit()
if (!path_fits2.exists()):
    print(f'Fits file "{file_fits2}" does not exist!!')
    sys.exit()
if (path_png.exists()):
    print(f'Output file "{file_png}" has existed!!')
    sys.exit()

# function for reading .fits file
def read_fits(file_fits):
    with astropy.io.fits.open(file_fits) as hdu:
        header = hdu[0].header
        image  = hdu[0].data
        if (header['NAXIS'] == 0):  # read next one
            header = hdu[1].header
            image  = hdu[1].data
    return image

# read .cat file
table_source1 = astropy.table.Table.read(file_cat1, format='ascii.commented_header')
table_source2 = astropy.table.Table.read(file_cat2, format='ascii.commented_header')

# (x, y) coordinates of sources
list_source1_x = list(table_source1['xcentroid'])
list_source1_y = list(table_source1['ycentroid'])
list_source2_x = list(table_source2['xcentroid'])
list_source2_y = list(table_source2['ycentroid'])
position_1 = numpy.transpose((list_source1_x, list_source1_y))
position_2 = numpy.transpose((list_source2_x, list_source2_y))

# finding star-to-star matching
transf, (list_matched_2, list_matched_1) \
    = astroalign.find_transform(position_2, position_1, max_control_points=n_controlpoints)

# transformation
list_matched_2_aligned = astroalign.matrix_transform(list_matched_2, transf.params)

print (f'# transformation matrix\n#\n')
print (f'# [')
print (f'#  [{transf.params[0][0]:11.6f}, {transf.params[0][1]:11.6f}, {transf.params[0][2]:11.6f}],')
print (f'#  [{transf.params[1][0]:11.6f}, {transf.params[1][1]:11.6f}, {transf.params[1][2]:11.6f}],')
print (f'#  [{transf.params[2][0]:11.6f}, {transf.params[2][1]:11.6f}, {transf.params[2][2]:11.6f}]')
print (f'# ]')
print (f'# list of matched stars')
for i in range(len(list_matched_1)):
    print(f'({list_matched_1[i][0]:8.3f}, {list_matched_1[i][1]:8.3f}) on 1st image', \
           f'==> ({list_matched_2[i][0]:8.3f}, {list_matched_2[i][1]:8.3f}) on 2nd image')

# reading .fits files
image1 = read_fits(file_fits1)
image2 = read_fits(file_fits2)

# byte swap (big endian) to (little endian)
image1 = image1.byteswap().newbyteorder()
image2 = image2.byteswap().newbyteorder()

# aligning 2nd image to 1st image
st = skimage.transform.SimilarityTransform(scale=transf.scale, rotation=transf.rotation, translation=transf.translation)
image2_aligned = skimage.transform.warp (image2, st.inverse)

# marker and colour for plotting
markers = ['o', 'v', '^', 's', 'p', 'h', '8']
colours = ['maroon', 'red', 'coral', 'bisque', 'orange', 'wheat', 'yellow', 'green', 'lime', 'aqua', \
           'skyblue', 'blue', 'indigo', 'violet', 'pink']

# objects for plotting
fig = matplotlib.figure.Figure()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

norm1 = astropy.visualization.mpl_normalize.ImageNormalize(stretch=astropy.visualization.HistEqStretch(image1))
im1 = ax1.imshow(image1, origin='lower', cmap='bone', norm=norm1)
for i in range(len(list_matched_1)):
    i_marker = i % len(markers)
    i_colour = i % len(colours)
    ax1.plot(list_matched_1[i][0], list_matched_1[i][1], marker=markers[i_marker], \
             color=colours[i_colour], markersize=8, fillstyle='none')
ax1.set_title('First Image')

norm2 = astropy.visualization.mpl_normalize.ImageNormalize(stretch=astropy.visualization.HistEqStretch(image2_aligned))
im2 = ax2.imshow(image2_aligned, origin='lower', cmap='bone', norm=norm2)
for i in range(len(list_matched_2_aligned)):
    i_marker = i % len(markers)
    i_colour = i % len(colours)
    ax2.plot(list_matched_2_aligned[i][0], list_matched_2_aligned[i][1], marker=markers[i_marker], \
             color=colours[i_colour], markersize=8, fillstyle='none')
ax2.set_title('Second Image')

fig.tight_layout()
fig.savefig(file_png, dpi=150)
