<template>
  <section class="formCont flex">
    <section class="inputSec flex">
      <Nuxt />
    </section>
  </section>
</template>

<script>
import axios from 'axios'
import { BASE_URL } from '../store/auth'
export default {

  // data:()=>({
  //   form: {
  //   'email': {
  //     value:'', class: "neutral", type: "email",
  //     for: "Valid Email Address",  placeholder: "you@youremail.com",
  //     visited: false, minLen: 10, msg:null
  //           },
  //   'userName': {
  //     value:'', class: "neutral", type: "text",
  //     for: "Your Username", placeholder: "DoggoDaddy73",
  //     visited: false, minLen: 5, msg:null
  //           },
  //   'password': {
  //     value:'', class: "neutral", type: "password",
  //     for: "Password", placeholder: "",
  //     visited: false, minLen: 8, msg:null
  //           },
  //   'confirm': {
  //     value:'', class: "neutral", type: "password",
  //     for: "Confirm Password", placeholder: "",
  //     visited: false, minLen: 8, msg:null
  //           }
  //   },
  // }),
  // methods:{
  //   charCheck(field){
  //     const charBools = []
  //     const acceptable = "1234567890qwertyuiopasdfghjklzxcvbnm"
  //     const charArr = this.form[field].value.split('')
  //     if(field === "userName"){
  //       charArr.forEach((char, i) => {
          
  //         if(acceptable.includes(char)){
  //           charBools.push("t")
  //         }else{
  //           charBools.push("f")
  //         }
          
  //       })
  //     }
  //     if(field === "email"){
  //       charArr.forEach((char, i) => {
  //           if (acceptable.includes(char)|| char === "@" || char ===".") {
  //             charBools.push("t")
  //           } else {
  //             charBools.push("f")
  //           }
  //       })
  //     }
  //     return charBools
  //   },
  //   checkIfInvalid(event){
  //     if(this.charCheck("email").indexOf("f") > -1){
  //       this.form.email.class = 'invalid'
  //       this.form.email.msg = "Must Be A Valid Address"
  //     } else if (this.form.email.class !== "valid"){
  //       this.form.email.class === "neutral"
  //     }
  //     if(this.charCheck("userName").includes("f")){
        
  //       this.form.userName.class = "invalid"
  //       this.form.userName.msg = "Username Must Be Alphanumeric"
  //     } else if (this.form.userName.class !== "valid"){
  //       this.form.userName.class === "neutral"
  //     }
  //     if(event.target.name == "confirm" && this.form.password.value.length
  //     < this.form.confirm.value.length){
  //       this.form.confirm.class = "invalid"
  //       this.form.confirm.msg = "Confirmation Must Match Original"
  //     } else if (this.form.confirm.class !== "valid"){
  //       this.form.confirm.class === "neutral"
  //     }
  //   },
  //   checkIfValid(){
  //   if(this.form.email.value.indexOf("@")>-1 && this.form.email.value.indexOf(".")>-1
  //     && this.form.email.value.length >= 10 && this.form.email.value.length < 50){
  //     this.form.email.class = "valid"
  //     this.form.email.msg = null
  //   }
  //   if(!( this.charCheck("userName").includes("f"))
  //     && this.form.userName.value.length >= 5 && this.form.userName.value.length < 50){
  //     this.form.userName.class = "valid"
  //     this.form.userName.msg = null
  //   }
  //   if (this.form.password.value.length >= 8 && this.form.password.value.length < 50){
  //     this.form.password.class = "valid"
  //     this.form.password.msg = null
  //   }
  //   if(this.form.password.class === "valid" && this.form.confirm.value
  //     === this.form.password.value){
  //     this.form.confirm.class = "valid"
  //     this.form.confirm.msg = null
  //   }
  //   },
  //   checkLength(event){
  //     const cond1 = this.form[event.target.name].visited === true || this.form[event.target.name].class 
  //     ==="valid"
  //     const cond2 = this.form[event.target.name].minLen && 
  //     event.target.value.length < this.form[event.target.name].minLen
  //     if (cond1){
  //       if(event.target.value.length > 50){
  //       this.form[event.target.name].class = "invalid"
  //       this.form[event.target.name].msg = `${event.target.name} must be less that 50 characters long`
  //     }else if(cond2){
  //       this.form[event.target.name].class = "invalid"
  //       this.form[event.target.name].msg = `${event.target.name} must be at least ${this.form[event.target.name].minLen} characters long`
  //     }else if (this.form[event.target.name].class !== "valid"){
  //       this.form[event.target.name].class === "neutral"
  //     }
  //     }
  //   },
  //   handleBlur(event){
  //     this.form[event.target.name].visited = true
  //     this.checkLength(event)
  //   },
    // handleChange(event) {
    //   this.form[event.target.name].value = event.target.value
    //   this.checkIfValid()
    //   this.checkIfInvalid(event)
    //   this.checkLength(event)
    // },
  //   async handleSubmit(){
  //     if(
  //       this.form.userName.class === "valid" &&
  //       this.form.email.class === "valid" &&
  //       this.form.password.class === "valid" &&
  //       this.form.confirm.class === "valid"
  //     ){
  //       const body = {
  //         "user_name": this.form.userName.value,
  //         "password": this.form.confirm.value,
  //         "email": this.form.email.value,
  //       }
  //       try{
  //         const res = await axios.post(`${BASE_URL}/register/users`, body)
  //         console.log(res.data)
          
  //       }catch(err){
  //         return err
  //       }
  //     }
  //   }
  // },
}
</script>

<style>
html, body, #__nuxt, #__layout{
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}
.flex{
  display: flex;
  align-items: center;
  justify-content: center;
}
#__layout{
  background-color: #e2fdff;
  display: flex;
  align-items: center;
  justify-content: center;
}
.formCont{
  height: 35vw;
  max-width: 45vw;
  background-color: #516b33;
  border-radius: 20px;
}
.inputSec{
  height: 27vw;
  max-width: 30vw;
  background-color: wheat;
}
  form{
    
  }
.inputCont{
  flex-direction: column;
}
</style>