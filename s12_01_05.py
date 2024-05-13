import argparse
import numpy

# using argparse
descr = 'baseline correction'
parser = argparse.ArgumentParser(description=descr)
parser.add_argument('-i', type=str, default="in.data", help='input file name (data)')
parser.add_argument('-o', type=str, default="out.eps", help='output file name (data)')
parser.add_argument('-a', type=float, default=0, help='coe a')
parser.add_argument('-b', type=float, default=0, help='coe b')
args = parser.parse_args()

# get value from argument
input_data = args.i
output_data = args.o
a = args.a
b = args.b

# store data
data_mjd = numpy.array([])
data_flux = numpy.array([])
data_err = numpy.array([])

# read data and write data
with open (input_data, 'r') as fh_read:
    with open (output_data, 'w') as fh_write:
        for line in fh_read:
            if (line[0] == '#'):
                continue
            line = line.strip()
            all_data = line.split()
            (datetime_str, mjd_str, flux_str, err_str) = line.split ()
            if (all_data[2] == 'nan'):
                continue
            mjd = float(all_data[1])
            flux = float(all_data[2]) / (-a * mjd + b)
            err = float(all_data[3]) / float(all_data[2])
            record = f"{datetime_str} {mjd:.10f} {flux:.10f} {err:.10f}\n"
            fh_write.write (record)
