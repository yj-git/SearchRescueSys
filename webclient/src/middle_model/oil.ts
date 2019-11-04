import { XYMidMode, PointMidModel } from "./coordinate";
import fecha from "fecha";
import { ElDropdownMenu } from "element-ui/types/dropdown-menu";
import { OilEquation } from "../enum/Equation";
/**
 * 溢油 mid model
 *
 * @class OilMidModel
 */
class OilMidModel {
  public time: Date;
  public status: number;
  public code: string;
  public latlon: number[];
  public current: XYMidMode;
  public wind: XYMidMode;
  private _windVal: number;
  private _windDir: number;
  private _currentVal: number;
  private _currentDir: number;

  constructor(
    time: Date = new Date(),
    status: number = 0,
    code: string = "",
    latlon: number[] = [],
    current: XYMidMode = new XYMidMode(),
    wind: XYMidMode = new XYMidMode()
  ) {
    this.time = time;
    this.status = status;
    this.code = code;
    this.latlon = latlon;
    this.current = current;
    this.wind = wind;
  }

  /**
   *  风速
   *
   * @returns {number}
   * @memberof OilMidModel
   */
  public get windVal(): number {
    this._windVal = Number(
      Math.sqrt(Math.pow(this.wind.x, 2) + Math.pow(this.wind.y, 2)).toFixed(2)
    );
    return this._windVal;
  }

  /**
   * 风向
   *
   * @returns {number}
   * @memberof OilMidModel
   */
  public get windDir(): number {
    let arctan = Math.atan2(this.wind.y, this.wind.x);
    let dir = Number((arctan * (180 / Math.PI)).toFixed(2));
    this._windDir = dir;
    return this._windDir;
  }

  /**
   * 流速
   *
   * @readonly
   * @type {number}
   * @memberof OilMidModel
   */
  public get currentVal(): number {
    this._currentVal = Number(
      Math.sqrt(
        Math.pow(this.current.x, 2) + Math.pow(this.current.y, 2)
      ).toFixed(2)
    );
    return this._currentVal;
  }

  /**
   * 流向
   *
   * @readonly
   * @type {number}
   * @memberof OilMidModel
   */
  public get currentDir(): number {
    let arctan = Math.atan2(this.current.y, this.current.x);
    let dir = Number((arctan * (180 / Math.PI)).toFixed(2));
    this._currentDir = dir;
    return this._currentDir;
  }

  toDivHtml(): string {
    var myself = this;
    //     let htmlStr = `
    //     <div id="oil_div" class=" card mb-4 col-md-4 box-shadow">
    //     <div class="card-header">溢油数据</div>
    //     <div class="card-body">
    //       <div class="row">
    //         <div class="col-md-4">时间</div>
    //         <div class="col-md-8">2019-02-23</div>
    //       </div>
    //       <div class="row">
    //         <div class="col-md-4">中心位置</div>
    //         <div class="col-md-8">18.2,112.0</div>
    //       </div>
    //       <div class="row row_footer">
    //         <div class="typhoon_footer">
    //           <div class="columnar my_primary">
    //             <div class="main_val">5.6</div>
    //             <div class="vice_vak">风速</div>
    //           </div>
    //           <div class="columnar my_success">
    //             <div class="main_val">115</div>
    //             <div class="vice_vak">风向</div>
    //           </div>
    //           <div class="columnar my_info">
    //             <div class="main_val">5.23</div>
    //             <div class="vice_vak">流速</div>
    //           </div>
    //           <div class="columnar my_danger">
    //             <div class="main_val">65</div>
    //             <div class="vice_vak">流向</div>
    //           </div>
    //         </div>
    //       </div>
    //     </div>
    //   </div>
    //     `
    //     return htmlStr;
    var htmlStr = `
        <div class="typhoon_data_div card mb-4 col-md-4 box-shadow">
                    <div class="card-header">台风数据</div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-4">时间</div>
                            <div class="col-md-8">${fecha.format(
                              new Date(myself.time),
                              "YYYY-MM-DD HH:mm"
                            )}</div>
                        </div>
                        <div class="row">
                            <div class="col-md-4">中心位置</div>
                            <div class="col-md-8">${this.latlon}</div>
                        </div>
                        <div class="row row_footer">
                            <div class="typhoon_footer">
                                <div class="columnar">
                                    <div class="subitem_top">${this.wind}</div>
                                    <div class="subitem_foot">风速</div>
                                </div>
                                <div class="columnar">
                                    <div class="subitem_top">${
                                      this.current
                                    }</div>
                                    <div class="subitem_foot">流速</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
        `;
    return htmlStr;
  }
}
/**
 * 溢油模型参数的 mid model
 *
 * @class OilModelDetailMidModel
 */
// tslint:disable-next-line: max-classes-per-file
class OilModelDetailMidModel {
  public time: Date;
  public point: any;
  /**
   * 风偏系数
   *
   * @type {number}
   * @memberof OilModelDetailMidModel
   */
  public windFactor: number;

  public windDir: number;
  /**
   * 模拟步长
   *
   * @type {number}
   * @memberof OilModelDetailMidModel
   */
  public simulateStep: number;
  public consoleStep: number;
  /**
   * 流场不确定性
   *
   * @type {number}
   * @memberof OilModelDetailMidModel
   */
  public currentIndeterminacy: number;
  /**
   * 风场不确定性
   *
   * @type {number}
   * @memberof OilModelDetailMidModel
   */
  public windIndeterminacy: number;

  /**
   * 求解方法
   *
   * @type {OilEquation}
   * @memberof OilModelDetailMidModel
   */
  public equation: OilEquation;

  constructor(
    time: Date,
    point: any,
    windFactor: number,
    windDir: number,
    simulateStep: number,
    consoleStep: number,
    currentIndeterminacy: number,
    windIndeterminacy: number,
    equation: OilEquation
  ) {
    this.time = time;
    this.point = point;
    this.windFactor = windFactor;
    this.windDir = windDir;
    this.simulateStep = simulateStep;
    this.consoleStep = consoleStep;
    this.currentIndeterminacy = currentIndeterminacy;
    this.windIndeterminacy = windIndeterminacy;
    this.equation = equation;
  }
}
export { OilMidModel, OilModelDetailMidModel };
