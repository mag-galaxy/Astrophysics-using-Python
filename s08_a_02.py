# extract data and visualize
import numpy
import astropy.units
import matplotlib.figure
import matplotlib.backends.backend_agg

file_input = 'hd98800_b.data'
file_output = 'hd98800_b.png'
resolution_dpi = 150

# units
micron = astropy.units.micron
Jy = astropy.units.Jy

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
            
            wl = float(wl_str)
            flux = float(flux_str) * 0.001            # 1 mJy = 0.001 Jy
            flux_error = float(flux_error_str) * 0.001

            data_wl = numpy.append (data_wl, wl)
            data_flux = numpy.append (data_flux, flux)
            data_flux_err = numpy.append (data_flux_err, flux_error)

# adding units
data_wl = data_wl * micron
data_flux = data_flux * Jy
data_flux_err = data_flux_err * Jy

# printing data
print (f'SED of HD 98800 B')
print (f'  wavelength:')
print (f'    {data_wl}')
print (f'  flux:')
print (f'    {data_flux}')
print (f'  error of flux:')
print (f'    {data_flux_err}')

# objects for plotting
fig = matplotlib.figure.Figure()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
ax = fig.add_subplot(111)

ax.set_xlabel (r'Wavelength [$\mu$m]')
ax.set_ylabel (r'Flux [Jy]')
ax.set_xscale ('log')
ax.set_yscale ('log')
ax.set_xlim (10**-1, 10**4)
ax.set_ylim (10**-2, 10**2)

# plotting data
ax.errorbar (data_wl, data_flux, yerr=data_flux_err, \
             linestyle='None', marker='o', markersize=5, color='red', \
             ecolor='black', elinewidth=2, capsize=5, \
             label='HD 98800 B')
ax.legend ()

fig.savefig (file_output, dpi=resolution_dpi)
