//state
export const state = () => ({
  status: 200,
  msg: ''
})

//getters
export const getters = {}

//actions
export const actions = {
  aPassError({ commit }, { status, msg }) {
    commit('mPassError', { status, msg })
  }
}

//mutations
export const mutations = {
  mPassError(state, { status, msg }) {
    state.msg = msg
    state.status = status
  }
}
