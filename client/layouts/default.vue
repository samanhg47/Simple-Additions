<template>
  <div id="contDiv">
    <img class='i1' src="../assets/saLogo.png"/>
    <section class="formCont flex">
      <section class="inputSec flex">
        <Nuxt />
      </section>
    </section>
    <img class="i2" src="../assets/saLogo.png"/>
  </div>
</template>


<style>
html, body, #__nuxt, #__layout,#contDiv{
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}
#contDiv{
  background-color: wheat;
  display: flex;
  align-items: center;
  justify-content: center;
}
.formCont{
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 45vw;
  max-width: 50vw;
  background-color: #606E38;
  border-radius: 20px;
  margin: 0;
  padding: 0;
  box-shadow: 0 0 3vw .1vw rgba(0, 0, 0, 0.808);
}
.inputSec{
  display: flex;
  align-items: center;
  justify-content: center;
  height: 37vw;
  max-width: 40vw;
  margin: 0;
  padding: 0;
  background-color: wheat;
}
.inputCont{
  flex-direction: column;
}
.i1{
  margin-right: 5vw;
  width: 15vw;
  box-shadow: 0 0 2.5vw .1vw rgba(0, 0, 0, 0.808);
  border-radius: 100%;
}
.i2{
  margin-left: 5vw;
  width: 15vw;
  box-shadow: 0 0 2.5vw .1vw rgba(0, 0, 0, 0.808);
  border-radius: 100%;
}
</style>