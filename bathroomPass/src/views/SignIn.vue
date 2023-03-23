<template>
     <ion-page id="main">
        <ion-content color="dark" id="main-container">
            <div id="container">
                <ion-title v-if="isSignedIn && showUnavailable">The Pass is Not Available</ion-title>
                    <ion-button v-if="isSignedIn && !showUnavailable" @click="tryTakeOutPass" size="large" shape="round" :strong="true" >
                        <ion-ripple-effect></ion-ripple-effect>
                        Take Out Pass</ion-button>
                <ion-button v-if="!isSignedIn" id="loginButton" shape="round" @click="GoToPassOptions" :strong="true" >Take Out
                <ion-ripple-effect></ion-ripple-effect> </ion-button>
                <GoogleLogin v-if="!isSignedIn" :callback="callback" popup-type="TOKEN" >
                <ion-button  id="loginButton" shape="round" :strong="true" > 
                    <ion-ripple-effect></ion-ripple-effect>
                    <ion-icon slot="start" :icon="logoGoogle"></ion-icon>
                    Sign In With Google </ion-button>
                </GoogleLogin>
            </div>
        </ion-content>
     </ion-page>
</template>

<script lang="ts">
import{ IonPage, IonContent, IonTitle, IonButton, IonRippleEffect } from '@ionic/vue';
import { defineComponent } from 'vue';
import { decodeCredential, CallbackTypes } from 'vue3-google-login';
import { logoGoogle } from 'ionicons/icons'
import { useRoomStore } from '../stores/counter'

export default defineComponent({
    name: "SignIn",
    components: {
        IonPage,
        IonContent,
        IonTitle,
        IonButton,
        IonRippleEffect
    },
    data() {
        return{
            userToken: "",
            isSignedIn: false,
            PassAvailability: "",
            showUnavailable: false,
            passRequirements: "",
            currentUserName: "",
            lastUserName: "",
            allowTakePass: true,
            buttonText: "Take Out Pass",
            roomNumber: ""
        }
    },
    setup() {
        const counter = useRoomStore()
        return { logoGoogle, counter }
    },
    methods:{ 
        GoToPassOptions() {
            //this.isSignedIn = true
        },
        sendPost() {
            const postRequestOptions = {
                method: "POST",
                headers: { "Content-Type": "application/json"},
                body: JSON.stringify({ token: this.userToken })
            };
            console.log(postRequestOptions.body)
            if(postRequestOptions.body) {
                this.isSignedIn = true
            }
        },
        callback(response: any) {
            console.log(response)
            this.userToken = response.access_token
            this.sendPost()
        },
        /* callback(response: any) {
            if (response.credential)
            {type signIn = {
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
            console.log(userData)
            this.isSignedIn = true
            this.currentUserName = givenName + ' ' + familyName
            console.log(this.currentUserName)} else {
                console.log("call the endpoint which validates authorization code", response)
            }
        }, */
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
     },
     doStuff() {
        console.log("doing Stuff")
     }
    },
    mounted() {
        this.roomNumber = this.counter.testNumber
        console.log(this.roomNumber)
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
  transform: translateY(-60%);
}

#loginButton {
    width: 16rem;
    height: 2rem;
    font-size: 14px;
}

ion-button {
    width: 18rem;
    height: 14rem;
    font-size: 1.7rem;

  --ion-font-family: 'Monserrat', sans-serif; 

  --background: #CABC71;
  --background-activated: #CABC71;
  
  --color: #000; 
}

ion-title {
    width: 100%;
    height: 3rem;
}
</style>