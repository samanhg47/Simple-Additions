<template>
  <form @submit.prevent="console.log('hi');aHandleSubmit()">
    <h1 v-if="registration">Register</h1>
    <h1 v-if="!registration">Login</h1>
    <div v-for="(field,index) in userForm" :key="index" class="inputCont">
      <section class="inpSec" :class="field.class">
        <div class="inpDiv">
          <label :for="index">{{field.for}}:</label>
          <button v-if='index === "password"' class="showPasswordBtn" type='button' @mousedown="showPass(index)" @mouseup="hidePass(index)">
            <img v-if='index === "password" && hidePassword' class="showPassword" src='../assets/hiddenPassword.png' alt='Show Password Icon'/>
            <img v-if='index === "password" && !hidePassword' class="hidePassword" src='../assets/shownPassword.png' alt='Show Password Icon'/>
          </button>
          <button v-if='index === "confirm"' class="showPasswordBtn" type='button' @mousedown="showPass(index)" @mouseup="hidePass(index)">
            <img v-if='index === "confirm" && hideConfirm' class="showPassword" src='../assets/hiddenPassword.png' alt='Show Password Icon'/>
            <img v-if='index === "confirm" && !hideConfirm' class="hidePassword" src='../assets/shownPassword.png' alt='Show Password Icon'/>
          </button>
          <input @input="aHandleChange($event)" @keypress.enter="aHandleSubmit()" @blur="aHandleBlur($event)"
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
      <div class="location">
        <div v-for="(field,index) in userLocation" :key="index" class="inputCont">
          <section v-if="registration" :class="`preSec ${field.class}`">
            <label v-if="index === 'state'" :for="index">{{field.for}}</label>
            <input v-if="index === 'state'" list="state_list" :name='index' id="stateInp" placeholder="state" @blur="aHandleBlur($event)" @change="aHandleChange($event)"/>
            <datalist v-if="index === 'state'" :name="index" id="state_list">
              <option v-for="state in states" :key="state" :value="state">{{state}}</option>
            </datalist>
            <label v-if="index === 'city'" :for="index">{{field.for}}</label>
            <input v-if="index === 'city'" disabled list="city_list" :name='index' id="cityInp" placeholder="city" @blur="aHandleBlur($event)" @change="aHandleChange($event)"/>
            <datalist v-if="index === 'city'" :name="index" id="city_list">
              <option v-for="city in city_list" :key="city" :value="city">{{city}}</option>
            </datalist>
            <label v-if="index === 'zipcode'" :for="index">{{field.for}}</label>
            <input v-if="index === 'zipcode'" disabled list="zipcode_list" :name="index" id="zipInp" placeholder="zipcode" @change="aHandleChange($event)" @blur="aHandleBlur($event)"/>
            <datalist v-if="index === 'zipcode'" :name="index" id="zipcode_list">
              <option v-for="zipcode in zipcode_list" :key="zipcode" :value="zipcode" class="zip">{{zipcode}}</option>
            </datalist>
            <div class="errDiv2">
              <p v-if="field.msg" class="errMsg2">{{field.msg}}</p>
            </div>
          </section>
        </div>
      </div>
    <div id='btmDiv'>
      <button type="submit" v-if="registration" id="sub">Register</button>
      <button type="submit" v-if="!registration" id="sub">Login</button>
      <button @click.prevent="aToggleRegistration" type='button' v-if="registration">Returning user? Click here for login.</button>
      <button @click.prevent="aToggleRegistration" type='button' v-if="!registration">New user? Click here to register.</button>
    </div>
  </form>
</template>
<script>
import {mapState, mapGetters, mapActions} from "vuex"
export default {
  async created(){
    await this.getStates()
  },
  data: ()=>({
    hidePassword: true,
    hideConfirm: true
  }),
  computed: {
    ...mapState(
      "login",[
        "user_auth",
        "registration"
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
      Object.keys(this.userForm).forEach(key => {
        validity.push(this.userForm[key].class)
      })
      Object.keys(this.userLocation).forEach(key => {
        validity.push(this.userLocation[key].class)
      })
      return validity
    }
  },
  watch:{
    'userLocation.state.value' : function(){
      if (this.registration){
        document.querySelector("#cityInp").value = ""
        const zips = document.querySelectorAll("option .zip")
        zips.forEach( zip => zip.remove())
        document.querySelector("#cityInp").placeholder = "...loading"
        document.querySelector("#cityInp").disabled = true
      }
    },
    city_list: function(){
      if(this.registration){
        document.querySelector("#cityInp").placeholder = "city"
        document.querySelector("#cityInp").disabled = false
      }
    },
    validVals: function(){
      if(this.validVals.includes("invalid")){
        document.getElementById("sub").disabled = true
      }else{
        document.getElementById("sub").disabled = false
      }
    },
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
        "aToggleRegistration"
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
    }
  }
}
</script>

<style>
form{
  display: flex;
  align-items: center;
  justify-content: flex-start;
  width: inherit;
  flex-direction: column;
  height: inherit;
  font-size: 1.8vw;
  padding: 0 2vw 0 2vw;
  align-content:space-between;
}

.inputCont{
  width: 100%;
  margin: auto;
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
}
h1{
  margin: 2vw;
  padding: 0;
  justify-self: start;
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
  max-width: inherit;
  align-items: center;
  justify-content: center;
  justify-content: space-between;
  color: black
}
.errMsg{
  margin-left: 14vw;
}
.preSec{
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
.location{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
}
#cityInp{
  width: 17vw;
  margin: 0 .5vw 0 .5vw;
  background-color: rgba(0, 0, 0, 0.137);
  text-align: center;
}
#stateInp{
  width: 7vw;
  margin: 0 .5vw 0 .5vw;
  background-color: rgba(0, 0, 0, 0.137);
  text-align: center;
}
#zipInp{
  width: 9vw;
  margin: 0 .5vw 0 .5vw;
  background-color: rgba(0, 0, 0, 0.137);
  text-align: center;
}
.valid > .errDiv,.errDiv2{
  color:green
}
.invalid > .errDiv,.errDiv2{
  color:rgb(214, 16, 16)
}
.valid > * > input,select{
  border: .2vw solid green;
}
.invalid > * > input,select{
  border: .2vw solid rgb(214, 16, 16);
}
.neutral > * > input,select{
  border: none;
}
.valid > input,select{
  border: .2vw solid green;
}
.invalid > input,select{
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
#btmDiv > *{
  /* margin: .5vw; */
}

.showPasswordBtn {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: .4vh;
  margin-left: 33.8vw;
}
.showPassword{
  width: 2vw;
}
.hidePassword{
  width: 1.6vw;
  height: 1.2vw;
  margin: .18vw .15vw .25vw .24vw;
}
</style>