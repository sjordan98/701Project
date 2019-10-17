import gdal
from PIL import Image



gdal.UseExceptions()  # not required, but a good idea
olddataset = gdal.Open('planet_data/pre_donnell_ps.tif', gdal.GA_ReadOnly)
data = olddataset.ReadAsArray()
print(data)

def array_to_raster(array, olddataset):
    """Array > Raster
    Save a raster from a C order array.

    :param array: ndarray
    """
    dst_filename = 'trial.tiff'


    # You need to get those values like you did.
    x_pixels = len(array[0][0])  # number of pixels in x
    y_pixels = len(array[0])  # number of pixels in y
    wkt_projection = olddataset.GetProjection()

    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create(
        dst_filename,
        x_pixels,
        y_pixels,
        4,
        gdal.GDT_UInt16)

    dataset.SetGeoTransform(olddataset.GetGeoTransform())

    dataset.SetProjection(wkt_projection)
    dataset.GetRasterBand(1).WriteArray(array[2])
    dataset.GetRasterBand(2).WriteArray(array[1])
    dataset.GetRasterBand(3).WriteArray(array[0])
    dataset.GetRasterBand(4).WriteArray(array[3])
    dataset.FlushCache()  # Write to disk.
    return "it prints"#dataset, dataset.GetRasterBand(1)  #If you need to return, remenber to return  also the dataset because the band don`t live without dataset.


print(array_to_raster(data, olddataset))
print(len(data))
print(len(data[0]))
print(len(data[0][0]))
