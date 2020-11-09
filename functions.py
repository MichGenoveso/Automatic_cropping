from math import sqrt
from skimage.feature import blob_log
from skimage import io
import os

def _find_blob(image, blob_args={'min_sigma':100, 'max_sigma':100, 'num_sigma':1, 'threshold':.01}):
    # find the blobs
    blobs_log = blob_log(image, **blob_args)
    blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2) # Compute radii in the 3rd column

    # get the blob in the middle
    for blob in blobs_log:
        y, x, r = blob
        if 200 < x <300 and 200 < y <300:
            return y, x, r

    # if no blob is found
    return None

def _incr_margin(r, perc):
    return r*perc

def _get_crop_area(x, y, r):
    return int(x-r), int(x+r), int(y-r), int(y+r)

def crop(input_files, output_names):
    # open image
    image_list = [io.imread(fname=file) for file in input_files]

    # find blob
    image_gray = io.imread(fname=input_files[0], as_gray=True)
    y, x, r = _find_blob(image_gray)
    # increase radius
    r = _incr_margin(r, 1.20)
    # define crop area
    x1, x2, y1, y2 = _get_crop_area(x, y, r)

    # crop
    cropped_list = [image[y1:y2, x1:x2] for image in image_list]

    # save
    for image, name in zip(cropped_list, output_names):
        io.imsave(name, image)

#to make directory. if it already exists, nothing will happen. Wont overwrite.
def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)
