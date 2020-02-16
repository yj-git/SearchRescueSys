import { SelectTypeEnum } from '../enum/select'

export interface ISelect {
    name: string
    desc: string
    id: number
    val: string
    parent: number
    type: number
}

class SelectMidModel implements ISelect {
    name: string
    desc: string
    id: number
    val: string
    parent: number
    type: number

    constructor(id: number, name: string, desc: string, val: string, parent: number, type: number) {
        this.name
        this.desc = desc
        this.id = id
        this.val = val
        this.parent = parent
        this.type = type
    }
}

export { SelectMidModel }
