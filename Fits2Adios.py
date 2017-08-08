from mpi4py import MPI
import adios2
import numpy as np
import os
import sys
from astropy.io import fits

local_dim = [384, 2049, 2049]
global_dim = [384, 2049, 2049]
offset = [0, 0, 0]

comm = MPI.COMM_WORLD
adios = adios2.ADIOS(comm, adios2.DebugON)

bpIO = adios.DeclareIO("NPTypes")
var = bpIO.DefineVariable("image", list(global_dim), list(offset), list(local_dim))

bpFileWriter = bpIO.Open("a", adios2.OpenModeWrite)

for root, dirs, files in os.walk(sys.argv[1]):
    for i in files:
        ext = i.split('.')[-1]
        if ext == 'fits':
            hdulist = fits.open(root + '/' + i)
            print hdulist.info()
            var.SetDimensions(list(global_dim), list(offset), list(local_dim))
            bpFileWriter.Write(var, np.ascontiguousarray(hdulist[0].data, dtype=np.float32))
            bpFileWriter.Advance()

bpFileWriter.Close()


