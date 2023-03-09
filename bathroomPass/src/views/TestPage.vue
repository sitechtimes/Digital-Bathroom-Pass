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
            testUrl: "http://localhost:8100/home/123",
            splitUrl: ""
        }
    },
    methods: {
        testClick() {
            var testForHome = "home"

            if(this.testUrl.includes(testForHome)) {
                const Bongbing = this.testUrl.split("/home/").pop()
                this.splitUrl = Bongbing!
            } else {
                console.log("herm")
            }
        }
    }
})

</script>

<style scoped>

</style>