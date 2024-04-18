import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
link = 'http://astro.phys.wvu.edu/wise/wise_hii_V2.2.csv'


import numpy
import astropy.coordinates
import astropy.time
import astropy.units
import matplotlib.figure
import matplotlib.backends.backend_agg

# date/time
date = astropy.time.Time ('2024-05-01 00:00:00')

# file names
file_input = 'asteroids_100000.data'
file_output = 'appy_s09_00_17.png'
resolution_dpi = 150

# making empty lists for storing data
list_ra_deg  = []
list_dec_deg = []

# units
u_deg = astropy.units.degree

# printing status
print (f'Now, reading data file...')

# opening data file
with open (file_input, 'r') as fh:
    # reading data file line-by-line
    for line in fh:
        # skipping line if the line starts with '#'
        if (line[0] == '#'):
            continue
        # splitting line
        (orbit, name) = line.split ('#')
        # extracting RA and Dec
        (ra_deg, dec_deg, ecl_lon_deg, ecl_lat_deg, \
         gal_lon_deg, gal_lat_deg, absmag, appmag) = orbit.split ()
        # conversion from string into float
        ra_deg  = float (ra_deg)
        if (ra_deg > 180.0):
            ra_deg -= 360.0
        dec_deg = float (dec_deg)
        # appending data to lists
        list_ra_deg.append (ra_deg)
        list_dec_deg.append (dec_deg)

# making numpy arrays
array_ra_deg = numpy.array(list_ra_deg)
array_dec_deg = numpy.array(list_dec_deg)

# printing status
print (f'Finished reading data file!')

# printing status
print (f"Now, generating a plot ...")

# ecliptic plane
ecl_lon = numpy.linspace (0.001, 359.999, 1000) * u_deg
ecl_lat = numpy.zeros (1000) * u_deg
ecl_coord = astropy.coordinates.GeocentricMeanEcliptic (lon=ecl_lon, \
                                                        lat=ecl_lat, \
                                                        obstime=date)
ecl_ra  = ecl_coord.transform_to (astropy.coordinates.ICRS ()) \
                   .ra.wrap_at (180.0 * u_deg).radian
ecl_dec = ecl_coord.transform_to (astropy.coordinates.ICRS ()).dec.radian

# galactic plane
gal_lon = numpy.linspace (0.001, 359.999, 1000) * u_deg
gal_lat = numpy.zeros (1000) * u_deg
gal_coord = astropy.coordinates.Galactic (l=gal_lon, \
                                          b=gal_lat)
gal_ra  = gal_coord.transform_to (astropy.coordinates.ICRS ()) \
                   .ra.wrap_at (180.0 * u_deg).radian
gal_dec = gal_coord.transform_to (astropy.coordinates.ICRS ()).dec.radian

# making objects "fig" and "ax"
fig    = matplotlib.figure.Figure ()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax     = fig.add_subplot (111, projection='mollweide')

# axes
ax.grid ()
ax.set_xlabel ('Right Ascension [deg]')
ax.set_ylabel ('Declination [deg]')

# title
text_title = f"Distribution of asteroids on the sky on {date}"
ax.set_title (text_title, loc='right')

# plotting data
ax.plot (numpy.deg2rad (array_ra_deg), numpy.deg2rad (array_dec_deg), \
         linestyle='None', marker='o', markersize=1, \
         color='blue', alpha=0.1, \
         label='Asteroids')
ax.plot (ecl_ra, ecl_dec, \
         linestyle='None', marker='o', markersize=5, \
         color='yellow', alpha=0.5, \
         label='Ecliptic plane')
ax.plot (gal_ra, gal_dec, \
         linestyle='None', marker='o', markersize=5, \
         color='silver', alpha=0.5, \
         label='Galactic plane')
ax.legend (bbox_to_anchor=(0.9, -0.1))

# saving file
fig.savefig (file_output, dpi=resolution_dpi)

# printing status
print (f"Finished generating a plot of asteroid distribution on the sky!")
