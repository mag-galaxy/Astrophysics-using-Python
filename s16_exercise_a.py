import argparse
import astropy.time
import astropy.units
import astropy.coordinates
import astroplan

descr = 'show information for astronomical observation'
parser = argparse.ArgumentParser(description=descr)
parser.add_argument('-l1', '--long', help='longitude of observing site (dms)')
parser.add_argument('-l2', '--lat', help='latitude of observing site (dms)')
parser.add_argument('-h', '--height', help='height of observing site (m)')
parser.add_argument('-d', '--date', help='observing date (yyyy-mm-dd)')
args = parser.parse_args()

# get value from argument
long = args.long
lat = args.lat
date = args.date
height = float(args.height)

# units
m = astropy.units.m

# solar system
astropy.coordinates.solar_system_ephemeris('de440')

# time object
time_str = f'{date} 00:00:00'
UTC = astropy.time.Time(time_str, format='iso', scale='utc')

# observer
height = height * m
observer = astroplan.Observer(longitude=long, latitude=lat, elevation=height, name='observer', timezone='UTC')

# sun rise time
sun_rise = observer.sun_rise_time(UTC, which='next')
print(f'sun rise time of next day: {sun_rise}')

# sun set time
sun_set = observer.sun_rise_time(UTC, which='nearset')
print(f'sun set time of today: {sun_set}')

# moon rise time
moon_rise = observer.moon_rise_time(UTC, which='nearset')
print(f'moon rise time: {moon_rise}')

# moon set time
moon_set = observer.moon_set_time(UTC, which='nearset')
print(f'moon set time: {moon_set}')

# moon phase
moon_phase = astroplan.moon_phase_angle(UTC)
print(f'moon phase: {moon_phase}')