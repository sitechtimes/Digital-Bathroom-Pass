import { createRouter, createWebHistory } from '@ionic/vue-router';
import { RouteRecordRaw } from 'vue-router';
import { useRoomStore } from '@/stores/room';
import HomePage from '../views/HomePage.vue';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/home',
    name: 'Home',
    component: HomePage,
  },
  {
    path: '/signin',
    name: 'SignIn',
    component: () => import('../views/SignIn.vue'),
    // props: (route) => ({query: route.query.id}) 
  },
  {
    path: '/pass',
    name: 'BathroomPass',
    component: () => import('../views/BathroomPass.vue'),
    meta: {
      requireLogin: false,
      requireRoom: true,
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  //add a check for the room numbers to make sure they're valid
  const roomStore = useRoomStore();
  const roomNumber = to.query.room;
  if(to.query.room && typeof roomNumber === 'string') {
    roomStore.roomNumber = roomNumber
    console.log(`Room number set to ${roomNumber}`)
  }
  if(to.matched.some((record) => record.meta.requireLogin) && !roomStore.isSignedIn) {
    next('/signin')
  }
  if(to.matched.some((record) => record.meta.requireRoom) && roomStore.roomNumber.length === 0) {
    console.log('Room not detected')
    next('/home')
  }
  else {
    next()
  }
})

export default router
