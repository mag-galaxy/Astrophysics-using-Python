import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

url_data = 'https://cdsarc.cds.unistra.fr/viz-bin/nph-Cat/txt.gz?V/84/main.dat.gz'    # URL of data
file_output = 'cstar.dat.gz'    # output file name

print (f'Now, fetching {url_data}...')
# open URL and read data
with urllib.request.urlopen (url_data) as fh_read:
    data_byte = fh_read.read ()

print (f'Finished fetching {url_data}!')
print (f'Now, writing data into file "{file_output}"...')

# write data to output file
with open (file_output, 'wb') as fh_write:
    fh_write.write (data_byte)

print (f'Finished writing data into file "{file_output}"!')
