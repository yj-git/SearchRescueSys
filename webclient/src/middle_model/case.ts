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

/**
 * 对应后台ICaseBaseModel
 *
 * @export
 * @interface ICaseBaseDescModel
 */
export interface ICaseBaseDescModel {
    caseName: string
    caseDesc: string
    caseCode: string
}

/**
 * ICaseBaseStore
 *
 * @export
 * @interface ICaseBaseStoreModel
/**
 *
 *
 * @export
 * @interface ICaseBaseStoreModel
 */
export interface ICaseBaseStoreModel {
    rootPath: string
    casePath: string
    createDate: Date
    forecastDate: Date
}

/**
 * IArea
 *
 * @export
 * @interface ICaseBaseAreaModel
 */
export interface ICaseBaseAreaModel {
    area: string
}

/**
 *
 * ICaseGeoBaseInfo
 * @export
 * @interface ICaseBaseGeoModel
 */
export interface ICaseBaseGeoModel {
    lat: number
    lon: number
}
/**
 *
 *
 * @export
 * @interface ICaseBaseModel
 */
export interface ICaseBaseModel {
    /**
     *
     *释放半径
     * @type {number}
     * @memberof ICaseBaseModel
     */
    radius: number

    /**
     *
     *释放粒子数
     * @type {number}
     * @memberof ICaseBaseModel
     */
    nums: number

    /**
     *模拟时长
     *
     * @type {number}
     * @memberof ICaseBaseModel
     */
    simulationDuration: number

    /**
     *模拟步长
     *
     * @type {number}
     * @memberof ICaseBaseModel
     */
    simulationStep: number

    /**
     *输出步长
     *
     * @type {number}
     * @memberof ICaseBaseModel
     */
    consoleStep: number

    /**
     *流场不确定性
     *
     * @type {number}
     * @memberof ICaseBaseModel
     */
    currentNondeterminacy: number

    /**
     *风场不确定性
     *
     * @type {number}
     * @memberof ICaseBaseModel
     */
    windNondeterminacy: number

    /**
     *求解方法
     *
     * @type {number}
     * @memberof ICaseBaseModel
     */
    equation: number
}

/**
 * 搜救模型 实体
 *
 * @class CaseOilModel
 * @implements {ICaseBaseDescModel}
 * @implements {ICaseBaseStoreModel}
 * @implements {ICaseBaseAreaModel}
 * @implements {ICaseBaseGeoModel}
 * @implements {ICaseBaseModel}
 */
class CaseOilModel
    implements
        ICaseBaseDescModel,
        ICaseBaseStoreModel,
        ICaseBaseAreaModel,
        ICaseBaseGeoModel,
        ICaseBaseModel {
    caseName: string
    caseDesc: string
    caseCode: string
    rootPath: string
    casePath: string
    createDate: Date
    forecastDate: Date
    area: string
    lat: number
    lon: number
    radius: number
    nums: number
    simulationDuration: number
    simulationStep: number
    consoleStep: number
    currentNondeterminacy: number
    windNondeterminacy: number
    equation: number
    constructor(
        caseName: string,
        caseDesc: string,
        caseCode: string,
        rootPath: string,
        casePath: string,
        createDate: Date,
        forecastDate: Date,
        area: string,
        lat: number,
        lon: number,
        radius: number,
        nums: number,
        simulationDuration: number,
        simulationStep: number,
        consoleStep: number,
        currentNondeterminacy: number,
        windNondeterminacy: number,
        equation: number
    ) {
        this.caseName = caseName
        this.caseDesc = caseDesc
        this.caseCode = caseCode
        this.rootPath = rootPath
        this.casePath = casePath
        this.createDate = createDate
        this.forecastDate = forecastDate
        this.area = area
        this.lat = lat
        this.lon = lon
        this.radius = radius
        this.nums = nums
        this.simulationDuration = simulationDuration
        this.simulationStep = simulationStep
        this.consoleStep = consoleStep
        this.currentNondeterminacy = currentNondeterminacy
        this.windNondeterminacy = windNondeterminacy
        this.equation = equation
    }
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

export { StatueInfo, CaseDailyDetail, CaseMinInfo, CaseOilModel }
