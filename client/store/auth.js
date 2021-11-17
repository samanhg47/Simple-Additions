import Axios from 'axios'
import bcrypt, { genSaltSync } from 'bcryptjs'
// state
export const state = () => ({
  authenticated: false,
  BASE_URL:
    process.env.NODE_ENV === 'production'
      ? `${window.location.origin}`
      : 'http://localhost:5000',
  userType: true,
  id: ''
})

//getters
export const getters = {
  client: state => {
    const Client = Axios.create({
      baseURL: state.BASE_URL
    })
    Client.interceptors.request.use(
      async function(config) {
        const secret = bcrypt.hashSync(process.env.SECRET_KEY, genSaltSync())
        config.headers['Secret'] = secret
        config.headers['Id'] = state.id
        return config
      },
      error => Promise.reject(error)
    )
    Client.defaults.withCredentials = true
    return Client
  }
}

//actions
export const actions = {
  async checkToken(store, bool = true) {
    const Client = store.getters.client
    try {
      if (!store.state.authenticated) {
        const res = await Client.get('/token')
        const user = await Client.get(`/user/${res.data}`)
        store.dispatch('aCurrentProfile', user.data, { root: true })
        store.dispatch('aAssignAuth', true)
      }
      if ($nuxt._router.history.current.fullPath === '/') {
        $nuxt._router.push('/home')
      }
    } catch (err) {
      if (bool) {
        store.dispatch('error/aPassError', err, { root: true })
        $nuxt._router.push('/')
      }
    }
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
