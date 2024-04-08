import astropy.io.fits
import astropy.units
import astropy.coordinates
import astropy.wcs
import astroquery.simbad
import astroquery.skyview
import matplotlib.figure
import matplotlib.backends.backend_agg

# files names
download_file = 'm101.fits'
output_file = 'm101.png'
resolution = 250

object_name = 'M101'
survey = 'DSS2 Red'

# field-of-view  = 45 * 45
fov_arcmin = 45.0
fov_arcsec = fov_arcmin * 60.0
npixel = int(fov_arcsec)

# colour map
cmap = 'magma'

# units
ha  = astropy.units.hourangle
deg = astropy.units.deg

# get query result
query_result = astroquery.simbad.Simbad.query_object(object_name)

# coordinate from Simbad
ra_str = query_result['RA'][0]
dec_str = query_result['DEC'][0]

# making SkyCoord object of astropy
coord = astropy.coordinates.SkyCoord(ra_str, dec_str, frame='icrs', \
                                      unit=(ha, deg) )
(RA, Dec) = coord.to_string(style='hmsdms').split ()

# printing result
print (f'Target name: "{object_name}"')
print (f'  RA = {RA}')
print (f'  Dec = {Dec}')

# getting a list of images
list_image = astroquery.skyview.SkyView.get_image_list(position=coord, \
                                                        survey=survey)

# printing a list of images found
print ("images =", list_image)

# getting images
images = astroquery.skyview.SkyView.get_images(position=coord, \
                                                survey=survey, \
                                                pixels=npixel)

# image
image = images[0]
header = image[0].header
data = image[0].data

print(image.info ())

print(f'Writing a FITS file "{file_fits}"...')
# writing FITS file
hdu = astropy.io.fits.PrimaryHDU (data = data, header = header)
hdu.writeto (file_fits)
print (f'Done!')

# opening FITS file
with astropy.io.fits.open (file_fits) as hdu_list:
    print (hdu_list.info ())
    header = hdu_list[0].header
    wcs    = astropy.wcs.WCS (header)
    image  = hdu_list[0].data

# objects figure, canvas, axes
fig = matplotlib.figure.Figure ()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax = fig.add_subplot (111, projection=wcs)

ax.set_title (object_name)
ax.set_xlabel ('Right Ascension')
ax.set_ylabel ('Declination')

# normalisation
norm \
    = astropy.visualization.mpl_normalize.ImageNormalize \
    ( stretch=astropy.visualization.AsinhStretch () )

# plot
im = ax.imshow(image, origin='lower', cmap = cmap, norm = norm)
fig.colorbar(im)

print(f'{file_fits} ==> {file_png}')
fig.savefig(file_png, dpi=resolution_dpi)
