<template>
    <ion-page id="main">
        <ion-content color="dark" id="main-container">
            <ion-card>
                <img class="card-icon" src="/assets/icon/seagull.png" alt="seagull">
                <ion-card-title v-if="counter.isSignedIn && counter.showUnavailable">
                    The pass is not available
                </ion-card-title>
                <ion-card-content>
                    <ion-button v-if="counter.isSignedIn && !counter.returnPass"
                        class="round-button"
                        id="takeout-button"
                        @click="takeOutPass"
                        size="default"
                        shape="round"
                        :disabled="disableButton()"
                    >
                        <ion-ripple-effect></ion-ripple-effect>
                        Take Out Pass
                    </ion-button>
                    <ion-button v-if="counter.isSignedIn && counter.returnPass"
                        class="round-button"
                        id="takeout-button"
                        @click="takeOutPass"
                        size="default"
                        shape="round"
                    >
                        <ion-ripple-effect></ion-ripple-effect>
                        Return Pass
                    </ion-button>
                    <ion-button 
                        class="round-button" 
                        id="login-button" 
                        v-if="!counter.isSignedIn" @click="doLogIn" size="default" 
                        shape="round">
                        Log In
                    </ion-button>
                    <ion-button 
                        v-else
                        class="round-button" 
                        id="logout-button" 
                        @click="logout" 
                        size="default" 
                        shape="round">
                        Logout
                    </ion-button>
                    <ion-button
                    @click="startButtonCooldown">
                    </ion-button>
                </ion-card-content>
            </ion-card>
        </ion-content>
    </ion-page>
</template>

<script lang="ts">
import { IonPage, IonContent, IonCard, IonCardContent, IonCardTitle, IonButton, IonRippleEffect } from '@ionic/vue';
import { defineComponent, onMounted } from 'vue';
import { logoGoogle } from 'ionicons/icons';
import { useRoomStore } from '../stores/counter';
import { GoogleAuth } from '@codetrix-studio/capacitor-google-auth'; //package for google login
import axios from 'axios';
// to get on own port go into backend directory and in terminal paste
// python -m uvicorn main:app --reload 
// 10.94.168.231:8000 school port 
// 10.94.168.231:8001
export default defineComponent({
    name: "SignIn",
    components: {
        IonPage,
        IonCard,
        IonCardContent,
        IonCardTitle,
        IonContent,
        IonButton,
        IonRippleEffect
    },
    data() {
        return {
            userToken: "",
            // isSignedIn: false,
            PassAvailability: "",
            // showUnavailable: false,
            // passRequirements: "",
            currentUserName: "",
            lastUserName: "",
            allowTakePass: true,
            buttonText: "Take Out Pass",
            roomNumber: "",
            buttonTimer: 0,
            buttonDisabled: false,
            changeTo: "",
        }
    },
    mounted() {
        this.getReturnStatus()
    },  
    setup() {
        const counter = useRoomStore()
        onMounted(() => {
            GoogleAuth.initialize({
                clientId: process.env.VUE_APP_GOOGLE_CLIENT_ID,
                scopes: ['profile', 'email'],
                grantOfflineAccess: true,
            });
        });

        const logIn = async () => {
            try {
                const response = await GoogleAuth.signIn()
                const idToken = response.authentication.idToken
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
        AuthenticateToken() {
            const token = JSON.stringify(this.counter.$state.idToken)
            const headers = {
                "user_agent": `${token}`
            }
            axios.post("http://100.101.65.56:8000/token_sign_in/", token, { headers }).then(response => {
                console.log(response)
                this.counter.$state.response = response.data.message
                console.log(this.counter.$state.response)
                const splitStr = this.counter.$state.response
                console.log("This is the split string:", splitStr)
                const nameArr = splitStr[1].split(" ")
                console.log("This is the name array:", nameArr)
                // const splitName = nameArr.split(" ")
                this.counter.$state.email = splitStr[0]
                this.counter.$state.firstName = nameArr[0]
                this.counter.$state.familyName = nameArr[1]
            })
        },
        ChangeToTrue() {
            // this.isSignedIn = true
            const changeCondition = this.counter.$state.idToken
            if(changeCondition !== ""){
               this.counter.$state.isSignedIn = true 
            } else {
                console.log("err")
            }
        },
        logIdToken() {
            console.log(this.counter.idToken)
        },
        doLogIn(){
            this.logIn().then(this.AuthenticateToken).then(() => {
                // console.log(this.isSignedIn, this.showUnavailable)
            }
            ).then(this.ChangeToTrue)
        },
        async takeOutPass() {
            const roomId = 125;
            const firstName = this.counter.$state.firstName;
            const lastName = this.counter.$state.familyName;
            const email = this.counter.$state.email;

            async function fetchInfo() {
                const response = await fetch(`http://100.101.65.56:8000/get_status/${roomId}`);
                const content = await response.json();
                console.log( content);
                return content
            }
            if(this.PassAvailability === "") {
                const info = await fetchInfo()
                // getting the last user's email to compare with the current user
                this.lastUserName = info.message[1];
                this.PassAvailability = info.message[0];

                console.log("pass avail", this.PassAvailability, "current user", this.counter.email, "last user", this.lastUserName)
                if(this.PassAvailability === "FALSE" && this.counter.email === this.lastUserName){
                    //checks if the pass is out, if it is then checks current email with last email to let them put it back in
                this.changeTo = "TRUE";
                }   else if(this.PassAvailability === "TRUE" && this.counter.email){
                    //checks if pass is in, if it is then if the user has email it lets them take it out
                this.changeTo = "FALSE";
                }   else {
                this.counter.showUnavailable = true; 
                }
            }
            let changeTo = this.changeTo
            console.log("changeTo value", changeTo)
            const apiUrl = `http://100.101.65.56:8000/change_status/?room_id=${roomId}&change_to=${changeTo}&first_name=${firstName}&last_name=${lastName}&email=${email}`
            console.log(apiUrl)
            try {
                const response = await axios.get(apiUrl);
                console.log(response)
            } catch (error) {
                console.log("An error occured:", error);
            }
        },
        logout() {
            this.counter.$state.showUnavailable = false
            this.counter.$state.isSignedIn = false
            this.counter.$state.idToken = ""
            this.counter.$state.familyName = ""
            this.counter.$state.firstName = "" 
            this.counter.$state.email = ""
            this.counter.$state.response = ""
        },
        async getReturnStatus() {
        try {
            const fetchPass = 'http://100.101.65.56:8000/get_status/125'
            const fetchFunction = await fetch(fetchPass, {
                method: 'get',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            const response = await fetchFunction.json()
            console.log(response.message)
            

            console.log(this.counter.$state.email)
            const status = response.message[0]
            const getEmail = response.message[1]

            console.log(status, getEmail)

            if (this.counter.$state.email === getEmail) {
                if (status === "True") {
                    this.counter.$state.returnPass = false
                } else {
                    this.counter.$state.returnPass = true
                }
            } else {
                this.counter.$state.returnPass = false
            }

        } catch (error) {
            console.log(error)
        }
    },
    disableButton() {
        while(this.buttonTimer !== 0) {
            return true
        }
     },
     startButtonCooldown() {
        this.buttonTimer = 100
        for(let i = 0; i < this.buttonTimer; i++) {
            while(this.buttonTimer !== 0) {
                this.buttonTimer = this.buttonTimer - 1
                console.log(this.buttonTimer)
            }
        }
     }
     },
    },

)

</script>

<style scoped>
ion-card {
  --background: #3e4145;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  text-align: center;
}

ion-card-content {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 1.25rem;
}

ion-button {
  --background: #CABC71;
  --background-activated: #CABC71;
  --color: #000;
}

ion-card-title {
  --color: #fff;
  font-size: 1.75rem;
  padding-top: 1rem;
}

ion-card-subtitle {
  font-size: 1.15rem;
}

ion-card > .card-icon {
    width: 128px;
}

.round-button {
    width: 16rem;
    height: 5rem;
    font-size: 1.6rem;
    font-weight: 600;
}

</style>