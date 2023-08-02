<template>
  <ion-page id="main">
    <ion-content color="dark" class="main-container" :fullscreen="true">
      <div class="container-wrapper">
        <ion-card color="dark">
          <ion-card-header>
            <img class="card-icon" src="/images/pass.gif" alt="seagulls" />
            <ion-card-title>Bathroom Pass</ion-card-title>
            <ion-card-subtitle v-if="roomStore.roomNumber"
              >Room {{ roomStore.roomNumber }}</ion-card-subtitle
            >
          </ion-card-header>
          <ion-card-content>
            <div v-if="roomStore.passAvailable">
              <ion-button @click="takeOutPass">
                <ion-ripple-effect></ion-ripple-effect>
                Take out pass
              </ion-button>
            </div>
            <div v-if="roomStore.hasPass && !roomStore.passAvailable">
              <p>You currently have the bathroom pass for this room.</p>
              <ion-button @click="returnPass">
                <ion-ripple-effect></ion-ripple-effect>
                Return pass
              </ion-button>
            </div>
            <div v-if="!roomStore.passAvailable && !roomStore.hasPass">
              <p>
                Someone in your class is currently out with the pass.
                <br />
                Please wait until they get back, or ask your teacher for
                permission to leave.
              </p>
            </div>
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
  IonCardTitle,
  IonCardHeader,
  IonRippleEffect,
  IonButton,
  toastController,
  modalController,
  IonCardSubtitle,
  loadingController,
} from "@ionic/vue";
import LimitModal from "@/components/LimitModal.vue";
import ReturnModal from "../components/Modal.vue";
import { useRoomStore } from "@/stores/room";
import { useRoute, useRouter } from "vue-router";
import { defineComponent } from "vue";
import axios from "axios";
import date from "date-and-time";

const roomStore = useRoomStore();
const route = useRoute();

export default defineComponent({
  name: "BathroomPass",
  components: {
    IonPage,
    IonContent,
    IonCard,
    IonCardContent,
    IonCardTitle,
    IonCardHeader,
    IonRippleEffect,
    IonButton,
    IonCardSubtitle,
  },
  data() {
    return {
      roomNumber: String,
      roomStore,
      route,
    };
  },
  setup() {
    const router = useRouter();
    return {
      router,
    };
  },
  methods: {
    getRoomNumber() {
      roomStore.roomNumber = route.params.id.toString();
      return roomStore.roomNumber;
    },
    autoReturn() {
      const intervalID = setInterval(async () => {
        const currentTime = new Date();
        const timestamp = Date.parse(roomStore.timestamp);
        const previousTime = new Date(timestamp);
        const minutesPassed = date
          .subtract(currentTime, previousTime)
          .toMinutes();
        console.log(minutesPassed);
        //change minutes to 10 in production
        if (minutesPassed >= 1) {
          console.log("You have exceeded the limit of the bathroom pass.");
          try {
            const res = await axios.patch(
              process.env.VUE_APP_LOCALHOST_URL +
                `/change_status/${parseInt(roomStore.roomNumber)}`,
              {
                change_to: true,
                first_name: roomStore.firstName,
                last_name: roomStore.familyName,
                email: roomStore.email,
              }
            );
            console.log(res);
            const modal = await modalController.create({
              component: LimitModal,
            });
            modal.present();
            clearInterval(intervalID);
            this.router.push("/home");
          } catch (error) {
            console.log(
              "Error occurred when automatically putting bathroom pass back."
            );
            console.error(error);
          }
        }
      }, 5000);
    },
    async getPassStatus() {
      const res = await axios.get(
        process.env.VUE_APP_LOCALHOST_URL +
          "/get_status/" +
          parseInt(roomStore.roomNumber)
      );
      console.log("PASS STATUS");
      console.log(res);
      if (
        res.data.isAvailable === "FALSE" &&
        res.data.userEmail === roomStore.email
      ) {
        //if the user has already has the pass for the current room
        console.log("User already has the pass");
        roomStore.hasPass = true;
        roomStore.passAvailable = false;
        return false;
      } else if (res.data.isAvailable === "TRUE") {
        roomStore.passAvailable = true;
        return true;
      } else {
        roomStore.passAvailable = false;
        return false;
      }
    },
    async takeOutPass() {
      const loading = await loadingController.create({
        message: "Taking Pass, Please Wait...",
        duration: 5000,
      });
      loading.present();
      console.log("User attempting to take out the pass");
      const passIsAvailable = this.getPassStatus();
      if (!passIsAvailable) {
        alert(
          "The pass is currenty not available, please wait for someone to come back or ask your teacher to leave!"
        );
      } else {
        try {
          const res = await axios.patch(
            process.env.VUE_APP_LOCALHOST_URL +
              `/change_status/${parseInt(roomStore.roomNumber)}`,
            {
              //changing pass availability for the room to false
              change_to: false,
              first_name: roomStore.firstName,
              last_name: roomStore.familyName,
              email: roomStore.email,
            }
          );
          console.log(res);
          const now = new Date();
          roomStore.timestamp = now.toISOString();
          const toast = await toastController.create({
            message: "Bathroom Pass Taken!",
            duration: 3000,
            position: "top",
          });
          await toast.present();
          this.autoReturn();
        } catch (error) {
          console.log("Error occurred when taking out the bathroom pass.");
          console.error(error);
          return;
        }
        roomStore.passAvailable = false;
        roomStore.hasPass = true;
      }
    },
    async returnPass() {
      if (!roomStore.hasPass) {
        console.log("You can't return the pass if you don't have it!");
        return;
      } else {
        try {
          const modal = await modalController.create({
            component: ReturnModal,
          });
          await modal.present();
          const { role } = await modal.onWillDismiss();
          if (role !== "confirm") {
            console.log("User cancelled returning the bathroom pass.");
            return;
          }
          const res = await axios.patch(
            process.env.VUE_APP_LOCALHOST_URL +
              `/change_status/${parseInt(roomStore.roomNumber)}`,
            {
              change_to: true,
              first_name: roomStore.firstName,
              last_name: roomStore.familyName,
              email: roomStore.email,
            }
          );
          console.log(res);
          const toast = await toastController.create({
            message:
              "Bathroom Pass Returned! Thanks for using the SITHS Bathroom Pass app!",
            duration: 3000,
            position: "top",
          });
          await toast.present();
          roomStore.hasPass = false;
          roomStore.passAvailable = true;
          // roomStore.roomNumber = "";
          this.router.push("/home");
        } catch (error) {
          console.log("Error occured when returning the bathroom pass.");
          console.error(error);
          return;
        }
      }
    },
  },
  mounted() {
    this.getPassStatus();
  },
});
</script>

<style scoped>
ion-card-title {
  --color: white;
  font-weight: 600;
  font-size: 1.75rem;
}

ion-card-subtitle {
  font-size: 1.25rem;
}

ion-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 2rem;
}

ion-card-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

ion-card-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

ion-card-content > div {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
}

.card-icon {
  width: 80%;
  border-radius: 0.3rem;
}

.container-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 6rem 0rem 0rem 0rem;
  margin: auto;
}
</style>
