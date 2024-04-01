# add data to SQL
import gzip
import sys

file_catalogue = 'sao.dat.gz'
file_sql = 'sao.sql'

# open SQL file for writing data
with open(file_sql, 'w') as fh_sql:
  # SQL command to create table
  sql_table = f'create table sao (sao integer primary key,' \
        + f'ra text, dec text, ' \
        + f'vmag real, sptype text);\n'
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
        RAh = int(line[7:9])
        RAm = int(line[9:11])
        RAs = float(line[11:17])
      except:
        RAh = 99
        RAm = 99
        RAs = 99.9
      RA = f'{RAh:02d}:{RAm:02d}:{RAs:04.1f}'
  
      # Declination
      try:
        Dec_sign = line[41:42].decode('utf-8')
        Dec_d = int(line[42:44])
        Dec_m = int(line[44:46])
        Dec_s = int(line[46:51])
      except:
        Dec_sign = '-'
        Dec_d = 99
        Dec_m = 99
        Dec_s = 99
      Dec = f'{Dec_sign}{Dec_d:02d}:{Dec_m:02d}:{Dec_s:02d}'
      
      # Visual Magnitude
      try:
        Vmag = float(line[80:84])# Vmag Byte 81~84
      except:
        Vmag = -999 # an impossible value
      
      # SpType
      SpType = line[84:87].strip().decode('utf-8')# SpType Byte 85~87

      # SQL command to add data to table
      sql_add = f'insert into sao values ({SAO}, ' \
          + f'"RA", "Dec", ' \
          + f'{Vmag}, "{SpType}");\n'
      fh_sql.write(sql_add)
