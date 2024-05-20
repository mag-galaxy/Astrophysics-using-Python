import argparse
import sys
import pathlib
import datetime
import numpy.ma
import astropy.io.fits
import astropy.stats
import astropy.convolution
import photutils.background
import photutils.segmentation

# using argparse
descr = 'Source extraction and catalogue generation'
parser = argparse.ArgumentParser(description=descr)
parser.add_argument('-i', '--input-file', default='', help='input file name (fits)')
parser.add_argument('-o', '--output-file', default='', help='output file name (cat)')
parser.add_argument('-t', '--threshold', type=float, default=2.0,  help='threshold for source detection')
args = parser.parse_args()

# get value from argument
file_input = args.input_file
file_output = args.output_file
threshold_rms = args.threshold

sigma_sky = 3.0
maxiters = 10
box_size = 50
filter_size = 3
fwhm_kernel = 3.0
array_size = 5
npixels = 10
nlevels = 32
contrast = 0.001

# pathlib objects
path_input = pathlib.Path(file_input)
path_output = pathlib.Path(file_output)

if (!path_input.exists()):
    print(f'Input file "{file_input}" does not exist!!')
    sys.exit()
if (path_output.exists()):
    print(f'Output file "{file_output}" has existed!!')
    sys.exit()

# read FITS file
with astropy.io.fits.open(file_input) as hdu:
    header = hdu[0].header
    image = hdu[0].data
    if (header['NAXIS'] == 0):    # read next one
        header = hdu[1].header
        image = hdu[1].data

# sigma-clipping algorithm for removing stars
sigma_clip = astropy.stats.SigmaClip(sigma=sigma_sky, maxiters=maxiters)

# sky background estimator
skybg_estimator = photutils.background.SExtractorBackground()

# 2D sky background map
image_skybg = photutils.background.Background2D(image, box_size=(box_size, box_size), \
     filter_size=(filter_size, filter_size), sigma_clip=sigma_clip, bkg_estimator=skybg_estimator)

# sky background subtraction
image_skysub = image - image_skybg.background

detection_threshold = threshold_rms * image_skybg.background_rms

# 2D Gaussian convolution kernel
convolution_kernel = photutils.segmentation.make_2dgaussian_kernel(fwhm=fwhm_kernel, size=array_size)

# convolution
image_convolved = astropy.convolution.convolve(image_skysub, convolution_kernel)

# detecting sources
image_segmented = photutils.segmentation.detect_sources(image_convolved, detection_threshold, npixels=npixels)

# de-blending
image_deblended = photutils.segmentation.deblend_sources\
    (image_convolved, image_segmented, npixels=npixels, nlevels=nlevels, contrast=contrast, progress_bar=False)

# make catalogue
catalogue = photutils.segmentation.SourceCatalog\
    (data=image_skysub, segment_img=image_segmented, convolved_data=image_convolved)

# change catalogue to Astropy table
table_source = catalogue.to_table()

# write table into output file
astropy.io.ascii.write(table_source, file_output, format='commented_header')
