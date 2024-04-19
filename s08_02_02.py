import numpy
import scipy.optimize
import astropy.constants
import astropy.units
import matplotlib.figure
import matplotlib.backends.backend_agg

# input file name
file_input = 'hd98800_b.data'
file_output = 'HD98800B.png'
resolution_dpi = 150

# constants & units
c = astropy.constants.c
h = astropy.constants.h
k = astropy.constants.k_B
u_micron = astropy.units.micron
u_Jy     = astropy.units.Jy

# making empty numpy arrays
data_wl = numpy.array([])
data_flux = numpy.array([])
data_flux_err = numpy.array([])

# opening data file
with open (file_input, 'r') as fh:
    for line in fh:
        # if the word '+or-' is found, then we process the line
        if ('+or-' in line):
            data = line.split('+or-')        # before +or- is wavelength and flux
            (wl_str, flux_str) = data[0].split()
            flux_error_str = (data[1].split())[0]    # after +or- is flux error
            wl = float(wl_str)
            flux = float(flux_str) * 0.001            # 1 mu_Jy = 0.001 u_Jy
            flux_error = float(flux_error_str) * 0.001
            data_wl = numpy.append(data_wl, wl)
            data_flux = numpy.append(data_flux, flux)
            data_flux_err = numpy.append(data_flux_err, flux_error)

# adding units
data_wl = data_wl * u_micron
data_flux = data_flux * u_Jy
data_flux_err = data_flux_err * u_Jy

# initial values of coefficients for fitting by least-squares method
T_phot = 5000.0
a_phot = 10**8
T_disk = 100.0
a_disk = 10**10
init_coeff = [T_phot, a_phot, T_disk, a_disk]

# Planck's radiation law
def twobb_nu (x, T_phot, a_phot, T_disk, a_disk):
    x_m = x * 10**-6            # wavelength in metre
    f = c.value / x_m           # frequency in Hz
    y_phot = a_phot * 2.0 * h.value * f**3 / c.value**2 \
        / (numpy.exp (h.value * f / (k.value * T_phot) ) - 1.0 )
    y_disk = a_disk * 2.0 * h.value * f**3 / c.value**2 \
        / (numpy.exp (h.value * f / (k.value * T_disk) ) - 1.0 )
    y = y_phot + y_disk
    return (y)

# weighted least-squares method
popt, pcov = scipy.optimize.curve_fit (twobb_nu, data_wl.value, data_flux.value, \
                                       p0=init_coeff, sigma=data_flux_err.value)

# result of fitting
print (f"T_phot = {popt[0]} K")
print (f"T_disk = {popt[2]} K")
print (f'{popt}')

# generating fitted curve
wl_min = -3.0
wl_max = 6.0
n = 9001
model_x = numpy.logspace(wl_min, wl_max, n)
model_y = twobb_nu(model_x, popt[0], popt[1], popt[2], popt[3])

# objects for plotting
fig = matplotlib.figure.Figure()
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
ax = fig.add_subplot(111)

ax.set_xlabel (r'Wavelength [$\mu$m]')
ax.set_ylabel (r'Flux [u_Jy]')
ax.set_xscale ('log')
ax.set_yscale ('log')
ax.set_xlim(10**-3, 10**6)
ax.set_ylim(10**-5, 10**2)

# plotting data
ax.errorbar (data_wl, data_flux, yerr=data_flux_err, \
             linestyle='None', marker='o', markersize=5, color='red', \
             ecolor='black', elinewidth=2, capsize=5, zorder=0.2, label='HD61005')
ax.plot (model_x, model_y, linestyle='-', linewidth=3, color='olive', \
         zorder=0.1, label='Two-temperature blackbody fitting')
ax.legend ()
fig.savefig (file_output, dpi=resolution_dpi)
