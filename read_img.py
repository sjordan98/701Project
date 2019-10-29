'''
LINKS TO LOOK INTO
Landcover: http://www.earthdefine.com/spatialcover_landcover/california_2014/

'''
import gdal
from PIL import Image
import numpy as np
import cv2
gdal.UseExceptions()


test_to_raster = True
classified_array = 'test2.npy'      #put the test dataset in
aoi = 'planet_data/pre_ndvi.tif'    #the dataset that was trained on


creating_test = False
aoi_pre = 'planet_data/pre_donnell_ps.tif'
aoi_post = 'planet_data/post_donnell_ps.tif'
land_class = 'planet_data/donnell_classified.tif'


calculating_NDVI = False
aoi = 'planet_data/pre_ndvi.tif'





def ndvi(img):
    index = []
    red = np.array(img[2], dtype=np.float)
    NIR = np.array(img[3], dtype=np.float)
    index = (NIR - red)/(NIR + red)
    return index


def multi_to_single(array):
    combined_array = []

    for image in array:
        for band in image:
            combined_array.append(band)

    return combined_array


def array_to_raster(array, image, output_name):
    """Array > Raster
    Save a raster from a C order array.

    :param array: ndarray
    """
    dst_filename = output_name

    # You need to get those values like you did.
    x_pixels = len(array[0][0])  # number of pixels in x
    y_pixels = len(array[0])  # number of pixels in y
    wkt_projection = image.GetProjection()

    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create(
        dst_filename,
        x_pixels,
        y_pixels,
        len(array),
        gdal.GDT_Int16)

    dataset.SetGeoTransform(image.GetGeoTransform())

    dataset.SetProjection(wkt_projection)

    for i in range(len(array)):
        dataset.GetRasterBand(i+1).WriteArray(array[i])

    dataset.FlushCache()  # Write to disk.
    return "it prints"#dataset, dataset.GetRasterBand(1)  #If you need to return, remenber to return  also the dataset because the band don`t live without dataset.


def output_to_array(chance_list):
    print(chance_list.shape)
    classed_list = []
    for chances in chance_list:
        if chances[0] == chances.max():
            classed_list.append(0)
        elif chances[1] == chances.max():
            classed_list.append(1)
        elif chances[2] == chances.max():
            classed_list.append(2)
        else:
            classed_list.append(3)
    print(len(classed_list))

    width = 1122

    current_width = 0
    current_row = 0
    output_array = np.arange(len(classed_list)).reshape(1373,1123)
    print(output_array.shape)
    for pixel in classed_list:
        output_array[current_row][current_width] = pixel
        if current_width == width:
            current_width = 0
            current_row = current_row + 1

        else:
            current_width = current_width + 1

    return output_array


def zero(x):
    return x if x >= 0 else 0
zero = np.vectorize(zero)


def gaussian_blur(file):
    print(file[1000])
    blurred = cv2.GaussianBlur(file, (21,21),0)
    print(blurred[1000])
    return blurred


if test_to_raster == True:
    classed = np.load(classified_array)
    ref_image = gdal.Open(aoi, gdal.GA_ReadOnly)
    output_array = output_to_array(classed)
    print(array_to_raster([output_array], ref_image, "nnet_rgboutput.tif"))

if creating_test == True:
    ref_image = gdal.Open(aoi_pre, gdal.GA_ReadOnly)
    ref_array = ref_image.ReadAsArray()
    ref_array2 = gdal.Open(aoi_post, gdal.GA_ReadOnly).ReadAsArray()
    classified_array_zero = gdal.Open(land_class, gdal.GA_ReadOnly).ReadAsArray()
    classified_array = zero(classified_array_zero)
    output_array = multi_to_single([ref_array, ref_array2, [classified_array]])
    array_to_raster(output_array, ref_image, "nnet_rgbimages.tif")

if calculating_NDVI == True:
    ref_image = gdal.Open(aoi, gdal.GA_ReadOnly)
    image_array = ref_image.ReadAsArray()
    ndvi_array = ndvi(image_array)
    print(array_to_raster([ndvi_array], ref_image))
