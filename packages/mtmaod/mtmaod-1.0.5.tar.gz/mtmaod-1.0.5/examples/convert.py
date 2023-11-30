from rasterio import Affine, CRS
import rasterio as rio
import numpy as np
from mtmaod.products.mod02_grid_rslab import MOD02Grid

def mod02grid_to_geotiff(src_file, dst_file, data, nodata=0):
    ds = MOD02Grid.open(src_file)
    crs = CRS.from_string(ds.ProjectionStr)
    crs_transform = Affine.from_gdal(*map(float, ds.ProjectionPara.split(",")))
    profile = {}
    np.nan_to_num(data, copy=False, nan=nodata)
    # 更新TIFF参数
    profile.update({
        "dtype": "float32",
        "width": data.shape[1], 
        "height": data.shape[2],
        "count": data.shape[0],
        "compress": "lzw",
        'nodata': nodata,
        "crs": crs,
        "transform": crs_transform
    })
    with rio.open(dst_file, "w", **profile) as ds:
        ds.write(data)
