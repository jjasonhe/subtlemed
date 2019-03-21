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

    # Calculate relative sigma values depending on pixel spacing
    sigma_x = config['sigma']/meta_data['spacing'][0]
    sigma_y = config['sigma']/meta_data['spacing'][1]
    sigma_z = config['sigma']/meta_data['spacing'][2]

    kernel_half_x = int(np.round(3*sigma_x))
    kernel_half_y = int(np.round(3*sigma_y))
    kernel_half_z = int(np.round(3*sigma_z))
    
    # Pad data in x
    pad_x = np.pad(input_3d, ((kernel_half_x,), (0,), (0,)), 'edge')
    conv_x = np.zeros_like(input_3d)
    # Create Gaussian kernel for x
    gauss_x = np.exp((-1/(2*sigma_x**2))*np.arange(-kernel_half_x, kernel_half_x+1)**2)
    gauss_x = gauss_x / np.sum(gauss_x)
    kernel_size_x = len(gauss_x)
    # Perform 1D convolutions in x
    for y in range(input_3d.shape[1]):
        for z in range(input_3d.shape[2]):
            for x in range(input_3d.shape[0]):
                conv_x[x,y,z] = np.convolve(gauss_x, pad_x[x:x+kernel_size_x,y,z], 'valid')
    # print('Done with x')

    # Pad data in y
    pad_y = np.pad(conv_x, ((0,), (kernel_half_y,), (0,)), 'edge')
    conv_y = np.zeros_like(input_3d)
    # Create Gaussian kernel for y
    gauss_y = np.exp((-1/(2*sigma_y**2))*np.arange(-kernel_half_y, kernel_half_y+1)**2)
    gauss_y = gauss_y / np.sum(gauss_y)
    kernel_size_y = len(gauss_y)
    # Perform 1D convolutions in y
    for x in range(input_3d.shape[0]):
        for z in range(input_3d.shape[2]):
            for y in range(input_3d.shape[1]):
                conv_y[x,y,z] = np.convolve(gauss_y, pad_y[x,y:y+kernel_size_y,z], 'valid')
    # print('Done with y')

    # Pad data in z
    pad_z = np.pad(conv_y, ((0,), (0,), (kernel_half_z,)), 'edge')
    output_3d = np.zeros_like(input_3d)
    # Create Gaussian kernel for z
    gauss_z = np.exp((-1/(2*sigma_z**2))*np.arange(-kernel_half_z, kernel_half_z+1)**2)
    gauss_z = gauss_z / np.sum(gauss_z)
    kernel_size_z = len(gauss_z)
    # Perform 1D convolutions in z
    for x in range(input_3d.shape[0]):
        for y in range(input_3d.shape[1]):
            for z in range(input_3d.shape[2]):
                output_3d[x,y,z] = np.convolve(gauss_z, pad_z[x,y,z:z+kernel_size_z], 'valid')
    # print('Done with z')

    return output_3d

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
    os.remove('tmp.h5')
