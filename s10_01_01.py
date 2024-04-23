import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
link = 'http://astro.phys.wvu.edu/wise/wise_hii_V2.2.csv'
data_output = 'data.txt'

# download data
with urllib.request.urlopen (link) as fh_read:
