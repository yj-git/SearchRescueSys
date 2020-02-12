import axios from 'axios'
import { host } from './common'
import authHeader from './auth-header'
// 后端的请求地址及端口
// export const host = host
axios.defaults.withCredentials = true
axios.defaults.headers = {}

const loadCaseListByUser = () => {
    const url = `${host}/users/case/list/`
    return axios.get(url, {
        headers: authHeader()
    })
}

export { loadCaseListByUser }
