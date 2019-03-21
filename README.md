# subtlemed

## generate_hdf5_json:
Creates hdf5 and JSON files from a directory of DICOMs. Test in the command-line with:
`python generate_hdf5_json.py -i <directory for DICOMs> -h <desired path for hdf5 file> -j <desired path for json file>`

## generate_dcm:
Creates new DICOMs in specified directory from hdf5 file and template DICOMs. Test in command-line with:
`python generate_dcm.py -h <path to hdf5 file> -d <directory for DICOM templates> -o <directory for output DICOMs>`

## gaussian_blur3d:
Contains `gaussian_blur3d` function, as well as preprocessing and postprocessing functions. Test the blurring effect with:
`python blur_test.py`, open the hdf5 file, and view the images.

## inference_pipeline:
Defines a class to handle a registry of job processes. Test by running `python pipe_test.py` and modify as desired.
