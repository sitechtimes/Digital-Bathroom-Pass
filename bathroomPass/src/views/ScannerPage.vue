<template>
    <ion-page>
        <ion-content>
            <ion-button @click="PushToSignIn"> scan </ion-button>
        </ion-content>
    </ion-page>
</template>

<script lang="ts">
import {IonContent, IonPage, IonButton} from '@ionic/vue'
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'ScannerPage',
    components: {
        IonContent, 
        IonPage,
        IonButton
    },
    methods: {
        PushToSignIn() {
            this.$router.push({name: "SignIn"})
        }
    }
})
</script>

<style scoped>

</style>