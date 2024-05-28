# do DBSCAN analysis using data we extract in part2
import argparse
import numpy
import sklearn.cluster

# use argparse
descr = 'finding star cluster members using parallax, rv, pmra, and pmdec'
parser = argparse.ArgumentParser(description=descr)
parser.add_argument('-i', '--input', help='input file name')
parser.add_argument('-o', '--output', help='output file name')
parser.add_argument('-d', '--norm-factor-distance', type=float, default=30, help='normalisation factor for distance in pc')
parser.add_argument('-r', '--norm-factor-rv', type=float, default=2, help='normalisation factor for rv in km/s')
parser.add_argument('-e', '--eps', type=float, default=1.0, help='parameter eps for DBSCAN analysis')
parser.add_argument('-n', '--min-samples', type=int, default=30, help='parameter min-samples for DBSCAN analysis')
parser.add_argument('-v', '--verbose', action='store_true', default=False, help='verbose mode')
args = parser.parse_args()

# get value from argument
file_input = args.input
file_output = args.output
normfactor_dist = args.norm_factor_distance
normfactor_rv = args.norm_factor_rv
eps = args.eps
min_samples = args.min_samples
verbose = args.verbose

# empty lists for storing data
list_id = []
list_ra = []
list_dec = []
list_parallax = []
list_dist = []
list_dist_norm = []
list_pmra = []
list_pmdec = []
list_rv = []
list_rv_norm = []
list_stars = []

if (verbose):
    print (f'Now, reading Gaia DR3 data file...')

# read input file for data
with open (file_input, 'r') as fh:
    for line in fh:
        if (line[0] == '#'):
            continue
        (source_id, ra, dec, parallax, pmra, pmdec, rv) = line.split()
        if (rv == 'nan'):  # skip nan rv
            continue
        source_id = int(source_id)
        ra = float(ra)
        dec = float(dec)
        parallax = float(parallax)
        pmra = float(pmra)
        pmdec = float(pmdec)
        rv = float(rv)
        dist_pc = 1000.0 / parallax        # calculation of distance in pc
        dist_norm = dist_pc / normfactor_dist        # normalisation of distance in pc
        rv_norm = rv / normfactor_rv        # normalisation of radial velocity in km/s
        list_id.append(source_id)
        list_ra.append(ra)
        list_dec.append(dec)
        list_parallax.append(parallax)
        list_dist.append(dist_pc)
        list_dist_norm.append(dist_norm)
        list_pmra.append(pmra)
        list_pmdec.append(pmdec)
        list_rv.append(rv)
        list_rv_norm.append(rv_norm)
       
if (verbose):
    print (f'Finished reading Gaia DR3 data file!')

if (verbose):
    print (f'Now, constructing Numpy array...')

# change into numpy arrays
array_id = numpy.array(list_id)
array_ra = numpy.array(list_ra)
array_dec = numpy.array(list_dec)
array_parallax = numpy.array(list_parallax)
array_dist = numpy.array(list_dist)
array_dist_norm = numpy.array(list_dist_norm)
array_pmra = numpy.array(list_pmra)
array_pmdec = numpy.array(list_pmdec)
array_rv = numpy.array(list_rv)
array_rv_norm = numpy.array(list_rv_norm)

# constructing a Numpy array for DBSCAN analysis
stars = numpy.stack ([array_dist_norm, array_pmra, array_pmdec, array_rv_norm]).transpose()
    
if (verbose):
    print (f'Finished constructing Numpy array!')
    
if (verbose):
    print (f'Now, doing DBSCAN analysis...')

# clustering analysis using DBSCAN
result_dbscan = sklearn.cluster.DBSCAN(eps=eps, min_samples=min_samples, n_jobs=-1).fit(stars)
labels = result_dbscan.labels_

if (verbose):
    print (f'Finished doing DBSCAN analysis!')

if (verbose):
    print (f'Now, writing results into output file...')

# write clustring result into output file
with open (file_output, 'w') as fh:
    header = f'#\n' \
        + f'# Results of DBSCAN analysis\n' \
        + f'#\n' \
        + f'#  format of this data file\n' \
        + f'#\n' \
        + f'#   column 01 : source ID\n' \
        + f'#   column 02 : RA in deg\n' \
        + f'#   column 03 : Dec in deg\n' \
        + f'#   column 04 : parallax in mas\n' \
        + f'#   column 05 : distance in pc\n' \
        + f'#   column 06 : normalised distance\n' \
        + f'#   column 07 : proper motion in RA in mas/yr\n' \
        + f'#   column 08 : proper motion in Dec in mas/yr\n' \
        + f'#   column 09 : radial velocity in km/s\n' \
        + f'#   column 10 : normalised radial velocity\n' \
        + f'#   column 11 : labels (0=1st cluster, 1=2nd cluster, ... , -1=field stars)\n' \
        + f'#\n'
    fh.write(header)

    for i in range(len(array_id)):
        record = f"{array_id[i]:19d}" \
            + f" {array_ra[i]:12.8f}" \
            + f" {array_dec[i]:12.8f}" \
            + f" {array_parallax[i]:8.3f}" \
            + f" {array_dist[i]:8.3f}" \
            + f" {array_dist_norm[i]:8.3f}" \
            + f" {array_pmra[i]:8.3f}" \
            + f" {array_pmdec[i]:8.3f}" \
            + f" {array_rv[i]:12.6f}" \
            + f" {array_rv_norm[i]:12.6f}" \
            + f" {labels[i]}\n"
        fh.write(record)

if (verbose):
    print (f'Finished writing results into output file!')
