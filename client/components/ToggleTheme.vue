<template>
  <section id='btnSec'>
    <h1 :style="h1">{{mode?"Light":"Dark"}} Mode</h1>
    <div id="themeDiv">
      <button id='iconBtn' @click="modeToggle">
        <img src="../assets/sunIcon.png" alt="Sun Icon" class="modeIcon" :style="sunIcon"/>
        <img src="../assets/moonIcon.png" alt="Moon Icon" class="modeIcon" :style="moonIcon"/>
      </button>
    </div>
  </section>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'
export default {
  data: ()=>({
    focused: true
  }),
  computed: {
    ...mapState(
      'theme',[
        'mode'
      ]
    ),
    ...mapGetters(
      'theme',[
        'theme'
      ]
    ),
    h1: function () {
      return `color:\
                ${this.theme.color};\
              margin:\
                0 0 .5vw 0;\
              font-size:\
                var(--fontSize);`
    },
    moonIcon: function(){
      let d = this.focused ? 'none' : 'flex'
      let o = this.focused ? 'opacity: 0;' : 'opacity: 1;'
      return `display:${d};\
              ${o}`
    },
    sunIcon: function(){
      let d = this.focused ? 'flex' : 'none'
      let o = this.focused ? 'opacity: 1;' : 'opacity: 0;'
      return `display:${d};\
              ${o}`
    },
  },
  methods: {
    ...mapActions(
      'theme',[
        'aLightMode',
        'aDarkMode'
      ]
    ),
    ...mapActions([
      'wait'
    ]),
    async modeToggle(){
      const iconBtn = document.getElementById('iconBtn')
      const imgs = document.querySelectorAll('.modeIcon')

      iconBtn.style.boxShadow = 'none'
      iconBtn.classList.add('spin')
      imgs.forEach( img => img.classList.add('shrink'))
      await this.wait(300)
      iconBtn.classList.remove('spin')
      imgs.forEach( img => img.classList.remove('shrink'))

      this.focused = this.focused ? false : true
      iconBtn.classList.add('unspin')
      imgs.forEach( img => img.classList.add('grow'))
      await this.wait(300)
      iconBtn.classList.remove('unspin')
      imgs.forEach( img => img.classList.remove('grow'))

      this.focused ? this.aLightMode() : this.aDarkMode()
      this.mode 
      ? iconBtn.style.boxShadow = '0 0 8vw 3vw #FFC30E'
      : iconBtn.style.boxShadow = '0 0 8vw 3vw #9D9D9D'
      iconBtn.classList.add('settle')
      await this.wait(150)
      iconBtn.classList.remove('settle')
    },
  },
}
</script>

<style>
template{
  width: inherit;
  height: inherit;
}
#btnSec{
  display: flex;
  justify-content: space-between;
  flex-direction: row;
  align-items: center;
  width: 55.6%;
  height: calc(var(--formWidth) * .074);
}
#themeDiv{
  width: 20%;
  height: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: calc(var(--formWidth) * .0034);
}
#iconBtn{
  width: 10%;
  height: 10%;
  border-radius: 100%;
  box-shadow: 0 0 5vw 2.5vw #FFC30E;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modeIcon{
  width: 650%;
}

.shrink{
  animation: shrink .32s linear;
  -webkit-animation: shrink .32s linear;
  -moz-animation: shrink .32s linear;
  animation-iteration-count: 1;
  -webkit-animation-iteration-count: 1;
  -moz-animation-iteration-count: 1;
}
@keyframes shrink {
    from {
      transform: scale(1);}
    to {
      transform: scale(.1); }
}
@-webkit-keyframes shrink {
    from {
      transform: scale(1);}
    to {
      transform: scale(.1); }
}
@-moz-keyframes shrink {
    from {
      transform: scale(1);}
    to {
      transform: scale(.1); }
}
.grow{
  animation: grow .32s linear;
  -webkit-animation: grow .32s linear;
  -moz-animation: grow .32s linear;
  animation-iteration-count: 1;
  -webkit-animation-iteration-count: 1;
  -moz-animation-iteration-count: 1;
}
@keyframes grow {
  from {
    transform: scale(.1);}
    to {
      transform: scale(1.3); }
}
@-webkit-keyframes grow {
  from {
    transform: scale(.1);}
    to {
      transform: scale(1.3); }
}
@-moz-keyframes grow {
  from {
    transform: scale(.1);}
    to {
      transform: scale(1.3); }
}
.settle{
  animation: settle .17s linear;
  -webkit-animation: settle .17s linear;
  -moz-animation: settle .17s linear;
  animation-iteration-count: 1;
  -webkit-animation-iteration-count: 1;
  -moz-animation-iteration-count: 1;
}
@keyframes settle {
  from {
    transform: scale(1.3);}
    to {
      transform: scale(1); }
}
@-webkit-keyframes settle {
  from {
    transform: scale(1.3);}
    to {
      transform: scale(1); }
}
@-moz-keyframes settle {
  from {
    transform: scale(1.3);}
    to {
      transform: scale(1); }
}
.spin{
  animation: spin .32s linear;
  -webkit-animation: spin .32s linear;
  -moz-animation: spin .32s linear;
  animation-iteration-count: 1;
  -webkit-animation-iteration-count: 1;
  -moz-animation-iteration-count: 1;
}
@keyframes spin {
  100% {transform: rotate(180deg);}
}
@-webkit-keyframes spin {
  100% {transform: rotate(180deg);}
}
@-moz-keyframes spin {
  100% {transform: rotate(180deg);}
}
.unspin{
  animation: unspin .33s linear;
  -webkit-animation: unspin .33s linear;
  -moz-animation: unspin .33s linear;
  animation-iteration-count: 1;
  -webkit-animation-iteration-count: 1;
  -moz-animation-iteration-count: 1;
}
@keyframes unspin {
  0% {transform: rotate(180deg);}
  100% {transform: rotate(-30deg);}
}
@-webkit-keyframes unspin {
  0% {transform: rotate(180deg);}
  100% {transform: rotate(-30deg);}
}
@-moz-keyframes unspin {
  0% {transform: rotate(180deg);}
  100% {transform: rotate(-30deg);}
}
</style>