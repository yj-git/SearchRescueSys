import axios from 'axios'
import { host } from './common'
import authHeader from './auth-header'
// 后端的请求地址及端口
// export const host = host
axios.defaults.withCredentials = true
axios.defaults.headers = {}

const area = '/users'

const loadCaseListByUser = (type: number) => {
    const url = `${host}${area}/case/list/`
    return axios.get(url, {
        headers: authHeader(),
        params: {
            type: type
        }
    })
}

const loadCaseHistory = (type: number) => {
    const url = `${host}${area}/case/history/`
    return axios.get(url, {
        headers: authHeader(),
        params: {
            type: type
        }
    })
}

export { loadCaseListByUser, loadCaseHistory }
