<template>
     <ion-page id="main">
        <ion-content color="dark" id="main-container">
            <div id="container">
                <ion-title v-if="isSignedIn && showUnavailable">The Pass is Not Available</ion-title>
                    <ion-button v-if="isSignedIn && !showUnavailable" @click="tryTakeOutPass" shape="round" weight="strong">
                        <ion-ripple-effect></ion-ripple-effect>
                        Take Out Pass</ion-button>
                <GoogleLogin v-if="!isSignedIn " :callback="callback"/>
            </div>
        </ion-content>
     </ion-page>
</template>

<script lang="ts">
import{ IonPage, IonContent, IonTitle, IonButton, IonRippleEffect } from '@ionic/vue';
import { defineComponent } from 'vue';
import { decodeCredential } from 'vue3-google-login';

export default defineComponent({
    name:"SignIn",
    components: {
        IonPage,
        IonContent,
        IonTitle,
        IonButton,
        IonRippleEffect
    },
    data() {
        return{
            isSignedIn: false,
            PassAvailability: "",
            roomNumber: "",
            showUnavailable: false,
            passRequirements: "",
            currentUserName: "",
            lastUserName: "",
            allowTakePass: true,
            buttonText: "Take Out Pass"
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
            const userInfo = givenName + "/" + familyName + "/" + email
            this.passRequirements = userInfo
            console.log( userInfo )
            this.isSignedIn = true
            this.currentUserName = givenName + ' ' + familyName
            console.log(this.currentUserName)
        },
        async tryTakeOutPass() {
            const changePass = 'https://gssgc6.deta.dev/change_status/'
            const changeToFalse = changePass + "120" + "/false/" + this.passRequirements
            const changeToTrue = changePass + "120" + "/true/" + this.passRequirements
            const fetchPass = 'https://gssgc6.deta.dev/get_status/120'
            const fetchFunction = await fetch(fetchPass, {
                method: 'get',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(res=>res.json()).then((response) => {
                this.lastUserName = response.message[1]
                this.PassAvailability = response.message[0]
                console.log(this.PassAvailability)
                console.log(this.currentUserName)
                console.log(this.lastUserName)
            }).catch((error) => {
                console.log('Error', error)
            }) 
            if(this.PassAvailability === "") {
            fetchFunction
        }
        if(this.PassAvailability === "FALSE" && this.currentUserName === this.lastUserName) {
            await fetch(changeToTrue).then(res=>res.json()).then((response) => {
                console.log({response})}).catch((error) => {
                console.log("Error", error)
            })
            fetchFunction
        } else if(this.PassAvailability === "TRUE") {
            await fetch(changeToFalse).then(res=>res.json()).then((response) => {
                
                console.log({response})}).catch((error) => {
                console.log("Error", error)
            })
            fetchFunction
        } else {
            console.log("before change", this.showUnavailable)
            this.showUnavailable = true
            console.log("after change", this.showUnavailable)
        }
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

ion-button {
  --background: #CABC71;
  --background-activated: #CABC71;
  
  --color: #000; 
}

</style>