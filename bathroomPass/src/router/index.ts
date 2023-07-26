import { createRouter, createWebHistory } from '@ionic/vue-router';
import { RouteRecordRaw } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import SignIn from '../views/SignIn.vue';
import { useRoomStore } from '@/stores/room';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/home',
    name: 'Home',
    component: HomePage,
    props: true
  },
  {
    path: '/signin',
    name: 'SignIn',
    component: SignIn,
    props: (route) => ({query: route.query.id}) 
  },
  {
    path: '/classroom/:id',
    name: 'ClassRoom',
    component: () => import('../views/ClassRoom.vue'),
    // props: (route) => ({query: route.query.id}) 
  },
  {
    path: '/pass',
    name: 'BathroomPass',
    component: () => import('../views/BathroomPass.vue'),
    meta: {
      requireLogin: false
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
  else {
    next()
  }
})

export default router
