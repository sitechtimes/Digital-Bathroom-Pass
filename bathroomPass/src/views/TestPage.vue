<template>
    <ion-page>
        <ion-content>
            <div class="container">
                <ion-button @click="testClick">check slug</ion-button>
                <ion-item>
                <ion-input v-model="inputValue" :counter="true" maxlength="3"></ion-input>
                </ion-item>
                <ion-button @click="doFunction">Set thing</ion-button>
            </div>
        </ion-content>
    </ion-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { IonPage, IonContent, IonButton, IonInput, IonItem } from '@ionic/vue'

export default defineComponent({
    name: "TestPage",
    components: {
        IonPage,
        IonContent,
        IonButton,
        IonInput,
        IonItem
    },
    data() {
        return {
            testUrl: "http://localhost:8100/home/",
            splitUrl: "",
            navUrl: "",
            inputValue: ""
        }
    },
    methods: {
        doFunction() {
            console.log(this.testUrl)
            this.testUrl = this.testUrl + this.inputValue
            console.log(this.testUrl)
        },
        doThing() {
            console.log("button works")
        },
        testClick() {
            var testForHome = "home"
            if( this.testUrl.includes(testForHome) == true) {
                this.navUrl = this.testUrl.slice(0,27)
                console.log(this.navUrl)
                const Bongbing = this.testUrl.split("/home/").pop()
                this.splitUrl = Bongbing!
                console.log(this.splitUrl)

            } else {
                this.navUrl = this.testUrl.slice(0,29)
                console.log(this.navUrl)
                const BingBong = this.testUrl.split("/SignIn/").pop()
                this.splitUrl = BingBong!
                console.log(this.splitUrl)
            }
        }
    }
})

</script>

<style scoped>

</style>