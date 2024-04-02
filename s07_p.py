import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

link = 'https://s3b.astro.ncu.edu.tw/appy_202402/data/p07.data'    # URL of data
file_output = 'sao.dat.gz'    # output file name

with urllib.request.urlopen(link) as f_read:
  data_read = f_read.read().decode('utf-8')
