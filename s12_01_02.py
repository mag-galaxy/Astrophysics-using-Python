# read fits data
import argparse
import astropy.timeseries
import astropy.units

# using argparse
descr = 'reading FITS files'
parser = argparse.ArgumentParser(description=descr)
parser.add_argument('-o', type=str, default='out.data', help='output file name')
parser.add_argument('files', type=str, nargs='+', help='input FITS files')
args = parser.parse_args()

# get value from argument
output_file = args.o
fits_file = args.files

# units
u_sec = astropy.units.second
u_electron = astropy.units.electron

# write into output file
with open(output_file, 'w') as fh:
    for file_fits in fits_file:
        ts = astropy.timeseries.TimeSeries.read(file_fits, format='kepler.fits')
        data_datetime = ts['time']
        data_mjd = ts.time.mjd
        data_flux = ts['sap_flux'] * u_sec / u_electron
        data_err = ts['sap_flux_err'] * u_sec / u_electron

        for i in range(len(data_datetime)):
            line = f"{data_datetime[i]} {data_mjd[i]:15.8f}" \
                + f" {data_flux[i]:15.6f} {data_err[i]:15.6f}\n"
            fh.write (line)
