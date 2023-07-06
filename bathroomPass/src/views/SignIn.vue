<template>
     <ion-page id="main">
        <ion-content color="dark" id="main-container">
            <div id="container">
                <ion-title v-if="counter.$state.isSignedIn && counter.$state.showUnavailable">The Pass is Not Available</ion-title>
                        <ion-ripple-effect></ion-ripple-effect>
                        Take Out Pass</ion-button>
               <!--  <ion-button v-if="!isSignedIn" id="loginButton" shape="round" @click="GoToPassOptions" :strong="true" >Take Out
                <ion-ripple-effect></ion-ripple-effect> 
                </ion-button> -->
                <ion-button id="loginButton" v-if="!counter.$state.isSignedIn" @click="doLogIn"> Log In </ion-button>
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
import axios from 'axios'
        // to get on own port go into backend directory and in terminal paste
        // python -m uvicorn main:app --reload 
        // 10.94.168.231:8000 school port 
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
            // isSignedIn: false,
            PassAvailability: "",
            // showUnavailable: false,
            passRequirements: "",
            currentUserName: "",
            lastUserName: "",
            allowTakePass: true,
            buttonText: "Take Out Pass",
            roomNumber: "",
            tokenResponse: {}
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
                const response =  await GoogleAuth.signIn()
                const idToken = response.authentication.idToken
                /* console.log(idToken) */
                counter.$state.idToken = idToken
               /*  counter.$state.familyName = response.familyName
                counter.$state.firstName = response.givenName
                counter.$state.email = response.email */

            } catch (e) {
                console.log("error")
            }
        }
        return { logoGoogle, counter, logIn }
    },

    methods:{ 
        doPost() {
        const token = JSON.stringify(this.counter.$state.idToken)
        const headers = {
            "user_agent": `${token}`
        }
        axios.post("http://localhost:8000/token_sign_in/", token, { headers }).then(response =>
         {
            console.log(response)
            this.counter.$state.response = response.data.message
            console.log(this.counter.$state.response)
            const splitStr = this.counter.$state.response
            console.log("this is the splitstr", splitStr)
            const nameArr =  splitStr[1].split(" ")
            console.log("this is the name array", nameArr)
            // const splitName = nameArr.split(" ")
            this.counter.$state.email = splitStr[0]
            this.counter.$state.firstName = nameArr[0]
            this.counter.$state.familyName = nameArr[1]
         })
        },
        storeResponse() {
            console.log(this.counter.$state.response)
            // const splitStr = this.counter.$state.response
            // console.log("this is the splitstr", splitStr)
            // const nameArr =  splitStr[1].split(" ")
            // console.log("this is the name array", nameArr)
            // // const splitName = nameArr.split(" ")
            // this.counter.$state.email = splitStr[0]
            // this.counter.$state.firstName = nameArr[0]
            // this.counter.$state.familyName = nameArr[1]
        },
        setParams(){
            this.passRequirements = this.counter.$state.firstName + "/" + this.counter.$state.familyName + "/" + this.counter.$state.email
            this.currentUserName = this.counter.$state.firstName + " " + this.counter.$state.familyName 
        },
        ChangeToTrue() {
            // this.isSignedIn = true
            this.counter.$state.isSignedIn = true
        },
        logIdToken() {
            console.log(this.counter.$state.idToken)
        },
        doLogIn(){
            this.logIn().then(this.doPost).then(this.storeResponse).then(() => {
                // console.log(this.isSignedIn, this.showUnavailable)
            }
            ).then(this.setParams).then(this.ChangeToTrue)
            // console.log(this.isSignedIn)
        },
        async tryTakeOutPass() {
            const changePass = 'http://10.94.168.231:8001/change_status/'
            const changeToFalse = changePass + "120" + "/false/" + this.passRequirements 
            const changeToTrue = changePass + "120" + "/true/" + this.passRequirements
            const fetchPass = 'http://10.94.168.231:8001/get_status/121'
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
            // console.log("before change", this.showUnavailable)
            // this.showUnavailable = true
            this.counter.$state.showUnavailable = true
            // console.log("after change", this.showUnavailable)
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