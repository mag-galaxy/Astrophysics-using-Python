# download .gz file

import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# URL of data
url_data = 'https://cdsarc.cds.unistra.fr/ftp/I/131A/sao.dat.gz'

# output file name
file_output = 'sao.dat.gz'

# printing status
print (f'Now, fetching {url_data}...')

# opening URL
with urllib.request.urlopen (url_data) as fh_read:
    # reading data
    data_byte = fh_read.read ()

# printing status
print (f'Finished fetching {url_data}!')

# printing status
print (f'Now, writing data into file "{file_output}"...')

# opening file for writing
with open (file_output, 'wb') as fh_write:
    # writing data
    fh_write.write (data_byte)

# printing status
print (f'Finished writing data into file "{file_output}"!')
