import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useRoomStore = defineStore('roomNumber', () => {
    const roomNumber = ref(0)

    function $reset() {
        roomNumber.value = 0
    }

    return { roomNumber, $reset }
})