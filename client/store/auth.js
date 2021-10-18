import axios from 'axios'
import Axios from 'axios'
// state
export const state = () => ({
  authenticated: false
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
  }
}

//mutations
export const mutations = {
  assignAuth(state, auth) {
    state.authenticated = auth
  }
}

//Server Request Auth
export const BASE_URL =
  process.env.NODE_ENV === 'production'
    ? `${window.location.origin}/api`
    : 'http://localhost:5000/api'

export const Client = Axios.create({ baseURL: BASE_URL })

Client.interceptors.request.use(
  config => {
    const adminAuth = localStorage.getItem('Admin')
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
      config.headers['Admin'] = adminAuth
    }
    return config
  },
  error => Promise.reject(error)
)

axios.defaults.withCredentials = true
