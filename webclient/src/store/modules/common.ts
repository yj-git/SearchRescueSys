import { SET_PRODUCT_TYPE, GET_PRODUCT_TYPE } from '../types'
import { CaseTypeEnum } from '@/enum/case'
// export enum ProductType {
//     oil = 0,
//     rescue = 1
// }

interface Common {
    // productType: ProductType
    productType: CaseTypeEnum
}

// const actions={

// }
const state: Common = {
    // productType: ProductType.oil
    productType: CaseTypeEnum.OIL
}
const getters = {
    productType: (state) => state.productType
}
// 使用dispatch调用
const actions = {
    setProductType({ commit }, type) {
        commit(SET_PRODUCT_TYPE, type)
    },
    // setProductType({ commit }, { type }) {
    //     commit(SET_PRODUCT_TYPE, type)
    // },
    login({ commit }, { type }) {
        console.log(type)
    }
}
// 使用commit调用
const mutations = {
    [SET_PRODUCT_TYPE](state: Common, type: CaseTypeEnum): void {
        state.productType = type
    },
    [GET_PRODUCT_TYPE](state: Common): CaseTypeEnum {
        return state.productType
    }
}

export default {
    namespaced: true,
    state: state,
    mutations,
    actions,
    getters
}
