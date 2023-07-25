import { defineStore } from 'pinia'

export const useRoomStore = defineStore('room', {
    state: () => ({ 
        firstName: '',
        familyName: '',
        email: '',
        idToken: '',
        response: '',
        isSignedIn: false,
        showUnavailable: false,
        returnPass: false,
        buttonTimer: 0,
        roomNumber: "",
        //if the pass for the requested room is available
        passAvailable: false,
        //if the current user has the pass
        hasPass: false,
    }),
    persist: {
      storage: sessionStorage
    } 
})


