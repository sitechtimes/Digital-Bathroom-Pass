import { defineStore } from 'pinia'

export const useRoomStore = defineStore('counter', {
    state: () => ({ 
        firstName: '',
        familyName: '',
        email: '',
        idToken: '',
        response: '',
        isSignedIn: false,
        showUnavailable: false,
        returnPass: false,
        buttonTimer: 0
     }),
    persist:  
     {
        storage: sessionStorage
    } 
})


