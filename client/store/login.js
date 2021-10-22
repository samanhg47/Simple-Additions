import axios from 'axios'
import { BASE_URL } from './auth'

//state
export const state = () => ({
  form: {
    email: {
      value: '',
      name: 'Email',
      class: 'neutral',
      type: 'email',
      for: 'Email Address',
      placeholder: 'you@youremail.com',
      visited: false,
      minLen: 10,
      msg: null
    },
    user_name: {
      value: '',
      name: 'Username',
      class: 'neutral',
      type: 'text',
      for: 'Your Username',
      placeholder: 'DoggoDaddy73',
      visited: false,
      minLen: 5,
      msg: null
    },
    password: {
      value: '',
      name: 'Password',
      class: 'neutral',
      type: 'password',
      for: 'Password',
      placeholder: '',
      visited: false,
      minLen: 10,
      msg: null
    },
    confirm: {
      value: '',
      name: 'Password Confirmation',
      class: 'neutral',
      type: 'password',
      for: 'Confirm Password',
      placeholder: '',
      visited: false,
      minLen: 10,
      msg: null
    },
    address: {
      value: '',
      name: 'Address',
      class: 'neutral',
      type: 'text',
      for: 'Accurate Address',
      placeholder: '1234 West State St.',
      visited: false,
      minLen: 5,
      msg: null
    },
    state: {
      value: '',
      class: 'neutral',
      type: 'text',
      placeholder: 'state',
      visited: false,
      msg: null
    },
    city: {
      value: '',
      class: 'neutral',
      type: 'text',
      placeholder: 'city',
      visited: false,
      msg: null
    },
    zipcode: {
      value: '',
      class: 'neutral',
      type: 'text',
      placeholder: 'zipcode',
      visited: false,
      msg: null
    },
    shelter_name: {
      value: '',
      name: 'Shelter name',
      class: 'neutral',
      type: 'text',
      for: 'Shelter Name',
      placeholder: 'Nice Shelter People Inc.',
      visited: false,
      minLen: 5,
      msg: null
    },
    phone_number: {
      value: '',
      name: 'Phone Number',
      class: 'neutral',
      type: 'text',
      for: 'Company Phone Number',
      placeholder: '(123)-456-7891',
      visited: false,
      minLen: 14,
      msg: null
    }
  },
  user: {},
  zipcodes: [],
  shelter: {},
  user_auth: true,
  registration: true
})

//getters
export const getters = {
  userForm: state => {
    const userForm = {}
    if (state.registration) {
      Object.keys(state.form).forEach(key => {
        if (['email', 'password', 'confirm', 'user_name'].includes(key)) {
          userForm[key] = state.form[key]
        }
      })
    } else if (!state.registration) {
      Object.keys(state.form).forEach(key => {
        if (['password', 'confirm', 'user_name'].includes(key)) {
          userForm[key] = state.form[key]
        }
      })
    }
    return userForm
  },
  userLocation: state => {
    const userLoc = {}
    Object.keys(state.form).forEach(key => {
      if (['state', 'city', 'zipcode'].includes(key)) {
        userLoc[key] = state.form[key]
      }
    })
    return userLoc
  },
  shelterForm: state => {
    const shelterForm = state.form
    if (state.registration) {
      Object.keys(state.form).forEach(key => {
        if (key !== 'user_name') {
          shelterForm[key] = state.form[key]
        }
      })
    } else if (!state.registration) {
      Object.keys(state.form).forEach(key => {
        if (['password', 'confirm', 'shelter_name', 'address'].includes(key)) {
          shelterForm[key] = state.form[key]
        }
      })
    }
    return shelterForm
  }
}

//actions
export const actions = {
  aToggleRegistration({ commit }) {
    commit('mToggleRegistration')
  },
  async aHandleSubmit(store) {
    const bool1 = store.state.user_auth
    const bool2 = store.state.registration
    let user = store.state.user
    if (bool1 && bool2) {
      const res = await axios.get(
        `${BASE_URL}/city/${user.state}/${user.city}/${parseInt(user.zipcode)}`
      )
      user['city_id'] = res.data.id
      if (res.status < 300) {
        delete user['city']
        delete user['state']
        delete user['zipcode']
        const res = await axios.post(`${BASE_URL}/register/users`, user)
        console.log('register', res)
        if (res.status < 200) {
          const log = await axios.post(`${BASE_URL}/login/users`, user)
          console.log(res)
          localStorage.setItem('token', res.data.token)
          user = res.data.user
        }
      }
    } else if (bool1 && !bool2) {
      const res = await axios.post(`${BASE_URL}/login/users`, user)
      user = res.data.user
    } else if (!bool1 && bool2) {
      const res = await axios.post(`${BASE_URL}/register/shelters`)
      console.log('login', res)
    } else {
    }
    const currentUser = store
    store.commit('mHandleSubmit', { user, currentUser })
    $nuxt._router.push('/home')
  },
  charCheck(store, field) {
    const charBools = []
    const acceptable = '1234567890qwertyuiopasdfghjklzxcvbnm'
    const charArr = store.state.form[field].value.split('')
    if (field === 'user_name') {
      charArr.forEach((char, i) => {
        if (acceptable.includes(char)) {
          charBools.push('t')
        } else {
          charBools.push('f')
        }
      })
    }
    if (field === 'email') {
      charArr.forEach((char, i) => {
        if (acceptable.includes(char) || char === '@' || char === '.') {
          charBools.push('t')
        } else {
          charBools.push('f')
        }
      })
    }
    if (field === 'address') {
      charArr.forEach((char, i) => {
        if (acceptable.includes(char) || char === '.') {
          charBools.push('t')
        } else {
          charBools.push('f')
        }
      })
    }
    if (field === 'phone_number') {
      charArr.forEach((char, i) => {
        if (
          acceptable.slice(0, 9).includes(char) ||
          char === '(' ||
          char === ')' ||
          char === '-'
        ) {
          charBools.push('t')
        } else {
          charBools.push('f')
        }
      })
    }
    if (field === 'state') {
      if (charArr.join('') == 'state') {
        charBools.push('f')
      } else {
        charBools.push('t')
      }
    }
    if (field === 'city') {
      if (charArr.join('') == 'city') {
        charBools.push('f')
      } else {
        charBools.push('t')
      }
    }
    if (field === 'zipcode') {
      if (charArr.join('') == 'zipcode') {
        charBools.push('f')
      } else {
        charBools.push('t')
      }
    }
    return charBools
  },
  async aCheckIfInvalid(store) {
    const charCheck = field => {
      return store.dispatch('charCheck', field)
    }
    const user_auth = store.state.user_auth
    const nameCheck = user_auth ? await charCheck('user_name') : null
    const phoneCheck = user_auth ? null : await charCheck('phone_number')
    const addressCheck = user_auth ? null : await charCheck('address')
    const emailCheck = await charCheck('email')
    const stateCheck = await charCheck('state')
    const cityCheck = await charCheck('city')
    const zipCheck = await charCheck('zipcode')
    const city_list = store.rootGetters.city_list
    store.commit('mCheckIfInvalid', {
      emailCheck,
      stateCheck,
      cityCheck,
      zipCheck,
      nameCheck,
      addressCheck,
      phoneCheck,
      city_list
    })
  },
  async aCheckIfValid(store) {
    const charCheck = field => {
      return store.dispatch('charCheck', field)
    }
    const user_auth = store.state.user_auth
    const nameCheck = user_auth ? await charCheck('user_name') : null
    const phoneCheck = user_auth ? null : await charCheck('phone_number')
    const addressCheck = user_auth ? null : await charCheck('address')
    const emailCheck = await charCheck('email')
    const stateCheck = await charCheck('state')
    const cityCheck = await charCheck('city')
    const zipCheck = await charCheck('zipcode')
    store.commit('mCheckIfValid', {
      emailCheck,
      stateCheck,
      cityCheck,
      zipCheck,
      nameCheck,
      addressCheck,
      phoneCheck
    })
  },
  aCheckLength(store, event) {
    store.commit('mCheckLength', event)
  },
  aHandleChange({ commit, dispatch }, event) {
    commit('mHandleChange', event)
    dispatch('aCheckIfValid')
    dispatch('aCheckIfInvalid')
    dispatch('aCheckLength', event)
  },
  aHandleBlur(store, event) {
    store.commit('mHandleBlur', event)
    store.dispatch('aCheckLength', event)
  }
}

//mutations
export const mutations = {
  mHandleSubmit(state, { user, currentUser }) {
    currentUser.rootState.currentUser = user
    console.log(currentUser)
  },
  mToggleRegistration(state) {
    state.registration
      ? (state.registration = false)
      : (state.registration = true)
  },
  mHandleChange(state, event) {
    let eventValue = event.target.value
    if (event.target.name === 'phone_number') {
      if (state.form[event.target.name].value.length === 1) {
        state.form[event.target.name].value = '(' + eventValue
        state.shelter[event.target.name].value = '(' + eventValue
      } else if (state.form[event.target.name].value.length === 4) {
        state.form[event.target.name].value = eventValue + ')-'
        state.shelter[event.target.name].value = eventValue + ')-'
      } else if (state.form[event.target.name].value.length === 9) {
        state.form[event.target.name].value = eventValue + '-'
        state.shelter[event.target.name].value = eventValue + '-'
      }
    } else {
      state.form[event.target.name].value = eventValue
      if (state.user_auth) {
        if (event.target.name !== 'confirm') {
          state.user[event.target.name] = eventValue
        }
      } else {
        if (event.target.name !== 'confirm') {
          state.shelter[event.target.name] = eventValue
        }
      }
    }
  },
  mHandleBlur(state, event) {
    state.form[event.target.name].visited = true
  },
  mCheckIfInvalid(
    state,
    {
      emailCheck,
      stateCheck,
      cityCheck,
      zipCheck,
      nameCheck,
      addressCheck,
      phoneCheck,
      city_list
    }
  ) {
    if (
      emailCheck.includes('f') ||
      (state.form.email.minLen < state.form.email.value.length &&
        !state.form.email.value.includes('@')) ||
      (state.form.email.minLen < state.form.email.value.length &&
        !state.form.email.value.includes('.'))
    ) {
      state.form.email.class = 'invalid'
      state.form.email.msg = 'Must Be A Valid Address'
    } else if (
      state.form.email.class !== 'valid' &&
      !state.form.zipcode.visited
    ) {
      state.form.email.class === 'neutral'
    }

    if (stateCheck.includes('f')) {
      state.form.state.class = 'invalid'
      state.form.state.msg = 'Required'
    } else if (
      state.form.state.class !== 'valid' &&
      !state.form.zipcode.visited
    ) {
      state.form.state.class === 'neutral'
    }
    if (
      cityCheck.includes('f') ||
      (city_list.length > 0 && !city_list.includes(state.form.city.value))
    ) {
      state.form.city.class = 'invalid'
      state.form.city.msg = 'Choose From Suggestions'
    } else if (
      state.form.city.class !== 'valid' &&
      !state.form.zipcode.visited
    ) {
      state.form.city.class = 'neutral'
    }
    if (zipCheck.includes('f')) {
      state.form.zipcode.class = 'invalid'
      state.form.zipcode.msg = 'Required'
    } else if (
      state.form.zipcode.class !== 'valid' &&
      !state.form.zipcode.visited
    ) {
      state.form.zipcode.class === 'neutral'
    }

    if (state.user_auth && nameCheck.includes('f')) {
      state.form.user_name.class = 'invalid'
      state.form.user_name.msg = 'Username Must Be Alphanumeric'
    } else if (
      state.user_auth &&
      state.form.user_name.class !== 'valid' &&
      !state.form.zipcode.visited
    ) {
      state.form.user_name.class === 'neutral'
    }

    if (!state.user_auth && phoneCheck.includes('f')) {
      state.form.phone_number.class = 'invalid'
      state.form.phone_number.msg = 'Phone Number Must Be Numeric'
    } else if (
      !state.user_auth &&
      state.form.phone_number.class !== 'valid' &&
      !state.form.zipcode.visited
    ) {
      state.form.phone_number.class === 'neutral'
    }

    if (!state.user_auth && addressCheck.includes('f')) {
      state.form.address.class = 'invalid'
      state.form.address.msg = 'Address Must Be Alphanumeric Besides "."'
    } else if (
      !state.user_auth &&
      state.form.user_name.class !== 'valid' &&
      !state.form.zipcode.visited
    ) {
      state.form.user_name.class === 'neutral'
    }

    if (state.form.password.value.length < state.form.confirm.value.length) {
      state.form.confirm.class = 'invalid'
      state.form.confirm.msg = 'Password Confirmation Must Match Original'
    } else if (
      state.form.confirm.class !== 'valid' &&
      !state.form.zipcode.visited
    ) {
      state.form.confirm.class === 'neutral'
    }
  },
  mCheckIfValid(
    state,
    {
      emailCheck,
      stateCheck,
      cityCheck,
      zipCheck,
      nameCheck,
      addressCheck,
      phoneCheck
    }
  ) {
    if (!emailCheck.includes('f')) {
      state.form.email.class = 'valid'
      state.form.email.msg = null
    }
    if (state.user_auth && !nameCheck.includes('f')) {
      state.form.user_name.class = 'valid'
      state.form.user_name.msg = null
    }
    if (!state.user_auth && !phoneCheck.includes('f')) {
      state.form.phone_number.class = 'valid'
      state.form.phone_number.msg = null
    }
    if (!state.user_auth && !addressCheck.includes('f')) {
      state.form.address.class = 'valid'
      state.form.address.msg = null
    }
    if (!stateCheck.includes('f')) {
      state.form.state.class = 'valid'
      state.form.state.msg = null
    }
    if (!cityCheck.includes('f')) {
      state.form.city.class = 'valid'
      state.form.city.msg = null
    }
    if (!zipCheck.includes('f')) {
      state.form.zipcode.class = 'valid'
      state.form.zipcode.msg = null
    }
    if (!state.user_auth) {
      state.form.shelter_name.class = 'valid'
      state.form.shelter_name.msg = null
    }
    state.form.password.class = 'valid'
    state.form.password.msg = null

    if (
      state.form.password.class === 'valid' &&
      state.form.confirm.value === state.form.password.value
    ) {
      state.form.confirm.class = 'valid'
      state.form.confirm.msg = null
    }
  },
  mCheckLength(state, event) {
    const cond1 =
      state.form[event.target.name].visited ||
      state.form[event.target.name].class === 'valid'
    const cond2 =
      state.form[event.target.name].minLen &&
      event.target.value.length < state.form[event.target.name].minLen
    if (cond1) {
      if (event.target.value.length > 50) {
        state.form[event.target.name].class = 'invalid'
        state.form[event.target.name].msg = `${
          state.form[event.target.name].name
        } Must Be Less Than 50 Characters Long`
      } else if (
        event.target.name === 'phone_number' &&
        event.target.value.length !== 14
      ) {
        state.form[event.target.name].class = 'invalid'
        state.form[event.target.name].msg = `${
          state.form[event.target.name].name
        } Must Be 10 Numbers`
      } else if (cond2) {
        state.form[event.target.name].class = 'invalid'
        state.form[event.target.name].msg = `${
          state.form[event.target.name].name
        } Has A ${state.form[event.target.name].minLen} Character Minimum`
      } else if (
        !state.form[event.target.name].visited &&
        state.form[event.target.name].class !== 'valid'
      ) {
        state.form[event.target.name].class === 'neutral'
      }
    }
  }
}
