import { getEnumVal } from './common'
export enum StatueEnum {
    CREATED = 0,
    RUNNING = 1,
    COMPLETED = 2,
    WAITTING = 3
}

const getStatueVal = (x: StatueEnum, index: number): string => {
    return getEnumVal<StatueEnum>(x, index)
}

export { getStatueVal }
