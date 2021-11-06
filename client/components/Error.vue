<template>
  <section id="errorSec">
    <div id="errorDiv">
      <h1>Error: {{status}}</h1>
      <div id="errorMsgDiv">
        <p v-html="msg" id="errorMsg"></p>
      </div>
    </div>
  </section>
</template>

<script>
import {mapState} from "vuex"
export default {
  computed: {
    ...mapState("error"["msg", 'status'])
  }
}
</script>

<style scoped>
#errorSec{
  background: rgba(0, 0, 0, 0.466);
  height: inherit;
  width: inherit;
}
#errorDiv{
  height: 20vw;
  width: 25vw
}
</style>