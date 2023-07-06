<template>
    <ion-page id="main">
        <ion-content color="dark" id="main-container">
            <div id="container">
                <ion-title v-if="counter.$state.isSignedIn && counter.$state.showUnavailable">The Pass is Not
                    Available</ion-title>
                <ion-button v-if="counter.$state.isSignedIn && !counter.$state.showUnavailable" 
                    class="round-button"
                    id="takeout-button"
                    @click="tryTakeOutPass"
                    size="default"
                    shape="round" :strong="true">
                    <ion-ripple-effect></ion-ripple-effect>
                    Take Out Pass</ion-button>
                <!--  <ion-button v-if="!isSignedIn" id="loginButton" shape="round" @click="GoToPassOptions" :strong="true" >Take Out
                <ion-ripple-effect></ion-ripple-effect> 
                </ion-button> -->
                <ion-button class="round-button" id="login-button" v-if="!counter.$state.isSignedIn" @click="doLogIn" size="default" shape="round"> Log In </ion-button>
                <ion-button class="round-button" id="logout-button" @click="logout" size="default" shape="round">Logout</ion-button>
            </div>
        </ion-content>
    </ion-page>
</template>

<script lang="ts">
import { IonPage, IonContent, IonTitle, IonButton, IonRippleEffect } from '@ionic/vue';
import { defineComponent, onMounted } from 'vue';
import { logoGoogle } from 'ionicons/icons'
import { useRoomStore } from '../stores/counter'
import { GoogleAuth } from '@codetrix-studio/capacitor-google-auth' //package for google login
import axios from 'axios'
// to get on own port go into backend directory and in terminal paste
// python -m uvicorn main:app --reload 
// 10.94.168.231:8000 school port 
// 10.94.168.231:8001
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
        return {
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
        onMounted(() => {
            GoogleAuth.initialize({
                clientId: '712891238786-8aj99006i0o1jsecsg8ds9n0ff7ehtmq.apps.googleusercontent.com',
                scopes: ['profile', 'email'],
                grantOfflineAccess: true,
            });
        });

        const logIn = async () => {
            try {
                const response = await GoogleAuth.signIn()
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

    methods: {
        doPost() {
            const token = JSON.stringify(this.counter.$state.idToken)
            const headers = {
                "user_agent": `${token}`
            }
            axios.post("http://100.101.65.32:8000/token_sign_in/", token, { headers }).then(response => {
                console.log(response)
                this.counter.$state.response = response.data.message
                console.log(this.counter.$state.response)
                const splitStr = this.counter.$state.response
                console.log("this is the splitstr", splitStr)
                const nameArr = splitStr[1].split(" ")
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
        setParams() {
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
        doLogIn() {
            this.logIn().then(this.doPost).then(this.storeResponse).then(() => {
                // console.log(this.isSignedIn, this.showUnavailable)
            }
            ).then(this.setParams).then(this.ChangeToTrue)
            // console.log(this.isSignedIn)
        },
        async tryTakeOutPass() {
            const changePass = 'http://100.101.65.32:8000/change_status/'
            const changeToFalse = changePass + "125" + "/false/" + this.passRequirements
            const changeToTrue = changePass + "125" + "/true/" + this.passRequirements
            const fetchPass = 'http://100.101.65.32:8000/get_status/125'
            const fetchFunction = await fetch(fetchPass, {
                method: 'get',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(res => res.json()).then((response) => {
                this.lastUserName = response.message[1]
                this.PassAvailability = response.message[0]
                console.log(this.PassAvailability)
                console.log(this.currentUserName)
                console.log(this.lastUserName)
            }).catch((error) => {
                console.log('Error', error)
            })
            if (this.PassAvailability === "") {
                fetchFunction
            }
            if (this.PassAvailability === "FALSE" && this.currentUserName === this.lastUserName) {
                await fetch(changeToTrue).then(res => res.json()).then((response) => {
                    console.log({ response })
                }).catch((error) => {
                    console.log("Error", error)
                })
                fetchFunction
            } else if (this.PassAvailability === "TRUE") {
                await fetch(changeToFalse).then(res => res.json()).then((response) => {

                    console.log({ response })
                }).catch((error) => {
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
        logout() {
            this.counter.$state.showUnavailable = false
            this.counter.$state.isSignedIn = false
        }
    },
})

</script>

<style scoped>
#container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 80vw;
    border-radius: 0.3rem;
    height: 50vh;
    margin: auto;
    margin-top: 35%;
    gap: 5rem;
    background-color: #3e4145;
}

.round-button {
    width: 16rem;
    height: 6rem;
    font-size: 1.6rem;
    font-weight: 600;
}

ion-button {
    /* --ion-font-family: 'Monserrat', sans-serif; */
    --background: #CABC71;
    --background-activated: #CABC71;
    --color: #000;
    font-size: 1.7rem;
}

ion-title {
    width: 100%;
    height: 3rem;
}
</style>