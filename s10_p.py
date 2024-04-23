import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

link = 'https://cdsarc.cds.unistra.fr/ftp/J/AJ/137/4186/table2.dat'    # URL of data
file_sql = 'UBVRI.sql'

with urllib.request.urlopen (link) as fh_read:
  with open(file_sql, 'w') as fh_sql:
    sql_table = f'create table UBVRI (UBVRI text primary key, vmag real);\n'
    fh_sql.write(sql_table)
    for line in fh_read:
      data_byte = line.decode('utf-8')
      Name = line[0:11].strip()
      Vmag = float(line[38:44])
    
    sql_add = f'insert into UBVRI values ("{Name}", {Vmag});\n'
    fh_sql.write(sql_add)
