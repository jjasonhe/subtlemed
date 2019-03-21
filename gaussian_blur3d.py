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
    # sz_x = np.round(config['sigma']/meta_data['spacing'][0])
    # sz_y = np.round(config['sigma']/meta_data['spacing'][1])
    # sz_z = np.round(config['sigma']/meta_data['spacing'][2])

    # gauss_kern = np.zeros((sz_x, sz_y, sz_z))

    sigma = config['sigma']
    kernel_half = int(np.round(3*sigma))

    gauss_k = np.exp((-1/(2*sigma**2))*np.arange(-kernel_half, kernel_half+1)**2)
    gauss_k = gauss_k / np.sum(gauss_k)
    kernel_size = len(gauss_k)

    pad_x = np.pad(input_3d, ((kernel_half,), (0,), (0,)), 'edge')
    conv_x = np.zeros_like(input_3d)
    for y in range(input_3d.shape[1]):
        for z in range(input_3d.shape[2]):
            for x in range(input_3d.shape[0]):
                conv_x[x,y,z] = np.convolve(gauss_k, pad_x[x:x+kernel_size,y,z], 'valid')
    # print('Done with x')

    pad_y = np.pad(conv_x, ((0,), (kernel_half,), (0,)), 'edge')
    conv_y = np.zeros_like(input_3d)
    for x in range(input_3d.shape[0]):
        for z in range(input_3d.shape[2]):
            for y in range(input_3d.shape[1]):
                conv_y[x,y,z] = np.convolve(gauss_k, pad_y[x,y:y+kernel_size,z], 'valid')
    # print('Done with y')

    pad_z = np.pad(conv_y, ((0,), (0,), (kernel_half,)), 'edge')
    output_3d = np.zeros_like(input_3d)
    for x in range(input_3d.shape[0]):
        for y in range(input_3d.shape[1]):
            for z in range(input_3d.shape[2]):
                output_3d[x,y,z] = np.convolve(gauss_k, pad_z[x,y,z:z+kernel_size], 'valid')
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
