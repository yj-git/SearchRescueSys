import { Commit, Dispatch } from 'vuex'
import { SET_GEO_COVERAGEID, GET_GEO_COVERAGEID } from './../types'

export interface IGeo {
    coverageid?: number
}

const state: IGeo = {
    coverageid: undefined
}

// const getters = {
//     getCoverageID: (state: IGeo): number | undefined => {
//         return state.coverageid
//     }
// }

const getters = {
    coverageid: (state: IGeo): number | undefined => state.coverageid
}

const actions = {
    setCoverageID({ commit }, id: number): void {
        commit(SET_GEO_COVERAGEID, id)
    },
    getCoverageID({ commit }): number {
        return commit(GET_GEO_COVERAGEID)
    }
}

const mutations = {
    [SET_GEO_COVERAGEID](state: IGeo, id: number): void {
        console.log(`-> geo ->${SET_GEO_COVERAGEID}: state ${state}|id ${id}`)
        state.coverageid = id
    },
    [GET_GEO_COVERAGEID](state: IGeo): number | undefined {
        return state.coverageid
    }
}

export default {
    namespaced: true,
    state: state,
    mutations,
    actions,
    getters
}
