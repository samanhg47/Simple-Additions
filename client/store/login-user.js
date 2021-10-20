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
      type: 'password',
      for: 'Address',
      placeholder: '',
      visited: false,
      minLen: 10,
      msg: null
    },
    city: {
      value: '',
      name: 'City',
      class: 'neutral',
      type: 'password',
      for: 'City',
      placeholder: '',
      visited: false,
      minLen: 10,
      msg: null
    },
    state: {
      value: '',
      name: 'State',
      class: 'neutral',
      type: 'password',
      for: 'State',
      placeholder: '',
      visited: false,
      minLen: 10,
      msg: null
    },
    shelter_name: {
      value: '',
      name: 'Shelter name',
      class: 'neutral',
      type: 'password',
      for: 'Shelter Name',
      placeholder: '',
      visited: false,
      minLen: 10,
      msg: null
    },
    phone_number: {
      value: '',
      name: 'phone_number',
      class: 'neutral',
      type: 'password',
      for: 'Phone Number',
      placeholder: '',
      visited: false,
      minLen: 10,
      msg: null
    }
  },
  user: true
})

//getters

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
    return charBools
  }
}

//mutations
