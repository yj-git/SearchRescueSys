import axios from 'axios'
import { host } from './common'
import authHeader from './auth-header'
// 后端的请求地址及端口
// export const host = host
axios.defaults.withCredentials = true
axios.defaults.headers = {}

import { SelectTypeEnum } from '../enum/select'

const area = '/common'

/**
 * 根据 type获取下拉框
 *
 * @param {SelectTypeEnum} type
 * @returns
 */
const loadSelectByType = (type: SelectTypeEnum, parent?: number) => {
    const url = `${host}${area}/select/`
    return axios.get(url, {
        headers: authHeader(),
        params: {
            type: type,
            parent: parent
        }
    })
}

/**
 *
 *
 * @param {number} dict
 * @param {SelectTypeEnum} [type]
 * @param {number} [parent]
 * @returns
 */
const loadSelectParentByType = (dict: number, type?: SelectTypeEnum, parent?: number) => {
    const url = `${host}${area}/select/parent/`
    return axios.get(url, {
        headers: authHeader(),
        params: {
            dict: dict,
            type: type,
            parent: parent
        }
    })
}

export { loadSelectByType, loadSelectParentByType }
