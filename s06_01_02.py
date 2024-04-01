# download readme file
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

url_data = 'https://cdsarc.cds.unistra.fr/ftp/I/131A/ReadMe'    # URL of data file
file_output = 'sao.readme'    # output file name

print (f'Now, fetching {url_data}...')

# open URL and read data
with urllib.request.urlopen (url_data) as fh_read:
    data_byte = fh_read.read ()

print (f'Finished fetching {url_data}!')

data_str = data_byte.decode ('utf-8')    #decode data

print (f'Now, writing data into file "{file_output}"...')

# write data to output file
with open (file_output, 'w') as fh_write:
    fh_write.write (data_str)

print (f'Finished writing data into file "{file_output}"!')
