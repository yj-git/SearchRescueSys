import Vue from 'vue'
import Vuex from 'vuex'

// 导入store/modules中的所有.ts，作为一个module引入
import oilStore from '@/store/modules/oil'
import mapStore from './modules/map'
import auth from './modules/auth'
import common from './modules/common'
import Case from './modules/case'
import geo from './modules/geo'

Vue.use(Vuex)

// export default new Vuex.Store({
//   modules
// })

export default new Vuex.Store({
    modules: {
        // oil:{
        //   namespaced:true
        // }
        oil: oilStore,
        map: mapStore,
        auth: auth,
        common: common,
        case: Case,
        geo: geo
        // oilStore
    },
    // TODO:[*] 19-11-08 此部分先注释掉
    state: {
        current: ''
    }
    // mutations: {
    //   current(state: any, current: string) {
    //     state.current = current;
    //   }
    // }
})
