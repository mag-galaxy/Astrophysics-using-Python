import argparse
import numpy
import astropy.timeseries

# using argparse
descr = 'Lomb-Scargle periodogram'
parser = argparse.ArgumentParser(description=descr)
parser.add_argument('-i', type=str, default="in.data", help='input file name (data)')
parser.add_argument('-o', type=str, default="out.data", help='output file name (data)')
parser.add_argument('-n', type=int, default=30, help='samples per peak for frequency grid spacing')
parser.add_argument('-a', type=float, default=0.01, help='min. trial period in min')
parser.add_argument('-b', type=float, default=14400.0, help='max. trial period in min')
args = parser.parse_args()

# get value from argument
input_data = args.i
output_data = args.o
n = args.n

# minimum trial period
per_min_min = args.a
per_min_hr = per_min_min / 60.0
per_min_day = per_min_min / 1440.0
freq_max_day = 1.0 / per_min_day

# maximum trial period
per_max_min = args.b
per_max_hr = per_max_min / 60.0
per_max_day = per_max_min / 1440.0
freq_min_day = 1.0 / per_max_day

# store data
data_mjd = numpy.array([])
data_mag = numpy.array([])
data_err = numpy.array([])

# read data
with open (input_data, 'r') as fh_read:
    for line in fh_read:
        if (line[0] == '#'):
            continue
        line = line.strip()
        all_data = line.split()
        mjd = float(all_data[1])
        mag = float(all_data[2])
        err = float(all_data[3])
        data_mjd = numpy.append(data_mjd, mjd)
        data_mag = numpy.append(data_mag, mag)
        data_err = numpy.append(data_err, err)

# Lomb-Scargle periodogram
freq, power = astropy.timeseries.LombScargle(data_mjd, data_mag)\
            .autopower(minimum_frequency=freq_min_day, \
                       maximum_frequency=freq_max_day, samples_per_peak=n)

# wrtie data into output file
with open (output_data, 'w') as fh_write:
    header  = f"# result of period search by Lomb-Scargle periodogram\n"
    header += f"# frequency in cycle day^-1, period in day, period in hr, "
    header += f"period in min, power\n"
    fh_write.write(header)

    for i in range(len(freq)):
        record = f"{freq[i]:15.8f} {1.0 / freq[i]:15.8f}" \
            + f" {1.0 / freq[i] * 24.0:15.8f} {1.0 / freq[i] * 1440:15.8f}" \
            + f" {power[i]:15.8f}\n"
        fh_write.write(record)
