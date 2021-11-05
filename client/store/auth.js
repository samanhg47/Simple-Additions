import axios from 'axios'
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
  Client: state => {
    return Axios.create({ baseURL: state.BASE_URL }).interceptors.request.use(
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
  }
}

//actions
export const actions = {
  async checkToken() {
    const token = localStorage.getItem('token')
    const res = token ? await Client.get('/login/users') : false
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
