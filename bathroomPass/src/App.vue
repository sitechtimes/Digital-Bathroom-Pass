<template>
  <ion-app>
    <ion-router-outlet />
  </ion-app>
</template>

<script lang="ts">
import { IonApp, IonRouterOutlet } from '@ionic/vue';
import { defineComponent } from 'vue';
import { App, URLOpenListenerEvent } from '@capacitor/app';
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
      // url: http:localhost:8100/home/122
      // roomNumber: 122
      // new url: http:localhost:8100/home
      // slug = /tabs/tabs2
      //51:46:46:57:F5:84:02:F7:45:EB:AB:ED:59:A5:BA:22:0B:AA:95:50:20:B4:37:75:D1:F3:0A:5F:B3:39:18:9C Android certificate fingerprint
      var roomNumber = event.url.split("/home/").pop()
      var roomsNumber = event.url.split("/SignIn/").pop()
      
      const slug = event.url.split(":8100/").pop();

      if(event.url.includes("home") == true){
        //
      } else {
        //
      }
      console.log(slug)
      if(slug) {
        router.push({
          path: slug,
          params: {
            props: roomsNumber
          }
        })
      }
    })
  }
});
</script>

<style>
* {
  font-family: 'Open Sans', sans-serif;
}

body {
  background-color: #18191A;
}
</style>