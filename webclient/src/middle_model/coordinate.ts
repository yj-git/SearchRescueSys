/**
 * 水平坐标系
 *
 * @class XYMidMode
 */
class XYMidMode {
    public x: number
    public y: number
    constructor(x = 0, y = 0) {
        this.x = x
        this.y = y
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
    constructor(lat = 0, lon = 0) {
        this.lat = lat
        this.lon = lon
    }
}

export { XYMidMode, PointMidModel }
