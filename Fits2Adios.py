from astropy.io import fits
from mpi4py import MPI
import adios as ad
import sys
import numpy as np
import copy
import os


ad.init_noxml()
ad.set_max_buffer_size (10000);
adios_group = ad.declare_group("shore", "", ad.FLAG.YES)
local_dimension = "1,384,2049,2049"
global_dimension = "1,384,2049,2049"

s = 0

for root, dirs, files in os.walk(sys.argv[1]):
    for i in files:
        ext = i.split('.')[-1]
        if ext == 'fits':
            hdulist = fits.open(root + '/' + i)
            print hdulist.info()
            offset = "0,0,0,0"
            adios_file = ad.open("shore", "image_cube.bp", 'a')
            group_size = 10000000000
            ad.set_group_size(adios_file, group_size)
            ad.select_method(adios_group, "POSIX", "", "")
            ad.define_var(adios_group, "image", "", ad.DATATYPE.real, local_dimension, global_dimension, offset)
            ad.write(adios_file, "image", hdulist[0].data)
            s = s+1
            ad.close(adios_file)
            print

ad.finalize()


