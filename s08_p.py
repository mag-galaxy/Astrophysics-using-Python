import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

link = 'https://www.minorplanetcenter.net/iau/MPCORB/NEA.txt'    # URL of data
file_sql = 'asteriod.sql'

with urllib.request.urlopen(link) as f_read:
  data_read = f_read.read().decode('utf-8')

all_data = data_read.split('\n')# by line

with open(file_sql, 'w') as fh_sql:
  # SQL command to create table
  sql_table = f'create table asteriod (number text primary key,' \
        + f'semi real);\n'
  fh_sql.write(sql_table)

  for i in range(len(all_data))
      number = all_data[i][0:7].strip().decode('utf-8')
      semi = float(all_data[i][92:103])
    
    sql_add = f'insert into asteriod values ("{number}", ' \
          + f'{semi});\n'
    fh_sql.write(sql_add)
