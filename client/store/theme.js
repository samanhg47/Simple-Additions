import darkLogo from '../assets/saLogoDark.png'
import lightLogo from '../assets/saLogo.png'
//state
export const state = () => ({
  mode: true,
  light: {
    darkGreen: '#566332',
    green: '#606E38',
    medGreen: '#879b4f',
    lightGreen: '#98af58',
    secondary: 'wheat',
    color: 'black',
    input: '#96969657',
    logoShadow: '0 0 2.5vw .1vw rgba(0, 0, 0, 0.753)',
    formShadow: '0 0 3vw .1vw rgba(0, 0, 0, 0.808)'
  },
  dark: {
    darkGreen: '#171d08',
    green: '#29350c',
    medGreen: '#394712',
    lightGreen: '#4d5f1d',
    darkSecondary: 'rgb(41, 31, 10)',
    lightSecondary: 'rgb(56, 43, 15)',
    color: '#e0e0e0',
    input: '#52525257',
    logo: ''
  }
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
