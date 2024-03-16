from astropy import constants as const
import numpy as np
mass = const.M_sun
volumn = 4/3 * np.pi * const.R_sun**3
density = mass / volumn
print(density)