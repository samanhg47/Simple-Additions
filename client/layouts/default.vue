<template>
  <div id="contDiv">
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
  /* min-height: 45vw; */
  /* max-width: 50vw; */
  background-color: #606E38;
  background: linear-gradient(
    to top right,
    #7c8f49,
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
  /* height: 37vw; */
  /* max-width: 40vw; */
  margin: 0;
  padding: 0;
  background-color: wheat;
}
.inputCont{
  flex-direction: column;
}
.liLogo{
  width: 15vw;
  box-shadow: 0 0 2.5vw .1vw rgba(0, 0, 0, 0.808);
  border-radius: 100%;
  padding-bottom: .1vw;
}
.left{
  margin-right: 5vw;
}
.right{
  margin-left: 5vw;
}
</style>