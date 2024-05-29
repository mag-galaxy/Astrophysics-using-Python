# read data we download from part1
import argparse
import numpy
import astropy.io.votable

# use argparse
descr  = f'read VOTable file and write data into output file'
parser = argparse.ArgumentParser(description=descr)
parser.add_argument('-i', '--input', help='input VOTable file name')
parser.add_argument('-o', '--output', help='output file name')
args = parser.parse_args()

# get value from argument
file_input = args.input
file_output = args.output

print(f'Now, reading VOTable file "{file_input}"...')
    
# read VOTable using astropy
table = astropy.io.votable.parse_single_table(file_input).to_table()

print(f'Finished reading VOTable file "{file_input}"!')

# extract necessary data from Gaia catalogue
data_id = numpy.array(table['SOURCE_ID'])
data_ra = numpy.array(table['ra'])
data_dec = numpy.array(table['dec'])
data_parallax = numpy.array(table['parallax'])
data_pmra = numpy.array(table['pmra'])
data_pmdec = numpy.array(table['pmdec'])
data_rv = numpy.array(table['radial_velocity'])

print(f'Now, writing data into file "{file_output}"...')

# write necessary data into output file
with open (file_output, 'w') as fh:
    header = f'#\n' \
        + f'# Gaia DR3 data\n' \
        + f'#  data format of this file\n\n' \
        + f'#   column 01 : source ID\n' \
        + f'#   column 02 : RA in deg\n' \
        + f'#   column 03 : Dec in deg\n' \
        + f'#   column 04 : parallax in mas\n' \
        + f'#   column 05 : proper motion in RA direction in mas/yr\n' \
        + f'#   column 06 : proper motion in Dec direction in mas/yr\n' \
        + f'#   column 07 : radial velocity in km/s\n\n' \
    fh.write(header)
    
    for i in range(len(data_id)):
        # rejecting data without parallax measurement
        if (numpy.isnan(data_parallax[i])):
            continue
        # rejecting data with negative parallax
        if (data_parallax[i] < 0.0):
            continue
        # rejecting data with poor S/N ratio of parallax measurement
        if (data_parallax_snr[i] < 10.0):
            continue
        # rejecting data if b or g or r band magnitude is NaN
        if (numpy.isnan (data_b[i]) or numpy.isnan(data_g[i]) or numpy.isnan(data_r[i])):
            continue
        record = f"{data_id[i]:19d} {data_ra[i]:12.8f} {data_dec[i]:12.8f}" \
            + f" {data_parallax[i]:8.3f} {data_pmra[i]:8.3f} {data_pmdec[i]:8.3f}" \
            + f" {data_rv[i]:12.6f}\n"
        fh.write(record)
print(f'Finished writing data into file "{file_output}"!')
