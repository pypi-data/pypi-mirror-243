import numpy as np

class SatelliteProductData:
    def __init__(self) -> None:
        pass

    def infos(self):
        pass

    @staticmethod
    def value_set_decimal(values, decimal=None):
        values = np.array(values)
        values_int = values.astype(int)
        values_decimal = np.round(values, decimal) if decimal is not None else values
        return values_int if values_int == values else values_decimal

    def __getitem__(self, *item):
        pass


class SatelliteProductReader:
    Product_File_Time_Format = None
    Band_Latitude = None
    Band_Longitude = None

    @staticmethod
    def open(data_file, *args, **kwargs):
        pass

    @staticmethod
    def read(fp, dataset_name, *args, **kwargs):
        pass

    @staticmethod
    def list_datasets(fp, full:bool = False, *args, **kwargs):
        pass