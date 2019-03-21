import numpy as np
import h5py as h5
import json
import matplotlib.pyplot as plt
from gaussian_blur3d import *

import time

hf = h5.File('dicom_data.h5', 'r')
jf = json.load(open('dicom_meta.txt'))
input_3d = hf['data'].value
config = {'sigma': 5.0}
t0 = time.time()
output_3d = gaussian_blur3d(input_3d, jf, config)
t_blur = time.time()-t0
print(t_blur)

of = h5.File('blur_data_5.h5', 'w')
ds = of.create_dataset('data', data=output_3d)

hf.close()
of.close()
