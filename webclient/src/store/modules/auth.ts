import auth from '../../api/auth'
import session from '../../api/session'
import { LOGIN_FAILURE, LOGIN_SUCCESS, SET_TOKEN, LOGIN_BEGIN } from '../types'

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
    login({ commit }, { username, password }) {
        return auth
            .authLogin(username, password)
            .then(({ data }) => commit(SET_TOKEN, data.token))
            .then(() => commit(LOGIN_SUCCESS))
            .catch(() => commit(LOGIN_FAILURE))
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
