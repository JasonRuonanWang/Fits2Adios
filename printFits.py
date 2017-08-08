from astropy.io import fits
import sys

hdulist = fits.open(sys.argv[1])
print hdulist[0].data


