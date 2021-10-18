import { Client } from './auth'

// state
export const state = () => ({
  location: [],
  shelters: [],
  users: [],
  comments: [],
  posts: []
})

//getters
export const getters = {}

//actions
export const actions = {
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
  addShelters(state, shelters) {
    state.shelters.push({ ...shelters })
  }
}
