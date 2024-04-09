import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

link = 'https://www.minorplanetcenter.net/iau/MPCORB/NEA.txt'    # URL of data
file_txt = 'asteriod.txt'
file_sql = 'asteriod.sql'

with urllib.request.urlopen (link) as fh_read:
    data_byte = fh_read.read ()

with open (file_txt, 'wb') as fh_write:
    fh_write.write (data_byte)

print('finish writing data to .txt')

with open (file_sql, 'w') as fh_sql:
  sql_table = f'create table asteriod (asteriod text primary key, semi real);\n'
  fh_sql.write(sql_table)
  
  with open(file_txt, 'rb') as fh:
    for line in fh:
      number = line[0:7].strip().decode('utf-8')
      semi = float(line[92:103])
      
      sql_add = f'insert into asteriod values ("{number}", {semi});\n'
      fh_sql.write(sql_add)
print('finish adding data into sql table')
