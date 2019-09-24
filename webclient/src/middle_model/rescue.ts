import { DatePickerType } from 'element-ui/types/date-picker'
/**
 * 矢量 model
 *
 * @class VectorMidModel
 */
class VectorMidModel {
  public x: number
  public y: number
  constructor(x: number, y: number) {
    this.x = x
    this.y = y
  }
}

/**
 * 搜救散点 model
 *
 * @class RescuePointRealDataMidModel
 */
class RescuePointRealDataMidModel {
  public code: string
  public num: string
  public latlon: number[]
  public date: Date
  public current: VectorMidModel
  public wind: VectorMidModel
  constructor(
    code: string,
    num: string,
    latlon: number[],
    date: Date,
    current: VectorMidModel,
    wind: VectorMidModel
  ) {
    this.code = code
    this.num = num
    this.latlon = latlon
    this.date = date
    this.current = current
    this.wind = wind
  }
}
/**
 * 溢油散点 model
 *
 * @class OilPointRealDataMidModel
 */
class OilPointRealDataMidModel{
  public latlon:number[]
  public date:Date
  constructor(latlon:number[],date:Date){
    this.latlon=latlon;
    this.date=date
  }
}
export { VectorMidModel, RescuePointRealDataMidModel,OilPointRealDataMidModel }
