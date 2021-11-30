import { _ } from 'core-js'

// state
export const state = () => ({
  config: null,
  newAccount: false,
  currentProfile: {
    user: {},
    shelter: {}
  },
  location: {},
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
  nuxtServerInit(store, context) {
    const config = context.$config
    store.commit('passConfig', config)
  },
  wait(store, delay) {
    return new Promise(resolve => setTimeout(resolve, delay))
  },
  async cityById(id) {
    const Client = store.rootGetters['auth/client']
    const res = await Client.get(`/city/${id}`)
    return res.data
  },
  aSetLocation({ commit }, { longitude, latitude }) {
    commit('mSetLocation', { longitude, latitude })
  },
  aCurrentProfile({ commit }, profile) {
    commit('mCurrentProfile', profile)
  },
  async aAddSheltersUser(store, body) {
    const Client = store.rootGetters['auth/client']
    store.commit('mAddShelters', '...requesting')
    try {
      const shelters = await Client.post('/shelters', body)
      store.commit('mAddShelters', shelters.data)
    } catch (err) {
      store.dispatch('error/aPassError', err, { root: true })
    }
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
  passConfig(state, config) {
    state.config = config
  },
  mSetLocation(state, { longitude, latitude }) {
    state.location = {
      lng: longitude,
      lat: latitude
    }
  },
  mCurrentProfile(state, profile) {
    profile.user_name && (state.currentProfile.user = profile)
    profile.shelter_name && (state.currentProfile.shelter = profile)
  },
  mAddShelters(state, shelters) {
    state.shelters = shelters
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
