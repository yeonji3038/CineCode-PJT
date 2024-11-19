import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/accounts/LoginView.vue'
import ProfileView from '@/views/accounts/ProfileView.vue'
import SignupView from '@/views/accounts/SignupView.vue'
import FindidView from '@/views/accounts/FindidView.vue'
import SearchView from '@/views/SearchView.vue'
import MyCodeView from '@/views/MyCodeView.vue'
import CodeShareView from '@/views/CodeShareView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: "Home",
      component: HomeView
    },

    {
      path: '/search',
      name: "Search",
      component: SearchView
    },

    {
      path: '/accounts/login',
      name : "Login",
      component: LoginView
    },

    {
      path: '/accounts/signup', 
      name: "Signup",
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

    {
      path: '/mycode/:username',
      name:"mycode",
      component: MyCodeView
    },

    {
      path: '/codeshare',
      name:"codeshare",
      component: CodeShareView
    },
  ],
})

export default router
