import axios from 'axios'

import { host } from './common'
import session from './session'

const authLogin = (username: string, password: string) => {
    // TODO:[-] 20-02-07 此处需要注意由于后端使用了jwt进行认证请求地址有改变，注意
    // TODO:[*] 此处还存在一个问题提交的password是一个明文的密码，如何加密
    // const authLoginUrl = `${host}/auth/login/`
    const authLoginUrl = `${host}/users/api-token-auth/`
    return session.post(authLoginUrl, { username, password })
}

const authLoginTest = (username: string, password: string) => {
    const trackAvglistUrl = `${host}/api-token-auth/`
    return axios.post(trackAvglistUrl, { username, password })
}

// 使用default导出，在引用时可以使用别名
export default { authLogin, authLoginTest }
