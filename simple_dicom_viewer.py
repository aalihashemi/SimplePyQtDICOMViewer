


import pydicom
import os
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

# specify your image path here
image_path = "imgs"

class DicomVolumeLoader():
    def __init__(self, image_path = "imgs"):
        self.data_path = image_path
        self.sagital_imgs_num = 0
        self.axial_imgs_num = 0
        self.coronal_imgs_num = 0

    def load_dicom_series(self, path="imgs"):
        #using this source: https://github.com/pydicom/pydicom/blob/main/examples/image_processing/reslice.py
        # load the DICOM files
        files = []
        for dir_name, subdir_list, file_list in os.walk(path):
            for filename in file_list:
                if ".dcm" in filename.lower():  # check whether the file's DICOM
                    files.append(pydicom.dcmread(os.path.join(dir_name, filename)))

        print("file count: {}".format(len(files)))

        # skip files with no SliceLocation (eg scout views)
        slices = []
        skip_count = 0
        for f in files:
            if hasattr(f, 'SliceLocation'):
                slices.append(f)
            else:
                skip_count = skip_count + 1

        print("skipped, no SliceLocation: {}".format(skip_count))

        # ensure they are in the correct order
        slices = sorted(slices, key=lambda s: s.SliceLocation)

        # pixel aspects, assuming all slices are the same
        ps = slices[0].PixelSpacing
        ss = slices[0].SliceThickness
        ax_aspect = ps[1]/ps[0]
        sag_aspect = ps[1]/ss
        cor_aspect = ss/ps[0]

        # create 3D array
        print (len(slices), len(slices[0]))
        self.img_shape = list(slices[0].pixel_array.shape)
        self.img_shape.append(len(slices))
        self.img3d = np.zeros(self.img_shape)


        # fill 3D array with the images from the files
        for i, s in enumerate(slices):
            img2d = s.pixel_array
            self.img3d[:, :, i] = img2d


    def get_sagital_img(self, index):
        return cv.resize(self.img3d[:, index, :], (np.max(self.img_shape), np.max(self.img_shape)), interpolation=cv.INTER_CUBIC)

    def get_axial_img(self, index):
        return cv.resize(self.img3d[:, :, index], (np.max(self.img_shape), np.max(self.img_shape)), interpolation=cv.INTER_CUBIC)

    def get_coronal_img(self, index):
        return cv.resize(self.img3d[index, :, :], (np.max(self.img_shape), np.max(self.img_shape)), interpolation=cv.INTER_CUBIC)


    def get_number_of_axial_slices(self):
        return self.img_shape[2]
    def get_number_of_sagital_slices(self):
        return self.img_shape[1]
    def get_number_of_coronal_slices(self):
        return self.img_shape[0]

# # plot 3 orthogonal slices
# a1 = plt.subplot(2, 2, 1)
# plt.imshow()
# a1.set_aspect(ax_aspect)

# a2 = plt.subplot(2, 2, 2)
# plt.imshow(img3d[:, img_shape[1]//2, :])
# a2.set_aspect(sag_aspect)

# a3 = plt.subplot(2, 2, 3)
# plt.imshow(img3d[img_shape[0]//2, :, :].T)
# a3.set_aspect(cor_aspect)

# plt.show()
