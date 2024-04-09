import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

link = 'https://iopscience.iop.org/0004-637X/865/1/77/suppdata/apjaad81bt3_ascii.txt?doi=10.3847/1538-4357/aad81b'

# output file name
file_output = 'hd98800_b.data'

print (f'Fetching {link}...')

# opening URL
with urllib.request.urlopen (link) as fh_read:
    data_byte = fh_read.read ()

print (f'Fetched {link}!')

# converting raw byte data into string
data_str = data_byte.decode ('utf-8')

print (f'Now, writing data into file "{file_output}"...')

# opening file for writing
with open (file_output, 'w') as fh_write:
    fh_write.write (data_str)

print (f'Finished writing data into file "{file_output}"!')
