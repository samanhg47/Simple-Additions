<<<<<<< HEAD
import { Client } from './auth'

// state
export const state = () => ({
  location: [],
  shelters: [],
  users: [],
  comments: [],
  posts: []
=======
// state
export const state = () => ({
  Authorized: false,
  User: {},
  Shelters: [],
  Users: [],
  Comments: [],
  Posts: []
>>>>>>> 88a071ce2c2ae03ecfbcc15b3d2dffaa6f34edbe
})

//getters
export const getters = {}

//actions
<<<<<<< HEAD
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
=======
export const actions = {}

//mutations
export const mutations = {}
>>>>>>> 88a071ce2c2ae03ecfbcc15b3d2dffaa6f34edbe
