import { createRouter, createWebHistory } from '@ionic/vue-router';
import { RouteRecordRaw } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import SignIn from '../views/SignIn.vue';
import TestPage from '../views/TestPage.vue';

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
    path: '/SignIn',
    name: 'SignIn',
    component: SignIn,
    props: (route) => ({query: route.query.id}) 
  },
  {
    path: '/TestPage',
    name: 'TestPage',
    component: TestPage,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
