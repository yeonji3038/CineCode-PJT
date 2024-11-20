import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/accounts/LoginView.vue'
import ProfileView from '@/views/accounts/ProfileView.vue'
import SignupView from '@/views/accounts/SignupView.vue'
import SearchView from '@/views/movies/SearchView.vue'
import CodeShareView from '@/views/communities/CodeShareView.vue'
import MyCodeView from '@/views/communities/MyCodeView.vue'
import UpdateView from '@/views/accounts/UpdateView.vue'



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

    // 회원가입, 로그인
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
      path: '/accounts/update', 
      name: "Update",
      component: UpdateView
    },
    
    {
      path: '/accounts/profile',
      name:"profile",
      component: ProfileView
    },

    // 영화
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
