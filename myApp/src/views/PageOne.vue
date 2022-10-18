<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar id="toolbar">
        <ion-button @click.prevent="backToHomePage">Home Page</ion-button>
      </ion-toolbar>
    </ion-header>
    
    <ion-content :fullscreen="true">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-button>Default</ion-button>
        </ion-toolbar>
      </ion-header>
      <div id="container">
        <ion-title>Testing Page One</ion-title>
      </div>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import { IonContent, IonHeader, IonPage, IonTitle, IonToolbar, IonButton } from '@ionic/vue';
import { defineComponent } from 'vue';


export default defineComponent({
  name: 'HomePage',
  components: {
    IonContent,
    IonHeader,
    IonPage,
    IonTitle,
    IonToolbar,
    IonButton
  },
  methods: {
    backToHomePage() {
      this.$router.push({name: "Home"})
    }
  }
});
</script>

<style scoped>
#container {
  text-align: center;
  
  position: absolute;
  left: 0;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
}

#container strong {
  font-size: 20px;
  line-height: 26px;
}

#container p {
  font-size: 16px;
  line-height: 22px;
  
  color: #8c8c8c;
  
  margin: 0;
}

#container a {
  text-decoration: none;
}

#toolbar {
  flex-direction: row;
}

#toolbar ion-button{
  padding-right: .3rem;
  padding-left: .5rem;
}
</style>
