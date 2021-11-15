import Axios from 'axios'
import bcrypt from 'bcryptjs'
// state
export const state = () => ({
  authenticated: false,
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
        const secret = bcrypt.hashSync(
          process.env.SECRET_KEY,
          bcrypt.genSaltSync(30)
        )
        console.log(secret)
        config.headers['Secret'] = secret
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
  async checkToken(store) {
    const Client = store.getters.client
    try {
      if (!store.state.authenticated) {
        const res = await Client.get('/token')
        console.log('token res', res)
        store.dispatch('aAssignAuth', res.data)
      }
      if ($nuxt._router.history.current.fullPath === '/') {
        $nuxt._router.push('/home')
      }
    } catch (err) {
      store.dispatch('error/aPassError', err, { root: true })
      if ($nuxt._router.history.current.fullPath !== '/') {
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
