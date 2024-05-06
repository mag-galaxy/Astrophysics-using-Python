import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
url_data = 'https://www.pas.rochester.edu/~emamajek/EEM_dwarf_UBVIJHK_colors_Teff.txt'
file_output = 'ms.data'

# opening URL
with urllib.request.urlopen (url_data) as fh_read:
    data_byte = fh_read.read ()

# opening file for writing
with open (file_output, 'wb') as fh_write:
    fh_write.write (data_byte)

print (f'Finished writing data into file "{file_output}"!')
