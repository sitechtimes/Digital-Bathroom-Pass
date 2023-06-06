import { ref } from 'vue'
import { defineStore } from 'pinia'

/* export const useRoomStore = defineStore('roomNumber', () => {
    const roomNumber = ref(0)

    function $reset() {
        roomNumber.value = 0
    }

    return { roomNumber, $reset }
}) */

/* export const useRoomStore = defineStore('counter', {
    state: () => {
        return { count: 0 }
    },
    actions: {
        increment() {
            this.count++
        },
    },
}) */

export const useRoomStore = defineStore('counter', {
    state: () => ({ 
        count: 0,
        testNumber: '',
        firstName: '',
        familyName: '',
        email: '',
        idToken: '',
        response: {}
     }),
    getters: {
        doubleCount: (state) => state.count * 2,
    },
    actions: {
        increment() {
            this.count++
        },
        decrement() {
            this.count--
        }
    }
})


