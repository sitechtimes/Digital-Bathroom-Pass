<template>
    <ion-page id="main">
        <ion-content color="dark" class="main-container" :fullscreen="true">
            <ion-card>
                <ion-card-header>
                    <img src="/img/pass.gif" alt="seagulls">
                    <ion-card-title>Bathroom Pass</ion-card-title>
                    <h2 v-if="roomStore.roomNumber">Room {{ roomStore.roomNumber }}</h2>
                </ion-card-header>
                <ion-card-content>
                    <div v-if="roomStore.passAvailable">
                        <ion-button>
                            <ion-ripple-effect></ion-ripple-effect>
                            Take out pass
                        </ion-button>
                    </div>
                    <div v-if="!roomStore.passAvailable">
                        <p>
                            Someone in your class is currently out with the pass.
                            <br>
                            Please wait until they get back, or ask your teacher for permission to leave.
                        </p>
                    </div>

                </ion-card-content>
            </ion-card>
        </ion-content>
    </ion-page>
</template>

<script lang="ts">
import { IonPage, IonContent, IonCard } from '@ionic/vue';
import { useRoomStore } from '@/stores/room';
import { useRoute } from 'vue-router';
import { defineComponent } from 'vue';
import axios from 'axios';

const roomStore = useRoomStore();
const route = useRoute();

export default defineComponent({
    name: 'BathroomPass',
    components: {
        IonPage,
        IonContent,
        IonCard
    },
    data() {
        return {
            roomNumber: String,
            roomStore,
            route
        }
    },
    methods: {
        getRoomNumber() {
            roomStore.roomNumber = route.params.id.toString();
            return roomStore.roomNumber;
        },
        async getPassStatus() {
            const res = await axios.get(process.env.VUE_APP_LOCALHOST_URL + '/get_status/' + parseInt(roomStore.roomNumber));
            console.log(res);
            if (res.data.isAvailable === 'TRUE') {
                roomStore.passAvailable = true;
                return true;
            }
            else {
                roomStore.passAvailable = false;
                return false;
            }
        },
        async takeOutPass() {
            console.log("Attempting to take out pass")
            const passIsAvailable = this.getPassStatus();
            if(!passIsAvailable) {
                alert("The pass is currenty not available, please wait for someone to come back or ask your teacher to leave!")
            }
            else {
                try {
                    await axios.get(process.env.VUE_APP_LOCALHOST_URL + )
                } catch(error) {    
                    console.error(error);
                }
                roomStore.hasPass = true;
            }
        }
    },
    mounted() {
        this.getPassStatus();   
    }
})
</script>