export interface IOilOptions {
  code: string;
  dt: Date;
  interval: number;
}
/**
 * 分页选项接口
 *
 * @export
 * @interface IPageOptions
 */
export interface IPageOptions {
  pageCount: number;
}

export interface IOptions extends IOilOptions, IPageOptions {}

interface Callback {
  (code: string, dt: Date, index: number, count: number): void;
}

export class Oil {
  private defaultsOil: IOilOptions = {
    code: "default",
    dt: new Date(),
    interval: 3000
  };
  private defaultsPage: IPageOptions = {
    pageCount: 200
  };

  private code: string;
  private dt: Date;
  private interval: number;
  private pageCount: number = 200;
  private options: IOptions;

  constructor(options?: IOptions) {
    this.options = {
      ...this.defaultsOil,
      ...this.defaultsPage,
      ...options
    };
    this.code = this.options.code;
    this.dt = this.options.dt;
    this.interval = this.options.interval;
    this.pageCount = this.options.pageCount;
  }

  /**
   * 定时请求
   * 根据传入的当前散点的总数/page_count => page_index
   *
   * @memberof Oil
   */
  intervalLoadTracks(count: number, func: any, options: { rate: number }) {
    // let interval = this.options?.interval;
    // 讲结果向上取整
    let pageIndex = Math.ceil(count / this.pageCount);
    // 循环进行分页请求
    // for (var index = 0; index < pageIndex; index++) {
    //   setTimeout(() => {
    //     // this.loadTracks(index, func);
    //     console.log(new Date());
    //   }, this.interval);
    // }
    // 注意不需要再写循环了，只在定时器中做计数器的加法即可

    let index_temp = 0;
    options.rate = 0;
    console.log(new Date());
    console.log(`${index_temp}`);
    this.loadTracks(index_temp, func);
    let timer = setInterval(() => {
      console.log(new Date());
      index_temp++;
      // 当前的进度(向上取整)
      options.rate = Math.ceil((100 / pageIndex) * index_temp);
      // console.log(options.rate);
      console.log(`${index_temp}`);
      this.loadTracks(index_temp, func);

      if (index_temp === pageIndex || index_temp > pageIndex) {
        clearInterval(timer);
        options.rate = 100;
        console.log("请求结束");
      }
    }, this.interval);

    // let timer = setInterval(() => {
    //   for (var index = 0; index < pageIndex; index++) {
    //     // this.loadTracks(index, func);
    //     console.log(new Date());
    //     index_temp++;
    //     if (index_temp === pageIndex) {
    //       clearInterval(timer);
    //     }
    //   }
    // }, this.interval);
    // if (index_temp == pageIndex) {
    //   clearInterval(timer);
    // }
  }

  /**
   * 根据code与dt获取指定时间的散点
   *
   * @param {number} index page_index
   * @param {Callback} func
   * @memberof Oil
   */
  loadTracks(index: number, func: Callback) {
    // let _that = this;
    // 获取每页的page_count
    let defaultCount = this.options.pageCount;
    func(this.code, this.dt, index, defaultCount);
  }
}
