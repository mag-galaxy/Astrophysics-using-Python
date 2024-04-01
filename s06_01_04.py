# add data to SQL
import gzip
import sys

file_catalogue = 'sao.dat.gz'
file_sql = 'sao.sql'

# open SQL file for writing data
with open(file_sql, 'w') as fh_sql:
  # SQL command to create table
  sql_table = f'create table sao (sao integer primary key,' \
        + f'ra text, vmag real, sptype text);\n'
  fh_sql.write(sql_table)

  #open catalogue file
  with gzip.open(file_catalogue, 'rb') as fh_sao:
    for line in fh_sao:
      # SAO number
      try:
        SAO = int(line[0:6])# SAO Byte 1~6
      except:
        print("ERROR: cannot extract SAO number!")
        sys.exit(1)
      
      # Right Ascension
      try:
        RAh = int(line[150:152])
        RAm = int(line[152:154])
        RAs = float(line[154:160])
      except:
        RAh = 99
        RAh = 99
        RAh = 99.9
      RA = f'{RAh:02d}:{RAm:02d}:{RAs:04.1f}'
        
      # Visual Magnitude
      try:
        Vmag = float(line[80:84])# Vmag Byte 81~84
      except:
        Vmag = -999 # an impossible value
      
      # SpType
      SpType = line[84:87].strip().decode('utf-8')# SpType Byte 85~87

      # SQL command to add data to table
      sql_add = f'insert into sao values ({SAO}, ' \
          + f'"{RA}", {Vmag}, "{SpType}");\n'
      fh_sql.write(sql_add)
