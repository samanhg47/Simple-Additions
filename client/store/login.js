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
      placeholder: '',
      visited: false,
      minLen: 10,
      msg: null
    },
    city: {
      value: '',
      name: 'City',
      class: 'neutral',
      type: 'text',
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
      type: 'text',
      for: 'State',
      placeholder: '',
      visited: false,
      minLen: 10,
      msg: null
    },
    zipcode: {
      value: '',
      name: 'Zipcode',
      class: 'neutral',
      type: 'text',
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
      type: 'text',
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
      type: 'text',
      for: 'Phone Number',
      placeholder: '',
      visited: false,
      minLen: 10,
      msg: null
    }
  },
  user_form: true,
  user: {},
  shelter: {}
})

//getters
export const getters = {
  userForm: state => {
    form = state.form
    delete form.phone_number
    delete form.shelter_name
    delete form.address
    return form
  },
  shelterForm: state => {
    form = state.form
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
  checkIfInvalid(state) {
    if (this.charCheck('email').indexOf('f') > -1) {
      this.form.email.class = 'invalid'
      this.form.email.msg = 'Must Be A Valid Address'
    } else if (this.form.email.class !== 'valid') {
      this.form.email.class === 'neutral'
    }
    if (this.charCheck('userName').includes('f')) {
      this.form.userName.class = 'invalid'
      this.form.userName.msg = 'Username Must Be Alphanumeric'
    } else if (this.form.userName.class !== 'valid') {
      this.form.userName.class === 'neutral'
    }
    if (
      event.target.name == 'confirm' &&
      this.form.password.value.length < this.form.confirm.value.length
    ) {
      this.form.confirm.class = 'invalid'
      this.form.confirm.msg = 'Confirmation Must Match Original'
    } else if (this.form.confirm.class !== 'valid') {
      this.form.confirm.class === 'neutral'
    }
  }
}

//mutations
