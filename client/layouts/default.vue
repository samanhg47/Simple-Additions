<template>
  <section class="formCont flex">
    <section class="inputSec flex">
      <Nuxt />
    </section>
  </section>
</template>


<style>
html, body, #__nuxt, #__layout{
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}
.flex{
  display: flex;
  align-items: center;
  justify-content: center;
}
#__layout{
  background-color: #e2fdff;
  display: flex;
  align-items: center;
  justify-content: center;
}
.formCont{
  height: 45vw;
  max-width: 50vw;
  background-color: #606E38;
  border-radius: 20px;
  margin: 0;
  padding: 0;
}
.inputSec{
  height: 37vw;
  max-width: 40vw;
  margin: 0;
  padding: 0;
  background-color: wheat;
}
.inputCont{
  flex-direction: column;
}
</style>