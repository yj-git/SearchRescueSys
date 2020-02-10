import auth from '../../api/auth'
import session from '../../api/session'
import { LOGIN_FAILURE, LOGIN_SUCCESS, SET_TOKEN, LOGIN_BEGIN, REMOVE_TOKEN } from '../types'
import { TOKEN_STORAGE_KEY } from '../constant'

const state: {
    authenticating: boolean
    error: boolean
    // Unexpected any. Specify a different type.eslint(@typescript-eslint/no-explicit-any)
    token: string
} = {
    authenticating: false,
    error: false,
    token: ''
}

const getters = {
    // 是否登录
    isAuthenticated: (state): boolean => !!state.token
}

const actions = {
    // login: (state) => {
    //     return auth
    //         .authLogin(username, password)
    //         .then(({ data }) => commit(SET_TOKEN, data.token))
    //         .then(() => commit(LOGIN_SUCCESS))
    //         .catch(() => commit(LOGIN_FAILURE))
    // }
    // 登录操作，根据 username 与 pwd 获取后台返回的jwt token
    login({ commit }, { username, password }) {
        // .then(({ data }) => commit(SET_TOKEN, data.token))

        // 此种方法可行，但是会引发一个错误，就是只能执行第一个then，之后的就不是promise了
        // var func1 = auth.authLogin(username, password).then((res) => {
        //     commit(SET_TOKEN, res.data['token'])
        //         .catch(() => commit(LOGIN_FAILURE))
        // })
        return auth
            .authLogin(username, password)
            .then((res) => {
                // 登录成功，将token写入 localStorge
                commit(SET_TOKEN, res.data['token'])
            })
            .then(() => console.log('执行login_success操作'))
            .catch(() => console.log('出现异常回滚'))

        // auth.authLogin(username, password)
        //     .then(({ data }) => commit(SET_TOKEN, data.token))
        //     .then((res) => {
        //         commit(LOGIN_SUCCESS)
        //         console.log(res)
        //     })
        //     .catch(() => commit(LOGIN_FAILURE))
    },

    // 进行初始化，若当前的localStorage中存在 token，则先删除，再重新赋值
    initialize({ commit }) {
        const token = localStorage.getItem(TOKEN_STORAGE_KEY)

        if (token) {
            commit(REMOVE_TOKEN)
        }
        if (token) {
            commit(SET_TOKEN, token)
        }
    }
}

const mutations = {
    [LOGIN_BEGIN](state): void {
        state.authenticating = true
        state.error = false
    },
    [LOGIN_FAILURE](state): void {
        state.authenticating = false
        state.error = false
    },
    // 为 localStorage赋值token
    [SET_TOKEN](state, token): void {
        localStorage.setItem(TOKEN_STORAGE_KEY, token)
        session.defaults.headers.Authorization = `Token ${token}`
        state.token = token
    },
    [REMOVE_TOKEN](state): void {
        localStorage.removeItem(TOKEN_STORAGE_KEY)
        delete session.defaults.headers.Authorization
        state.token = null
    }
}
export default {
    // TODO [*] 19-03-21 暂时取消namespaced，先实现功能
    namespaced: true,
    state,
    mutations,
    actions,
    getters
}
