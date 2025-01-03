import argparse
import numpy
import astropy.io.votable
import matplotlib.figure
import matplotlib.backends.backend_agg

# using argparse
descr = 'selecting stars in given distance range'
parser = argparse.ArgumentParser(description=descr)
parser.add_argument('-i', '--input', help='input file name (gzip)')
parser.add_argument('-o', '--output', help='output file name (list)')
parser.add_argument('-a', '--min', type=float, help='min. dist. value')
parser.add_argument('-b', '--max', type=float, help='max. dist. value')
args = parser.parse_args()

# get value from argument
file_votable = args.input
file_output = args.output
dist_min = args.min
dist_max = args.max

# read input file
table = astropy.io.votable.parse_single_table(file_votable).to_table()

# data
data_parallax = numpy.array(table['parallax'])
data_pmra = numpy.array(table['pmra'])
data_pmdec = numpy.array(table['pmdec'])
data_g = numpy.array(table['phot_g_mean_mag'])
data_br = numpy.array(table['bp_rp'])
data_b_snr = numpy.array(table['phot_bp_mean_flux_over_error'])
data_g_snr = numpy.array(table['phot_g_mean_flux_over_error'])
data_r_snr = numpy.array(table['phot_rp_mean_flux_over_error'])
data_p_snr = numpy.array(table['parallax_over_error'])

# filter data
data_dis = numpy.array([])    # empty numpy array for storing dist. data
for i in range(len(data_parallax)):
    # not use negative parallax, null parallax, parallax SNR < 10.0
    if (data_parallax[i] <= 0.0 or numpy.isnan(data_parallax[i]) \
         or data_p_snr[i] < 10.0):
        data_dis = numpy.append(data_dis, -1.0)
    else:
        data_dis = numpy.append(data_dis, 1000.0 / data_parallax[i])

# writing data into list file
with open (file_output, 'w') as fh:
    header = f'# parallax, pmra, pmdec, g mag, b-r\n'
    fh.write(header)
    for i in range (len(data_dis)):
        # rejecting stars of low signal-to-noise ratio
        if(data_b_snr[i] < 10.0):
            continue
        if(data_g_snr[i] < 10.0):
            continue
        if(data_r_snr[i] < 10.0):
            continue
        # select data in the given range
        if(data_dis[i] >= dist_min and data_dis[i] <= dist_max):
            record = f" {data_parallax[i]:10.6f}" \
                + f" {data_pmra[i]:10.6f} {data_pmdec[i]:10.6f}" \
                + f" {data_g[i]:9.6f} {data_br[i]:9.6f}\n"
            fh.write(record)
