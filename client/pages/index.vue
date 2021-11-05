<template>
  <form @submit.prevent="aHandleSubmit()">
    <h1 v-if="registration">Register</h1>
    <h1 v-if="!registration">Login</h1>


    <div v-if='user_auth' class="inputCont">
      <section v-for="(field,index) in userForm" :key="index" :class="'inpSec ' + field.class">
        <div class="inpDiv">
          <label :for="index">{{field.for}}:</label>
          <button tabindex="-1" v-if='index === "password"' class='showPasswordBtn' type='button' @mousedown="showPass(index)" @mouseup="hidePass(index)">
            <img v-if='index === "password" && hidePassword' class="showPassword" src='../assets/hiddenPassword.png' alt='Show Password Icon'/>
            <img v-if='index === "password" && !hidePassword' class="hidePassword" src='../assets/shownPassword.png' alt='Show Password Icon'/>
          </button>
          <button tabindex="-1" v-if='index === "confirm"' class='showPasswordBtn' type='button' @mousedown="showPass(index)" @mouseup="hidePass(index)">
            <img v-if='index === "confirm" && hideConfirm' class="showPassword" src='../assets/hiddenPassword.png' alt='Show Password Icon'/>
            <img v-if='index === "confirm" && !hideConfirm' class="hidePassword" src='../assets/shownPassword.png' alt='Show Password Icon'/>
          </button>
          <input @input="aHandleChange($event)" @blur="aHandleBlur($event)"
          :name="index"
          :type="field.type"
          :placeholder="field.placeholder"
          />
        </div>
        <div class="errDiv">
          <p v-if="field.minLen" class="charCount">{{field.value.length}}/{{field.minLen}}</p>
          <p v-if="field.msg" class="errMsg">{{field.msg}}</p>
        </div>
      </section>
    </div >


    <div v-if='!user_auth' class="inputCont">
      <section v-for="(field,index) in shelterForm" :key="index" :class="'inpSec ' + field.class">
        <div class="inpDiv">
          <label :for="index">{{field.for}}:</label>
          <button tabindex="-1" v-if='index === "password"' :class="registration?'sheltShowPasswordBtn':'showPasswordBtn'" type='button' @mousedown="showPass(index)" @mouseup="hidePass(index)">
            <img v-if='index === "password" && hidePassword' class="showPassword" src='../assets/hiddenPassword.png' alt='Show Password Icon'/>
            <img v-if='index === "password" && !hidePassword' class="hidePassword" src='../assets/shownPassword.png' alt='Show Password Icon'/>
          </button>
          <button tabindex="-1" v-if='index === "confirm"' :class="registration?'sheltShowPasswordBtn':'showPasswordBtn'" type='button' @mousedown="showPass(index)" @mouseup="hidePass(index)">
            <img v-if='index === "confirm" && hideConfirm' class="showPassword" src='../assets/hiddenPassword.png' alt='Show Password Icon'/>
            <img v-if='index === "confirm" && !hideConfirm' class="hidePassword" src='../assets/shownPassword.png' alt='Show Password Icon'/>
          </button>
          <input @input="aHandleChange($event)" @blur="aHandleBlur($event)"
          :name="index"
          :type="field.type"
          :placeholder="field.placeholder"
          />
        </div>
        <div class="errDiv">
          <p v-if="field.minLen" class="charCount">{{field.value.length}}/{{field.minLen}}</p>
          <p v-if="field.msg" class="sheltErrMsg">{{field.msg}}</p>
        </div>
      </section>
    </div >


    <div class="location" v-if="registration">
      <div v-for="(field,index) in userLocation" :key="index" class='inputCont'>
        <section :class="`preSec ${field.class}`">
          <label v-if="index === 'state'" :for="index">{{field.for}}</label>
          <input v-if="index === 'state'" list="state_list" :name='index' id="stateInp" placeholder="state" @blur="aHandleBlur($event)" @change="aHandleChange($event)"/>
          <datalist v-if="index === 'state'" :name="index" id="state_list">
            <option v-for="state in states" :key="state" :value="state" >{{state}}</option>
          </datalist>
          <label v-if="index === 'city'" :for="index">{{field.for}}</label>
          <input v-if="index === 'city'" disabled list="city_list" :name='index' id="cityInp" placeholder="city" @blur="aHandleBlur($event)" @change="aHandleChange($event)"/>
          <datalist v-if="index === 'city'" :name="index" id="city_list">
            <option v-for="city in city_list" :key="city" :value="city" class="city">{{city}}</option>
          </datalist>
          <label v-if="index === 'zipcode'" :for="index">{{field.for}}</label>
          <input v-if="index === 'zipcode'" disabled list="zipcode_list" :name="index" id="zipInp" placeholder="zipcode" @change="aHandleChange($event)" @blur="aHandleBlur($event)"/>
          <datalist v-if="index === 'zipcode'" :name="index" id="zipcode_list">
            <option v-for="zipcode in zipcode_list" :key="zipcode" :value="zipcode" class="zip">{{zipcode}}</option>
          </datalist>
          <div class="errDiv2">
            <p v-if="field.msg" :class="'errMsg2 ' + index">{{field.msg}}</p>
          </div>
        </section>
      </div>
    </div>


    <div id='btmDiv'>
      <section id='btnDiv'>
        <button type="submit" v-if="registration" disabled id="sub">Register</button>
        <button type="submit" v-if="!registration" disabled id="sub">Login</button>
      </section>
      <button @click.prevent="aToggleAuth" class='toggleLink' type='button' v-if="user_auth">Shelter Login/Registration Here.</button>
      <button @click.prevent="aToggleRegistration" class='toggleLink' type='button' v-if="user_auth && registration">Returning user? Click Here To Login.</button>
      <button @click.prevent="aToggleRegistration" class='toggleLink' type='button' v-if="user_auth && !registration">New user? Click Here To Register.</button>
      <button @click.prevent="aToggleAuth" class='toggleLink' type='button' v-if="!user_auth">User Login/Registration Here</button>
      <button @click.prevent="aToggleRegistration" class='toggleLink' type='button' v-if="!user_auth && registration">Returning Shelter? Click Here To Login.</button>
      <button @click.prevent="aToggleRegistration" class='toggleLink' type='button' v-if="!user_auth && !registration">New Shelter? Click Here To Register.</button>
    </div>
  </form>
</template>
<script>
import {mapState, mapGetters, mapActions} from "vuex"
export default {
  async created () {
    await this.getStates()
  },
  mounted () {
    window.addEventListener('beforeunload', this.clearForm)
  },
  updated(){
    if (this.layout === null){
      this.layout = document.firstElementChild.children[1].children[0].children[1]
      ? document.firstElementChild.children[1].children[0].children[1]
      : document.firstElementChild.children[1].children[0].firstElementChild
    }
    if(!this.user_auth){
        this.phoneNumber = this.layout
        .firstElementChild.children[1].firstElementChild.firstElementChild.children[1]
        .children[3].firstElementChild.children[1].value
    }
  },
  data: ()=>({
    hidePassword: true,
    hideConfirm: true,
    phoneNumber: null,
    layout: null
  }),
  computed: {
    ...mapState(
      "login",[
        "user_auth",
        "registration",
        'form'
        ]
      ),
    ...mapState([
      "states"
      ]),
    ...mapGetters([
      "city_list",
      "zipcode_list"
      ]),
    ...mapGetters(
      "login",[
        "userForm",
        "shelterForm",
        "userLocation"
        ]
      ),
    validVals: function(){
      let validity = []
      if(this.user_auth){
        Object.keys(this.userForm).forEach(key => {
          validity.push(`${key} ${this.userForm[key].class}`)
        })
      }
      if(!this.user_auth){
        Object.keys(this.shelterForm).forEach(key => {
          validity.push(`${key} ${this.shelterForm[key].class}`)
        })
      }
      Object.keys(this.userLocation).forEach(key => {
        validity.push(`${key} ${this.userLocation[key].class}`)
      })
      return validity
    }
  },
  methods: {
    ...mapActions([
      "getStates",
      "getCities"
      ]),
    ...mapActions(
      "login", [
        "aHandleBlur",
        "aHandleChange",
        "aHandleSubmit",
        "aToggleRegistration",
        "aToggleAuth",
        "charCheck",
        'aClearForm'
        ]
      ),
    showPass(i){
      i == "confirm" && (this.hideConfirm = false)
      i == "password" && (this.hidePassword = false)
      document.querySelector(`[name="${i}"]`).setAttribute("type", "text")
      },
    hidePass(i){
      i == "confirm" && (this.hideConfirm = true)
      i == "password" && (this.hidePassword = true)
      document.querySelector(`[name="${i}"]`).setAttribute("type", "password")
    },
    clearForm(){
      document.querySelectorAll('input').forEach( inp => {
        inp.value = ''
      })
      this.aClearForm()
    }
  },
  watch:{
    'userLocation.state.value' : function(){
      if (this.registration){
        if(this.states.includes(this.userLocation.state.value)){
        this.getCities(this.userLocation.state.value)
        }
        document.querySelector("#cityInp").value &&
        (document.querySelector("#cityInp").value = "")
        !document.querySelector("#cityInp").disabled &&
        (document.querySelector("#cityInp").disabled = true)

        document.querySelector("#zipInp").value &&
        (document.querySelector("#zipInp").value = "")
        document.querySelector("#zipInp").disabled &&
        (document.querySelector("#zipInp").disabled = true)

        if (this.states.includes(this.userLocation.state.value)){
          document.querySelector("#cityInp").placeholder = "...loading"
        }
      }
    },
    city_list: function(){
      if(this.registration && this.states.includes(this.userLocation.state.value)){
        document.querySelector("#cityInp").placeholder = "city"
        document.querySelector("#cityInp").disabled = false
      }
    },
    'userLocation.city.value' : function(){
      if (this.registration){
        document.querySelector("#zipInp").value &&
        (document.querySelector("#zipInp").value = "")
        document.querySelector("#zipInp").disabled &&
        (document.querySelector("#zipInp").disabled = true)
      }
    },
    zipcode_list: function(oldVal, newVal){
      if(this.registration && this.city_list.includes(this.userLocation.city.value)){
        document.querySelector("#zipInp").placeholder = "zipcode"
        document.querySelector("#zipInp").disabled = false
      }
    },
    validVals: function(newVal, oldVal){
      if(!this.validVals.every( val => val.split(' ')[1] === "valid")){
        document.getElementById("sub").disabled = true
      }else{
        document.getElementById("sub").disabled = false
      }

      if (oldVal.length === newVal.length){
        this.validVals.forEach( (val, i) => {
          if(val.split(' ')[1] === "invalid" && oldVal[i].split(' ')[1] !== val.split(' ')[1]){
            const element = document.querySelector(`[name="${val.split(' ')[0]}"]`)
            element.classList.add('error')
            setTimeout(function() {
              element.classList.remove('error')
            }, 300)
          }
        })
      }
    },
    phoneNumber: function(newVal, oldVal){
      if(newVal.length){
        if(newVal.length > oldVal.length){
          if (this.phoneNumber.length === 1) {
            this.phoneNumber = `(${this.phoneNumber}`
            this.layout.firstElementChild.children[1].firstElementChild
            .firstElementChild.children[1].children[3]
            .firstElementChild.children[1].value = this.phoneNumber
          } else if (this.phoneNumber.length === 5) {
            this.phoneNumber = `${this.phoneNumber.slice(0,4)})-${this.phoneNumber.slice(4)}`
            this.layout.firstElementChild.children[1].firstElementChild
            .firstElementChild.children[1].children[3]
            .firstElementChild.children[1].value = this.phoneNumber
          } else if (this.phoneNumber.length === 10) {
            this.phoneNumber = `${this.phoneNumber.slice(0,9)}-${this.phoneNumber.slice(9)}`
            this.layout.firstElementChild.children[1].firstElementChild
            .firstElementChild.children[1].children[3]
            .firstElementChild.children[1].value = this.phoneNumber
          }
        }
        if(newVal.length < oldVal.length){
          if(newVal.length === 10){
            this.phoneNumber = this.phoneNumber.slice(0,9)
            this.layout.firstElementChild.children[1].firstElementChild
            .firstElementChild.children[1].children[3]
            .firstElementChild.children[1].value = this.phoneNumber
          }
          if(newVal.length === 6){
            this.phoneNumber = this.phoneNumber.slice(0,4)
            this.layout.firstElementChild.children[1].firstElementChild
            .firstElementChild.children[1].children[3]
            .firstElementChild.children[1].value = this.phoneNumber
          }
          if(newVal.length === 1){
            this.phoneNumber = ''
            this.layout.firstElementChild.children[1].firstElementChild
            .firstElementChild.children[1].children[3]
            .firstElementChild.children[1].value = this.phoneNumber
          }
        }
      }
    },

  },
}
</script>

<style>
form{
  display: flex;
  align-items: center;
  justify-content: flex-start;
  flex-direction: column;
  font-size: 1.8vw;
  padding: 0 2vw 0 2vw;
  align-content:space-between;
}

.inputCont{
  width: 100%;
}
.inpSec{
  width: 100%;
}
.location > .inputCont{
  display: inline-block;
  width: auto;
}
img{
  width: 10vw;
}
.inpSec > div{
  display: flex;
  max-width: inherit;
}
.inpDiv{
  width: inherit;
  flex-direction: row;
  justify-content: space-between;
}
input{
  background-color: #96969657;
  border: none;
  padding-left: .5vw;
  width: 22vw;
  height: 2.5vw;
}
[name='password'],[name='confirm'] {
  padding-right: 2.5vw;
}
h1{
  margin: 2vw;
  padding: 0;
  justify-self: start;
}
datalist{
  max-width: 7vw;
  text-align: center;
}

.errDiv{
  font-size: 1.2vw;
  max-width: inherit;
  flex-direction: row-reverse;
  justify-content: space-between;
  color: black
}
.errDiv2{
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2vw;
  color: black;
  position: relative;
  justify-self: center;
}
.errMsg{
  margin-left: 14vw;
  margin-bottom: 0;
  margin-top: 0;
}
.sheltErrMsg{
  margin-left: 18.8vw;
  margin-bottom: 0;
  margin-top: 0;
}
.errMsg2{
  text-align: center;
}
.errMsg2.state{
  width: 7vw;
}
.errMsg2.zipcode{
  width: 9vw;
}


.preSec{
  display: inline-block;
  text-align: center;
  flex-direction: column;
}
.location{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-content: flex-start;
  width: 100%;
  height: 4vw;
}
#cityInp{
  width: 17vw;
  /* margin: 0 .5vw 0 .5vw; */
  background-color: rgba(0, 0, 0, 0.137);
  text-align: center;
}
#stateInp{
  width: 7vw;
  /* margin: 0 .5vw 0 .5vw; */
  background-color: rgba(0, 0, 0, 0.137);
  text-align: center;
}
#zipInp{
  width: 9vw;
  /* margin: 0 .5vw 0 .5vw; */
  background-color: rgba(0, 0, 0, 0.137);
  text-align: center;
}
.valid > .errDiv,.valid > .errDiv2{
  color:green
}
.invalid > .errDiv,.invalid > .errDiv2{
  color:rgb(214, 16, 16)
}
.valid > * > input{
  border: .2vw solid green;
}
.invalid > * > input{
  border: .2vw solid rgb(214, 16, 16);
}
.neutral > * > input{
  border: none;
}
.valid > input{
  border: .2vw solid green;
}
.invalid > input{
  border: .2vw solid rgb(214, 16, 16);
}
.neutral > input,select{
  border: none;
}


#btmDiv{
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  margin-top: auto;
}
#btmDiv > * {
  margin: .5vw;
}
#sub{
  background: #606E38;
  background: linear-gradient(
    to bottom left,
    #606E38,
    #98af58
  );
  box-shadow: 0px .3vw 0 0 #606E38;
  padding: .3vw .7vw;
  border-radius: 20px;
}
#sub:hover{
  background: linear-gradient(
    to bottom left,
    #98af58,
    #606E38
  );
}
#sub:active{
  box-shadow: none;
  margin-top: .5vw;
}
#btnDiv{
  /* width: 10vw; */
  height: 3vw;
  display: flex;
  align-items: center;
  justify-content: center;
}


.showPasswordBtn {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: .5vw;
  margin-left: 33.5vw;
}
.sheltShowPasswordBtn {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: .5vw;
  margin-left: 38.4vw;
}
.showPassword{
  width: 2vw;
}
.hidePassword{
  width: 1.6vw;
  height: 1.2vw;
  margin: .18vw .15vw .25vw .24vw;
}


.toggleLink{
  color: #758842;
  text-decoration: underline;
}
.toggleLink:hover{
  color: #606E38;
}
.toggleLink:active{
  color: #98af58;
}


.error {
    position: relative;
    animation: shake .1s linear;
    animation-iteration-count: 3;
}
@keyframes shake {
    0% { top: -.2vw; }
    100% { bottom: -.2vw; }
}
</style>