import urllib.request
import numpy
import astropy.coordinates
import astropy.time
import astropy.units
import matplotlib.figure
import matplotlib.backends.backend_agg

date = astropy.time.Time('2024-04-22 00:00:00')
data_input = 'data.txt'            # the file with galactic coords we need
png_output = 'glactic_hii.png'     # plot and save as .png file
resolution_dpi = 150

# units
u_deg = astropy.units.degree

# empty lists for storing data
list_ra_deg = []
list_dec_deg = []

# add data to list
with open(data_input, 'r') as f_read:
  for line in f_read:
    data = line.split(',')
    gal_l = float(data[0])   # glactic longitude (deg)
    gal_b = float(data[1])   # glactic latitude (deg)

    # galactic coorddinates to equatorial coorddinates
    galactic_coords = astropy.coordinates.SkyCoord(l=gal_l*u_deg, b=gal_b*u_deg, frame='galactic')
    equatorial_coords = galactic_coords.transform_to('icrs')
    ra_deg = equatorial_coords.ra.deg
    dec_deg = equatorial_coords.dec.deg
    if(ra_deg > 180.0):
      ra_deg -= (360.0)
    list_ra_deg.append(ra_deg)    # equatorial coords (deg)
    list_dec_deg.append(dec_deg)  # equatorial coords (deg)

# change into numpy arrays
array_ra_deg = numpy.array(list_ra_deg)
array_dec_deg = numpy.array(list_dec_deg)

# ecliptic plane
ecl_lon = numpy.linspace(0.001, 359.999, 1000) * u_deg
ecl_lat = numpy.zeros(1000) * u_deg
ecl_coord = astropy.coordinates.GeocentricMeanEcliptic(lon=ecl_lon, lat=ecl_lat, obstime=date)
ecl_ra = ecl_coord.transform_to(astropy.coordinates.ICRS()).ra.wrap_at(180.0*u_deg).radian
ecl_dec = ecl_coord.transform_to(astropy.coordinates.ICRS()).dec.radian

# galactic plane
gal_lon = numpy.linspace(0.001, 359.999, 1000) * u_deg
gal_lat = numpy.zeros(1000) * u_deg
gal_coord = astropy.coordinates.Galactic(l = gal_lon, b = gal_lat)
gal_ra = gal_coord.transform_to(astropy.coordinates.ICRS()).ra.wrap_at(180.0*u_deg).radian
gal_dec = gal_coord.transform_to(astropy.coordinates.ICRS()).dec.radian

# figure, canvas, axes object for plotting
fig = matplotlib.figure.Figure()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
ax = fig.add_subplot (111, projection='mollweide')        # use Mollweide projection
ax.grid()
ax.set_xlabel('Right Ascension [deg]')
ax.set_ylabel('Declination [deg]')
ax.set_title(f'Distribution of Galictic Hii regions on {date}', loc='right')
ax.plot(numpy.deg2rad(array_ra_deg), numpy.deg2rad(array_dec_deg), \
        linestyle='None', marker='.', markersize=5, color='blue')
# ax.scatter(numpy.deg2rad(array_ra_deg), numpy.deg2rad(array_dec_deg), marker='o', c='blue')
ax.plot (ecl_ra, ecl_dec, linestyle='None', marker='o', markersize=5, \
         color='yellow', alpha=0.5, label='Ecliptic plane')
ax.plot (gal_ra, gal_dec, linestyle='None', marker='o', markersize=5, \
         color='silver', alpha=0.5, label='Galactic plane')
fig.savefig(png_output, dpi=resolution_dpi)
