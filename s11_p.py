import astropy.io.ascii

file_csv = 'earthquack.csv'
table = astropy.io.ascii.read (file_csv, format='csv')

print(f'{table['規模']}')
