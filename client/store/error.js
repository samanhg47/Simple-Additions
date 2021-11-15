//state
export const state = () => ({
  status: 200,
  msg: ''
})

//getters
export const getters = {}

//actions
export const actions = {
  aPassError({ commit }, err) {
    commit('mPassError', err)
  }
}

//mutations
export const mutations = {
  mPassError(state, err) {
    state.msg = err.response.data
    state.status = err.response.status
  }
}
