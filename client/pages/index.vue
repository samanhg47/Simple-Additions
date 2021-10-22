<template>
  <form @submit.prevent="aHandleSubmit()" class="flex">
    <img src="../assets/saLogo.png"/>
    <h1 v-if="registration">Register</h1>
    <h1 v-if="!registration">Login</h1>
    <div v-for="(field,index) in userForm" :key="index" class="inputCont">
      <section class="inpSec">
        <div class="inpDiv">
          <label :for="index">{{field.for}}:</label>
          <i></i>
          <input @input="aHandleChange($event)" @keypress.enter="aHandleSubmit()" @blur="aHandleBlur($event)"
          :name="index"
          :type="field.type"
          :placeholder="field.placeholder"
          :class="field.class"
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
          <section v-if="registration" class="preSec">
            <label v-if="index === 'state'" :for="index">{{field.for}}</label>
            <select v-if="index === 'state'" :name="index" @change="aHandleChange($event);getCities($event)">
              <option value="state" >state ▾</option>
              <option v-for="state in states" :key="state" :value="state">{{state}}</option>
            </select>
            <label v-if="index === 'city'" :for="index">{{field.for}}</label>
            <input v-if="index === 'city'" list="city_list" :name='index' id="cityInp" placeholder="city"  @change="aHandleChange($event)"/>
            <datalist v-if="index === 'city'" :name="index" id="city_list">
              <option v-for="city in city_list" :key="city" :value="city">{{city}}</option>
            </datalist>
            <label v-if="index === 'zipcode'" :for="index">{{field.for}}</label>
            <select v-if="index === 'zipcode'" :name="index" @change="aHandleChange($event)">
              <option value="zipcode">zipcode ▾</option>
              <option v-for="zipcode in zipcode_list" :key="zipcode" :value="zipcode" class="zip">{{zipcode}}</option>
            </select>
            <div class="errDiv2 flex">
          <p v-if="field.msg" class="errMsg">{{field.msg}}</p>
        </div>
          </section>
        </div>
      </div>
    <div>
      <button type="submit" v-if="registration" id="sub">Register</button>
      <button type="submit" v-if="!registration" id="sub">Login</button>
    </div>
    <p @click="aToggleRegistration" v-if="registration">Returning user? Click here for login.</p>
    <p @click="aToggleRegistration" v-if="!registration">New user? Click here to register.</p>
  </form>
</template>

<script>
import {mapState, mapGetters, mapActions} from "vuex"
export default {
  async created(){
    await this.getStates()
  },
  // data: () => ({
  //   valid: true
  // }),
  computed: {
    ...mapState("login", ["user_auth", "registration"]),
    ...mapState(["states"]),
    ...mapGetters(["city_list", "zipcode_list"]),
    ...mapGetters("login", ["userForm", "shelterForm", "userLocation"]),
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
    validVals: function(){
        if(this.validVals.includes("invalid")){
          document.getElementById("sub").disabled = true
        }else{
          document.getElementById("sub").disabled = false
        }
      },
    city_list: function(){
      if(this.registration){
        document.querySelector("#cityInp").placeholder = "city"
        document.querySelector("#cityInp").disabled = false
        }
    },
  },

  methods: {
    ...mapActions(["getStates", "getCities"]),
    ...mapActions("login", ["aHandleBlur", "aHandleChange", "aHandleSubmit", "aToggleRegistration"]),
  }
}
</script>

<style>
form{
  width: inherit;
  flex-direction: column;
  height: inherit;
  font-size: 1.8vw;
  padding: 0 2vw 0 2vw;
  align-content:space-between;
}
form > *{
  margin: .2vw;
}
.inputCont{
  width: 100%
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
  margin: 0;
  padding: 0;
  justify-self: start;
}
.errDiv{
  font-size: 1.2vw;
  max-width: inherit;
  flex-direction: row-reverse;
  justify-content: space-between;
}
.errDiv2{
  font-size: 1.2vw;
  max-width: inherit;
  align-items: center;
  justify-content: center;
}
.invalid
.preSec{
  display: flex;
  justify-content: center;
  align-items: center;
}
.location{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
}
#cityInp{
  width: 17vw;
  margin: 0 2vw 0 2vw;
  background-color: rgba(0, 0, 0, 0);
  text-align: center;
}

</style>