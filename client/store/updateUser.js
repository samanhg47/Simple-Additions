import axios from 'axios'
import { BASE_URL, Client } from './auth'

// state
export const state = () => ({
  update: false
})

//getters
export const getters = {}

//actions
export const actions = {
  aToggleUpdate(store) {
    store.commit('mToggleUpdate')
  },
  async ahandleDelete(store) {
    user = store.rootState.currentUser
    res = await Client.delete()
  },
  async aHandleUpdate(store) {
    const id = store.rootState.currentUser.id
    const username = store.rootState.currentUser.user_name
    console.log()
    const res = await axios.patch(`${BASE_URL}/user/${id}`, {
      user_name: username
    })
    const home = store
    store.commit('maHandleUpdate', { username, home })
  },
  async aHandleDelete(store) {
    const id = store.rootState.currentUser.id
    const res = await axios.delete(`${BASE_URL}/user/${id}`)
    $nuxt._router.push('/')
  }
}

//mutations
export const mutations = {
  mToggleUpdate(state) {
    state.update = state.update === true ? false : true
  },
  maHandleUpdate(state, { username, home }) {
    home.rootState.currentUser.user_name = username
    state.update = false
  },
  maHandleDelete(state, { username, home }) {
    state.update = false
  }
}
