<template>
  <ion-page id="main">
    <ion-content color="dark" id="main-container" :fullscreen="true">
      <div id="container">
        <div id="card-wrapper">
          <ion-title size="small" weight="strong" id="cardTitle">SITHS Bathroom Scanner</ion-title>
          <p class="card-text">Pooping made easy</p>
          </div>
          <div>Current Count: {{ counter.count }} </div>
          <ion-button @click="logIncrament"> Click me :D</ion-button>
          <ion-button @click="counter.increment()"> increment?</ion-button>
          <ion-button  on-button id="buttonText" shape="round" size="large" @click="PushToScanner" >
          <ion-ripple-effect></ion-ripple-effect>Go To Scanner</ion-button>
          <ion-item>
            <ion-label>Input</ion-label>
            <ion-input></ion-input>
          </ion-item>
      </div>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import { IonContent, IonPage, IonTitle, IonButton, IonRippleEffect, IonInput, IonItem, IonLabel } from '@ionic/vue';
import { defineComponent } from 'vue';
import { useRoomStore } from '../stores/counter';

export default defineComponent({
  name: 'HomePage',
  components: {
    IonContent,
    IonPage,
    IonTitle,
    IonButton,
    IonRippleEffect,
    IonInput,
    IonItem,
    IonLabel
  },
  data() {
    return {
      roomNumber: 122
    }
  },
  setup() {
    const counter =  useRoomStore()
    return {
      counter
    }
  },
  methods: {
    logIncrament() {
      console.log(this.counter.count)
    },
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
    //
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
