// 用来读取下拉选项的
// TODO:[-] 20-02-16 注意此处需要与 commom/models -> SelectModel中的choice一致

/**
 *  用来读取下拉选项的
 *
 * @export
 * @enum {number}
 */
export enum SelectTypeEnum {
    /**
     * 失事类型
     */
    WRECK = 1,

    /**
     * 求解方法
     */
    EQUATION = 2
}
