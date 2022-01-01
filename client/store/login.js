import axios from 'axios'
import { pick, omit } from 'underscore'

//state
export const state = () => ({
  form: {
    shelter_name: {
      value: '',
      class: 'neutral',
      type: 'text',
      for: 'Shelter Name',
      placeholder: 'Nice Shelter People Inc.',
      visited: false,
      minLen: 5,
      msg: null
    },
    address: {
      value: '',
      class: 'neutral',
      type: 'text',
      for: 'Company Address',
      placeholder: '1234 West State St.',
      visited: false,
      minLen: 5,
      msg: null
    },
    user_name: {
      value: '',
      class: 'neutral',
      type: 'text',
      for: 'Username',
      placeholder: 'DoggoDaddy73',
      visited: false,
      minLen: 5,
      msg: null
    },
    email: {
      value: '',
      class: 'neutral',
      type: 'email',
      for: 'Email Address',
      placeholder: 'You@YourEmail.com',
      visited: false,
      minLen: 10,
      msg: null
    },
    phone_number: {
      value: '',
      class: 'neutral',
      type: 'text',
      for: 'Company Phone Number',
      placeholder: '(123)-456-7891',
      visited: false,
      minLen: 14,
      msg: 'Only Enter Numbers'
    },
    password: {
      value: '',
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
      class: 'neutral',
      type: 'password',
      for: 'Confirm Password',
      placeholder: '',
      visited: false,
      minLen: 10,
      msg: null
    },
    state: {
      value: '',
      class: 'neutral',
      type: 'text',
      visited: false,
      msg: 'Includes D.C.'
    },
    city: {
      value: '',
      class: 'neutral',
      type: 'text',
      visited: false,
      msg: null
    },
    zipcode: {
      value: '',
      class: 'neutral',
      type: 'text',
      visited: false,
      msg: null
    }
  },
  user_auth: true,
  registration: true
})

//getters
export const getters = {
  userForm: (state) => {
    const userForm = state.registration
      ? pick(state.form, ['user_name', 'email', 'password', 'confirm'])
      : pick(state.form, ['email', 'password', 'confirm'])
    return userForm
  },
  userLocation: (state) => {
    const userLoc = pick(state.form, ['state', 'city', 'zipcode'])
    return userLoc
  },
  shelterForm: (state) => {
    const shelterForm = state.registration
      ? omit(state.form, ['user_name', 'city', 'state', 'zipcode'])
      : pick(state.form, ['shelter_name', 'address', 'password', 'confirm'])
    return shelterForm
  }
}

//actions
export const actions = {
  async aLocationAutofill(store, { lng, lat }) {
    const Client = store.rootGetters['auth/client']
    const res = await Client.get(`/google/${lat}/${lng}`)
    const location = res.data.results[0].formatted_address
    const address = location.split(',')[0]
    const city = location.split(',')[1].replace(' ', '')
    const state = location.split(',')[2].replaceAll(' ', '').slice(0, 2)
    const zipcode = location.split(',')[2].replaceAll(' ', '').slice(2)
    try {
      let ret
      const lookup = await Client.get(`/city/${state}/${city}/${zipcode}`)
      if (lookup.data) {
        ret = { city, state, zipcode, address }
        store.commit('mLocationAutofill', ret)
      } else {
        ret = false
      }
      return ret
    } catch (err) {
      store.commit('mLocationAutofill', null)
      return null
    }
  },
  async aUserRegister(store, user) {
    const Client = store.rootGetters['auth/client']
    try {
      // Check/Set Location
      if (!user.city_id) {
        const res = await Client.get(
          `/city/${user.state}/${user.city}/${user.zipcode}`
        )
        user.city_id = res.data.id
        if (!store.rootState.location) {
          const latitude = res.data.latitude
          const longitude = res.data.longitude
          store.dispatch(
            'aSetLocation',
            { longitude, latitude },
            { root: true }
          )
        }
      }

      user = omit(user, ['city', 'state', 'zipcode', 'confirm'])
      // Register User
      await Client.post(`/register/users`, user)
      store.dispatch('aNewAccount', true, { root: true })
      return true
    } catch (err) {
      store.dispatch('error/aPassError', err, { root: true })
      return false
    }
  },
  async aShelterRegister(store, shelter) {
    const Client = store.rootGetters['auth/client']
    try {
      // Check/Set Location
      if (!shelter.city_id) {
        const city = await Client.get(
          `/city/${shelter.state}/${shelter.city}/${shelter.zipcode}`
        )
        shelter.city_id = city.data.id
      }
      if (!store.rootState.location.latitude) {
        const address = shelter.address.replaceAll(' ', '+')
        const city = shelter.city.replaceAll(' ', '+')
        const call = await Client.get(
          `/google/${address}/${city}/${shelter.state}`
        )
        const lat = call.data.results[0].geometry.location.lat
        const lng = call.data.results[0].geometry.location.lng
        await store.dispatch('aSetLocation', { lng, lat }, { root: true })
      }
      Object.keys(store.rootState.location).forEach((key) => {
        key == 'lat' && (shelter['latitude'] = store.rootState.location[key])
        key == 'lng' && (shelter['longitude'] = store.rootState.location[key])
      })
      shelter = omit(shelter, ['city', 'state', 'zipcode', 'confirm'])

      // Register Shelter
      await Client.post(`/register/shelters`, shelter)
      store.dispatch('aNewAccount', true, { root: true })
      return true
    } catch (err) {
      store.dispatch('error/aPassError', err, { root: true })
      return false
    }
  },
  async aUserLogin(store, user) {
    const Client = store.rootGetters['auth/client']
    try {
      const res = await Client.post(`/login/users`, user)
      return true
    } catch (err) {
      if (err.response.status === 401) {
        store.dispatch('aIncorrectPassword')
      } else {
        store.dispatch('error/aPassError', err, { root: true })
      }
      return false
    }
  },
  async aShelterLogin(store, user) {
    const Client = store.rootGetters['auth/client']
    try {
      const res = await Client.post(`/login/shelters`, user)
      store.dispatch('aCurrentProfile', res.data, { root: true })
      return true
    } catch (err) {
      if (err.response.status === 401) {
        store.dispatch('aIncorrectPassword')
      } else {
        store.dispatch('error/aPassError', err, { root: true })
      }
      return false
    }
  },
  async aHandleSubmit(store) {
    const userAuth = store.state.user_auth
    const registration = store.state.registration
    const userForm = store.getters.userForm
    const shelterForm = store.getters.shelterForm
    const userLocation = store.getters.userLocation
    let success

    // User Registration
    if (userAuth && registration) {
      const user = {}
      Object.keys(userForm).forEach((key) => (user[key] = userForm[key].value))
      Object.keys(userLocation).forEach(
        (key) => (user[key] = userLocation[key].value)
      )
      success = await store.dispatch('aUserRegister', user)
      success && (success = await store.dispatch('aUserLogin', user))

      // User Login
    } else if (userAuth && !registration) {
      let user = {}
      Object.keys(userForm).forEach((key) => (user[key] = userForm[key].value))
      success = await store.dispatch('aUserLogin', user)

      // Shelter Registration
    } else if (!userAuth && registration) {
      const shelter = {}
      Object.keys(shelterForm).forEach(
        (key) => (shelter[key] = shelterForm[key].value)
      )
      Object.keys(userLocation).forEach(
        (key) => (shelter[key] = userLocation[key].value)
      )
      success = await store.dispatch('aShelterRegister', shelter)
      success && (success = await store.dispatch('aShelterLogin', shelter))

      // Shelter Login
    } else if (!userAuth && !registration) {
      const shelter = {}
      Object.keys(shelterForm).forEach(
        (key) => (shelter[key] = shelterForm[key].value)
      )
      success = await store.dispatch('aShelterLogin', shelter)
    }
    success && store.dispatch('auth/checkToken', null, { root: true })
  },
  aIncorrectPassword(store) {
    store.commit('mIncorrectPassword')
  },
  aCheckValidity(store, event) {
    store.commit('mCheckValidity', { store, event })
  },
  aHandleChange({ commit, dispatch }, event) {
    commit('mHandleChange', event)
    dispatch('aCheckValidity', event)
  },
  aHandleBlur({ commit, dispatch }, event) {
    commit('mHandleBlur', event)
    dispatch('aCheckValidity', event)
  },
  aSetPhoneNumber({ commit }, val) {
    commit('mSetPhoneNumber', val)
  },
  aToggleRegistration({ commit }) {
    commit('mToggleRegistration')
  },
  aToggleAuth({ commit }) {
    commit('mToggleAuth')
  },
  aClearForm(store) {
    store.commit('mClearForm')
  }
}

//mutations
export const mutations = {
  mLocationAutofill(state, location) {
    if (location) {
      const keyArr = ['state', 'city', 'zipcode', 'address']
      keyArr.forEach((key) => {
        state.form[key].value = location[key]
        state.form[key].class = 'valid'
        state.form[key].msg = ''
      })
    }
  },
  mClearForm(state) {
    Object.keys(state.form).forEach((key) => {
      state.form[key].class = 'neutral'
      state.form[key].value = ''
      state.form[key].visited = false
      state.form[key].msg = null
    })
    state.user_auth = true
    state.registration = true
  },
  mIncorrectPassword(state) {
    state.form.password.class = 'invalid'
    state.form.password.msg = 'Password Incorrect. Try Again'
    state.form.confirm.class = 'invalid'
    state.form.confirm.msg = 'Password Incorrect. Try Again'
  },
  mToggleRegistration(state) {
    state.registration
      ? (state.registration = false)
      : (state.registration = true)
  },
  mToggleAuth(state) {
    state.user_auth ? (state.user_auth = false) : (state.user_auth = true)
  },
  mCheckValidity(state, { event, store }) {
    let valid = true
    const eTarget = event.target.name
    const eValue = event.target.value
    const eLen = event.target.value.length
    let minLen = state.form[eTarget].minLen
    const visited = state.form[eTarget].visited
    const userNameCheck = /^(?!.*_.*)\w+$/m
    const addressCheck = /^(?!.*_.*)[\w \.]+$/m
    const passwordCheck = /^(?!.*_.*)[@#\$%!&\w]+$/m
    const shelterNameCheck = /^(?!.*_.*)[\w \.-]+$/m
    const phoneNumberCheck = /^[(]\d{3}[)]-\d{3}-\d{4}$/m
    const specialCasesTest = /(?=address|email)/.test(eTarget)
    const emailCheck = /^[\w-]+@(?![^\d_]*[\d_][^\d_]*)\w+\.(com|org|net|co)$/m
    eTarget === 'confirm' && (minLen = state.form.password.value.length)

    const makeInvalid = (msg) => {
      state.form[eTarget].class = 'invalid'
      state.form[eTarget].msg = msg
    }

    function lengthCheck() {
      if (
        eTarget === 'phone_number' &&
        ((visited && eLen !== 14) || (!visited && eLen > 14))
      ) {
        makeInvalid(`Phone Number Must Be 10 Numbers.`)
        valid = false
      } else if (visited && minLen && eLen < minLen) {
        eTarget === 'confirm'
          ? makeInvalid('Confirmation Must Match Password')
          : makeInvalid(`Must Be At Least ${minLen} Characters Long.`)
        valid = false
        if (eTarget === 'password' && state.form.confirm.visited) {
          state.form.confirm.class = 'invalid'
          state.form.confirm.msg = 'Password Invalid'
        }
      } else if (
        (specialCasesTest && eLen > 50) ||
        (!specialCasesTest && eLen > 30)
      ) {
        const length = specialCasesTest ? 50 : 30
        makeInvalid(`Less Than ${length} Characters, Please 😊`)
        valid = false
      }
    }

    function charCheck() {
      const zipcodeCheck = () => {
        let check = store.rootGetters.zipcode_list.includes(
          parseInt(store.state.form.zipcode.value)
        )
        return check
      }
      const cityCheck = () => {
        const check = store.rootGetters.city_list.includes(
          store.state.form.city.value
        )
        return check
      }
      const stateCheck = () => {
        const check = store.rootState.states.includes(
          store.state.form.state.value
        )
        return check
      }

      if (eTarget === 'user_name') {
        valid = userNameCheck.test(eValue)
        !valid && makeInvalid('Must Be Alphanumerical')
      } else if (eTarget === 'shelter_name') {
        valid = shelterNameCheck.test(eValue)
        !valid && makeInvalid('Acceptable Characters: [A-Z, 0-9, ., -]')
      } else if (eTarget === 'phone_number') {
        valid =
          eLen === 14
            ? phoneNumberCheck.test(eValue)
            : /^[-\d\()]*$/m.test(eValue)
        !valid && makeInvalid('Enter Only Numeric Characters')
      } else if (eTarget === 'email') {
        valid = emailCheck.test(eValue)
        !valid && makeInvalid('Must Be Valid Email Address')
      } else if (eTarget === 'address') {
        valid = addressCheck.test(eValue)
        !valid && makeInvalid('Accepted Characters: [A-Z, 0-9, .]')
      } else if (eTarget === 'password') {
        valid = passwordCheck.test(eValue)
        !valid && makeInvalid('Accepted Characters: [A-Z, 0-9, !@#$%&]')
        if (state.form.confirm.value) {
          state.form.confirm.class = 'invalid'
          state.form.confirm.msg = 'Confirmation Must Match Password'
        }
      } else if (eTarget === 'confirm') {
        valid = visited
          ? state.form.password.value === eValue
          : eValue === state.form.password.value.slice(0, eLen)
        !valid && makeInvalid('Confirmation Must Match Password')
      } else if (eTarget === 'zipcode') {
        if (!eValue) {
          makeInvalid('Required')
          valid = false
        } else {
          valid = zipcodeCheck(eValue)
          if (!valid) {
            makeInvalid('Choose From Suggestions')
          }
        }
      } else if (eTarget === 'city') {
        if (!eValue) {
          makeInvalid('Required')
          valid = false
        } else {
          valid = cityCheck(eValue)
          if (!valid) {
            makeInvalid('Choose From Suggestions')
          }
        }
      } else if (eTarget === 'state') {
        if (!eValue) {
          makeInvalid('Required')
          valid = false
        } else {
          valid = stateCheck(eValue)
          if (!valid) {
            makeInvalid('Choose From Suggestions')
          }
        }
      }

      if (
        (visited && valid) ||
        (!visited && valid && !minLen) ||
        (!visited && valid && minLen && eLen >= minLen)
      ) {
        state.form[eTarget].class = 'valid'
        state.form[eTarget].msg = ''
        if (eTarget === 'password') {
          if (eValue === state.form.confirm.value) {
            state.form.confirm.class = 'valid'
            state.form.confirm.msg = ''
          } else {
            if (state.form.confirm.visited) {
              state.form.confirm.class = 'invalid'
              state.form.confirm.msg = 'Confirmation Must Match Password'
            }
          }
        }
      }
    }

    if (!visited) {
      state.form[eTarget].class = 'neutral'
      state.form[eTarget].msg = ''
    }

    lengthCheck()
    valid && charCheck()

    if (!eValue) {
      state.form[eTarget].class = 'neutral'
      state.form[eTarget].msg = ''
      state.form[eTarget].visited = false
      if (eTarget === 'password') {
        if (state.form.confirm.value) {
          state.form.confirm.class = 'invalid'
          state.form.confirm.msg = 'Confirmation Must Match Password'
        }
      }
    }
  },
  mHandleChange(state, event) {
    const eventValue = event.target.value

    state.form[event.target.name].value = eventValue

    if (event.target.name === 'state') {
      state.form.city.class = 'neutral'
      state.form.city.value = ''
      state.form.city.msg = null
      state.form.zipcode.class = 'neutral'
      state.form.zipcode.value = ''
      state.form.zipcode.msg = null
    }

    if (event.target.name === 'city') {
      state.form.zipcode.class = 'neutral'
      state.form.zipcode.value = ''
      state.form.zipcode.msg = null
    }
  },
  mHandleBlur(state, event) {
    state.form[event.target.name].visited = true
  },
  mSetPhoneNumber(state, val) {
    state.form.phone_number.value = val
  }
}
