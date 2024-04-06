# Moon position at 2024-04-24 13:00:00 (utc)
# Moon position at 2024-04-24 21:00:00 (in Taiwan)
import astropy.time
import astropy.units
import astropy.coordinates

# using "DE440" for solar system ephemeris
astropy.coordinates.solar_system_ephemeris.set ('de440')

m = astropy.units.m
t_Taiwan = astropy.time.Time ('2024-04-24 21:00:00', format='iso', scale='utc')
UTC = astropy.time.Time ('2024-04-24 13:00:00', format='iso', scale='utc')

# location of observer: Mt. Jade
longitude = '120d57m26s'
latitude  = '+23d28m12s'
height    = 3952 * m
observer  = astropy.coordinates.EarthLocation (longitude, latitude, height)

# position of the Moon
moon = astropy.coordinates.get_body ('moon', UTC, location = observer)

# get RA and Dec
(moon_ra, moon_dec) = moon.to_string('hmsdms').split()

# convert RA/Dec to azimuth/elevation
altaz = astropy.coordinates.AltAz(obstime = UTC, location = observer)
moon_altaz = moon.transform_to(altaz)
moon_az = moon_altaz.az
moon_alt = moon_altaz.alt

print(f'position of the Moon as observed at Mt. Jade at {t_Taiwan}:')
print(f'(azimuth, elevation) = ({moon_az}, {moon_alt})')
