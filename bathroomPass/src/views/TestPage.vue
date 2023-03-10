<template>
    <ion-page>
        <ion-content>
            <div class="container">
                <a href="http://localhost:8100/" >testing links 1</a>
                <a href="http://localhost:8100/SignIn" >testing links 2</a>
                <ion-button @click="testClick">click test</ion-button>
            </div>
        </ion-content>
    </ion-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { IonPage, IonContent, IonButton } from '@ionic/vue'

export default defineComponent({
    name: "TestPage",
    components: {
        IonPage,
        IonContent,
        IonButton
    },
    data() {
        return {
            testUrl: "http://localhost:8100/SignIn/123",
            splitUrl: ""
        }
    },
    methods: {
        doThing() {
            console.log("button works")
        },
        testClick() {
            var testForHome = "home"
            if( this.testUrl.includes(testForHome) == true) {
                const Bongbing = this.testUrl.split("/home/").pop()
                this.splitUrl = Bongbing!
                console.log(this.splitUrl)
            } else {
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