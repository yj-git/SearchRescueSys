import axios from 'axios'

// 后端的请求地址及端口
export const host = 'http://127.0.0.1:8000'
axios.defaults.withCredentials = true
axios.defaults.headers = {}
/**
 * 根据code以及date 读取指定时刻的散点
 *
 * @param {string} code
 * @returns
 */
const loadTrackList = (code: string, targetDate: Date) => {
  let trackAvglistUrl = `${host}/rescue/track/`
  return axios.get(trackAvglistUrl, {
    params: {
      code: code,
      date: targetDate
    }
  })
}

const loadTrackAvgList = (code: string) => {
  let trackAvglistUrl = `${host}/rescue/track/avg/`
  return axios.get(trackAvglistUrl, {
    params: {
      code: code
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
  let url = `${host}/oilspilling/track/avg/`
  return axios.get(url, {
    params: {
      code: code
    }
  })
}
/**
 * 加载指定 code 及 对应时间 的散点
 *
 * @param {string} code
 * @param {Date} targetDate
 * @returns
 */
const loadOilScatterTrackList = (code: string, targetDate: Date) => {
  let trackAvglistUrl = `${host}/oilspilling/track/`
  return axios.get(trackAvglistUrl, {
    params: {
      code: code,
      date: targetDate
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
  let oilRealDataUrl = `${host}/oilspilling/realdata/avg/`
  return axios.get(oilRealDataUrl, {
    params: {
      code: code,
      date: targetDate
    }
  })
}

// const loadOilAvgTargetDateRealData=(code:string,targe)


export { loadTrackList, loadTrackAvgList, loadOilSpillingAvgTrackList, loadOilScatterTrackList,loadOilRealData }
