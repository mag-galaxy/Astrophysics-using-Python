import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
link = 'http://astro.phys.wvu.edu/wise/wise_hii_V2.2.csv'
file_output = 'hii.data'    # output file name

print (f'Now, fetching {link}...')
with urllib.request.urlopen (link) as fh_read:
    for line in fh_read:
        print(line)

with open (file_output, 'wb') as fh_write:
    fh_write.write (data_byte)
print (f'Finished writing data into file "{file_output}"!')
