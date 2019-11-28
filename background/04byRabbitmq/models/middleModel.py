from datetime import datetime


class OilPatternMidModel:
    '''
        溢油模式的信息
    '''
    __slots__ = ['time', 'point', 'wind_coefficient', 'wind_dir', 'console_step',
                 'simulation_step', 'current_nondeterminacy', 'wind_nondeterminacy', 'equation']

    def __init__(self, time: datetime, point, wind_coefficient: float, wind_dir: float, console_step: float,
                 simulation_step: float, current_nondeterminacy: float, wind_nondeterminacy, equation: int):
        '''
            溢油模式的信息
        :param time:时间
        :param point:中心位置
        :param wind_coefficient:风偏系数
        :param wind_dir:风偏角度
        :param console_step:输出步长
        :param simulation_step:模拟步长
        :param current_nondeterminacy:流场不确定性
        :param wind_nondeterminacy:风场不确定性
        :param equation:求解方法
        '''
        self.time = time
        self.point = point
        self.wind_coefficient = wind_coefficient
        self.wind_dir = wind_dir
        self.console_step = console_step
        self.simulation_step = simulation_step
        self.current_nondeterminacy = current_nondeterminacy
        self.wind_nondeterminacy = wind_nondeterminacy
        self.equation = equation


class OilDescMidModel:
    '''
        溢油描述信息
    '''
    __slots__ = ['name', 'desc', 'point', 'timestamp', 'duration', 'range',
                 'radius', 'nums', 'quality', 'mass', 'wt']

    def __init__(self, name: str, desc: str, point: object, timestamp: datetime, duration: float, range: float,
                 radius: float, nums: int, quality: int, mass: float, wt: float):
        '''
                溢油描述信息
        :param name: 案例名称
        :param desc:案例描述
        :param point:经纬度
        :param timestamp:时间
        :param duration:模拟时长
        :param range:释放时长
        :param radius:释放半径
        :param nums:释放粒子数
        :param quality:油品
        :param mass:油量
        :param wt:水温
        '''
        self.name = name
        self.desc = desc
        self.point = point
        self.timestamp = timestamp
        self.duration = duration
        self.range = range
        self.radius = radius
        self.nums = nums
        self.quality = quality
        self.mass = mass
        self.wt = wt


class OilSearchMidModel:
    '''
        溢油搜索的请求model
    '''

    def __init__(self, pattern: OilPatternMidModel, desc: OilDescMidModel):
        self.pattern = pattern
        self.desc = desc
