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
        roomid: 0
     }),
    persist: 
    {
        paths: ['firstName, familyName, email, idToken, response, isSignedIn, showUnavailable'],
        storage: sessionStorage
    }
})


