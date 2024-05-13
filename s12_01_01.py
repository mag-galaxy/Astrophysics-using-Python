import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

list_url = [
    'http://exoplanetarchive.ipac.caltech.edu:80/data/ETSS//Kepler/005/755/20/kplr010666592-2013017113907_slc.fits', \
    'http://exoplanetarchive.ipac.caltech.edu:80/data/ETSS//Kepler/005/755/20/kplr010666592-2013065031647_slc.fits', \
    'http://exoplanetarchive.ipac.caltech.edu:80/data/ETSS//Kepler/005/755/20/kplr010666592-2013098041711_slc.fits']

# download Kepler data
for url_data in list_url:
    file_output_name = url_data.split('/')[-1]
    with urllib.request.urlopen(url_data) as fh_read:
        data_byte = fh_read.read ()

    # write data
    with open (file_output_name, 'wb') as fh_write:
        fh_write.write (data_byte)
    print (f'Finished writing data into file "{file_output_name}"!')
