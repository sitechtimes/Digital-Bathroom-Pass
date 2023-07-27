<template>
    <ion-header color="dark">
      <ion-toolbar color="dark">
        <ion-buttons slot="start">
          <ion-button @click="cancel">
            <ion-ripple-effect></ion-ripple-effect>
            Back
          </ion-button>
        </ion-buttons>
        <ion-title>Limit exceeded</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content color="dark">
      <div class="modal-wrapper">
        <img class="modal-icon" src="/images/toilet-paper.png" alt="toilet paper" />
        <ion-text>
            The bathroom pass has been returned because you've exceeded the 10 minute time limit.
            If you're still out of the classroom, please keep this open as proof.
        </ion-text>
        <ion-button @click="cancel">
          <ion-ripple-effect></ion-ripple-effect>
          I understand, close this window
        </ion-button>
      </div>
    </ion-content>
  </template>
  
  <script lang="ts">
  import {
    IonHeader,
    IonToolbar,
    IonButtons,
    IonButton,
    IonTitle,
    IonContent,
    IonRippleEffect,
    modalController,
    IonText,
  } from "@ionic/vue";
  import { defineComponent } from "vue";
  
  export default defineComponent({
    name: "ReturnModal",
    components: {
      IonHeader,
      IonToolbar,
      IonButtons,
      IonButton,
      IonTitle,
      IonContent,
      IonRippleEffect,
      IonText,
    },
    methods: {
      cancel() {
        return modalController.dismiss(null, "cancel");
      }
    },
  });
  </script>
  
  <style scoped>
  ion-text {
    font-size: 1.15rem;
    padding: 0 4rem;
  }
  .modal-wrapper {
    margin-top: 15%;
    font-family: "Open Sans", sans-serif;
    font-size: 1.25rem;
    font-weight: 600;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2rem;
    text-align: center;
  }
  
  .modal-icon {
    width: 30%;
  }
  </style>
  