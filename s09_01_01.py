import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
link = 'http://astro.phys.wvu.edu/wise/wise_hii_V2.2.csv'
data_output = 'data.txt'

# download data
with urllib.request.urlopen (link) as fh_read:
    with open(data_output, 'w') as f_write:
        for line in fh_read:
            data_str = line.decode('utf-8')
            data_list = data_str.split(',')
            if data_list[2]=="GLong<br>(deg.)":
                continue
            f_write.write(data_list[2] + ',' + data_list[3] + '\n')
f_write.close()
print('finish downloading data')
