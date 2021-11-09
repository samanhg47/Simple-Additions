import { _ } from 'core-js'

// state
export const state = () => ({
  newAccount: false,
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
  wait(store, delay) {
    return new Promise(resolve => setTimeout(resolve, delay))
  },
  aCurrentUser({ commit }, user) {
    commit('mCurrentUser', user)
  },
  async aAddSheltersUser(store, proximity, coordinates) {
    body = {
      coordinates: coordinates,
      proximity: proximity
    }
    const Client = store.rootGetters['auth/client']
    const shelters = await Client.get('/shelters', body)
    store.commit('mUserAddShelters', shelters)
    return shelters
  },
  async aAddSheltersAdmin(store) {
    const Client = store.rootGetters['auth/client']
    const shelters = await Client.get('/admin/shelters')
    store.commit('mAddShelters', shelters)
  },
  async aAddStates(store) {
    const Client = store.rootGetters['auth/client']
    const states = await Client.get(`/states`)
    const state_list = []
    states.data.forEach(state => state_list.push(state.shorthand))
    store.commit('mAddStates', state_list)
  },
  async aAddCities(store, state) {
    const Client = store.rootGetters['auth/client']
    const cities = await Client.get(`/cities/${state}`)
    store.commit('mAddCities', cities.data)
  },
  aNewAccount({ commit }, bool) {
    commit('mNewAccount', bool)
  }
}

//mutations
export const mutations = {
  mCurrentUser(state, user) {
    state.currentUser = user
  },
  mAddShelters(state, shelters) {
    state.shelters.push({ ...shelters })
  },
  mAddStates(state, states) {
    state.states = states
  },
  mAddCities(state, cities) {
    state.cities = cities
  },
  mNewAccount(state, bool) {
    state.newAccount = bool
  }
}
