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
      for: 'Valid Email Address',
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
      name: 'Password confirmation',
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
      for: 'Address',
      placeholder: '1234 West State St.',
      visited: false,
      minLen: 1,
      msg: null
    },
    city: {
      value: '',
      name: 'City',
      class: 'neutral',
      type: 'text',
      for: 'City',
      placeholder: 'city',
      visited: false,
      msg: null
    },
    state: {
      value: '',
      name: 'State',
      class: 'neutral',
      type: 'text',
      for: 'State',
      placeholder: 'state',
      visited: false,
      msg: null
    },
    zipcode: {
      value: '',
      name: 'Zipcode',
      class: 'neutral',
      type: 'text',
      for: 'Zipcode',
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
      minLen: 1,
      msg: null
    },
    phone_number: {
      value: '',
      name: 'phone_number',
      class: 'neutral',
      type: 'text',
      for: 'Phone Number',
      placeholder: '(123)-456-7891',
      visited: false,
      minLen: 14,
      msg: null
    }
  },
  user_form: true,
  user: {
    email: '',
    user_name: '',
    password: '',
    city: '',
    state: '',
    zipcode: ''
  },
  shelter: {}
})

//getters
export const getters = {
  userForm: state => {
    let form = state.form
    delete form.phone_number
    delete form.shelter_name
    delete form.address
    return form
  },
  shelterForm: state => {
    let form = state.form
    delete form.username
  }
}

//actions
export const actions = {
  async handleSubmit(form, bool) {
    const validity = []
    Object.keys(form).forEach(key => {
      validity.push(form[key].class)
    })
    if (!validity.includes('invalid')) {
      if (bool) {
        const res = await axios.post(`${BASE_URL}/register/users`)
        console.log(res)
      } else {
        const res = await axios.post(`${BASE_URL}/register/shelters`)
        console.log(res)
      }
      // $nuxt.$router.push('/home')
    }
  },
  charCheck(field) {
    const charBools = []
    const acceptable = '1234567890qwertyuiopasdfghjklzxcvbnm'
    const charArr = this.form[field].value.split('')
    if (`${field}` === 'user_name') {
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
    if (`${field}` === 'state') {
      if (''.join(charArr) == 'state') {
        charBools.push('f')
      } else {
        charBools.push('t')
      }
    }
    if (`${field}` === 'city') {
      if (''.join(charArr) == 'city') {
        charBools.push('f')
      } else {
        charBools.push('t')
      }
    }
    if (`${field}` === 'zipcode') {
      if (''.join(charArr) == 'zipcode') {
        charBools.push('f')
      } else {
        charBools.push('t')
      }
    }
    if (`${field}` === 'phone_number') {
      if (charArr.length > 14 || charArr.join('') === 'phone_number') {
        charBools.push('f')
      } else {
        charBools.push('t')
      }
    }
    return charBools
  },
  checkIfInvalid(state, event) {
    console.log()
    // if (state.charCheck('email').indexOf('f') > -1) {
    //   state.form.email.class = 'invalid'
    //   state.form.email.msg = 'Must Be A Valid Address'
    // } else if (state.form.email.class !== 'valid') {
    //   state.form.email.class === 'neutral'
    // }
    // if (state.charCheck('userName').includes('f')) {
    //   state.form.userName.class = 'invalid'
    //   state.form.userName.msg = 'Username Must Be Alphanumeric'
    // } else if (state.form.userName.class !== 'valid') {
    //   state.form.userName.class === 'neutral'
    // }
    // if (
    //   state.form.password.value.length < state.form.confirm.value.length
    // ) {
    //   state.form.confirm.class = 'invalid'
    //   state.form.confirm.msg = 'Confirmation Must Match Original'
    // } else if (state.form.confirm.class !== 'valid') {
    //   state.form.confirm.class === 'neutral'
    // }
  },
  handleChange(store, event) {
    // store.state.form[event.target.name].value = event.target.value
    // console.log(store.state)
    // store.checkIfValid()
    // store.checkIfInvalid(event)
    // store.checkLength(event)
    store.commit('commitChange', event)
  },
  handleBlur(event) {
    console.log(event)
    //     this.form[event.target.name].visited = true
    //     this.checkLength(event)
  }
}

//mutations
export const mutations = {
  commitChange(state, event) {
    state.form[event.target.name].value = event.target.value
  }
}
