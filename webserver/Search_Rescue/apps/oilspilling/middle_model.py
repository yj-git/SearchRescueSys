class StartEndDateMidModel:
    __slots__ = ['start', 'end']

    def __init__(self, start, end):
        self.start = start
        self.end = end


class OilSpillingAvgMidModelbak:
    # TODO:[*] 20-01-18 按理说在存储数据的model中加入__slots__可以节省内存，但为何写入速度会变慢？
    # __slots__ = ['code', 'status', 'point', 'time']

    def __init__(self, code, status, point, time, x_wind, y_wind, x_sea_water_velocity, y_sea_water_velocity, mass_oil,
                 mass_evaporated, mass_dispersed, oil_film_thickness, density, sea_water_temperature, water_fraction):
        self.code = code
        self.status = status
        self.point = point
        self.time = time
        self.x_wind = x_wind
        self.y_wind = y_wind
        self.x_sea_water_velocity = x_sea_water_velocity
        self.y_sea_water_velocity = y_sea_water_velocity
        self.mass_oil = mass_oil
        self.mass_evaporated = mass_evaporated
        self.mass_dispersed = mass_dispersed
        self.oil_film_thickness = oil_film_thickness
        self.density = density
        self.sea_water_temperature = sea_water_temperature
        self.water_fraction = water_fraction


class OilSpillingAvgMidModel:
    # TODO:[*] 20-01-18 按理说在存储数据的model中加入__slots__可以节省内存，但为何写入速度会变慢？
    # __slots__ = ['code', 'status', 'point', 'time']

    def __init__(self, code, status, point, time):
        self.code = code
        self.status = status
        self.point = point
        self.time = time
