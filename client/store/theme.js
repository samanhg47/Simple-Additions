//state
export const state = () => ({
  mode: true,
  light: {
    darkGreen: '#566332',
    green: '#606E38',
    medGreen: '#879b4f',
    lightGreen: '#98af58',
    darkSecondary: 'rgb(235, 207, 155)',
    lightSecondary: 'rgb(248, 228, 190)',
    color: 'black',
    input: '#96969657',
    shadow: '0 0 3vw .1vw rgba(0, 0, 0, 0.808)',
    lightOpacity: 1,
    lightZindex: 3,
    lightPosition: 'relative',
    darkOpacity: 0,
    darkZindex: 2,
    darkPosition: 'absolute'
  },
  dark: {
    darkGreen: '#171d08',
    green: '#29350c',
    medGreen: '#394712',
    lightGreen: '#4d5f1d',
    darkSecondary: 'rgb(26, 19, 5)',
    lightSecondary: 'rgb(41, 31, 10)',
    color: '#e0e0e0',
    input: '#52525257',
    shadow: '0 0 4vw .1vw rgb(0, 0, 0);',
    lightOpacity: 0,
    lightZindex: 2,
    lightPosition: 'relative',
    darkOpacity: 1,
    darkZindex: 3,
    darkPosition: 'absolute'
  }
})

//getter
export const getters = {
  theme: state => {
    const theme = state.mode ? state.light : state.dark
    return theme
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
