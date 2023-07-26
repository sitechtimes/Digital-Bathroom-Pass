<template>
  <ion-page id="main">
    <ion-content color="dark" id="main-container">
      <div class="container-wrapper">
        <ion-card>
          <ion-card-content>
            <img
              class="card-icon"
              src="/img/signin.png"
              alt="seagull"
            />
            <ion-card-header>
              <ion-card-title>SITHS Digital Bathroom Pass</ion-card-title>
              <ion-card-subtitle>"Pooping made easy"</ion-card-subtitle>
              <ion-text v-if="roomStore.roomNumber === ''">Room Not Detected</ion-text>
            </ion-card-header>
            <ion-button
              class="round-button"
              id="login-button"
              v-if="!roomStore.isSignedIn"
              @click="doLogIn"
              shape="round"
              >
              <ion-icon :icon="logoGoogle" slot="start"></ion-icon>
              Continue with Google
            </ion-button>
          </ion-card-content>
        </ion-card>
      </div>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import {
  IonPage,
  IonContent,
  IonCard,
  IonCardContent,
  IonButton,
  IonCardTitle,
  IonCardSubtitle,
  IonText,
  IonIcon,
  IonCardHeader
} from "@ionic/vue";
import { defineComponent } from "vue";
import { logoGoogle } from "ionicons/icons";
import { useRoomStore } from "@/stores/room";
import { GoogleAuth } from "@codetrix-studio/capacitor-google-auth"; //package for google login
import { useRouter } from "vue-router";
import axios from "axios";

// to get on own port go into backend directory and in terminal paste
// python -m uvicorn main:app --reload
// 10.94.168.231:8000 school port
// 10.94.168.231:8001

export default defineComponent({
  name: "SignIn",
  components: {
    IonPage,
    IonCard,
    IonCardContent,
    IonContent,
    IonButton,
    IonCardTitle,
    IonCardSubtitle,
    IonText,
    IonIcon,
    IonCardHeader
  },
  setup() {
    const roomStore = useRoomStore();
    const router = useRouter();
    return {
      roomStore,
      router,
      logoGoogle
    }
  },
  methods: {
    async login() {
      try {
        const response = await GoogleAuth.signIn();
        const idToken = response.authentication.idToken;
        this.roomStore.idToken = idToken;
        this.router.push(`/pass/?room=${this.roomStore.roomNumber}`);
      }
      catch(error) {
        console.log("Error occurred when attempting to login");
        console.error(error);
      }
    },
    async authenticateToken() {
      const token = JSON.stringify(this.roomStore.idToken);
      const headers = {
        user_agent: token
      };
      const res = await axios.post(`${process.env.VUE_APP_LOCALHOST_URL}/token_sign_in/`, token, { headers })
      const nameArr = res.data.message.name.split(" ");
      console.log(nameArr);

      this.roomStore.email = res.data.message.email;
      this.roomStore.firstName = nameArr[0]
      this.roomStore.familyName = nameArr[1]

      console.log("Inserted data from Google into store.")
    },
    changeToTrue() {
      setTimeout(() => {
        if (this.roomStore.idToken.length === 0 && this.roomStore.email !== "") {
          this.roomStore.isSignedIn = true;
        }
        else {
          console.log("There was an error or the user cancelled login.")
        }
      })
    },
    async doLogIn() {
      await this.login()
      await this.authenticateToken()
      this.changeToTrue()
    }
  },
  mounted() {
    GoogleAuth.initialize({
      clientId: process.env.VUE_APP_GOOGLE_OAUTH_CLIENT_ID,
      scopes: ['profile', 'email'],
      grantOfflineAccess: true
    })
  }
});
</script>

<style scoped>
ion-title {
  font-size: 1.75rem;
  --color: #fff;
}

ion-card {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  text-align: center;
  gap: 1.5rem;
}

ion-card-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 1.25rem;
}

ion-button {
  --background: #cabc71;
  --background-activated: #cabc71;
  --color: #000;
}

ion-card-title {
  --color: #fff;
  font-size: 1.75rem;
  padding-top: 1rem;
  font-weight: 600;
}

ion-card-subtitle {
  font-size: 1.15rem;
}

ion-card > .card-icon {
  width: 128px;
}

.round-button {
  width: 16rem;
  height: 5rem;
  font-weight: 600;
}

.container-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 5rem 0rem 0rem 0rem;
}

.card-icon {
  width: 40%;
}
</style>
