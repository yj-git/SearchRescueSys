
/**
 * 影响油的因素（权重）
 *
 * @enum {number}
 */
enum OilFactor {
    /**
     *油膜厚度
     */
    THICKNESS = 0,
    /**
     *油膜质量
     */
    MASS = 1
}
/**
 * 油的表示方式
 *
 * @enum {number}
 */
enum ShowType {
    /**
     * 散点
     */
    SCATTER = 0,

    /**
     * 热图
     */
    HEATMAP = 1
}
export {
    OilFactor, ShowType
}