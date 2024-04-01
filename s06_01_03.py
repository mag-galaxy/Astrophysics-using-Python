# read data from catalogue
import gzip
import sys

file_catalogue = 'sao.dat.gz'

# open catalogue file
with gzip.open(file_catalogue, 'rb') as fh:
  for line in fh:
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

    # print extracted data
    print(f'SAO = {SAO}')
    print(f'  RA = {RA}')
    print(f'  Vmag = {Vmag}')
    print(f'  SpType = {SpType}')
