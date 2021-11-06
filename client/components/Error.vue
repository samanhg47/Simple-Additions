<template>
  <section :style="`display:${display};`" id="errorSec">
    <div id="errorDiv">
      <h1>Error: {{status}}</h1>
      <div id="errorMsgDiv">
        <p v-html="msg" id="errorMsg"></p>
        <button type="button" @click="aPassError(200, '')">OK</button>
      </div>
    </div>
  </section>
</template>

<script>
import { mapState, mapActions } from "vuex"
export default {
  computed: {
    ...mapState(
      "error", [
        "msg", 'status'
        ]),
    display: function(){
      return this.status >= 300 ? "flex" : "none"
    }
  },
  methods: {
    ...mapActions('error', [
      'aPassError'
    ])
  }
}
</script>

<style scoped>
#errorSec{
  background: rgba(0, 0, 0, 0.466);
  height: inherit;
  width: inherit;
  position: absolute;
  z-index: 5;
}
#errorDiv{
  height: 20vw;
  width: 25vw;
  display: flex;
  flex-flow: wrap;
}
</style>