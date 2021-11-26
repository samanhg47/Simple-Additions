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
  userForm: state => {
    const userForm = state.registration
      ? pick(state.form, ['user_name', 'email', 'password', 'confirm'])
      : pick(state.form, ['email', 'password', 'confirm'])
    return userForm
  },
  userLocation: state => {
    const userLoc = pick(state.form, ['state', 'city', 'zipcode'])
    return userLoc
  },
  shelterForm: state => {
    const shelterForm = state.registration
      ? omit(state.form, ['user_name', 'city', 'state', 'zipcode'])
      : pick(state.form, ['shelter_name', 'address', 'password', 'confirm'])
    return shelterForm
  }
}

//actions
export const actions = {
  async aLocationAutofill(store, { longitude, latitude }) {
    const Client = store.rootGetters['auth/client']
    const res = await axios.get(
      `https://maps.googleapis.com/maps/api/geocode/json?latlng=${latitude},${longitude}&key=${store.rootState.config.apiKey}`
    )
    const location = res.data.results[0].formatted_address
    const address = location.split(',')[0]
    const city = location.split(',')[1].replace(' ', '')
    const state = location
      .split(',')[2]
      .replaceAll(' ', '')
      .slice(0, 2)
    const zip = location
      .split(',')[2]
      .replaceAll(' ', '')
      .slice(2)
    try {
      const lookup = await Client.get(`/city/${state}/${city}/${parseInt(zip)}`)
      store.commit('mLocationAutofill', { city, state, zip, address })
      return { city, state, zip, address }
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
          `/city/${user.state}/${user.city}/${parseInt(user.zipcode)}`
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
      return false
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
          `/city/${shelter.state}/${shelter.city}/${parseInt(shelter.zipcode)}`
        )
        shelter.city_id = city.data.id
      }
      if (!store.rootState.location.latitude) {
        const address = shelter.address.replaceAll(' ', '+')
        const city = shelter.city.replaceAll(' ', '+')
        const call = await axios.get(
          `https://maps.googleapis.com/maps/api/geocode/json?address=${address},
        +${city},+${shelter.state}&key=${store.rootState.config.apiKey}`
        )
        const latitude = call.data.results[0].geometry.location.lat
        const longitude = call.data.results[0].geometry.location.lng
        store.dispatch('aSetLocation', { longitude, latitude }, { root: true })
      }
      Object.keys(store.rootState.location).forEach(
        key => (shelter[key] = store.rootState.location[key])
      )
      shelter = omit(shelter, ['city', 'state', 'zipcode', 'confirm'])

      // Register Shelter
      await Client.post(`/register/shelters`, shelter)
      store.dispatch('aNewAccount', true, { root: true })
      return false
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
      Object.keys(userForm).forEach(key => (user[key] = userForm[key].value))
      Object.keys(userLocation).forEach(
        key => (user[key] = userLocation[key].value)
      )
      await store.dispatch('aUserRegister', user)
      success = await store.dispatch('aUserLogin', user)

      // User Login
    } else if (userAuth && !registration) {
      let user = {}
      Object.keys(userForm).forEach(key => (user[key] = userForm[key].value))
      success = await store.dispatch('aUserLogin', user)

      // Shelter Registration
    } else if (!userAuth && registration) {
      const shelter = {}
      Object.keys(shelterForm).forEach(
        key => (shelter[key] = shelterForm[key].value)
      )
      Object.keys(userLocation).forEach(
        key => (shelter[key] = userLocation[key].value)
      )
      await store.dispatch('aShelterRegister', shelter)
      success = await store.dispatch('aShelterLogin', shelter)

      // Shelter Login
    } else if (!userAuth && !registration) {
      const shelter = {}
      Object.keys(shelterForm).forEach(
        key => (shelter[key] = shelterForm[key].value)
      )
      success = await store.dispatch('aShelterLogin', shelter)
    }
    success && store.dispatch('auth/checkToken', null, { root: true })
  },
  aIncorrectPassword(store) {
    store.commit('mIncorrectPassword')
  },
  charCheck(store, field) {
    const charBools = []
    const acceptable =
      '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    const charArr = Array.from(store.state.form[field].value)
    if (field === 'user_name') {
      charArr.forEach(char => {
        if (acceptable.includes(char)) {
          charBools.push('t')
        } else {
          charBools.push('f')
        }
      })
    }
    if (field === 'email') {
      charArr.forEach(char => {
        if (acceptable.includes(char) || char === '@' || char === '.') {
          charBools.push('t')
        } else {
          charBools.push('f')
        }
      })
    }
    if (field === 'address') {
      charArr.forEach(char => {
        if (acceptable.includes(char) || char === ',' || char === ' ') {
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
          if (i === 13) {
            if (
              `${parseInt(
                charArr
                  .slice(1, 4)
                  .concat(charArr.slice(6, 9).concat(charArr.slice(10)))
                  .join('')
              )}`.length === 10
            ) {
              charBools.push('t')
            } else {
              charBools.push('f')
            }
          } else {
            charBools.push('t')
          }
        } else {
          charBools.push('f')
        }
      })
    }
    if (field === 'state') {
      if (!store.state.form.state.value) {
        charBools.push('n')
      } else if (!store.rootState.states.includes(charArr.join(''))) {
        charBools.push('f')
      } else {
        charBools.push('t')
      }
    }
    if (field === 'city') {
      if (!store.state.form.city.value) {
        charBools.push('n')
      } else if (!store.rootGetters.city_list.includes(charArr.join(''))) {
        charBools.push('f')
      } else {
        charBools.push('t')
      }
    }
    if (field === 'zipcode') {
      if (!store.state.form.zipcode.value) {
        charBools.push('n')
      } else if (
        !parseInt(charArr.join('')) ||
        !store.rootGetters.zipcode_list.includes(parseInt(charArr.join('')))
      ) {
        charBools.push('f')
      } else {
        charBools.push('t')
      }
    }
    return charBools
  },
  async aCheckIfInvalid(store, event) {
    const charCheck = field => {
      return store.dispatch('charCheck', field)
    }
    const user_auth = store.state.user_auth
    const nameCheck =
      user_auth && event.target.name === 'user_name'
        ? await charCheck('user_name')
        : null
    const phoneCheck =
      !user_auth && event.target.name === 'phone_number'
        ? await charCheck('phone_number')
        : null
    const addressCheck =
      !user_auth && event.target.name === 'address'
        ? await charCheck('address')
        : null
    const emailCheck =
      event.target.name === 'email' ? await charCheck('email') : null
    const stateCheck =
      event.target.name === 'state' ? await charCheck('state') : null
    const cityCheck =
      event.target.name === 'city' ? await charCheck('city') : null
    const zipCheck =
      event.target.name === 'zipcode' ? await charCheck('zipcode') : null
    store.commit('mCheckIfInvalid', {
      emailCheck,
      stateCheck,
      cityCheck,
      zipCheck,
      nameCheck,
      addressCheck,
      phoneCheck,
      event
    })
  },
  async aCheckIfValid(store, event) {
    const charCheck = field => {
      return store.dispatch('charCheck', field)
    }
    const user_auth = store.state.user_auth
    const nameCheck =
      user_auth && event.target.name === 'user_name'
        ? await charCheck('user_name')
        : null
    const phoneCheck =
      !user_auth && event.target.name === 'phone_number'
        ? await charCheck('phone_number')
        : null
    const addressCheck =
      !user_auth && event.target.name === 'address'
        ? await charCheck('address')
        : null
    const emailCheck =
      event.target.name === 'email' ? await charCheck('email') : null
    const stateCheck =
      event.target.name === 'state' ? await charCheck('state') : null
    const cityCheck =
      event.target.name === 'city' ? await charCheck('city') : null
    const zipCheck =
      event.target.name === 'zipcode' ? await charCheck('zipcode') : null
    store.commit('mCheckIfValid', {
      emailCheck,
      stateCheck,
      cityCheck,
      zipCheck,
      nameCheck,
      addressCheck,
      phoneCheck,
      event
    })
  },
  aCheckLength(store, event) {
    store.commit('mCheckLength', event)
  },
  aHandleChange({ commit, dispatch }, event) {
    commit('mHandleChange', event)
    dispatch('aCheckIfValid', event)
    dispatch('aCheckIfInvalid', event)
    dispatch('aCheckLength', event)
  },
  aHandleBlur(store, event) {
    store.commit('mHandleBlur', event)
    store.dispatch('aCheckLength', event)
    store.dispatch('aCheckIfInvalid', event)
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
      state.form.state.value = location.state
      state.form.city.value = location.city
      state.form.zipcode.value = location.zip
      state.form.address.value = location.address
      state.form.state.class = 'valid'
      state.form.city.class = 'valid'
      state.form.zipcode.class = 'valid'
      state.form.address.class = 'valid'
      state.form.state.msg = ''
    }
  },
  mClearForm(state) {
    Object.keys(state.form).forEach(key => {
      state.form[key].class = 'neutral'
      state.form[key].value = ''
      state.form[key].visited = false
      state.form[key].msg = null
    })
    state.user_auth = true
    state.registration = true
  },
  mIncorrectPassword(state) {
    state.form.password.msg = 'Password Incorrect. Try Again'
    state.form.password.class = 'invalid'
    state.form.confirm.class = 'invalid'
  },
  mToggleRegistration(state) {
    state.registration
      ? (state.registration = false)
      : (state.registration = true)
  },
  mToggleAuth(state) {
    state.user_auth ? (state.user_auth = false) : (state.user_auth = true)
  },
  mHandleChange(state, event) {
    const eventValue = event.target.value

    state.form[event.target.name].value = eventValue

    if (!eventValue) {
      state.form[event.target.name].class = 'neutral'
      state.form[event.target.name].visited = false
    }

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
      event
    }
  ) {
    const eTarget = event.target.name
    if (eTarget === 'email') {
      if (
        emailCheck.includes('f') ||
        (state.form.email.minLen < state.form.email.value.length &&
          !state.form.email.value.includes('@')) ||
        (state.form.email.minLen < state.form.email.value.length &&
          !state.form.email.value.includes('.'))
      ) {
        state.form.email.class = 'invalid'
        state.form.email.msg = 'Must Be Valid Email Address'
      }
    }

    if (eTarget === 'state') {
      if (stateCheck.includes('n')) {
        state.form.state.class = 'invalid'
        state.form.state.msg = 'Required'
      } else if (stateCheck.includes('f')) {
        state.form.state.class = 'invalid'
        state.form.state.msg = 'Choose From Suggestions'
      }
    }

    if (eTarget === 'city') {
      if (cityCheck.includes('n')) {
        state.form.city.class = 'invalid'
        state.form.city.msg = 'Required'
      } else if (cityCheck.includes('f')) {
        state.form.city.class = 'invalid'
        state.form.city.msg = 'Choose From Suggestions'
      }
    }

    if (eTarget === 'zipcode') {
      if (zipCheck.includes('n')) {
        state.form.zipcode.class = 'invalid'
        state.form.zipcode.msg = 'Required'
      } else if (zipCheck.includes('f')) {
        state.form.zipcode.class = 'invalid'
        state.form.zipcode.msg = 'Choose From Suggestions'
      } else if (state.form.zipcode.value == 'zipcode') {
        state.form.zipcode.class = 'invalid'
        state.form.zipcode.msg = 'Required'
      }
    }

    if (eTarget === 'user_name') {
      if (nameCheck.includes('f')) {
        state.form.user_name.class = 'invalid'
        state.form.user_name.msg = 'Username Must Be Alphanumeric'
      }
    }

    if (eTarget === 'phone_number') {
      if (phoneCheck.includes('f')) {
        state.form.phone_number.class = 'invalid'
        state.form.phone_number.msg = 'Phone Number Must Be 10 Numbers'
      }
    }

    if (eTarget === 'address') {
      if (addressCheck.includes('f')) {
        state.form.address.class = 'invalid'
        state.form.address.msg = 'Address Must Be Alphanumeric'
      }
    }

    if (eTarget === 'confirm') {
      if (state.form.password.value !== state.form.confirm.value) {
        state.form.confirm.class = 'invalid'
        state.form.confirm.msg = 'Confirm Password Must Match Original'
      }
    }
    if (
      state.form[eTarget].class === 'neutral' ||
      (state.form[eTarget].class === 'invalid' && !state.form[eTarget].visited)
    ) {
      state.form[eTarget].class = 'neutral'
      state.form[eTarget].msg = null
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
      phoneCheck,
      event
    }
  ) {
    const eTarget = event.target.name
    if (eTarget === 'email') {
      if (
        !emailCheck.includes('f') &&
        state.form.email.value.length >= state.form.email.minLen &&
        state.form.email.value.length < 50
      ) {
        state.form.email.class = 'valid'
        state.form.email.visited = true
        state.form.email.msg = null
      }
    }

    if (
      eTarget === 'user_name' &&
      state.form.user_name.value.length >= state.form.user_name.minLen &&
      state.form.user_name.value.length < 50
    ) {
      if (!nameCheck.includes('f')) {
        state.form.user_name.class = 'valid'
        state.form.user_name.visited = true
        state.form.user_name.msg = null
      }
    }

    if (
      eTarget === 'phone_number' &&
      state.form.phone_number.value.length >= state.form.phone_number.minLen &&
      state.form.phone_number.value.length < 50
    ) {
      if (!phoneCheck.includes('f')) {
        state.form.phone_number.class = 'valid'
        state.form.phone_number.visited = true
        state.form.phone_number.msg = null
      }
    }

    if (
      eTarget === 'address' &&
      state.form.address.value.length >= state.form.address.minLen &&
      state.form.address.value.length < 50
    ) {
      if (!addressCheck.includes('f')) {
        state.form.address.class = 'valid'
        state.form.address.visited = true
        state.form.address.msg = null
      }
    }

    if (eTarget === 'state') {
      if (!stateCheck.includes('f') && !stateCheck.includes('n')) {
        state.form.state.class = 'valid'
        state.form.state.visited = true
        state.form.state.msg = null
      }
    }

    if (eTarget === 'city') {
      if (!cityCheck.includes('f') && !cityCheck.includes('n')) {
        state.form.city.class = 'valid'
        state.form.city.visited = true
        state.form.city.msg = null
      }
    }

    if (eTarget === 'zipcode') {
      if (!zipCheck.includes('f') && !zipCheck.includes('f')) {
        state.form.zipcode.class = 'valid'
        state.form.zipcode.visited = true
        state.form.zipcode.msg = null
      }
    }

    if (
      eTarget === 'shelter_name' &&
      state.form.shelter_name.value.length >= state.form.shelter_name.minLen &&
      state.form.shelter_name.value.length < 50
    ) {
      state.form.shelter_name.class = 'valid'
      state.form.shelter_name.visited = true
      state.form.shelter_name.msg = null
    }

    if (
      eTarget === 'password' &&
      state.form.password.value.length >= state.form.password.minLen &&
      state.form.password.value.length < 50
    ) {
      state.form.password.class = 'valid'
      state.form.password.visited = true
      state.form.password.msg = null
      if (state.form.confirm.visited) {
        if (state.form.password.value === state.form.confirm.value) {
          state.form.confirm.class = 'valid'
          state.form.confirm.msg = null
        } else {
          state.form.confirm.class = 'invalid'
          state.form.confirm.msg = 'Confirm Password Must Match Original'
        }
      }
    }

    if (
      eTarget === 'confirm' &&
      state.form.confirm.value.length >= state.form.confirm.minLen &&
      state.form.confirm.value.length < 50
    ) {
      if (
        state.form.password.class === 'valid' &&
        state.form.confirm.value === state.form.password.value
      ) {
        state.form.confirm.class = 'valid'
        state.form.confirm.visited = true
        state.form.confirm.msg = null
      }
    }
  },
  mCheckLength(state, event) {
    const eTarget = event.target.name
    const eLen = event.target.value.length
    const minLen = state.form[eTarget].minLen
    const cond1 =
      state.form[eTarget].visited || state.form[eTarget].class === 'valid'
    const cond2 = minLen && eLen < minLen

    if (minLen && eLen >= minLen) {
      state.form[eTarget].visited = true
    }

    if (cond1) {
      if (eLen > 50) {
        state.form[eTarget].class = 'invalid'
        state.form[
          eTarget
        ].msg = `${state.form[eTarget].for} Must Be Less Than 50 Characters Long.`
      } else if (eTarget === 'phone_number' && eLen !== 14) {
        state.form[eTarget].class = 'invalid'
        state.form[eTarget].msg = `Phone Number Must Be 10 Numbers.`
      } else if (cond2) {
        state.form[eTarget].class = 'invalid'
        state.form[eTarget].msg = `Must Be At Least ${minLen} Characters Long.`
        if (eTarget === 'password') {
          state.form.confirm.class = 'invalid'
          state.form.confirm.msg = 'Password Invalid'
        }
      } else if (
        !state.form[eTarget].visited &&
        state.form[eTarget].class !== 'valid'
      ) {
        state.form[eTarget].class = 'neutral'
        state.form[eTarget].msg = null
      }
    }
  },
  mSetPhoneNumber(state, val) {
    state.form.phone_number.value = val
  }
}
