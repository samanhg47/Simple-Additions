//state
export const state = () => ({
  mode: true,
  light: {
    primaryDark: '#566332',
    primary: '#606E38',
    primaryMed: '#879b4f',
    primaryLight: '#98af58',
    secondary: 'wheat'
  },
  dark: {}
})

//getter
export const getter = {
  theme: state => {
    return state.mode ? state.light : state.dark
  }
}

//actions
export const actions = {
  aDarkMode({ commit }) {
    commit('mDarkMode')
  },
  aLightMode({ commit }) {
    commit('mLightMode')
  }
}

//mutations
export const mutations = {
  mDarkMode(state) {
    state.mode = false
  },
  mLightMode(state) {
    state.mode = true
  }
}
