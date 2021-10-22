<template>
  <form class="flex">
    <img src="../assets/saLogo.png"/>
    <h1 v-if="!update">Welcome {{currentUser.user_name}}!</h1>
    <h1 v-if="update">Update</h1>
      <section v-if="update" class="inpSec">
    <div class="inputCont">
        <div class="inpDiv">
          <label for="user_name">Username:</label>
          <input @input="aHandleChange($event)" @blur="aHandleBlur($event)"
          name="user_name"
          type="text"
          :placeholder="currentUser.user_name"
          :class="userForm.user_name.class"
          />
        </div>
        <div class="errDiv">
          <p v-if="userForm.user_name.minLen" class="charCount">{{userForm.user_name.value.length}}/{{userForm.user_name.minLen}}</p>
          <p v-if="userForm.user_name.msg" class="errMsg">{{userForm.user_name.msg}}</p>
        </div>
    </div >
      </section>
      <div v-if="!update" class="location">
          <h1>Username: {{currentUser.user_name}}</h1>
      </div>
    <div>
      <button type="click" v-if="update" @click.prevent="aHandleUpdate" id="sub">Update</button>
      <button type="delete" v-if="update" @click.prevent="aHandleDelete">Delete</button>
      <button type="click" v-if="!update" @click.prevent="aToggleUpdate" >Update/Delete Profile</button>
      <button type="click" v-if="update" @click.prevent="aToggleUpdate" >Abort</button>
    </div>
  </form>
</template>

<script>
import {mapState, mapGetters, mapActions} from "vuex"
export default {
  async created(){
    await this.getStates()
  },
  computed: {
    ...mapState("login", ["user_auth", "registration"]),
    ...mapState(["states", "currentUser"]),
    ...mapState("updateUser", ["update"]),
    ...mapGetters("login", ["userForm", "user"]),
  },

  methods: {
    ...mapActions(["getStates", "getCities"]),
    ...mapActions("login", ["aHandleBlur", "aHandleChange", "aHandleSubmit", "aToggleRegistration"]),
    ...mapActions("updateUser", ["aToggleUpdate", "aHandleUpdate", "aHandleDelete"]),
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