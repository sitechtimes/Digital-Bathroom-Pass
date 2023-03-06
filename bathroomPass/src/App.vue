<template>
  <ion-app>
    <ion-router-outlet />
  </ion-app>
</template>

<script lang="ts">
import { IonApp, IonRouterOutlet } from '@ionic/vue';
import { defineComponent } from 'vue';
import { App, URLOpenListenerEvent } from '@capacitor/app';
import Vue from 'vue';
import { useRouter } from 'vue-router'

export default defineComponent({
  name: 'App',
  components: {
    IonApp,
    IonRouterOutlet
  },
  data() {
    return {
      roomNumber: "122"
    }
  },
  setup() {
    const router = useRouter();
    App.addListener('appUrlOpen', function(event: URLOpenListenerEvent) {
      // Example url: https://beerswift.app/tabs/tabs2
      // slug = /tabs/tabs2
      const slug = event.url.split(":8100").pop();

      if(slug) {
        router.push({
          path: slug,
        })
      }
    })
  }
});
</script>