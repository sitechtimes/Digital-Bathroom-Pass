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
        roomid: 0,
     }),
    persist: true 
    
    /* {
        paths: ['firstName, familyName, emial, idToken, isSignedIn, showUnavailable'],
        storage: sessionStorage
    } */
})


