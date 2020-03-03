import { loadCaseListByUser, loadCaseHistory, loadCaseModelInfo } from '@/api/api'
import { AreaEnum, getAreaVal } from '@/enum/area'
import { StatueEnum } from '@/enum/status'
import { ICaseMin, CaseMinInfo, CaseOilModel, ICaseOilModelOptions } from '@/middle_model/case'

export class Case {
    private typeProduct: number

    // private caseList: CaseMinInfo[]
    constructor(type: number) {
        this.typeProduct = type
        // this.caseList = []
    }

    /**
     * 根据传入的type加载对应的case类型的case list
     * 注意！:此处不要通过参数直接传入list，因为是异步调用，
     * 所以方法执行完，未必执行了对list的赋值操作
     *
     * @param {CaseMinInfo[]} caselist
     * @param {number} [type]
     * @memberof Case
     */
    getCaseListByUser(type?: number) {
        const caselist: CaseMinInfo[] = []
        // const caselist: Array<CaseMinInfo> = []
        // TODO:[-] 20-02-18 注意promise.then()方法时定义在原型对象上的，
        // then方法的返回值(可选)，是一个新的promise实例，可以使用链式写法
        return loadCaseListByUser(type ? type : this.typeProduct)
            .then((res) => {
                if (res.status === 200) {
                    res.data.forEach(
                        (temp: {
                            rate: number
                            date: string
                            name: string
                            state: StatueEnum
                            tag: string
                            area: AreaEnum
                            code: string
                        }) => {
                            // const caseTemp: CaseMinInfo = new CaseMinInfo()
                            // Object.assign()
                            const tempData = new CaseMinInfo(
                                new Date(temp.date),
                                temp.name,
                                temp.code,
                                temp.state,
                                temp.tag,
                                temp.rate,
                                temp.area
                            )
                            // TODO:[*] 20-02-18 注意由后台返回的data建议使用接口声明，然后需要new成实现对象
                            caselist.push(tempData)
                        }
                    )
                }
                return caselist
            })
            .catch((res) => {
                return []
            })
        // .finally(() => {
        //     return []
        // })
    }
}

export class CaseModelInfo {
    public code: string
    constructor(code: string) {
        this.code = code
    }

    /**
     * 根据指定code获取对应的 case model
     *
     * @param {string} code
     * @returns {Promise<CaseOilModel>}
     * @memberof CaseModelInfo
     */
    getCaseModelInfo(code?: string): Promise<CaseOilModel> {
        let caseModel: CaseOilModel
        return loadCaseModelInfo(code ? code : this.code).then((res) => {
            if (res.status === 200) {
                if (res.data) {
                    caseModel = new CaseOilModel({
                        caseName: res.data.case_name,
                        caseDesc: res.data.case_desc,
                        caseCode: res.data.case_code,
                        rootPath: res.data.root_path,
                        casePath: res.data.case_path,
                        createDate: res.data.create_date,
                        forecastDate: res.data.forecast_date,
                        area: res.data.area,
                        lat: res.data.lat,
                        lon: res.data.lon,
                        radius: res.data.radius,
                        nums: res.data.nums,
                        simulationDuration: res.data.simulation_duration,
                        simulationStep: res.data.simulation_step,
                        consoleStep: res.data.console_step,
                        currentNondeterminacy: res.data.current_nondeterminacy,
                        windNondeterminacy: res.data.wind_coefficient,
                        equation: res.data.equation,
                        windCoefficient: res.data.wind_coefficient,
                        windDir: res.data.wind_dir
                    })
                }
            }
            return caseModel
        })
    }
}
