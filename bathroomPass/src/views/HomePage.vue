<template>
  <ion-page id="main">
    <ion-content color="dark" id="main-container" :fullscreen="true">
      <ion-card>
        <ion-card-title>
          SITHS Bathroom Scanner
        </ion-card-title>
        <ion-card-subtitle>
          "Pooping made easy"
        </ion-card-subtitle>

        <ion-card-content id="buttonText" shape="round" size="large" @click="pushToScanner">
          <ion-button>
            <ion-ripple-effect></ion-ripple-effect>
            Go to scanner
          </ion-button>
        </ion-card-content>
      </ion-card>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import { IonContent, IonPage, IonCardTitle, IonCardContent, IonRippleEffect } from '@ionic/vue';
import { defineComponent } from 'vue';
import { useRoomStore } from '../stores/counter';

export default defineComponent({
  name: 'HomePage',
  components: {
    IonContent,
    IonCardTitle,
    IonCardContent,
    IonPage,
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
    pushToScanner() {
      this.$router.push('/signin');
    }
  },
  created() {
    //
  }
});
</script>

<style scoped>

ion-card-title {
  font-size: 1.75rem;
  --color: #fff;
}

ion-card-subtitle {
  font-size: 1.15rem;
}

ion-card {
  --background: #3e4145;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  text-align: center;
  gap: 1.5rem;
}
ion-button {
  --background: #CABC71;
  --background-activated: #CABC71;
  --color: #000;
}
</style>
