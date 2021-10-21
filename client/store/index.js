import { Client } from './auth'

// state
export const state = () => ({
  authenticated: false,
  newAccount: true,
  currentUser: {},
  location: [],
  shelters: [],
  users: [],
  comments: [],
  posts: [],
  states: [],
  cities: []
})

//getters
export const getters = {}

//actions
export const actions = {
  async checkToken() {
    let auth = false
    const token = localStorage.getItem('token')
    if (token) {
      auth = await Client.get('/login/users')
    }
    commit('assignAuth', auth)
    return auth
  },
  async userGetShelters(proximity, coordinates) {
    body = {
      coordinates: coordinates,
      proximity: proximity
    }
    const shelters = await Client.get('/shelters', body)
    commit('addShelters', shelters)
    return shelters
  },
  async adminGetShelters() {
    const shelters = await Client.get('/admin/shelters')
    commit('addShelters', shelters)
  }
}

//mutations
export const mutations = {
  assignAuth(state, auth) {
    state.authenticated = auth
  },
  addShelters(state, shelters) {
    state.shelters.push({ ...shelters })
  },
  toggleNewAccount(state, bool) {
    state.newAccount = bool
  }
}
