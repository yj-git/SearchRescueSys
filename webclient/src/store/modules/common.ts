import { SET_PRODUCT_TYPE, GET_PRODUCT_TYPE } from '../types'
export enum ProductType {
    oil = 0,
    rescue = 1
}

interface Common {
    productType: ProductType
}

// const actions={

// }
const state: Common = {
    productType: ProductType.oil
}
const getters = {
    productType: (state) => state.productType
}
const mutations = {
    [SET_PRODUCT_TYPE](state: Common, type: ProductType): void {
        state.productType = type
    },
    [GET_PRODUCT_TYPE](state: Common): ProductType {
        return state.productType
    }
}

export default {
    namespaced: true,
    state: state,
    mutations,
    getters
}
