import os, sys
import argparse
import numpy as np
import pydicom
from pydicom.tag import Tag
from pydicom.uid import generate_uid
import h5py as h5
import json

# Tags for desired metadata, as defined by DICOM standards
t_ser = Tag(0x0020000E) # Series Instance UID
t_sop = Tag(0x00080018) # SOP Instance UID

def extract_dcm(filepath):
    """Multi-purpose 
    """
    ds = pydicom.dcmread(filepath)
    im = np.float32(ds.pixel_array)
    sl = ds[t_sl].value
    sp = ds[t_xy].value
    sp.append(sl)
    sp = list(sp)
    sd = ds[t_sd].value
    mod = ds[t_mod].value
    return im, im.shape, sp, sd, mod

def generate_dcm(h5_path, temp_path, dcm_path):
    """Creates new DICOMs from hdf5 and template DICOMs

    :param h5_path: path to input hdf5 file
    :param temp_path: path to the template DICOM directory
    :param dcm_path: path to output DICOM directory
    """
    temp_list = os.listdir('temp_path')
    temp_list.sort()

    # Open hdf5 and generate Series Instance UID
    f = h5.File(h5_path, "r")
    h5_data = f['data']
    ser = generate_uid()

    for idx, file in enumerate(temp_list):
        # Read dicom
        ds = pydicom.dcmread(os.path.join(temp_path, file))
        # Scale
        im = (h5_data[idx,:,:]-0.5)*2*np.iinfo(ds.pixel_array.dtype).max
        ds.PixelData = np.int16(im).tobytes()
        # Add Series Instance UID
        ds[t_ser].value = ser
        # Add SOP Instance UID
        ds[t_sop].value = generate_uid()
        # Save to output directory
        ds.save_as(os.path.join(dcm_path, file))
    f.close()

def main(argv):
    parser = argparse.ArgumentParser(description="Convert DICOMs to hdf5", add_help=False)
    parser.add_argument("-h", "--input-hdf5", dest="h5_path", help="path to input hdf5 file")
    parser.add_argument("-d", "--input-dicom", dest="temp_path", help="path to the template DICOM directory")
    parser.add_argument("-o", "--output-dicom", dest="dcm_path", help="path to output DICOM directory")

    args = parser.parse_args()

    generate_dcm(args.h5_path, args.temp_path, args.dcm_path)

if __name__ == "__main__":
    main(sys.argv[1:])