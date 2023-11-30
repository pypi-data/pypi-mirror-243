import numpy as np
from mtmaod.utils.pyhdf import PyHDF, SDS

from .template import SatelliteProductReader, SatelliteProductData


class MOD04_Data(SatelliteProductData):
    def __init__(self, dp:SDS, isRaw:bool = False, *args, **kwargs) -> None:
        self.dp = dp
        self.isRaw = isRaw
        pass

    def scale_and_offset(self, data:np.ndarray):
        infos:dict = self.infos()
        scale_factor = MOD04_Data.value_set_decimal(infos.get("scale_factor", 1), decimal=8)
        add_offset = MOD04_Data.value_set_decimal(infos.get("add_offset", 0), decimal=8)
        fill_value = infos.get("_FillValue")
        data = data.astype(np.float64)
        data[data == fill_value] = np.nan
        return data * scale_factor + add_offset

    def infos(self):
        return PyHDF.get_dataset_info_from_dp(self.dp)

    def __getitem__(self, *item):
        data = self.dp.__getitem__(*item)
        return self.scale_and_offset(data) if not self.isRaw else data


class MOD04(SatelliteProductReader):
    Product_File_Time_Format = "[.]A%Y%j[.]%H%M[.]"
    Band_Latitude = "Latitude"
    Band_Longitude = "Longitude"

    @staticmethod
    def open(data_file, *args, **kwargs):
        return PyHDF.open(data_file, *args, **kwargs)

    @staticmethod
    def read(fp, dataset_name, *args, isRaw=False, **kwargs):
        dp = PyHDF.read(fp, dataset_name, *args, **kwargs)
        return MOD04_Data(dp, isRaw=isRaw)
    
    @staticmethod
    def list_datasets(fp, full:bool = False, *args, **kwargs):
        return PyHDF.list_datasets(fp, full=full, *args, **kwargs)
