import gzip
import numpy
import astropy.units
import astropy.coordinates
import matplotlib.figure
import matplotlib.backends.backend_agg

# units
u_ha  = astropy.units.hourangle
u_deg = astropy.units.deg
u_rad = astropy.units.rad

# file names
input_file = 'cstar.dat.gz'
output_file = 'cstar.png'
resolution = 150

# list to store data
list_ra_rad  = []
list_dec_rad = []
n = 0

# opening file for reading data
with gzip.open (input_file, 'rb') as fh:
    for line in fh:                        # read by line
        line = line.decode ('utf-8')
        # extracting data
        # Right Ascension
        try:
          RAh = int(line[12:14])
          RAm = int(line[15:17])
          RAs = float(line[19:23])
        except:
          RAh = 99
          RAm = 99
          RAs = 99.9
        RA = (RAh + RAm/60 + RAs/3600) * 15  # an hour is 15 degree
    
        # Declination
        try:
          Dec_sign = line[23:24].decode('utf-8')
          Dec_d = int(line[24:26])
          Dec_m = int(line[27:29])
          Dec_s = float(line[30:34])
        except:
          Dec_sign = '-'
          Dec_d = 99
          Dec_m = 99
          Dec_s = 99.99
        Dec = f'{Dec_sign}{Dec_d:02d}:{Dec_m:02d}:{Dec_s:04.1f}'

        # skipping, if any of data is missing.
        if ((RA == '') or (Dec == '')):
            continue
    
        # coordinate
        coord = astropy.coordinates.SkyCoord (ra_rad, dec_rad, \
                                              frame=astropy.coordinates.ICRS, \
                                              unit=u_rad)

        # appending data to lists
        ra_rad_wrap = coord.ra.wrap_at (180 * u_deg).radian
        list_ra_rad.append (ra_rad_wrap)
        list_dec_rad.append (coord.dec.radian)

        # progress
        n += 1
        if (i % 5000 == 0):
            print ("progress: %6d / %6d" % (n, n) )
