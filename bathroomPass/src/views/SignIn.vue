<template>
     <ion-page>
        <ion-content>
            <ion-header collapse="condense">
            </ion-header>
            <div id="container">
                <ion-title >The Pass is Not Available</ion-title>
                <ion-button v-if="isSignedIn" >Take Out the Pass</ion-button>
                <GoogleLogin v-if="!isSignedIn" :callback="callback"/>
            </div>
        </ion-content>
     </ion-page>
</template>

<script lang="ts">
import{ IonPage, IonContent, IonTitle, IonHeader, IonButton } from '@ionic/vue';
import { defineComponent } from 'vue';
import { decodeCredential } from 'vue3-google-login';

export default defineComponent({
    name:"SignIn",
    components: {
        IonPage,
        IonContent,
        IonTitle,
        IonHeader,
        IonButton
    },
    data() {
        return{
            isSignedIn: false,
            PassAvailability: false,
            roomNumber: ""
        }
    },
    methods:{ 
        callback(response: any) {
            type signIn = {
            iss?: string;
            aud?: string;
            azp?: string;
            email?: string;
            email_verified?: boolean;
            exp?: number;
            family_name?: string;
            given_name?: string;
            iat?: number;
            jti?: string;
            name?: string;
            nbf?: number;
            picture?: string;
            sub?: number;
            hd?: string;
            }
            const userData: signIn = decodeCredential(response.credential)
            const givenName = userData.given_name
            const familyName = userData.family_name
            const email = userData.email
            console.log( givenName, familyName, email )
            this.isSignedIn = true
        }
    }
})

</script>

<style scoped>
#container {   
  text-align: center;
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  transform: translateY(-150%);
}
</style>