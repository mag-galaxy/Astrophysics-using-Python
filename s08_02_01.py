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
phot_wl = numpy.array([])
phot_flux = numpy.array([])
phot_flux_err = numpy.array([])
disk_wl = numpy.array([])
disk_flux = numpy.array([])
disk_flux_err = numpy.array([])

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
            
            # photosphere data
            if (wl < 5.0):
                phot_wl = numpy.append(phot_wl, wl)
                phot_flux = numpy.append(phot_flux, flux)
                phot_flux_err = numpy.append(phot_flux_err, flux_error)
            # debris disk data
            if (wl > 30.0):
                disk_wl = numpy.append(disk_wl, wl)
                disk_flux = numpy.append(disk_flux, flux)
                disk_flux_err = numpy.append(disk_flux_err, flux_error)

# adding units
data_wl = data_wl * u_micron
data_flux = data_flux * u_Jy
data_flux_err = data_flux_err * u_Jy
phot_wl = phot_wl * u_micron
phot_flux = phot_flux * u_Jy
phot_flux_err = phot_flux_err * u_Jy
disk_wl = disk_wl * u_micron
disk_flux = disk_flux * u_Jy
disk_flux_err = disk_flux_err * u_Jy

# printing data
print (f'data for SED fitting at visible-NIR:')
print (f'  {phot_wl}')
print (f'  {phot_flux}')
print (f'data for SED fitting at mid-IR:')
print (f'  {disk_wl}')
print (f'  {disk_flux}')

# coefficients for least-squares method
T_phot = 10000.0
a_phot = 10**8
init_phot = [T_phot, a_phot]
T_disk = 100.0
a_disk = 10**10
init_disk = [T_disk, a_disk]

# Planck's radiation law
def bb_nu (x, T, a):
    x_m = x * 10**-6                # wavelength in meter
    f = c.value / x_m               # frequency in Hz
    y = a * 2.0 * h.value * f**3 / c.value**2 \
        / (numpy.exp (h.value * f / (k.value * T) ) - 1.0 )
    return(y)

# weighted least-squares method
popt_phot, pcov_phot = scipy.optimize.curve_fit(bb_nu, phot_wl.value, phot_flux.value, \
                                                 p0=init_phot, sigma=phot_flux_err.value)
popt_disk, pcov_disk = scipy.optimize.curve_fit(bb_nu, disk_wl.value, disk_flux.value, \
                                                 p0=init_disk, sigma=disk_flux_err.value)

# result of fitting
print (f"T_phot = {popt_phot[0]} K")
print (f"T_disk = {popt_disk[0]} K")

# generating fitted curve
wl_min = -3.0
wl_max = 6.0
n = 4001
phot_x = numpy.logspace(wl_min, wl_max, n)
phot_y = bb_nu(phot_x, popt_phot[0], popt_phot[1])
disk_x = numpy.logspace(wl_min, wl_max, n)
disk_y = bb_nu(disk_x, popt_disk[0], popt_disk[1])

# two temperature model
twoT_x = numpy.logspace(wl_min, wl_max, n)
twoT_y = phot_y + disk_y

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
ax.errorbar(data_wl, data_flux, yerr=data_flux_err, \
             linestyle='None', marker='o', markersize=5, color='red', \
             ecolor='black', elinewidth=2, capsize=5, zorder=0.4, label='HD61005')
ax.plot(phot_x, phot_y, linestyle='--', linewidth=3, color='blue', \
         zorder=0.2, label='Blackbody fitting at visible-NIR')
ax.plot(disk_x, disk_y, linestyle=':', linewidth=3, color='green', \
         zorder=0.3, label='Blackbody fitting at mid-IR')
ax.plot(twoT_x, twoT_y, linestyle='-', linewidth=5, color='orange', \
         zorder=0.1, label='two temperature blackbody model')
ax.legend()
fig.savefig (file_output, dpi=resolution_dpi)
