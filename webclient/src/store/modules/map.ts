import { Commit, Dispatch } from 'vuex'
import { SET_MAP_NOW, GET_MAP_NOW } from '../types'
export interface State {
    // range:number,
    // 风场与流场需要使用的当前时间（datetime）
    current: string
    now: Date
}

// 用来存储应用状态的数据对象
const state: State = {
    // 地图中使用的指定经纬度的范围半径
    // range: 20000,
    current: '',
    now: new Date()
}

// 用来改变应用状态的函数
const mutations = {
    setcurrent(state: State, current: string) {
        state.current = current
    },
    [SET_MAP_NOW](state: State, now: Date): void {
        state.now = now
    },
    [GET_MAP_NOW](state: State): Date {
        return state.now
    }
}

// tslint:disable-next-line:typedef
const getters = {
    getCurrent(state: State) {
        return state.current
    },
    getNow: (state: State) => {
        return state.now
    }
}

// 异步调用api的函数（暂时不用）
const actions = {
    setNow({ commit }, now: Date) {
        commit(SET_MAP_NOW, now)
    },
    getNow({ commit }): Date {
        return commit(GET_MAP_NOW)
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
