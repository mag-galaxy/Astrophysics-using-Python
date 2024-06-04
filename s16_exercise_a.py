import argparse
import astropy.time
import astropy.units
import astropy.coordinates
import astroplan

descr = 'show information for astronomical observation'
parser = argparse.ArgumentParser(description=descr)
parser.add_argument('-l1', '--long', help='longitude of observing site (dms)')
parser.add_argument('-l2', '--lat', help='latitude of observing site (dms)')
parser.add_argument('-e', '--height', help='height of observing site (m)')
parser.add_argument('-d', '--date', help='observing date (yyyy-mm-dd)')
parser.add_argument('-z', '--timezone', help='timezone of observing site ')
args = parser.parse_args()

# get value from argument
long = args.long
lat = args.lat
date = args.date
timez = args.timezone
height = float(args.height)

# units
m = astropy.units.m

# time object
time_str = f'{date} 00:00:00'
obs_time = astropy.time.Time(time_str)

# observer
height = height * m
observer = astroplan.Observer(longitude=long, latitude=lat, elevation=height, name='observer', timezone=timez)

# sun rise time
sun_rise = observer.sun_rise_time(obs_time, which='next')
print("sun rise time:  {0.iso}".format(sun_rise))

# sun set time
sun_set = observer.sun_set_time(obs_time, which='nearest')
print("sun set time:   {0.iso}".format(sun_set))

# moon rise time
moon_rise = observer.moon_rise_time(obs_time, which='nearest')
print("moon rise time: {0.iso}".format(moon_rise))

# moon set time
moon_set = observer.moon_set_time(obs_time, which='nearest')
print("moon set time:  {0.iso}".format(moon_set))

# moon phase
moon_phase = astroplan.moon_phase_angle(obs_time)
print(f'moon phase: {moon_phase}')
