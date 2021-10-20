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
  states: [
    'Alabama',
    'Alaska',
    'Arizona',
    'Arkansas',
    'California',
    'Colorado',
    'Connecticut',
    'Delaware',
    'Florida',
    'Georgia',
    'Hawaii',
    'Idaho',
    'IllinoisIndiana',
    'Iowa',
    'Kansas',
    'Kentucky',
    'Louisiana',
    'Maine',
    'Maryland',
    'Massachusetts',
    'Michigan',
    'Minnesota',
    'Mississippi',
    'Missouri',
    'MontanaNebraska',
    'Nevada',
    'New Hampshire',
    'New Jersey',
    'New Mexico',
    'New York',
    'North Carolina',
    'North Dakota',
    'Ohio',
    'Oklahoma',
    'Oregon',
    'PennsylvaniaRhode Island',
    'South Carolina',
    'South Dakota',
    'Tennessee',
    'Texas',
    'Utah',
    'Vermont',
    'Virginia',
    'Washington',
    'West Virginia',
    'Wisconsin',
    'Wyoming'
  ],
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
