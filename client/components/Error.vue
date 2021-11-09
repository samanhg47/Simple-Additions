<template>
  <section :style="`display:${display};`" id="errorSec">
    <div id="errorDiv" :style="errorDiv">
      <h1>Error: {{status}}</h1>
      <div id='msgDiv' :style="msgDiv">
        <p v-html="msg" id="errorMsg"></p>
        <div id='btnDiv'>
          <button :style="btnStyles" type="button" @click="aPassError({status:200, msg:''})">
            OK
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex"
export default {
  computed: {
    ...mapState(
      "error", [
        "msg",
        'status'
      ]
    ),
    ...mapState(
      'theme',[
        'mode'
      ]
    ),
    ...mapGetters(
      'theme', [
        'theme'
      ]
    ),
    display: function(){
      return this.status >= 300 ? "flex" : "none"
    },
    errorDiv: function(){
      let shadow = this.mode ? '0 0 6vw 1vw rgb(214, 16, 16)' : '0 0 6vw 1vw rgba(214, 16, 16, 0.6)'
      return `backgroundColor:\
                ${this.theme.green};\
              boxShadow:\
                ${shadow};\
              background:\
                linear-gradient(\
                  to top right,\
                  ${this.theme.lightSecondary},\
                  ${this.theme.darkSecondary}\
                  );\
              color:\
                ${this.theme.color}`
    },
    msgDiv: function(){
      return `backgroundColor:\
                ${this.theme.lightSecondary};\
              color:\
                ${this.theme.color};\
              background:\
                linear-gradient(\
                  to top right,\
                  ${this.theme.medGreen},\
                  ${this.theme.darkGreen}\
                );`
    },
    btnStyles: function(){
      return `width:\
                8vw;\
              --subBckGrndClr:\
                ${this.theme.darkSecondary};\
              --subShadow:\
                0px .6vw 0 0 ${this.theme.darkSecondary};\
              --subBckGrnd:\
                linear-gradient(\
                  to top right,\
                  ${this.theme.darkSecondary},\
                  ${this.theme.lightSecondary}\
                );\
              --subHovBckGrndClr:\
              ${this.theme.lightSecondary};\
              --subHovShadow: 0px .6vw 0 0 ${this.theme.lightSecondary};\
              --subHovBckGrnd:\
                linear-gradient(\
                  to top right,\
                  ${this.theme.lightSecondary},\
                  ${this.theme.darkSecondary}\
                );`
    },
  },
  methods: {
    ...mapActions(
      'error', [
      'aPassError'
      ]
    ),
    ...mapActions([
      'wait'
    ])
  },
  watch: {
    display: async function(){
      if(this.display==='flex'){
        document.querySelector('#errorSec').classList.add('error')
        await this.wait(300)
        document.querySelector('#errorSec').classList.remove('error')
      }
    }
  }
}
</script>

<style scoped>
#errorSec{
  background: rgba(0, 0, 0, 0.719);
  justify-content: center;
  align-items: center;
  height: inherit;
  width: inherit;
  position: absolute;
  z-index: 5;
}
#msgDiv{
  text-align: center;
  font-size: 2vw;
  padding: 1vw;
}
#errorDiv{
  width: 55vw;
  text-align: center;
  padding: 1vw 2vw 2vw 2vw;
  border-radius: 20px;
}
h1{
  margin: 0 auto 1vw auto;
  color: rgb(214, 16, 16);
  font-size: 3vw;
}
button{
  background-color: var(--subBckGrndClr);
  background: var(--subBckGrnd);
  box-shadow: var(--subShadow);
  padding: .3vw .7vw;
  border-radius: 5px;
  font-size: 1.5vw;
}
button:hover{
  background-color: var(--subHovBckGrndClr);
  background: var(--subHovBckGrnd);
  box-shadow: var(--subHovShadow);
}
button:active{
  box-shadow: none;
  margin-top: .6vw;
}
#btnDiv{
  height: 4vw;
  margin-top: 1.5vw;
  display: flex;
  align-items: flex-start;
  justify-content: center;
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
    0% { top: -.7vw; }
    100% { bottom: -.7vw; }
}
@-moz-keyframes shake {
    0% { top: -.7vw; }
    100% { bottom: -.7vw; }
}
@keyframes shake {
    0% { top: -.7vw; }
    100% { bottom: -.7vw; }
}
</style>