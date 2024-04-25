import astropy.io.ascii

# CSV file name
file_csv = 'Leda_data_1.txt'

# reading a CSV file and storing data in an astropy table
table = astropy.io.ascii.read(file_csv, format='csv')
print(table)
