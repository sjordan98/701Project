import gdal
from PIL import Image
import numpy as np
import cv2



gdal.UseExceptions()  # not required, but a good idea
image = gdal.Open('planet_data/pre_ndvi.tif', gdal.GA_ReadOnly)
ndvi_post =  gdal.Open('planet_data/post_ndvi.tif', gdal.GA_ReadOnly).ReadAsArray()
land_classed =  gdal.Open('planet_data/donnell_classified.tif', gdal.GA_ReadOnly).ReadAsArray()
ndvi_pre = image.ReadAsArray()




def ndvi(img):
    index = []
    red = np.array(img[2], dtype=np.float)
    NIR = np.array(img[3], dtype=np.float)
    index = (NIR - red)/(NIR + red)
    return index




def array_to_raster(array,ndvi_post,land_classed, image):
    """Array > Raster
    Save a raster from a C order array.

    :param array: ndarray
    """
    dst_filename = 'nnet_training.tif'

    land_classed[land_classed < 0] ='nan'
    print(land_classed)
    output_array = [array[0],ndvi_post,land_classed]

    print(output_array)

    # You need to get those values like you did.
    x_pixels = len(array[0][0])  # number of pixels in x
    y_pixels = len(array[0])  # number of pixels in y
    wkt_projection = image.GetProjection()

    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create(
        dst_filename,
        x_pixels,
        y_pixels,
        len(output_array),
        gdal.GDT_Float64)

    dataset.SetGeoTransform(image.GetGeoTransform())

    dataset.SetProjection(wkt_projection)

    for i in range(len(output_array)):
        dataset.GetRasterBand(i+1).WriteArray(output_array[i])

    dataset.FlushCache()  # Write to disk.
    return "it prints"#dataset, dataset.GetRasterBand(1)  #If you need to return, remenber to return  also the dataset because the band don`t live without dataset.




def gaussian_blur(file):
    print(file[1000])
    blurred = cv2.GaussianBlur(file, (21,21),0)
    print(blurred[1000])
    return blurred




print(array_to_raster([ndvi_pre],ndvi_post,land_classed, image))










# click Image
# caxis([-15,15])
#
# improfile
# then draw a line across the image for a profile of the topagraphy
