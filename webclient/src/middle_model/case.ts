import { StatueEnum } from '../enum/status'
export interface IState {
    status: StatueEnum
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

export { StatueInfo }
