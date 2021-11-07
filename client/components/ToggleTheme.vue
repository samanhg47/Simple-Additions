<template>
  <section id='btnSec'>
    <div id="themeDiv">
      <button id='iconBtn' @click="modeToggle">
        <img src="../assets/sunIcon.png" alt="Sun Icon" :style="sunIcon"/>
        <img src="../assets/moonIcon.png" alt="Moon Icon" :style="moonIcon"/>
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
    moonIcon: function(){
      let z = this.focused ? 'zIndex: 2;' : 'zIndex: 3;'
      let o = this.focused ? 'opacity: 0;' : 'opacity: 1;'
      return `position:relative;\
              ${z}\
              ${o}`
    },
    sunIcon: function(){
      let z = this.focused ? 'zIndex: 3;' : 'zIndex: 2;'
      let o = this.focused ? 'opacity: 1;' : 'opacity: 0;'
      return `position:absolute;\
              ${z}\
              ${o}`
    },
    div: function(){
      let val = this.mode ? '40.2vw' : '40.32vw'
      return `margin-top: ${val}`
    }
  },
  methods: {
    ...mapActions(
      'theme',[
        'aLightMode',
        'aDarkMode'
      ]
    ),
    wait(delay){
      return new Promise(resolve => setTimeout(resolve, delay))
      },
    async modeToggle(){
      const iconBtn = document.getElementById('iconBtn')
      const imgs = document.querySelectorAll('img')

      iconBtn.style.boxShadow = 'none'
      iconBtn.classList.add('shrink')
      imgs.forEach( img => img.classList.add('spin'))
      await this.wait(300)
      iconBtn.classList.remove('shrink'),
      imgs.forEach( img => img.classList.remove('spin'))

      this.focused = this.focused ? false : true
      iconBtn.classList.add('grow')
      imgs.forEach( img => img.classList.add('unspin'))
      await this.wait(300)
      iconBtn.classList.remove('grow')
      imgs.forEach( img => img.classList.remove('unspin'))

      this.focused ? this.aLightMode() : this.aDarkMode()
      this.mode 
      ? iconBtn.style.boxShadow = '0 0 8vw 3vw #FFC30E'
      : iconBtn.style.boxShadow = '0 0 8vw 3vw #9D9D9D'
      iconBtn.classList.add('settle')
      imgs.forEach( img => img.classList.add('adj'))
      await this.wait(150)
      iconBtn.classList.remove('settle')
      imgs.forEach( img => img.classList.remove('adj'))
    },
  },
}
</script>

<style scoped>
template{
  width: inherit;
  height: inherit;
}
#btnSec{
  display: flex;
  justify-content: center;
  align-items: center;
  width: inherit;
  height: inherit;
}
#themeDiv{
  z-index: 2;
  position: absolute;
}
#iconBtn{
  width: .5vw;
  height: .5vw;
  border-radius: 100%;
  box-shadow: 0 0 5vw 2.5vw #FFC30E;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 4.1vw;
}

img{
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
  animation: unspin .32s linear;
  -webkit-animation: unspin .32s linear;
  -moz-animation: unspin .32s linear;
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
.adj{
  animation: adj .17s linear;
  -webkit-animation: adj .17s linear;
  -moz-animation: adj .17s linear;
  animation-iteration-count: 1;
  -webkit-animation-iteration-count: 1;
  -moz-animation-iteration-count: 1;
}
@keyframes adj {
  0% {transform: rotate(-30deg);}
  100% {transform: rotate(0deg);}
}
@-webkit-keyframes adj {
  0% {transform: rotate(-30deg);}
  100% {transform: rotate(0deg);}
}
@-moz-keyframes adj {
  0% {transform: rotate(-30deg);}
  100% {transform: rotate(0deg);}
}
</style>