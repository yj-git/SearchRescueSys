import axios from 'axios'
import { host } from './common'
import authHeader from './auth-header'
// 后端的请求地址及端口
// export const host = host
axios.defaults.withCredentials = true
axios.defaults.headers = {}

import { SelectTypeEnum } from '../enum/select'

const area = '/geo'

const loadCoverageList = (typeVal: number, areaVal: number, current?: Date) => {
    const url = `${host}${area}/coverage/list/`
    return axios.get(url, {
        headers: authHeader(),
        params: {
            type: typeVal,
            area: areaVal,
            current: current
        }
    })
}

const loadCoverageInfo = (taskId: number) => {
    const url = `${host}${area}/coverage/geoinfo/`
    return axios.get(url, {
        headers: authHeader(),
        params: {
            taskid: taskId
        }
    })
}

const loadGeoserverInfo = () => {
    const url = `${host}${area}/server/list/`
    return axios.get(url, {
        headers: authHeader()
    })
}

export { loadCoverageList, loadCoverageInfo, loadGeoserverInfo }
