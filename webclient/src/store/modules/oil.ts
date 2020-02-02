const state = {
    showFactor: null,
    showType: null
}

const mutations = {
    setShowFactor(state, { data }) {
        state.showFactor = data
    },

    setShowType(state, { data }) {
        state.showType = data
    }
}

const getters = {
    getShowFactor(state) {
        return state.showFactor
    },

    getShowType(state) {
        return state.showType
    }
}

export default {
    namespaced: true,
    state,
    mutations,
    getters
}
