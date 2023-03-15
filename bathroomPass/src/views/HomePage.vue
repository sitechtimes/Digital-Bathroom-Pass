<template>
  <ion-page id="main">
    <ion-content color="dark" id="main-container" :fullscreen="true">
      <div id="container">
        <div id="card-wrapper">
          <ion-title size="small" weight="strong" id="cardTitle">SITHS Bathroom Scanner</ion-title>
          <p class="card-text">Pooping made easy</p>
        </div>
        <ion-button id="buttonText" shape="round" size="large" @click="PushToScanner" >
          <ion-ripple-effect></ion-ripple-effect>Go To Scanner</ion-button>
      </div>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import { IonContent, IonPage, IonTitle, IonButton, IonRippleEffect } from '@ionic/vue';
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'HomePage',
  components: {
    IonContent,
    IonPage,
    IonTitle,
    IonButton,
    IonRippleEffect
  },
  data() {
    return {
      roomNumber: 122
    }
  },
  methods: {
    sendMessage() {
      this.$root?.$emit("message-from-alexis", "eat ass")
    },
    PushToScanner() {
      this.$router.push({
        name: "SignIn",
      })
    }
  },
  created() {
    console.log(this.roomNumber)
  }
});
</script>

<style scoped>

#container {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  position: absolute;
  left: 0;
  right: 0;
  top: 55%;
  transform: translateY(-65%);
}

#main {
  background-color: #000;
}

#buttonText {
  font-size: medium;
}

#cardTitle {
  padding-top: 25%;
}

#card-wrapper {
  background-color: #CABC71;
  width: 50%;
  display: flex;
  border-radius: 2.5rem;
  margin-bottom: 13%;
  flex-direction: column;
  padding-bottom: 14%;
  left: 0;
  right: 0;
  top: 55%;
  transform: translateY(25%);
}

p {
  color: black;
}

ion-title {
  color: #000;
  font-size: 2em;
}

ion-button {
  --background: #CABC71;
  --background-activated: #CABC71;
  
  --color: #000; 
}

@media screen and (min-width : 300px) and (max-width : 1200px) {
  #card-wrapper{
    background-color: #CABC71;
  width: 86%;
  display: flex;
  border-radius: 2.5rem;
  margin-bottom: 13%;
  flex-direction: column;
  padding-bottom: 14%;
  left: 0;
  right: 0;
  top: 55%;
  transform: translateY(-5%);
  }
}

</style>
