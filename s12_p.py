import ssl
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context

dat_url = 'https://cdsarc.cds.unistra.fr/ftp/J/A+A/438/1163/cocd.dat'
readme_url = 'https://cdsarc.cds.unistra.fr/ftp/J/A+A/438/1163/ReadMe'

output_dat = 'cocd.dat'
output_read = 'cocd.readme'

with open(dat_url, 'r') as f_read:
  with open(output_dat, 'w') as f_write:
    for line in f_read:
      data = line.decode('utf-8')
      f_write.write(data)
f_read.close()
f_write.close()

with open(readme_url, 'r') as f_read:
  with open(output_read, 'w') as f_write:
    for line in f_read:
      data = line.decode('utf-8')
      f_write.write(data)
f_read.close()
f_write.close()
