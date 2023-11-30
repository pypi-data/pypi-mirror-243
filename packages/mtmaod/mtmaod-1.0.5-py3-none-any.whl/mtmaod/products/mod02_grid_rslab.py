import numpy as np
from mtmaod.utils.netCDF4 import NetCDF4

from .template import SatelliteProductReader, SatelliteProductData


class MOD02Grid_Data(SatelliteProductData):
    def __init__(self, dp, isRaw:bool = False, *args, **kwargs) -> None:
        self.dp = dp
        self.isRaw = isRaw
        pass

    def infos(self):
        return NetCDF4.get_dataset_info_from_dp(self.dp)

    def scale_and_offset(self, data:np.ndarray):
        infos:dict = self.infos()
        fill_value = infos.get("FillValue")
        if isinstance(fill_value, str):
            fill_value = float(fill_value)
        data = data.astype(np.float64).data
        data[data == fill_value] = np.nan
        return data

    def __getitem__(self, *item):
        data = self.dp.__getitem__(*item)
        return self.scale_and_offset(data) if not self.isRaw else data.data


class MOD02Grid(SatelliteProductReader):
    Product_File_Time_Format = "[.]%Y%j%H%M%S[.]" # MOD021KM_L.1000.2021001040500.H26V05.000000.h5

    @staticmethod
    def open(data_file, *args, **kwargs):
        return NetCDF4.open(data_file, *args, **kwargs)

    @staticmethod
    def read(fp, dataset_name, *args, isRaw=False, **kwargs):
        dp = NetCDF4.read(fp, dataset_name, *args, **kwargs)
        return MOD02Grid_Data(dp, isRaw=isRaw)
    
    @staticmethod
    def list_datasets(fp, full:bool = False, *args, **kwargs):
        return NetCDF4.list_datasets(fp, full=full, *args, **kwargs)
