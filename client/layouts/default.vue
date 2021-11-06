<template>
  <div id="contDiv">
    <Error />
    <img class='liLogo left' src="../assets/saLogo.png"/>
    <section class="formCont">
      <section class="inputSec">
        <Nuxt />
      </section>
    </section>
    <img class="liLogo right" src="../assets/saLogo.png"/>
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
  background-color: #606E38;
  background: linear-gradient(
    to bottom left,
    #879b4f,
    #566332
  );
  border-radius: 20px;
  margin: 0;
  padding: 4vw;
  box-shadow: 0 0 3vw .1vw rgba(0, 0, 0, 0.808);
}
.inputSec{
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0;
  padding: 0;
  background-color: wheat;
}
.inputCont{
  flex-direction: column;
}
.liLogo{
  width: 15vw;
  box-shadow: 0 0 2.5vw .1vw rgba(0, 0, 0, 0.753);
  border-radius: 100%;
  margin-top: .05vw;
}
.left{
  margin-right: 5vw;
}
.right{
  margin-left: 5vw;
}
</style>