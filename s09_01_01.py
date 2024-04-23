import urllib.request
import ssl
import numpy
import astropy.coordinates
import astropy.time
import astropy.units

ssl._create_default_https_context = ssl._create_unverified_context
link = 'http://astro.phys.wvu.edu/wise/wise_hii_V2.2.csv'
data_output = 'data.txt'

# download data
i = 0
with urllib.request.urlopen (link) as fh_read:
    with open(data_output, 'w') as f_write:
        for line in fh_read:
            if i==0:
                ++i
                continue
            data_str = line.decode('utf-8')
            data_list = data_str.split(',')
            f_write.write(data_list[2] + ',' + data_list[3] + '\n')
f_write.close()
#             gal_l = float(data_list[2])    # glactic longitude
#             gal_b = float(data_list[3])    # glactic latitude
#             print(gal_l + ' ' + gal_b)
#             gal_coord = astropy.coordinates.Galactic(l=gal_l, b=gal_b)
#             ra_deg = gal_coord.transform_to(astropy.coordinates.ICRS ()).ra.wrap_at(180.0*u_deg).radian
#             dec_deg = gal_coord.transform_to(astropy.coordinates.ICRS ()).dec.radian    
#             # if(ra_deg > 180):
#             #     ra_deg -= 360.0
#             list_ra_deg.append(ra_deg)
#             list_dec_deg.append(dec_deg)
            
# # change into numpy arrays
# array_ra_deg = numpy.array(list_ra_deg)
# array_dec_deg = numpy.array(list_dec_deg)

print('finish adding data')
