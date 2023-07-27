import { defineStore } from 'pinia'

export const useRoomStore = defineStore('room', {
    state: () => ({ 
        email: '',
        firstName: '',
        familyName: '',
        idToken: '',
        response: '',
        roomNumber: '',
        timestamp: '',
        isSignedIn: false,
        returnPass: false,
        //if the pass for the requested room is available
        passAvailable: false,
        //if the current user has the pass
        hasPass: false,
    }),
    persist: {
      storage: sessionStorage
    } 
})


