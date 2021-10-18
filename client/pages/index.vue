<<<<<<< HEAD
<template>
  <section class="formCont">
    <form @submit.prevent="handleSubmit()">
      <div v-for="(field,index) in form" :key="index" class="inputCont">
        <label :for="index">{{field.for}}</label>
        <input @input="handleChange($event)" @keypress.enter="handleSubmit()" @blur="handleBlur($event)"
        :name="index"
        :type="field.type"
        :placeholder="field.placeholder"
        :class="field.class"
        />
        <div :class="field.class">
          <p v-if="field.msg" class="errMsg">{{field.msg}}</p>
          <p v-if="field.minLen">{{field.value.length}}/{{field.minLen}}</p>
        </div>
      </div>
      <button type="submit">login</button>
    </form>
  </section>
</template>

<script>
import axios from 'axios'
import {BASE_URL} from "../store/auth"
export default {
  name: "index",
  data:()=>({
    form: {
    'email': {
      value:'', class: "neutral", type: "email",
      for: "Valid Email Address",  placeholder: "you@youremail.com",
      visited: false, minLen: 10, msg:null
            },
    'userName': {
      value:'', class: "neutral", type: "text",
      for: "Your Username", placeholder: "DoggoDaddy73",
      visited: false, minLen: 5, msg:null
            },
    'password': {
      value:'', class: "neutral", type: "password",
      for: "Password", placeholder: "",
      visited: false, minLen: 8, msg:null
            },
    'confirm': {
      value:'', class: "neutral", type: "password",
      for: "Confirm Password", placeholder: "",
      visited: false, minLen: 8, msg:null
            }
    },
  }),
  methods:{
    charCheck(field){
      const charBools = []
      const acceptable = "1234567890qwertyuiopasdfghjklzxcvbnm"
      const charArr = this.form[field].value.split('')
      if(field === "userName"){
        charArr.forEach((char, i) => {
          
          if(acceptable.includes(char)){
            charBools.push("t")
          }else{
            charBools.push("f")
          }
          
        })
      }
      if(field === "email"){
        charArr.forEach((char, i) => {
            if (acceptable.includes(char)|| char === "@" || char ===".") {
              charBools.push("t")
            } else {
              charBools.push("f")
            }
        })
      }
      return charBools
    },
    checkIfInvalid(event){
      if(this.charCheck("email").indexOf("f") > -1){
        this.form.email.class = 'invalid'
        this.form.email.msg = "Must Be A Valid Address"
      } else if (this.form.email.class !== "valid"){
        this.form.email.class === "neutral"
      }
      if(this.charCheck("userName").includes("f")){
        
        this.form.userName.class = "invalid"
        this.form.userName.msg = "Username Must Be Alphanumeric"
      } else if (this.form.userName.class !== "valid"){
        this.form.userName.class === "neutral"
      }
      if(event.target.name == "confirm" && this.form.password.value.length
      < this.form.confirm.value.length){
        this.form.confirm.class = "invalid"
        this.form.confirm.msg = "Confirmation Must Match Original"
      } else if (this.form.confirm.class !== "valid"){
        this.form.confirm.class === "neutral"
      }
    },
    checkIfValid(){
    if(this.form.email.value.indexOf("@")>-1 && this.form.email.value.indexOf(".")>-1
      && this.form.email.value.length >= 10 && this.form.email.value.length < 50){
      this.form.email.class = "valid"
      this.form.email.msg = null
    }
    if(!( this.charCheck("userName").includes("f"))
      && this.form.userName.value.length >= 5 && this.form.userName.value.length < 50){
      this.form.userName.class = "valid"
      this.form.userName.msg = null
    }
    if (this.form.password.value.length >= 8 && this.form.password.value.length < 50){
      this.form.password.class = "valid"
      this.form.password.msg = null
    }
    if(this.form.password.class === "valid" && this.form.confirm.value
      === this.form.password.value){
      this.form.confirm.class = "valid"
      this.form.confirm.msg = null
    }
    },
    checkLength(event){
      const cond1 = this.form[event.target.name].visited === true || this.form[event.target.name].class 
      ==="valid"
      const cond2 = this.form[event.target.name].minLen && 
      event.target.value.length < this.form[event.target.name].minLen
      if (cond1){
        if(event.target.value.length > 50){
        this.form[event.target.name].class = "invalid"
        this.form[event.target.name].msg = `${event.target.name} must be less that 50 characters long`
      }else if(cond2){
        this.form[event.target.name].class = "invalid"
        this.form[event.target.name].msg = `${event.target.name} must be at least ${this.form[event.target.name].minLen} characters long`
      }else if (this.form[event.target.name].class !== "valid"){
        this.form[event.target.name].class === "neutral"
      }
      }
    },
    handleBlur(event){
      this.form[event.target.name].visited = true
      this.checkLength(event)
    },
    handleChange(event) {
      this.form[event.target.name].value = event.target.value
      this.checkIfValid()
      this.checkIfInvalid(event)
      this.checkLength(event)
    },
    handleSubmit(){
      if(
        this.form.userName.class === "valid" &&
        this.form.email.class === "valid" &&
        this.form.password.class === "valid" &&
        this.form.confirm.class === "valid"
      ){
        const body = {
          "user_name": this.form.userName.value,
          "password": this.form.confirm.value,
          "email": this.form.email.value,
        }
        try{
          const req = axios.post(`http://127.0.0.1:5000/register/users`, body)
          console.log(req)
        }catch(err){
          return err
        }
      }
    }
  },
}
</script>

<style scoped>

</style>
=======
>>>>>>> 88a071ce2c2ae03ecfbcc15b3d2dffaa6f34edbe
