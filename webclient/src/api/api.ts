import axios from 'axios'

// 实际部署地址及端口
export const host = 'http://128.5.10.26:8000'

axios.defaults.withCredentials = true
axios.defaults.headers = {
    // 'Access-Control-Allow-Headers': 'Authorization,Origin, X-Requested-With, Content-Type, Accept,access-control-allow-methods,access-control-allow-origin',
    // 'Access-Control-Allow-Headers': 'Content-Type',
    // 'Content-Type': 'application/json;charset=UTF-8',
    // 'Content-Type': 'application/x-www-form-urlencoded',
    // 'Access-Control-Allow-Origin': '*',
    // 'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, PUT, PATCH, DELETE'
}

/**
 * 读取轨迹的平均值
 *
 * @param {string} code
 * @returns
 */
const loadTrackAvg = (code: string) => {
    let trackAvgUrl = `${host}/rescue/track/avg/`
    return axios.get(trackAvgUrl, {
        params: code
    })
}