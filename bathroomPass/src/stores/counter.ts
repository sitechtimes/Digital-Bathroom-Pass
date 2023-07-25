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
        buttonTimer: 0,
        roomNumber: "",
     }),
    persist:
      {
        // paths: ['firstName, familyName, emial, idToken, isSignedIn, showUnavailable'], 
        storage: sessionStorage
    } 
})


