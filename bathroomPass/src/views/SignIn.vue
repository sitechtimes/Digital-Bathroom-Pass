<template>
     <ion-page id="main">
        <ion-content color="dark" id="main-container">
            <div id="container">
                <ion-title v-if="isSignedIn && showUnavailable">The Pass is Not Available</ion-title>
                    <ion-button v-if="isSignedIn && !showUnavailable" @click="tryTakeOutPass" size="large" shape="round" :strong="true" >
                        <ion-ripple-effect></ion-ripple-effect>
                        Take Out Pass</ion-button>
                <ion-button v-if="!isSignedIn" id="loginButton" shape="round" @click="GoToPassOptions" :strong="true" >Take Out
                <ion-ripple-effect></ion-ripple-effect> 
                </ion-button>
                <ion-button id="loginButton" @click="logIn"> test new Log In </ion-button>
            </div>
        </ion-content>
     </ion-page>
</template>

<script lang="ts">
import{ IonPage, IonContent, IonTitle, IonButton, IonRippleEffect } from '@ionic/vue';
import { defineComponent, onMounted } from 'vue';
import { logoGoogle } from 'ionicons/icons'
import { useRoomStore } from '../stores/counter'
import { GoogleAuth } from '@codetrix-studio/capacitor-google-auth' //package for google login

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
        onMounted(()=> {
            GoogleAuth.initialize({
            clientId: '712891238786-8aj99006i0o1jsecsg8ds9n0ff7ehtmq.apps.googleusercontent.com',
            scopes: ['profile', 'email'],
            grantOfflineAccess: true,
            });
        });

        const logIn = async () => {
            try {
                const response =  await GoogleAuth.signIn();
                console.log(response)
                const idToken = response.authentication.idToken
                console.log(idToken)
            } catch (e) {
                console.log("error")
            }
        }
        return { logoGoogle, counter, logIn }
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
     },
    },
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