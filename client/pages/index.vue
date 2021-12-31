<template>
  <form @submit.prevent="aHandleSubmit()">
    <h1 v-if="registration">Register</h1>
    <h1 v-if="!registration">Login</h1>

<!-- User Form(s) -->
    <div v-if='user_auth' class="inputCont">
      <section v-for="(field,index) in userForm"
        :key="index"
        :class="index=='confirm'
          ? 'btmInp inpSec ' + field.class
          : 'inpSec ' + field.class">
            <div class="inpDiv">
              <label :for="index">{{field.for}}:</label>
              <button @mousedown="showPass(index)" @mouseup="hidePass(index)"
                tabindex="-1"
                v-if='index === "password"'
                class='showPasswordBtn'
                type='button'>
                  <img
                    v-if='index === "password" && hidePassword'
                    class="showPassword"
                    src='../assets/hiddenPassword.png'
                    alt='Show Password Icon'/>
                  <img
                    v-if='index === "password" && !hidePassword'
                    class="hidePassword"
                    src='../assets/shownPassword.png'
                    alt='Show Password Icon'/>
              </button>
              <button @mousedown="showPass(index)" @mouseup="hidePass(index)"
                tabindex="-1"
                v-if='index === "confirm"'
                class='showPasswordBtn'
                type='button'>
                  <img
                    v-if='index === "confirm" && hideConfirm'
                    class="showPassword"
                    src='../assets/hiddenPassword.png'
                    alt='Show Password Icon'/>
                  <img
                    v-if='index === "confirm" && !hideConfirm'
                    class="hidePassword"
                    src='../assets/shownPassword.png'
                    alt='Show Password Icon'/>
              </button>
              <input @input="aHandleChange($event)" @blur="aHandleBlur($event)"
                :name="index"
                :type="field.type"
                :placeholder="field.placeholder"
                disabled
                v-if="index === 'confirm'"
              />
              <input @input="aHandleChange($event)" @blur="aHandleBlur($event)"
                :name="index"
                :type="field.type"
                :placeholder="field.placeholder"
                v-if="index !== 'confirm'"
              />
            </div>
            <div class="errDiv">
              <p v-if="field.minLen" class="charCount">
                {{field.value.length}}/{{field.minLen}}
              </p>
              <p v-if="field.msg" class="errMsg">
                {{field.msg}}
              </p>
            </div>
      </section>
    </div >

<!-- Shelter Form(s) -->
    <div v-if='!user_auth' class="inputCont">
      <section v-for="(field,index) in shelterForm"
      :key="index"
        :class="index=='confirm'
          ? 'btmInp inpSec ' + field.class
          : 'inpSec ' + field.class">
            <div class="inpDiv">
              <label :for="index">{{field.for}}:</label>
              <button @mousedown="showPass(index)" @mouseup="hidePass(index)"
                :class="registration?'sheltShowPasswordBtn':'showPasswordBtn'"
                v-if='index === "password"'
                tabindex="-1"
                type='button'>
                  <img
                    v-if='index === "password" && hidePassword'
                    class="showPassword"
                    src='../assets/hiddenPassword.png'
                    alt='Show Password Icon'/>
                  <img
                    v-if='index === "password" && !hidePassword'
                    class="hidePassword"
                    src='../assets/shownPassword.png'
                    alt='Show Password Icon'/>
              </button>
              <button  @mousedown="showPass(index)" @mouseup="hidePass(index)"
                tabindex="-1"
                v-if='index === "confirm"'
                :class="registration?'sheltShowPasswordBtn':'showPasswordBtn'"
                type='button'>
                  <img
                    v-if='index === "confirm" && hideConfirm'
                    class="showPassword"
                    src='../assets/hiddenPassword.png'
                    alt='Show Password Icon'/>
                  <img
                    v-if='index === "confirm" && !hideConfirm'
                    class="hidePassword"
                    src='../assets/shownPassword.png'
                    alt='Show Password Icon'/>
              </button>
              <input @input="aHandleChange($event)" @blur="aHandleBlur($event)"
                :name="index"
                :type="field.type"
                :placeholder="field.placeholder"
                disabled
                v-if="index === 'confirm'"
              />
              <input @input="aHandleChange($event)" @blur="aHandleBlur($event)"
                :name="index"
                :type="field.type"
                :placeholder="field.placeholder"
                v-if="index !== 'confirm'"
              />
            </div>
            <div class="errDiv">
              <p v-if="field.minLen" class="charCount">
                {{field.value.length}}/{{field.minLen}}
              </p>
              <p v-if="field.msg" class='errMsg'>
                {{field.msg}}
              </p>
            </div>
      </section>
    </div >

<!-- Location Selectors -->
    <div class="location" v-if="registration">
      <div v-for="(field,index) in userLocation" :key="index" class='inputCont'>
        <section :class="`preSec ${field.class}`">
          <label v-if="index === 'state'" :for="index">{{field.for}}</label>
          <input @blur="aHandleBlur($event)" @change="aHandleChange($event)"
            v-if="index === 'state'"
            list="state_list" :name='index'
            id="stateInp" placeholder="state"/>
              <datalist v-if="index === 'state'" :name="`${index}List`" id="state_list">
                <option v-for="state in states" :key="state" :value="state" >
                  {{state}}
                </option>
              </datalist>
          <label v-if="index === 'city'" :for="index">{{field.for}}</label>
          <input @blur="aHandleBlur($event)" @change="aHandleChange($event)"
            disabled
            v-if="index === 'city'"
            list="city_list"
            :name='index'
            id="cityInp"
            placeholder="city"/>
              <datalist v-if="index === 'city'" :name="`${index}List`" id="city_list">
                <option v-for="city in city_list" 
                  :key="city"
                  :value="city"
                  class="city">
                    {{city}}
                </option>
              </datalist>
          <label v-if="index === 'zipcode'" :for="index">{{field.for}}</label>
          <input @change="aHandleChange($event)" @blur="aHandleBlur($event)"
            disabled
            v-if="index === 'zipcode'"
            list="zipcode_list"
            :name="index"
            id="zipInp"
            placeholder="zipcode"/>
              <datalist v-if="index === 'zipcode'" :name="`${index}List`" id="zipcode_list">
                <option v-for="zipcode in zipcode_list"
                  :key="zipcode"
                  :value="zipcode"
                  class="zip">
                    {{zipcode}}
                </option>
              </datalist>
          <div class="errDiv2">
            <p v-if="field.msg" :class="'errMsg2 '+index">
              {{field.msg}}
            </p>
          </div>
        </section>
      </div>
    </div>

<!-- Buttons -->
    <div id='btmDiv'>
      <section id='btnDiv'>
        <button type="submit" v-if="registration" disabled id="sub" :style="submitStyles">
          Register
        </button>
        <button type="submit" v-if="!registration" disabled id="sub" :style="submitStyles">
          Login
        </button>
      </section>
      <button @click.prevent="aToggleAuth"
        v-if="user_auth"
        class='toggleLink'
        type='button'>
          Shelter Login/Registration Here.
      </button>
      <button @click.prevent="aToggleRegistration"
        v-if="user_auth && registration"
        class='toggleLink'
        type='button'>
          Returning user? Click Here To Login.
      </button>
      <button @click.prevent="aToggleRegistration"
        v-if="user_auth && !registration"
        class='toggleLink'
        type='button'>
          New user? Click Here To Register.
      </button>
      <button @click.prevent="aToggleAuth"
        v-if="!user_auth"
        class='toggleLink'
        type='button'>
          User Login/Registration Here
      </button>
      <button @click.prevent="aToggleRegistration"
        v-if="!user_auth && registration"
        class='toggleLink'
        type='button'>
          Returning Shelter? Click Here To Login.
      </button>
      <button @click.prevent="aToggleRegistration"
        v-if="!user_auth && !registration"
        class='toggleLink'
        type='button'>
          New Shelter? Click Here To Register.
      </button>
    </div>
  </form>
</template>
<script>
import { mapState, mapGetters, mapActions } from "vuex"
export default {
  async created () {
    await this.checkToken()
    this.aAddStates()
    if(this.shelters.length === 0){
      this.grabShelters()
    }
  },
  mounted () {
    if(Object.keys(this.location).length == 0){
        navigator.geolocation.getCurrentPosition(async(position)=>{
        const lat = position.coords.latitude
        const lng = position.coords.longitude
        this.aSetLocation({lng, lat})
        })
    }
    const locationVals = []
    Object.values(this.userLocation).forEach(obj => locationVals.push(obj.value))
    if(Object.keys(this.location).length !== 0 && locationVals.includes('')){
      this.aLocationAutofill(this.location)
    }

    this.formUpdate()
    this.styling()
  },
  updated(){
    if(!this.user_auth && this.registration){
        this.phoneNumber = document.querySelector('[name="phone_number"]').value
    }
    this.styling()
  },
  beforeDestroy(){
    this.clearForm()
  },
  data: ()=>({
    hidePassword: true,
    hideConfirm: true,
    phoneNumber: null,
    layout: null
  }),
  computed: {
    // login state
    ...mapState(
      "login",[
        "user_auth",
        "registration",
        "user"
        ]),
    // root state
    ...mapState([
      'states',
      'location',
      'shelters'
      ]),
    // root getters
    ...mapGetters([
      "city_list",
      "zipcode_list"
      ]),
    // theme getters
    ...mapGetters(
      "theme",[
        "theme"
        ]),
    // login getters
    ...mapGetters(
      "login",[
        "userForm",
        "shelterForm",
        "userLocation"
        ]
      ),
    //theme getters
    ...mapGetters(
      'theme',[
        'theme'
      ]
    ),
    validVals: function(){
      let validity = []
      if(this.user_auth){
        if(this.registration){
          Object.keys(this.userForm).forEach(key => {
            validity.push(`${key} ${this.userForm[key].class}`)
          })
        } else {
          Object.keys(this.userForm).forEach(key => {
            validity.push(`${key} ${this.userForm[key].class}`)
          })
        }
      }
      if(!this.user_auth){
        if(this.registration){
          Object.keys(this.shelterForm).forEach(key => {
            validity.push(`${key} ${this.shelterForm[key].class}`)
        })
        } else {
          Object.keys(this.shelterForm).forEach(key => {
            validity.push(`${key} ${this.shelterForm[key].class}`)
          })
        }
      }
      if (this.registration) {
        Object.keys(this.userLocation).forEach(key => {
          validity.push(`${key} ${this.userLocation[key].class}`)
        })
      }
      return validity
    },
    inpStyles: function(){
      return `background-color:\ 
                ${this.theme.input};\
              color:\
                ${this.theme.color};`
    },
    errDivStyles: function(){
      return `color:\
                ${this.theme.color};`
    },
    submitStyles: function(){
      return `--subBckGrndClr:\
                ${this.theme.green};\
              --subShadow:\
                0px calc(var(--formWidth) * .00925) 0 0 ${this.theme.medGreen};\
              --subBckGrnd:\
                linear-gradient(\
                  to top right,\
                  ${this.theme.lightGreen},\
                  ${this.theme.green}\
                );\
              --subHovBckGrndClr:\
              ${this.theme.lightGreen};\
              --subHovShadow: 0px calc(var(--formWidth) * .00925) 0 0 ${this.theme.green};\
              --subHovBckGrnd:\
                linear-gradient(\
                  to top right,\
                  ${this.theme.green},\
                  ${this.theme.lightGreen}\
                );`
    },
    linkStyles: function(){
      return `--tl: ${this.theme.medGreen};\
              --tlh: ${this.theme.green};\
              --tla: ${this.theme.lightGreen};`
    }
  },
  methods: {
    async grabShelters(){
      const body = {
        coordinates: this.location,
        proximity: 0
      }
      await this.aAddSheltersUser(body)
    },
    // root actions
    ...mapActions([
      "aAddStates",
      "aCitiesByState",
      "aSetLocation",
      'wait',
      'aAddSheltersUser'
      ]),
    // login actions
    ...mapActions(
      "login", [
        "aHandleBlur",
        "aHandleChange",
        "aHandleSubmit",
        "aToggleRegistration",
        "aToggleAuth",
        "charCheck",
        'aClearForm',
        'aSetPhoneNumber',
        'aLocationAutofill'
        ]
    ),
      // auth actions
    ...mapActions(
    "auth", [
      "checkToken"
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
    },
    async formUpdate(){
      const wait = await this.wait(10)
      if(this.user_auth){
      wait
      Object.keys(this.userForm).forEach(key =>
      this.userForm[key].value !== '' && (document.querySelector(`[name="${key}"]`).value = this.userForm[key].value)
      )
      }else{
        wait
        Object.keys(this.shelterForm).forEach(key =>
        this.shelterForm[key].value !== '' && (document.querySelector(`[name="${key}"]`).value = this.shelterForm[key].value)
        )
      }
      if(this.registration){
        wait
        Object.keys(this.userLocation).forEach(key =>
        this.userLocation[key].value !== '' && (document.querySelector(`[name="${key}"]`).value = this.userLocation[key].value)
        )
      }
    },
    styling(){
      // input styling
    document.querySelectorAll('input').forEach(inp => {
      inp.style = this.inpStyles
    })
    // toggle link styling
    document.querySelectorAll('.toggleLink').forEach(link => {
      link.style = this.linkStyles
    })
    // error div styling
    const divList = ['.inpSec']
    this.registration && divList.push('.preSec')
    divList.forEach( secType => {
      document.querySelectorAll(secType).forEach( sec => {
        sec.classList.contains("inpSec") && sec.classList.contains("neutral") && (sec.children[1].style = this.errDivStyles)
        sec.classList.contains("preSec") && sec.classList.contains("neutral") && (sec.children[3].style = this.errDivStyles)
        sec.classList.contains("inpSec") && !sec.classList.contains("neutral") && (sec.children[1].style = '')
        sec.classList.contains("preSec") && !sec.classList.contains("neutral") && (sec.children[3].style = '')
      })
    })
    },
    async locationAutofill(){
        const location = await this.aLocationAutofill(this.location)
        if(location){
          Object.keys(location).forEach(key => {
            document.querySelector(`input[name="${key}"]`) &&
            (document.querySelector(`input[name="${key}"]`).value = location[key])
          })
      }
    },
  },
  watch:{
    'userLocation.state.value' : function(){
      if (this.registration){
        if(this.states.includes(this.userLocation.state.value)){
        this.aCitiesByState(this.userLocation.state.value)
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
    zipcode_list: function(){
      if(this.registration && this.city_list.includes(this.userLocation.city.value)){
        document.querySelector("#zipInp").placeholder = "zipcode"
        document.querySelector("#zipInp").disabled = false
      }
    },
    validVals: function(newVal, oldVal){
      if(newVal.includes("password valid")){
        document.querySelector(`[name="confirm"]`).disabled = false
      } else {
        document.querySelector(`[name="confirm"]`).disabled = true
      }


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
            document.querySelector('[name="phone_number"]').value = this.phoneNumber
            this.aSetPhoneNumber(this.phoneNumber)
          } else if (this.phoneNumber.length === 5) {
            this.phoneNumber = `${this.phoneNumber.slice(0,4)})-${this.phoneNumber.slice(4)}`
            document.querySelector('[name="phone_number"]').value = this.phoneNumber
            this.aSetPhoneNumber(this.phoneNumber)
          } else if (this.phoneNumber.length === 10) {
            this.phoneNumber = `${this.phoneNumber.slice(0,9)}-${this.phoneNumber.slice(9)}`
            document.querySelector('[name="phone_number"]').value = this.phoneNumber
            this.aSetPhoneNumber(this.phoneNumber)
          }
        }
        if(newVal.length < oldVal.length){
          if(newVal.length === 10){
            this.phoneNumber = this.phoneNumber.slice(0,9)
            document.querySelector('[name="phone_number"]').value = this.phoneNumber
            this.aSetPhoneNumber(this.phoneNumber)
          }
          if(newVal.length === 6){
            this.phoneNumber = this.phoneNumber.slice(0,4)
            document.querySelector('[name="phone_number"]').value = this.phoneNumber
            this.aSetPhoneNumber(this.phoneNumber)
          }
          if(newVal.length === 1){
            this.phoneNumber = ''
            document.querySelector('[name="phone_number"]').value = this.phoneNumber
            this.aSetPhoneNumber(this.phoneNumber)
          }
        }
      }
    },
    registration: function(){
      this.formUpdate('reg')
    },
    user_auth: function(){
      this.formUpdate('auth')
    },
    location: function(){
      this.locationAutofill()
    }
  },
}
</script>

<style>
/* html tags */
form{
  display: flex;
  align-items: center;
  justify-content: flex-start;
  flex-direction: column;
  font-size: var(--fontSize);
  padding: 0 calc(var(--formWidth) * .037) 0 calc(var(--formWidth) * .037);
  align-content: space-between;
}
h1{
  margin: calc(var(--formWidth) * .037);
  padding: 0;
  justify-self: start;
}
input{
  border: none;
  padding-left: calc(var(--formWidth) * .00925);
  width: var(--inpWidth);
  height: calc(var(--formWidth) * .04625);
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
.inpSec > div{
  display: flex;
  max-width: inherit;
}
.inpDiv{
  width: inherit;
  flex-direction: row;
  justify-content: space-between;
}
[name='password'],[name='confirm'] {
  padding-right: calc(var(--formWidthS) * .049);
}
.btmInp{
  margin-bottom: calc(var(--formWidth) * .01);
}

.errDiv{
  font-size: calc(var(--fontSize) * .77);
  max-width: inherit;
  flex-direction: row-reverse;
  justify-content: flex-start;
  color: black;
}
.errDiv2{
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: calc(var(--fontSize) * .77);
  color: black;
  position: relative;
  justify-self: center;
}
.charCount{
  width: calc(var(--inpWidth) * .11);
  text-align: right;
}
.errMsg{
  width: calc(var(--inpWidth) - calc(var(--inpWidth) * .115));
}
.errMsg2{
  text-align: center;
}
.errMsg2.state{
  width: calc(var(--formWidth) * .1665);
}
.errMsg2.zipcode{
  width: calc(var(--formWidth) * .1665);
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
  height: calc(var(--formWidth) * .074);
}
#cityInp{
  width: calc(var(--formWidth) * .3145);
  margin: 0;
  text-align: center;
}
#stateInp{
  width: calc(var(--formWidth) * .1665);
  margin: 0;
  text-align: center;
}
#zipInp{
  width: calc(var(--formWidth) * .1665);
  margin: 0;
  text-align: center;
}
.valid > .errDiv,.valid > .errDiv2{
  color:green
}
.invalid > .errDiv,.invalid > .errDiv2{
  color:rgb(214, 16, 16)
}
.valid > * > input{
  border: calc(var(--formWidth) * .0037) solid green;
}
.invalid > * > input{
  border: calc(var(--formWidth) * .0037) solid rgb(214, 16, 16);
}
.neutral > * > input{
  border: none;
}
.valid > input{
  border: calc(var(--formWidth) * .0037) solid green;
}
.invalid > input{
  border: calc(var(--formWidth) * .0037) solid rgb(214, 16, 16);
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
  margin: calc(var(--formWidth) * .00925);
}
#sub{
  background-color: var(--subBckGrndClr);
  background: var(--subBckGrnd);
  box-shadow: var(--subShadow);
  text-align: center;
  padding: calc(var(--formWidth) * .004) calc(var(--formWidth) * .01295);
  border-radius: 20px;
}
#sub:hover{
  background-color: var(--subHovBckGrndClr);
  background: var(--subHovBckGrnd);
  box-shadow: var(--subHovShadow);
}
#sub:active{
  box-shadow: none;
  margin-top: calc(var(--formWidth) * .0185);
}
#btnDiv{
  height: calc(var(--formWidth) * .0555);
  display: flex;
  margin-top: 0;
  align-items: center;
  justify-content: center;
}


.showPasswordBtn {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: calc(var(--formWidth) * .00925);
  margin-left: calc(var(--formWidth)* 0.735);
}
.sheltShowPasswordBtn {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: calc(var(--formWidth) * .00925);
  margin-left: calc(var(--formWidth)* 0.735);
}
.showPassword{
  width: calc(var(--formWidth) * .037);
}
.hidePassword{
  width: calc(var(--formWidth) * .0296);
  height: calc(var(--formWidth) * .0222);
  margin: calc(var(--formWidth) * .00333)
    calc(var(--formWidth) * .002775)
    calc(var(--formWidth) * .004625)
    calc(var(--formWidth) * .00444);
}


.toggleLink{
  color: var(--tl);
  text-decoration: underline;
}
.toggleLink:hover{
  color: var(--tlh);

}
.toggleLink:active{
  color: var(--tla);
}


.error {
    position: relative;
    animation: shake .1s linear;
    -webkit-animation: shake .1s linear;
    -moz-animation: shake .1s linear;
    animation-iteration-count: 3;
    -webkit-animation-iteration-count: 3;
    -moz-animation-iteration-count: 3;
}
@-webkit-keyframes shake {
    0% { top: calc(var(--formWidth) * -.0037); }
    100% { bottom: calc(var(--formWidth) * -.0037)w; }
}
@-moz-keyframes shake {
    0% { top: calc(var(--formWidth) * -.0037); }
    100% { bottom: calc(var(--formWidth) * -.0037); }
}
@keyframes shake {
    0% { top: calc(var(--formWidth) * -.0037); }
    100% { bottom: calc(var(--formWidth) * -.0037); }
}
</style>