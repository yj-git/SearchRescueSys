import axios from 'axios'
import { host } from './common'
// 后端的请求地址及端口
// export const host = host
axios.defaults.withCredentials = true
axios.defaults.headers = {}
/**
 * 根据code以及date 读取指定时刻的散点
 *
 * @param {string} code
 * @returns
 */
const loadTrackList = (code: string, targetDate: Date) => {
    const trackAvglistUrl = `${host}/rescue/track/`
    return axios.get(trackAvglistUrl, {
        params: {
            code: code,
            date: targetDate
        }
    })
}

const loadTrackAvgList = (code: string) => {
    const trackAvglistUrl = `${host}/rescue/track/avg/`
    return axios.get(trackAvglistUrl, {
        params: {
            code: code
        }
    })
}

const getTargetTimeTrackCount = (code: string, dt: Date) => {
    const countUrl = `${host}/oilspilling/times/count/`
    return axios.get(countUrl, {
        params: {
            code: code,
            date: dt
        }
    })
}

/**
 * 加载指定 code 与 date 的溢油 avg realdata
 *
 * @param {string} code
 * @param {Date} targetDate
 * @returns
 */
const loadOilSpillingAvgRealData = (code: string, targetDate: Date) => {
    const url = `${host}/oilspilling/realdata/target/`
    return axios.get(url, {
        params: {
            code: code,
            date: targetDate
        }
    })
}

/**
 * 加载溢油平均轨迹（根据:code）
 *
 * @param {string} code
 * @returns
 */
const loadOilSpillingAvgTrackList = (code: string) => {
    const url = `${host}/oilspilling/track/avg/`
    return axios.get(url, {
        params: {
            code: code
        }
    })
}
/**
 * 加载指定 code 及 对应时间 的散点 原始版本(一次性读取散点版本)
 *
 * @param {string} code
 * @param {Date} targetDate
 * @returns
 */
const loadOilScatterTrackList = (code: string, targetDate: Date) => {
    const trackAvglistUrl = `${host}/oilspilling/track/`
    return axios.get(trackAvglistUrl, {
        params: {
            code: code,
            date: targetDate
        }
    })
}

/**
 * 分页读取散点(非一次性读取散点)
 *
 * @param {string} code
 * @param {Date} targetDate
 * @param {number} pageindex
 * @param {number} pagecount
 * @returns
 */
const loadOilScatterTrackListPage = (
    code: string,
    targetDate: Date,
    pageindex: number,
    pagecount: number
) => {
    const trackAvglistUrl = `${host}/oilspilling/track/`
    return axios.get(trackAvglistUrl, {
        params: {
            code: code,
            date: targetDate,
            pageindex: pageindex,
            pagecount: pagecount
        }
    })
}
/**
 * 加载指定 code 以及 时间 对应的平均值
 *
 * @param {string} code
 * @param {Date} targetDate
 * @returns
 */
const loadOilRealData = (code: string, targetDate: Date) => {
    const oilRealDataUrl = `${host}/oilspilling/realdata/avg/`
    return axios.get(oilRealDataUrl, {
        params: {
            code: code,
            date: targetDate
        }
    })
}

/**
 * 获取指定code对应的时间范围(start,end)
 *
 * @param {string} code
 * @returns
 */
const getTargetCodeDateRange = (code: string) => {
    const tempUrl = `${host}/oilspilling/track/date/range/`
    return axios.get(tempUrl, {
        params: {
            code: code
        }
    })
}

// const loadOilAvgTargetDateRealData=(code:string,targe)

export {
    loadTrackList,
    loadTrackAvgList,
    loadOilSpillingAvgTrackList,
    loadOilScatterTrackList,
    loadOilRealData,
    loadOilSpillingAvgRealData,
    getTargetCodeDateRange,
    getTargetTimeTrackCount,
    loadOilScatterTrackListPage
}
