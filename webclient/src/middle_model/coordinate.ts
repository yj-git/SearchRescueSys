

/**
 * 水平坐标系
 *
 * @class XYMidMode
 */
class XYMidMode {
    public x: number
    public y: number
    constructor(
        x: number,
        y: number
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
    constructor(lat: number, lon: number) {
        this.lat = lat;
        this.lon = lon;
    }
}

export {
    XYMidMode,
    PointMidModel
}