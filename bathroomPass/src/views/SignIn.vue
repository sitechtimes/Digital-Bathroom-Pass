<template>
  <ion-page id="main">
    <ion-content color="dark" id="main-container">
      <div class="container-wrapper">
        <ion-card>
          <img class="card-icon" src="/assets/icon/seagull.png" alt="seagull" />
          <ion-card-content>
            <ion-button
              class="round-button"
              id="login-button"
              v-if="!counter.isSignedIn"
              @click="doLogIn"
              size="default"
              shape="round"
            >
              Log In
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
} from "@ionic/vue";
import { defineComponent, onMounted } from "vue";
import { logoGoogle } from "ionicons/icons";
import { useRoomStore } from "../stores/counter";
import { GoogleAuth } from "@codetrix-studio/capacitor-google-auth"; //package for google login
import axios from "axios";
import { useRouter } from "vue-router";
import router from "@/router";
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
    // IonCardTitle,
    IonContent,
    IonButton,
    // IonRippleEffect,
    // IonButtons,
    // IonToolbar,
    // IonModal,
    // IonHeader
  },
  data() {
    return {
      userToken: "",
      PassAvailability: "",
      currentUserName: "",
      lastUserName: "",
      allowTakePass: true,
      buttonText: "Take Out Pass",
      roomNumber: "",
      buttonTimer: 0,
      buttonDisabled: false,
      changeTo: "",
      isOpen: false,
    };
  },
  mounted() {
    /* this.getReturnStatus(); */
    console.log(this.counter.isSignedIn);
    console.log("68 signin", this.counter.roomNumber);
  },
  setup() {
    const counter = useRoomStore();
    onMounted(() => {
      GoogleAuth.initialize({
        clientId: process.env.VUE_APP_GOOGLE_CLIENT_ID,
        scopes: ["profile", "email"],
        grantOfflineAccess: true,
      });
      const router = useRouter();
    });

    const logIn = async () => {
      try {
        const response = await GoogleAuth.signIn();
        const idToken = response.authentication.idToken;
        counter.$state.idToken = idToken;

        router.push(`/classroom/${counter.roomNumber}`);
      } catch (e) {
        console.log("error");
      }
    };
    return { logoGoogle, counter, logIn };
  },

  methods: {
    AuthenticateToken() {
      const token = JSON.stringify(this.counter.$state.idToken);
      const headers = {
        user_agent: `${token}`,
      };
      axios
        .post("http://100.101.65.52:8000/token_sign_in/", token, { headers })
        .then((response) => {
          console.log("131", response);
          const nameArr = response.data.message.name.split(" ");
          console.log("This is the name array:", nameArr);
          this.counter.$state.email = response.data.message.email;
          this.counter.$state.firstName = nameArr[0];
          this.counter.$state.familyName = nameArr[1];
          console.log(
            this.counter.email,
            this.counter.firstName,
            this.counter.familyName
          );
        });
    },
    ChangeToTrue() {
      setTimeout(() => {
        if (this.counter.idToken !== "" && this.counter.email !== "") {
          this.counter.isSignedIn = true;
        } else {
          console.log("There was an error or user cancelled log in");
        }
      }, 500);
    },
    doLogIn() {
      this.logIn().then(this.AuthenticateToken).then(this.ChangeToTrue);
    },
  },
});
</script>

<style scoped>
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
  font-size: 1.6rem;
  font-weight: 600;
}

.container-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 13.6rem 0rem 0rem 0rem;
}
</style>
