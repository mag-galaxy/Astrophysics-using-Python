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
   print('{i}. : {all_data[i]}')
print(f'data number: {len(all_data)}')

total = 0
for i in range(len(all_data)):
  total += float(all_data[i])
print(f'total: {total}')
mean = total/len(all_data)
print(f'mean = {mean}')
