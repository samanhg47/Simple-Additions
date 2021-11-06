import Axios from 'axios'
// state
export const state = () => ({
  authenticated: null,
  BASE_URL:
    process.env.NODE_ENV === 'production'
      ? `${window.location.origin}`
      : 'http://localhost:5000',
  userType: true
})

//getters
export const getters = {
  client: state => {
    const Client = Axios.create({
      baseURL: state.BASE_URL
    })
    Client.interceptors.request.use(
      config => {
        const token = localStorage.getItem('token')
        const admin = localStorage.getItem('admin')
        if (token) {
          config.headers['Authorization'] = `Bearer ${token}`
          config.headers['Admin'] = admin
        }
        return config
      },
      error => Promise.reject(error)
    )
    return Client
  }
}

//actions
export const actions = {
  async checkToken(store) {
    const token = localStorage.getItem('token')
    const res = token ? await Client.get('/login/users', token) : false
    store.dispatch('aAssignAuth', res.data)
    return store.state.authenticated
  },
  aAssignAuth({ commit }, bool) {
    commit('mAssignAuth', bool)
  }
}

//mutations
export const mutations = {
  mAssignAuth(state, bool) {
    state.authenticated = bool
  }
}
