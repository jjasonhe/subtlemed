import numpy as np
from inference_pipeline_starter import *; from gaussian_blur3d_starter import *

pipe = InferencePipeline([])
job = JobEntry(name='3dblur', config={'sigma': 1.0}, preprocess=pre_gaussian_blur3d, postprocess=post_gaussian_blur3d, func=gaussian_blur3d)
pipe.register(job)

pipe.execute('3dblur', '/Users/noodles/Google Drive File Stream/My Drive/Grad/subtlemed/dicom_data/01_BreastMriNactPilot/Mr_Breast - 148579/SagittalIR_3DFGRE_3', '/Users/noodles/Google Drive File Stream/My Drive/Grad/subtlemed/ip_dir')
