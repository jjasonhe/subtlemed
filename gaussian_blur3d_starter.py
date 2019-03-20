import os
import numpy as np
import h5py as h5
from generate_hdf5_json import *
from generate_dcm import *


def gaussian_blur3d(input_3d: np.ndarray, meta_data: dict,
                    config: dict) -> np.array:
    '''Performs 3D Gaussian blur on the input volume

    :param input_3d: input volume in 3D numpy array
    :param meta_data: a dict object with the following key(s):
        'spacing': 3-tuple of floats, the pixel spacing in 3D
    :param config: a dict object with the following key(s):
        'sigma': a float indicating size of the Gaussian kernel

    :return: the blurred volume in 3D numpy array, same size as input_3d
    '''
    print('blurred')
    return input_3d

def pre_gaussian_blur3d(in_dir: str):
    '''Takes DICOM directory and produces numpy array
    :param in_dir: path to input DICOM directory
    '''
    generate_hdf5_json(in_dir, 'tmp.h5', 'tmp.txt')
    f = h5.File('tmp.h5', 'r')
    j = json.load(open('tmp.txt'))
    os.remove('tmp.h5')
    os.remove('tmp.txt')
    print(f)
    print(j)
    return f['data'].value, j

def post_gaussian_blur3d(output_3d: np.ndarray, in_dir: str, out_dir: str):
    f = h5.File('tmp.h5', 'w')
    ds = f.create_dataset("data", data=output_3d)
    f.close()
    print('generating')
    generate_dcm('tmp.h5', in_dir, out_dir)
