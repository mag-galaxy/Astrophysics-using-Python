# extract data
import numpy
import astropy.units

file_input = 'hd98800_b.data'

# units
micron = astropy.units.micron
Jy     = astropy.units.Jy

# empty numpy arrays for storing data
data_wl = numpy.array([])
data_flux = numpy.array([])
data_flux_err = numpy.array([])

# opening data file
with open (file_input, 'r') as fh:
    for line in fh:
        # if the word '+or-' is found, then we process the line
        if ('+or-' in line):
            data = line.split ('+or-')        # before +or- is wavelength and flux
            (wl_str, flux_str) = data[0].split()
            flux_error_str = (data[1].split())[0]    # after +or- is flux error
            
            wl = float (wl_str)
            flux = float (flux_str)
            flux_error = float (flux_error_str)

            data_wl = numpy.append (data_wl, wl)
            data_flux = numpy.append (data_flux, flux)
            data_flux_err = numpy.append (data_flux_err, flux_error)

# adding units
data_wl = data_wl * micron
data_flux = data_flux * Jy
data_flux_err = data_flux_err * Jy

print (f'SED of HD 98800 B')
print (f'  wavelength:')
print (f'    {data_wl}')
print (f'  flux:')
print (f'    {data_flux}')
print (f'  error of flux:')
print (f'    {data_flux_err}')
