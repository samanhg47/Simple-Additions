<template>
  <div id="contDiv" :style="contDivStyles" >
    <Error />
    <div class='logoDiv left'>
      <img class='liLogo' src="../assets/saLogoDark.png" :style="darkStyles" />
      <img class='liLogo' src="../assets/saLogo.png" :style="lightStyles" />
    </div>
    <section class="formCont" :style="formContStyles" >
      <section class="inputSec" :style="inpSecStyles">
        <Nuxt />
      </section>
      <ToggleTheme />
    </section>
    <div class="logoDiv right">
      <img class="liLogo" src="../assets/saLogoDark.png" :style="darkStyles" />
      <img class="liLogo" src="../assets/saLogo.png" :style="lightStyles" />
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex"
export default {
  computed: {
    ...mapGetters("theme",["theme"]),
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
    contDivStyles: function(){
      return `backgroundColor:\
                ${this.theme.lightSecondary};\
              background:\
                linear-gradient(\
                  to top right,\
                  ${this.theme.lightSecondary},\
                  ${this.theme.darkSecondary}\
                );`
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
    }
  }
}
</script>

<style>
html, body, #__nuxt, #__layout,#contDiv{
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}
#contDiv{
  display: flex;
  align-items: center;
  justify-content: center;
}
.formCont{
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  border-radius: 20px;
  margin: 0;
  padding: 4vw;
}
.inputSec{
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0;
  padding: 0;
}
.inputCont{
  flex-direction: column;
}
.logoDiv{
  width: 15vw;
  border-radius: 100%;
}
img{
  width: inherit;
  border-radius: 100%;
}
.left{
  margin-right: 5vw;
}
.right{
  margin-left: 5vw;
}
</style>