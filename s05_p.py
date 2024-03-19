import argparse
import ssl
import urllib.request
parser = argparse.ArgumentParse(description = 'download data')
parser.add_argument('url', default = '', help = 'URL of data')

args = parser.parse_args()

url_data = args.url
ssl._create_default_https_context = ssl._create_unverified_context

with urllib.request.urlopen(url_data) as f_read:
  data_read = f_read.read()
total = 0
for i in range(len(data_read)):
  total += data_read[i]
mean = total/len(data_read)
print(f'mean = {mean}')