import axios from 'axios'
import { BASE_URL, Client } from './auth'

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
export const getters = {
  city_list: state => {
    const city_list = []
    state.cities.forEach(city => {
      if (!city_list.includes(city.city)) {
        city_list.push(city.city)
      }
    })
    return city_list
  },
  zipcode_list: state => {
    if (state.login.form.city.class === 'valid') {
      const zipcode_list = []
      const city = state.login.form.city.value
      state.cities.forEach(obj => {
        if (obj.city === city) {
          zipcode_list.push(obj.zipcode)
        }
      })
      return zipcode_list
    }
  }
}

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
  async userGetShelters(store, proximity, coordinates) {
    body = {
      coordinates: coordinates,
      proximity: proximity
    }
    const shelters = await Client.get('/shelters', body)
    store.commit('addShelters', shelters)
    return shelters
  },
  async adminGetShelters(store) {
    const shelters = await Client.get('/admin/shelters')
    store.commit('addShelters', shelters)
  },
  async getStates(store) {
    const states = await axios.get(`${BASE_URL}/states`)
    const state_list = []
    states.data.forEach(state => state_list.push(state.shorthand))
    store.commit('addStates', state_list)
  },
  async getCities(store, state) {
    const cities = await axios.get(`${BASE_URL}/cities/${state}`)
    store.commit('addCities', cities.data)
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
  },
  addStates(state, states) {
    state.states = states
  },
  addCities(state, cities) {
    state.cities = cities
  }
}
