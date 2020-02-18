import { SET_CASE_CODE, GET_CASE_CODE } from '../types'
import { getTargetCodeDateRange } from '@/api/api'

interface ICase {
    casecode?: string
}
const state: ICase = {
    casecode: undefined
}

const getters = {
    casecode: (state) => state.casecode
}

const actions = {
    setCaseCode({ commit }, code: string) {
        commit(SET_CASE_CODE, code)
    },
    getCode({ commit }, code: string): string {
        return commit(GET_CASE_CODE)
    }
}

const mutations = {
    [SET_CASE_CODE](state: ICase, code: string): void {
        state.casecode = code
    },
    [GET_CASE_CODE](state: ICase): string | undefined {
        return state.casecode
    }
}

export default {
    namespaced: true,
    state: state,
    mutations,
    actions,
    getters
}
