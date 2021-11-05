import axios from 'axios'
import Axios from 'axios'
// state
export const state = () => ({
  admin: false,
  authenticated: false,
  userType: true
})

//getters
export const getters = {
  Client: (state, second) => {
    return Axios.create({ baseURL: BASE_URL }).interceptors.request.use(
      config => {
        const token = localStorage.getItem('token')
        const admin = localStorage.getItem('admin')
        if (token) {
          config.headers['Authorization'] = `Bearer ${token}`
          config.headers['Admin'] = state.Admin
        }
        return config
      },
      error => Promise.reject(error)
    )
  }
}

//actions
export const actions = {
  async checkToken() {
    let auth = false
    const token = localStorage.getItem('token')
    if (token) {
      const res = await Client.get('/login/users')
    }
    // commit('assignAuth', auth)
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
    ? `${window.location.origin}`
    : 'http://localhost:5000'

// export const Client = Axios.create({ baseURL: BASE_URL }).interceptors.request.use(
//   config => {
//     const adminAuth = localStorage.getItem('Admin')
//     const token = localStorage.getItem('token')
//     if (token) {
//       config.headers['Authorization'] = `Bearer ${token}`
//       config.headers['Admin'] = adminAuth
//     }
//     return config
//   },
//   error => Promise.reject(error)
// )
