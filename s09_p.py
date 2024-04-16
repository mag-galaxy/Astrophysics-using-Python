import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

link = 'https://cdsarc.cds.unistra.fr/ftp/cats/I/239/hip_main.dat'    # URL of data
file_output = 'hip.data'    # output file name
file_sql = 'hip.sql'

print (f'Now, fetching {link}...')
# open URL and read data
with urllib.request.urlopen (link) as fh_read:
    data_byte = fh_read.read ()

print (f'Finished fetching {link}!')
print (f'Now, writing data into file "{file_output}"...')

# write data to output file
with open (file_output, 'wb') as fh_write:
    fh_write.write (data_byte)

print (f'Finished writing data into file "{file_output}"!')

# create table
with open(file_sql, 'w') as fh_sql:
    # SQL command to create table
    sql_table = f'create table hip (hip integer primary key,  B_V real);\n'
    fh_sql.write(sql_table)
    with open(file_output, 'rb') as fh:
      for line in fh:
        try:
          HIP = int(line[8:14])
        except:
          print("ERROR: cannot extract HIP number!")
          sys.exit(1)
    
        # Right Ascension
        try:
            B_V = float(line[244:251])
        except:
            B_V = 0

        # SQL command to add data to table
        sql_add = f'insert into hip values ({HIP}, {B_V});\n'
        fh_sql.write(sql_add)
