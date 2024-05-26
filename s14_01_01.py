import rebound

file_sim = 'sirius.bin'

# make simulation object using rebound
sim = rebound.Simulation()
sim.add(m=2.063)  # Sirius A
sim.add(m=1.018)  # Sirius B

print (sim)
sim.save_to_file(file_sim)
