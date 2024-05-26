import numpy
import rebound

file_sim = 'sirius.bin'    # input file name (bin)
file_out = 'sirius.data'   # output file name (data)

sim = rebound.Simulation(file_sim)  # read binary file
sim.move_to_com()  # move to centre of momentum frame
ps = sim.particles

# parameters for simulation
t_interval = 30.0
n_output = 1000  # number of output data

sim.integrator = 'ias15'
sim.dt = 0.1

# open output file and write result
with open (file_out, 'w') as fh:
    header = f"# year from start of simulation, Sirius A (x, y, z), Sirius B (x, y, z)\n"
    fh.write (header)

    # orbital integration
    for i in range(n_output):
        # time
        t = t_interval * i
        t_yr = t_interval * i / (2.0 * numpy.pi)
        # orbital integration for a time step
        sim.integrate(t)
        # position of Sirius A at time t
        sirA_x = ps[0].x
        sirA_y = ps[0].y
        sirA_z = ps[0].z
        # position of Sirius B at time t
        sirB_x = ps[1].x
        sirB_y = ps[1].y
        sirB_z = ps[1].z

        record = f"{t_yr:12.6f}" \
            + f" {sirA_x:+10.6f} {sirA_y:+10.6f} {sirA_z:+10.6f}" \
            + f" {sirB_x:+10.6f} {sirB_y:+10.6f} {sirB_z:+10.6f}\n"
        fh.write(record)
