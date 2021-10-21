<template>
  <form @submit.prevent="handleSubmit()">
        <div v-for="(field,index) in userForm" :key="index" class="inputCont flex">
          <label :for="index">{{field.for}}</label>
          <input @input="handleChange($event)" @keypress.enter="handleSubmit()" @blur="handleBlur($event)"
          :name="index"
          :type="field.type"
          :placeholder="field.placeholder"
          :class="field.class"
          />
          <!-- <div :class="field.class">
            <p v-if="field.msg" class="errMsg">{{field.msg}}</p>
            <p v-if="field.minLen">{{field.value.length}}/{{field.minLen}}</p>
          </div> -->
        </div>
        <div>
          <button type="submit">Login/Register</button>
          <button type="toggle">Shelters Login/Register Here</button>
        </div>
      </form>
</template>

<script>
import {mapState, mapGetters, mapActions, mapMutations} from "vuex"
export default {
  computed: {
    ...mapState("login", ["user_form"]),
    ...mapGetters("login", ["userForm"])

  },
  methods: {
    ...mapActions("login", ["checkIfInvalid", "handleChange"])
  }
  // name: "index",
  // props:["form"],
  // methods: {
  //   console(){
  //     console.log(form)
  //   }
  // }
}
</script>
