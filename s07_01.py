import astropy.coordinates
import astropy.time
import astropy.units

# using "DE440" for solar system ephemeris
astropy.coordinates.solar_system_ephemeris.set ('de440')

m = astropy.units.m
UTC = astropy.time.Time ('2024-04-24 13:00:00', format='iso', scale='utc')

# location of observer: NCU main campus
longitude = '121d11m12s'
latitude  = '+24d58m12s'
height    = 151.6 * m
observer  = astropy.coordinates.EarthLocation (longitude, latitude, height)

# position of the Sun
sun = astropy.coordinates.get_body ('sun', UTC, location = observer)

# change ra to azimuth, dec to elevation
print(f'position of the Sun as observed at NCU main campus at {UTC}:')
print(f' azimuth: {}')
print(f' elevation: {sun.dec.dms.d + sun.dec.dms.m / 60 + sun.dec.dms.s / 3600}')

# print (f'  RA:  {int (sun.ra.hms.h):02d}:{int (sun.ra.hms.m):02d}', \
#        f':{sun.ra.hms.s:06.3f}', sep='')
# print (f'  Dec: {int (sun.dec.dms.d):02d}', \
#        f':{abs (int (sun.dec.dms.m)):02d}:{abs (sun.dec.dms.s):06.3f}', \
#        sep='')
