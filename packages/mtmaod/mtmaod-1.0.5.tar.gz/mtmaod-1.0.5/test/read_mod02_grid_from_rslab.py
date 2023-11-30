from mtmaod.products.mod02_grid_rslab import MOD02Grid

if __name__ == '__main__':
    path = r"C:\Users\imutu\Desktop\MOD021KM_L.1000.2021001040500.H26V05.000000.h5"
    with MOD02Grid.open(path) as ds:
        print(MOD02Grid.list_datasets(ds))
        d = MOD02Grid.read(ds, "/AngleData/SolarAzimuthAngle")
        dp = MOD02Grid.read(ds, "/AngleData/SolarAzimuthAngle").dp
        data = MOD02Grid.read(ds, "/AngleData/SolarAzimuthAngle")[:]
