import { StatueEnum } from '../enum/status'
export interface IState {
    status: StatueEnum
    nums: number
}
export interface IDaily {
    current: Date
    nums: number
}

class StatueInfo implements IState {
    status: StatueEnum
    nums: number
    sort: number
    style: string
    icon: string
    constructor(
        status: StatueEnum,
        nums: number,
        sort: number,
        icon = 'fa-edit',
        style = 'my-default'
    ) {
        this.status = status
        this.nums = nums
        this.sort = sort
        this.style = style
        this.icon = icon
    }
}
/**
 * 每日的case 数量
 *
 * @class CaseDailyDetail
 * @implements {IDaily}
 */
class CaseDailyDetail implements IDaily {
    current: Date
    nums: number
    constructor(current: Date, nums: number) {
        this.current = current
        this.nums = nums
    }
}
export { StatueInfo, CaseDailyDetail }
