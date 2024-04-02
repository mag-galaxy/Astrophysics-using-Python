import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

link = 'https://s3b.astro.ncu.edu.tw/appy_202402/data/p07.data'    # URL of data
file_sql = 'sao.sql'

with urllib.request.urlopen(link) as f_read:
  data_read = f_read.read().decode('utf-8')

all_data = data_read.split('\n')# by line

with open(file_sql, 'w') as fh_sql:
  # SQL command to create table
  sql_table = f'create table sao (name text primary key,' \
        + f'app_mag real, abs_mag real, sptype text);\n'
  fh_sql.write(sql_table)

  for i in range(10,31):
    item = all_data[i].split()
    name = item[0]
    app_mag = item[1]
    abs_mag = item[2]
    sptype = item[3]
    sql_add = f'insert into star values ("{name}", ' \
          + f'{app_mag}, {abs_mag}, "{SpType}");\n'
      fh_sql.write(sql_add)
