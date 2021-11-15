<template>
  <div id="contDiv" :style="contDivStyles" >
    <Error />
    <div class='logoDiv' :style="logoStyles">
      <img src="../assets/saLogoDark.png" :style="darkStyles" />
      <img src="../assets/saLogo.png" :style="lightStyles" />
    </div>
    <section class="formCont" :style="formContStyles" >
      <section class="inputSec" :style="inpSecStyles">
        <Nuxt />
      </section>
      <ToggleTheme />
    </section>
    <div class="logoDiv" :style="logoStyles">
      <img src="../assets/saLogoDark.png" :style="darkStyles" />
      <img src="../assets/saLogo.png" :style="lightStyles" />
    </div>
  </div>
</template>

<script>
import { mapGetters, mapState } from "vuex"
export default {
  data: () => ({
    display_class: null,
    formWid1: '88.07vw',
    formWid2: '95vw',
    formUlh: "calc(var(--formWidth) * .67504)",
    formUrh: "calc(var(--formWidth) * .82373)",
    formSlh: "calc(var(--formWidth) * .74977)",
    formSrh: "calc(var(--formWidth) * .95221)",
    logoWid: "calc(var(--formWidth) * .15789)",
  }),
  mounted(){
    window.addEventListener('resize', this.onResize)
    this.responsiveness()
  },
  beforeDestroy() { 
    window.removeEventListener('resize', this.onResize); 
    },
  computed: {
    ...mapGetters(
      "theme",[
        "theme"
      ]
    ),
    ...mapState(
      'login',[
        'user_auth',
        'registration'
      ]
    ),
    darkStyles: function(){
      return `boxShadow:${this.theme.shadow};\
              opacity:${this.theme.darkOpacity};\
              position: ${this.theme.darkPosition};\
              zIndex:${this.theme.darkZindex};`
    },
    lightStyles: function(){
      return `boxShadow:${this.theme.shadow};\
              opacity:${this.theme.lightOpacity};\
              position: ${this.theme.lightPosition};\
              zIndex:${this.theme.lightZindex};`
    },
    logoStyles: function(){
      return `--logoW:\
              ${this.logoWid}`
    },
    contDivStyles: function(){
      const inpWidth = (!this.user_auth && this.registration) 
                        ? "calc(var(--formWidth) * 0.482)" 
                        : "calc(var(--formWidth) * 0.533)"
      return `--formWidth:\
                ${this.formContWidth};\
              --formWidthS:\
                ${this.formWid1};\
              --formHeight:\
                ${this.formContHeight};\
              --fontSize:\
                calc(${this.formWid1} * 0.0259);\
              --inpWidth:\
                ${inpWidth};\
              backgroundColor:\
                ${this.theme.lightSecondary};\
              background:\
                linear-gradient(\
                  to top right,\
                  ${this.theme.lightSecondary},\
                  ${this.theme.darkSecondary}\
                );`
    },
    formContWidth: function(){
      if(!this.user_auth && this.registration){
        return this.formWid2
      } else {
        return this.formWid1
      }
    },
    formContHeight: function(){
      if(this.user_auth && this.registration){
        return this.formUrh
      } else if(this.user_auth && !this.registration){
        return this.formUlh
      } else if(!this.user_auth && this.registration){
        return this.formSrh
      } else if(!this.user_auth && !this.registration){
        return this.formSlh
      }
    },
    formContStyles: function(){
      return `backgroundColor:\
                ${this.theme.green};\
              boxShadow:\
                ${this.theme.shadow};\
              background:\
                linear-gradient(\
                  to top right,\
                  ${this.theme.darkGreen},\
                  ${this.theme.medGreen});`
    },
    inpSecStyles: function(){
      return `backgroundColor:\
                ${this.theme.lightSecondary};\
              color:\
                ${this.theme.color};\
              background:\
                linear-gradient(\
                  to top right,\
                  ${this.theme.darkSecondary},\
                  ${this.theme.lightSecondary}\
                );`
    },
  },
  methods: {
    responsiveness(){
      const windowH = window.innerHeight
      const windowW = window.innerWidth
      const smallW = windowW * .95
      const smallH = smallW * .95221
      const smallLogo = smallW * .15789
      const highW = windowH / 1.15

      if (windowW - highW < (windowW * .02)){
        this.display_class = "small"
      }
      if(windowW - highW >= (windowW * .02) && windowW <= highW + (2 * (highW * .25789)) + (windowW * .15)){
        this.display_class = "high"
      }
      if (windowW > highW + (2 * (highW * .25789)) + (windowW * .15)){
        this.display_class = 'wide'
      }

    },
    onResize() {
      this.responsiveness()
    },
  },
  watch: {
    display_class: function () {
      if(this.display_class == "small"){
        document.querySelector('#contDiv').style.flexDirection !== 'column'
        && (document.querySelector('#contDiv').style.flexDirection = 'column')

        document.querySelector('#contDiv').style.justifyContent !== 'flex-start'
        && (document.querySelector('#contDiv').style.justifyContent = 'flex-start')

        document.querySelectorAll('.logoDiv')[0].style.marginBottom !== '2vh'
        && (document.querySelectorAll('.logoDiv')[0].style.marginBottom = '2vh')

        document.querySelectorAll('.logoDiv')[0].style.marginTop !== '2vh'
        && (document.querySelectorAll('.logoDiv')[0].style.marginTop = '2vh')

        document.querySelectorAll('.logoDiv')[1].style.display !== 'none'
        && (document.querySelectorAll('.logoDiv')[1].style.display = 'none')

        this.formWid2 = '95vw'
        this.formWid1 = '88.07vw'
        this.logoWid = 'calc(var(--formWidth) * .15789)'
      }
      if(this.display_class == "high"){
        document.querySelector('#contDiv').style.flexDirection !== 'column'
        && (document.querySelector('#contDiv').style.flexDirection = 'column')

        document.querySelector('#contDiv').style.justifyContent !== 'flex-start'
        && (document.querySelector('#contDiv').style.justifyContent = 'flex-start')

        document.querySelectorAll('.logoDiv')[0].style.marginBottom !== '2vh'
        && (document.querySelectorAll('.logoDiv')[0].style.marginBottom = '2vh')

        document.querySelectorAll('.logoDiv')[0].style.marginTop !== '2vh'
        && (document.querySelectorAll('.logoDiv')[0].style.marginTop = '2vh')

        document.querySelectorAll('.logoDiv')[1].style.display !== 'none'
        && (document.querySelectorAll('.logoDiv')[1].style.display = 'none')

        this.formWid2 = `${window.innerHeight / 1.19}px`
        this.formWid1 = `${(window.innerHeight / 1.19) * .92705}px`
        this.logoWid = 'calc(var(--formWidth) * .15789)'
      }
      if(this.display_class == "wide"){
        document.querySelector('#contDiv').style.flexDirection
        && (document.querySelector('#contDiv').style.flexDirection = '')

        document.querySelector('#contDiv').style.justifyContent
        && (document.querySelector('#contDiv').style.justifyContent = '')

        document.querySelectorAll('.logoDiv')[0].style.marginBottom
        && (document.querySelectorAll('.logoDiv')[0].style.marginBottom = '')

        document.querySelectorAll('.logoDiv')[0].style.marginTop
        && (document.querySelectorAll('.logoDiv')[0].style.marginTop = '')

        document.querySelectorAll('.logoDiv')[1].style.display == 'none'
        && (document.querySelectorAll('.logoDiv')[1].style.display = 'flex')

        this.formWid2 = '54.15vw'
        this.formWid1 = '50.2vw'
        this.logoWid = 'calc(var(--formWidth) * .25789)'
      }
    }
  }
}
</script>

<style>
@font-face {
  font-family: myFont;
  src: url(../assets/ZenAntique-Regular.ttf);
}
html{
  background: wheat;
}
html, body, #__nuxt, #__layout{
  min-height: 100%;
  font-family: myFont;
}
#contDiv{
  display: flex;
  align-items: center;
  justify-content: space-evenly;
  min-height: 100vh;
}
.formCont{
  display: inline-block;
  border-radius: 20px;
  margin: 0;
  padding: calc(var(--formWidth) * .074);
  padding-bottom: 0;
  width:var(--formWidth);
  height:var(--formHeight)
}
.inputSec{
  display: inherit;
}
.inputCont{
  flex-direction: column;
}
.logoDiv{
  width: var(--logoW);
  border-radius: 100%;
}
img{
  width: inherit;
  border-radius: 100%;
}
</style>