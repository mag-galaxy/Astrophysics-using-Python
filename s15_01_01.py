# download Gaia DR3 data of NGC 2232
import argparse
import astropy.units
import astropy.coordinates
import astroquery.simbad
import astroquery.gaia
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# Gaia query
astroquery.gaia.Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"
astroquery.gaia.Gaia.ROW_LIMIT = -1

# use argparse
descr = 'download Gaia DR3 Catalogue'
parser = argparse.ArgumentParser(description=descr)
parser.add_argument('-t', '--target', help='target name')
parser.add_argument('-o', '--output', help='output file name (.gz)')
parser.add_argument('-r', '--radius', type=float, help='radius of search in arcmin')
args = parser.parse_args ()

# get value from argument
target = args.target
file_output = args.output
radius_arcmin = args.radius
radius_deg = radius_arcmin / 60.0

# units
u_deg = astropy.units.deg
u_ha     = astropy.units.hourangle

# find target using Simbad and get its coordinate using Skycoord
result_simbad = astroquery.simbad.Simbad.query_object(target)
obj_ra = result_simbad['RA'][0]
obj_dec = result_simbad['DEC'][0]
coord = astropy.coordinates.SkyCoord(obj_ra, obj_dec, frame='icrs', unit=(u_ha, u_deg))
ra_deg = coord.ra.deg
dec_deg = coord.dec.deg
ra_hms = coord.ra.to_string(u_ha)
dec_dms = coord.dec.to_string(u_deg, alwayssign=True)

print(f"target: {target}")
print(f" RA  = {ra_hms:>14s} = {ra_deg:10.6f} deg")
print(f" Dec = {dec_dms:>14s} = {dec_deg:+10.6f} deg")

# command for doing query
table  = f"gaiadr3.gaia_source"
field  = f"*"
point  = f"POINT({ra_deg:8.4f},{dec_deg:8.4f})"
circle = f"CIRCLE(ra,dec,{radius_deg})"
query  = f"SELECT {field} from {table} WHERE 1=CONTAINS({point},{circle});"
print (f"SQL query for Gaia database:")
print (f" {query}")

# sending a job to Gaia database
job = astroquery.gaia.Gaia.launch_job_async\
      (query, dump_to_file=True, output_format="votable_gzip", output_file=file_output)
print(job)
results = job.get_results()
print(results)