<template>
    <ion-page>
        <ion-content>
            <div class="container">
                <a href="http://localhost:8100/" >testing links 1</a>
                <a href="http://localhost:8100/SignIn" >testing links 2</a>
            </div>
        </ion-content>
    </ion-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { IonPage, IonContent } from '@ionic/vue'

export default defineComponent({
    name: "TestPage",
    components: {
        IonPage,
        IonContent
    },
    methods: {
        //
    },
    data() {
        return {
            //
        }
    } 


})

</script>

<style scoped>

</style>