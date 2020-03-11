class Coverage:
    '''
        coverage
    '''
    pass


CRS = {'4326': 'EPSG:4326'}


class NativeBoundingBox:

    def __init__(self, maxx: float = 150.1, minx: float = 99.9, maxy: float = 50.1, miny: float = -0.1,
                 crs: str = CRS.get('4326')):
        self.maxx = maxx
        self.minx = minx
        self.maxy = maxy
        self.miny = miny
        self.crs = crs


class LatLonBoundingBox:
    pass


class Metadata:
    pass


class Entry:
    pass


class CoverageView:
    pass


class CoverageBands:
    pass


class CoverageBand:
    def __init__(self, inputCoverageBands, definition, index, compositionType):
        self.inputCoverageBands = inputCoverageBands
        self.definition = definition
        self.compositionType = compositionType


class InputCoverageBand:
    def __init__(self, coverageNames: str):
        self.coverageNames = coverageNames
        # self.class=None


def main():
    import json
    data = {
        "coverage": {
            "metadata": {
                "entry": [
                    {
                        "@key": "cachingEnabled",
                        "$": "false"
                    }
                ]
            }
        }}
    json_data = json.dumps(data)
    pass


if __name__ == '__main__':
    main()
