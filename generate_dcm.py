import os, sys
import argparse
import numpy as np
import pydicom
from pydicom.tag import Tag
import h5py as h5
import json

# Tags for desired metadata, as defined by DICOM standards
t_sl = Tag(0x00180088) # spacing - slice
t_xy = Tag(0x00280030) # spacing - x,y
t_sd = Tag(0x0008103e) # series description
t_mod = Tag(0x00080060) # modality

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

def generate_dcm(dcm_path, h5_path, json_path):
    """Creates hdf5 and JSON from DICOMs

    :param dcm_path: path to input DICOM directory
    :param h5_path: path to output hdf5 file
    :param json_path: path to output JSON file
    """
    dcm_list = os.listdir(dcm_path)
    dcm_list.sort()
    num_dcm = len(dcm_list)
    _, xy, sp, sd, mod = extract_dcm(os.path.join(dcm_path, dcm_list[0]))
    if len(xy) is not 2:
        print("Error: Expected 2-D DICOM")
        return

    # Fill and normalize volume
    volume = np.zeros((num_dcm, xy[0], xy[1]))
    for idx, dcm_file in enumerate(dcm_list):
        im, _, sp, sd, mod = extract_dcm(os.path.join(dcm_path, dcm_file))
        volume[idx,:,:] = im
    volume = volume + np.min(volume)
    volume = volume / np.max(volume)

    # Create hdf5 dataset
    f = h5.File(h5_path, "w")
    ds = f.create_dataset("data", data=np.float32(volume))

    # Create JSON file
    json_data = dict([('pixelSpacing', sp), ('seriesDescription', sd), ('modality', mod)])
    with open(json_path, 'w') as json_file:
        json.dump(json_data, json_file)

def main(argv):
    parser = argparse.ArgumentParser(description="Convert DICOMs to hdf5", add_help=False)
    parser.add_argument("-h", "--input-hdf5", dest="h5_path", help="path to input hdf5 file")
    parser.add_argument("-d", "--input-dicom", dest="temp_path", help="path to the template DICOM directory")
    parser.add_argument("-o", "--output-dicom", dest="dcm_path", help="path to output DICOM directory")

    args = parser.parse_args()

    generate_dcm(args.h5_path, args.temp_path, args.dcm_path)

if __name__ == "__main__":
    main(sys.argv[1:])