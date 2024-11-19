import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/accounts/LoginView.vue'
import ProfileView from '@/views/accounts/ProfileView.vue'
import SignupView from '@/views/accounts/SignupView.vue'
import FindidView from '@/views/accounts/FindidView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: HomeView
    },

    {
      path: '/accounts/login',
      name : "Login",
      component: LoginView
    },

    {
      path: '/accounts/signup',
      component: SignupView
    },

    {
      path: '/accounts/findid',
      name:"Findid",
      component: FindidView
    },

    {
      path: '/accounts/profile/:username',
      name:"profile",
      component: ProfileView
    },    
  ],
})

export default router
