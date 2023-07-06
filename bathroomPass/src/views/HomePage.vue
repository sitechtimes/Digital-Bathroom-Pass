<template>
  <ion-page id="main">
    <ion-content color="dark" id="main-container" :fullscreen="true">
      <div id="container">
        <div id="card-wrapper">
          <ion-title size="small" weight="strong" id="card-title">SITHS Bathroom Scanner</ion-title>
          <p class="card-text">"Pooping made easy"</p>
        </div>
        <ion-button on-button id="buttonText" shape="round" size="large" @click="PushToScanner">
          <ion-ripple-effect></ion-ripple-effect>Go To Scanner</ion-button>
      </div>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import { IonContent, IonPage, IonTitle, IonButton, IonRippleEffect } from '@ionic/vue';
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
  },
  data() {
    return {
      roomNumber: ""
    }
  },
  setup() {
    const counter = useRoomStore()
    return {
      counter
    }
  },
  methods: {
    doTest() {
      this.counter.testNumber = this.roomNumber
      console.log(this.counter.testNumber)
    },
    test() {
      setTimeout(this.doTest, 10)
    },
    logValue() {
      console.log(this.roomNumber)
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
  justify-content: center;
  min-height: 100vh;
}

#card-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 80vw;
  padding-top: 10%;
}

#card-title {
  text-align: left;
  width: 90%;
  margin-left: auto;
  font-size: 2.8rem;
}

.card-text {
  font-size: 1.3rem;
}

ion-button {
  --background: #CABC71;
  --background-activated: #CABC71;
  --color: #000;
}

@media screen and (min-width : 300px) and (max-width : 1200px) {
  #card-wrapper {
    background-color: #CABC71;
    width: 86%;
    display: flex;
    border-radius: 2.5rem;
    margin-bottom: 13%;
    flex-direction: column;
    padding-bottom: 14%;
  }
}
</style>
