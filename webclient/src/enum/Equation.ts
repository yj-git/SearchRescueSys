/**
 * 溢油求解方法
 *
 * @enum {number}
 */
enum OilEquation {
    /**
     * 欧拉
     */
    Euler = 0,
    /**
     * 龙格库塔法
     */
    RungeKutta,
    /**
     * 4阶龙格库塔法
     */
    FourRungeKutta
}
export { OilEquation }
