<template>
    <div>

    </div>
</template>

<script lang="ts" setup>
import { onMounted } from "vue";
import { useRoute } from "vue-router";

onMounted(() => {
    //
    const router = useRoute()
    console.log("ClassRoom.vue mounted", router.params.id )
})
</script>

<style lang="scss" scoped>

</style>