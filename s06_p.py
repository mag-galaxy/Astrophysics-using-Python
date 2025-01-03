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

total_price = 0

#line 8~14
all_data = data_read.split('\n')# by line

for i in range(8, 15):
  item_data = all_data[i].split()
  total_price += int(item_data[1])*int(item_data[2])

print(f'total price: {total_price}')
