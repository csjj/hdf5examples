"""
This example shows how to read and write data to a dataset using
the shuffle filter with gzip compression.  The program first 
writes integers to a dataset using shuffle+gzip, then closes the
file.  Next, it reopens the file, reads back the data, and outputs
the types of filters and the maximum value in the dataset to the
screen.
"""
import sys

import numpy as np
import h5py

FILE = "h5ex_d_shuffle.h5"
DATASET = "DS1"

DIM0 = 32
DIM1 = 64
CHUNK0 = 4
CHUNK1 = 8

def run():

    # Initialize the data.
    wdata = np.zeros((DIM0, DIM1), dtype=np.int32)
    for i in range(DIM0):
        for j in range(DIM1):
            wdata[i][j] = i * j - j

    with h5py.File(FILE, 'w') as f:
        dset = f.create_dataset(DATASET, (DIM0, DIM1), chunks=(CHUNK0, CHUNK1),
                                compression='gzip', fletcher32=True,
                                dtype='<i4')
        dset[...] = wdata


    with h5py.File(FILE) as f:
        dset = f[DATASET]

        msg = "{0} has gzip filter enabled:  {1}"
        msg = msg.format(DATASET, dset.compression == 'gzip')
        print(msg)

        msg = "{0} has shuffle filter enabled:  {1}"
        msg = msg.format(DATASET, dset.fletcher32)
        print(msg)

        rdata = np.zeros((DIM0, DIM1))
        dset.read_direct(rdata)

        # Verify that the dataset was read correctly.
        np.testing.assert_array_equal(rdata, wdata)
        print("Maximum value in DS1 is:  %d" % rdata.max())

if __name__ == "__main__":
    run()
