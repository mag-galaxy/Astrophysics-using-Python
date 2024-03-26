import argparse
import ssl
import urllib.request
parser = argparse.ArgumentParser(description = 'download data')
parser.add_argument('-url', default = '', help = 'URL of data')

args = parser.parse_args()

link = args.url
ssl._create_default_https_context = ssl._create_unverified_context

with urllib.request.urlopen(link) as f_read:
  data_read = f_read.read().decode('utf-8')
all_data = data_read.split('\n')
for i in range(len(all_data)):
   print(all_data[i])
print(f'data number: {len(data_read)}')

total = 0
for i in range(len(data_read)):
  total += float(data_read[i])
print(f'total: {total}')
mean = total/len(data_read)
print(f'mean = {mean}')
