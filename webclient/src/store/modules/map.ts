import { Commit, Dispatch } from 'vuex'


export interface State {
  // range:number,
  // 风场与流场需要使用的当前时间（datetime）
  current: String
}

// 用来存储应用状态的数据对象
const state: State = {
  // 地图中使用的指定经纬度的范围半径
  // range: 20000,
  current: ''
}

// 用来改变应用状态的函数
const mutations = {
  current(state: State, current: string) {
    state.current = current
  }
}

// tslint:disable-next-line:typedef
const getters = {

}

// 异步调用api的函数（暂时不用）
const actions = {}

export default {
  // TODO [*] 19-03-21 暂时取消namespaced，先实现功能
  // namespaced: true,
  state,
  mutations,
  actions,
  getters
}
