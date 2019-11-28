

/**
 * 水平坐标系
 *
 * @class XYMidMode
 */
class XYMidMode {
    public x: number
    public y: number
    constructor(
        x: number=0,
        y: number=0
    ) {
        this.x = x;
        this.y = y;
    }
}
/**
 * 经纬度
 *
 * @class PointMidModel
 */
class PointMidModel {
    public lat: number
    public lon: number
    constructor(lat: number=0, lon: number=0) {
        this.lat = lat;
        this.lon = lon;
    }
}

export {
    XYMidMode,
    PointMidModel
}