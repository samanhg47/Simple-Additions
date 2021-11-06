<template>
  <div id="contDiv">
    <Error />
    <img class='liLogo left' src="../assets/saLogoDark.png"/>
    <section class="formCont">
      <section class="inputSec">
        <Nuxt />
      </section>
    </section>
    <img class="liLogo right" src="../assets/saLogoDark.png"/>
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
  background-color: rgb(41, 31, 10);
  background: linear-gradient(
    to top right,
    rgb(56, 43, 15),
    rgb(29, 21, 5)
  );
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
    #394712,
    #171d08
  );
  border-radius: 20px;
  margin: 0;
  padding: 4vw;
  box-shadow: 0 0 4vw .1vw rgb(0, 0, 0);
}
.inputSec{
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0;
  padding: 0;
  background-color: rgb(56, 43, 15);
  background: linear-gradient(
    to bottom left,
    rgb(56, 43, 15),
    rgb(29, 21, 5)
  );
  color: #e0e0e0;
}
.inputCont{
  flex-direction: column;
}
.liLogo{
  width: 15vw;
  box-shadow: 0 0 4vw .1vw rgb(0, 0, 0);
  border-radius: 100%;
}
.left{
  margin-right: 5vw;
}
.right{
  margin-left: 5vw;
}
</style>