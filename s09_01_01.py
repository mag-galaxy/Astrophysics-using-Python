import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
link = 'http://astro.phys.wvu.edu/wise/wise_hii_V2.2.csv'
file_output = 'hii.data'    # output file name

print (f'Now, fetching {link}...')
with urllib.request.urlopen (link) as fh_read:
    i = 0
    for line in fh_read:
        if i==0:
            ++i
            continue
        else:
            data_str = line.decode('utf-8')
            data_list = data_str.split(',')
            print(data_list)
