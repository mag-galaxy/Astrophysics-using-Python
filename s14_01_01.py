import rebound
import numpy

file_sim = 'sirius.bin'

# calculate semimajor axis
a_arcsec = 7.4957
distance = 2.6  # pc
a_au = a_arcsec * distance

# make simulation object using rebound
sim = rebound.Simulation()
sim.add(m=2.063)  # Sirius A
sim.add(m=1.018, a = a_au, e = 0.59142)  # Sirius B

print (sim)
sim.save_to_file(file_sim)
