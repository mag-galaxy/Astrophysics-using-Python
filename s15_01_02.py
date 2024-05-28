# read data we download from part1
import argparse
import numpy
import astropy.io.votable

# use argparse
descr  = f'reading a VOTable file and writing data into a file'
parser = argparse.ArgumentParser(description=descr)
parser.add_argument('-i', '--input', help='input VOTable file name')
parser.add_argument('-o', '--output', help='output file name')
parser.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose mode')
args = parser.parse_args()

# get value from argument
file_votable = args.input
file_output = args.output
verbose = args.verbose

if(verbose):
    print (f'Now, reading VOTable file "{file_votable}"...')
    
# read VOTable using astropy
table = astropy.io.votable.parse_single_table(file_votable).to_table ()

if(verbose):
    print (f'Finished reading VOTable file "{file_votable}"!')

# data
data_id = numpy.array(table['SOURCE_ID'])
data_ra = numpy.array(table['ra'])
data_dec = numpy.array(table['dec'])
data_parallax = numpy.array(table['parallax'])
data_pmra = numpy.array(table['pmra'])
data_pmdec = numpy.array(table['pmdec'])
data_rv = numpy.array(table['radial_velocity'])

if (verbose):
    print (f'Now, writing data into file "{file_output}"...')

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
        + f'#   column 07 : radial velocity in km/s\n' \
        + f'#\n'
    fh.write(header)
    
    for i in range (len(data_id)):
        # rejecting data without parallax measurement
        if ( numpy.isnan(data_parallax[i])):
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
        record = f"{data_id[i]:19d}" \
            + f" {data_ra[i]:12.8f}" \
            + f" {data_dec[i]:12.8f}" \
            + f" {data_parallax[i]:8.3f}" \
            + f" {data_pmra[i]:8.3f}" \
            + f" {data_pmdec[i]:8.3f}" \
            + f" {data_rv[i]:12.6f}\n" \
        fh.write(record)

# printing status
if (verbose):
    print (f'Finished writing data into file "{file_output}"!')
