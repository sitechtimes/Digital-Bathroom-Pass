<template>
    <ion-header>
        <ion-toolbar>
            <ion-buttons slot="start">
                <ion-button @click="cancel">
                    <ion-ripple-effect></ion-ripple-effect>
                    Back
                </ion-button>
            </ion-buttons>
            <ion-title>Return Pass</ion-title>
        </ion-toolbar>
    </ion-header>
    <ion-content>
        <div class="modal-wrapper">
            <img class="modal-icon" src="/img/modal.png" alt="seagull">
            <ion-text>
                <h3>Are you sure you want to return your bathroom pass?</h3>
            </ion-text>
                <ion-button @click="confirm">
                    <ion-ripple-effect></ion-ripple-effect>
                    Yes, I want to return the pass
                </ion-button>
                <ion-button @click="cancel">
                    <ion-ripple-effect></ion-ripple-effect>
                    No, take me back
                </ion-button>
        </div>
    </ion-content>
</template>

<script lang="ts">
import { IonHeader, IonToolbar, IonButtons, IonButton, IonTitle, IonContent, IonRippleEffect, modalController, IonText } from "@ionic/vue";
import { defineComponent } from "vue";

export default defineComponent({
    name: 'ReturnModal',
    components: {
        IonHeader,
        IonToolbar,
        IonButtons,
        IonButton,
        IonTitle,
        IonContent,
        IonRippleEffect,
        IonText
    },
    methods: {
        cancel() {
            return modalController.dismiss(null, 'cancel')
        },
        confirm() {
            return modalController.dismiss(true, 'confirm')
        }
    }
})
</script>

<style scoped>
.modal-wrapper {
    margin-top: 15%;
    font-family: 'Open Sans', sans-serif;
    font-size: 1.25rem;
    font-weight: 600;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1rem;
}

.modal-icon {
    width: 25%;
}
</style>