import { loadCoverageInfo, loadGeoserverInfo } from '@/api/geo'

export interface IBaseUrlOptions {
    baseUrl: string
}
export interface ICoverageOptions {
    // baseUrl: string
    workSpace: string
    layer: string
    style: string
    // format: string
}

export interface IOptions extends IBaseUrlOptions, ICoverageOptions {
    // baseUrl?: string
}
export class Coverage {
    private defaultCoverage: IBaseUrlOptions = {
        baseUrl: 'xx'
    }
    private defaultFormat: { format: string } = {
        format: 'image/png'
    }
    private baseUrl: string
    private workSpace: string
    private layer: string
    private style: string
    private format: string
    private options: IOptions

    public constructor(options: IOptions) {
        /*
            不能将类型“{ baseUrl: string; } | 
            { workSpace: string; layer: string; style: string; format: string; baseUrl: string; }
            ”分配给类型“IOptions”。
            Type '{ baseUrl: string; }' is missing the following properties from type 'IOptions': workSpace, layer, style, formatts(2322)
        */
        this.options = {
            ...this.defaultCoverage,
            ...this.defaultFormat,
            ...options
        }

        this.baseUrl = this.options.baseUrl
        this.workSpace = this.options.workSpace
        this.layer = this.options.layer
        this.style = this.options.style
        this.format = this.options.format
    }

    /**
     *  根据 task_id 加载 对应的 :
     *  -> geo_workspaceinfo
     *  -> geo_storeinfo
     *  -> geo_layerinfo
     *
     * @param {number} taskId
     * @memberof Coverage
     */
    public loadGeoLayer(taskId: number): void {
        // loadCoverageInfo(taskId).then((res) => {
        //     console.log(res)
        // })
        // loadGeoserverInfo().then((res) => {
        //     console.log(res)
        // })
        console.log(taskId)
        loadCoverageInfo(taskId)
            .then(
                (res: {
                    status: number
                    data: {
                        work_space: string
                        title: string
                        store_name: string
                        layer_name: string
                        style_name: string
                    }[]
                }): void => {
                    if (res.status === 200) {
                        /* 
                        work_space: "nmefc_wind"
                        title: "current_ecs_200407"
                        store_name: "ecs_new_current_20200407"
                        layer_name: "nmefc_wind:current_ecs_200407"
                        style_name: "default"
                    */
                        if (res.data.length > 0) {
                            this.workSpace = res.data[0].work_space
                            this.layer = res.data[0].layer_name
                            this.style = res.data[0].style_name
                        }
                        console.log(res.data)
                    }
                }
            )
            .catch((err): void => {
                console.log(`|coverage.ts->loadGeoLayer|引发错误:${err}`)
            })
    }
}
