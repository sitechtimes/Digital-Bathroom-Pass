<template>
  <ion-page id="main">
    <ion-content color="dark" id="main-container" :fullscreen="true">
      <div class="container-wrapper">
        <ion-card color="dark">
          <img class="card-icon" src="/images/signin.png" alt="seagull" />
          <ion-card-title>SITHS Bathroom Scanner</ion-card-title>
          <ion-card-subtitle>Scan your classroom's QR code</ion-card-subtitle>
          <ion-card-content>
            <ion-button
              @click="pushToScanner"
              class="round-button"
              id="route-button"
              shape="round"
            >
              <ion-ripple-effect></ion-ripple-effect>
              Go To Bathroom Pass
            </ion-button>
          </ion-card-content>
        </ion-card>
      </div>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import {
  IonContent,
  IonPage,
  IonCardTitle,
  IonCardContent,
  IonRippleEffect,
  IonCardSubtitle,
  IonButton,
  IonCard,
} from "@ionic/vue";
import { defineComponent } from "vue";
import { useRoomStore } from "../stores/room";
import axios from "axios";
import { body } from "ionicons/icons";

export default defineComponent({
  name: "HomePage",
  components: {
    IonContent,
    IonCardTitle,
    IonCardContent,
    IonPage,
    IonRippleEffect,
    IonCardSubtitle,
    IonButton,
    IonCard,
  },
  data() {
    return {
      roomNumber: "",
    };
  },
  async mounted() {
    if (this.$route.params.code) {
      let authcode = this.$route.params.code
      const res = await axios.post(`${window.location.origin}/token_sign_in/`, {
        code: authcode
      })
      console.log(res.data)
    }
  },
  setup() {
    const counter = useRoomStore();
    return {
      counter,
    };
  },
  methods: {
    logValue() {
      console.log(this.roomNumber);
    },
    pushToScanner() {
      this.$router.push("/signin");
    },
  },
});
</script>

<style scoped>
ion-card-title {
  font-size: 1.75rem;
  font-weight: 600;
  --color: #fff;
}

ion-card-subtitle {
  font-size: 1rem;
}

ion-card {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  text-align: center;
  gap: 1.5rem;
  color: #fff;
}

ion-button {
  --background: #cabc71;
  --background-activated: #cabc71;
  --color: #000;
}

.round-button {
  width: 16rem;
  height: 5rem;
  font-size: 1rem;
  font-weight: 600;
}
.container-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 6rem 0rem 0rem 0rem;
}
.card-icon {
  width: 40%;
}
</style>
