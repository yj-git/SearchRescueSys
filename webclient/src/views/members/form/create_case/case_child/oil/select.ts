import { loadSelectByType } from '@/api/select'
import { SelectTypeEnum } from '@/enum/select'
export interface IFormOilCaseInfo {
    caseName: string
    caseDesc: string
    lat: number
    lon: number
    forecastdate: Date
    duration: number
    goodType: number
    radius: number
    nums: number
}
export interface IFormOilCaseModel {
    simulationStep: number
    consoleStep: number
    windNon: number
    currentNon: number
    optionEquationType: number
}
export interface IInitSelectFunc {
    (value: string, label: string): void
}

// export interface IInitSelectImpl{

// }
const loadSelectionByType = (type: SelectTypeEnum, func: IInitSelectFunc): void => {
    // const myself = this
    loadSelectByType(type).then((res) => {
        if (res.status === 200) {
            // console.log(res.data)
            // 找到所有失事类型的selec集合
            if (res.data.length > 0) {
                res.data.map(
                    (temp: { name: string; val: string; id: number; type_select: number }) => {
                        if (temp.type_select === type) {
                            // 此处修改为调用方法
                            // this.optionWreckType.push({ value: temp.val, label: temp.name })
                            func(temp.val, temp.name)
                        }
                    }
                )
            }
        }
    })
}

export { loadSelectionByType }
