import gdal



gdal.UseExceptions()  # not required, but a good idea
dataset = gdal.Open('planet_data/pre_donnell_ps.tif', gdal.GA_ReadOnly)
data = dataset.ReadAsArray()


print(data)
