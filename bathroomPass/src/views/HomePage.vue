<template>
  <ion-page id="main">
    <ion-content color="dark" id="main-container" :fullscreen="true">
      <div id="container">
        <div id="card-wrapper">
          <ion-title size="small" weight="strong" id="cardTitle">SITHS Bathroom Scanner</ion-title>
          <p class="card-text">Pooping made easy</p>
        </div>
        <ion-button id="buttonText" shape="round" size="large" color="warning" @click="PushToScanner">Go To Scanner</ion-button>
      </div>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import { IonContent, IonPage, IonTitle, IonButton } from '@ionic/vue';
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'HomePage',
  components: {
    IonContent,
    IonPage,
    IonTitle,
    IonButton
  },
  methods: {
    PushToScanner() {
      this.$router.push({name: "SignIn" })
    }
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
  top: 50%;
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
  background-color: yellow;
  width: 86%;
  display: flex;
  border-radius: 2.5rem;
  margin-bottom: 13%;
  flex-direction: column;
  padding-bottom: 14%;
}

#card-text {
  color: black;
}

ion-title {
  color: black;
  font-size: 2em;
}

</style>
