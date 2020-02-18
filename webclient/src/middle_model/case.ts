import { StatueEnum } from '../enum/status'
import { AreaEnum, getAreaVal } from '@/enum/area'
import moment from 'moment'
export interface IState {
    status: StatueEnum
    nums: number
}
export interface IDaily {
    current: Date
    nums: number
}

export interface ICaseMin {
    current: Date
    name: string
    status: StatueEnum
    tag: string
    area: AreaEnum
    code: string
    rate: number
}

class StatueInfo implements IState {
    status: StatueEnum
    nums: number
    sort: number
    style: string
    icon: string
    onclick: string
    constructor(
        status: StatueEnum,
        nums: number,
        sort: number,
        icon = 'fa-edit',
        style = 'my-default',
        onclick = 'onClickDefalut'
    ) {
        this.status = status
        this.nums = nums
        this.sort = sort
        this.style = style
        this.icon = icon
        this.onclick = onclick
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

class CaseMinInfo implements ICaseMin {
    rate: number
    current: Date
    name: string
    status: StatueEnum
    tag: string
    area: AreaEnum
    code: string
    constructor(
        current: Date,
        name: string,
        code: string,
        status: StatueEnum,
        tag: string,
        rate: number,
        area: AreaEnum
    ) {
        this.current = current
        this.name = name
        this.code = code
        this.status = status
        this.tag = tag
        this.area = area
        this.rate = rate
    }

    convertDate(): string {
        // 将current输出
        return moment(this.current).format('YYYY-MM-DD')
    }
}
export { StatueInfo, CaseDailyDetail, CaseMinInfo }
