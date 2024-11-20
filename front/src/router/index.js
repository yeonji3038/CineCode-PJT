import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/accounts/LoginView.vue'
import ProfileView from '@/views/accounts/ProfileView.vue'
import SignupView from '@/views/accounts/SignupView.vue'
import SearchView from '@/views/movies/SearchView.vue'
import CodeShareView from '@/views/community/CodeShareView.vue'
import MyCodeView from '@/views/community/MyCodeView.vue'
import UpdateView from '@/views/accounts/UpdateView.vue'
import MovieDetailView from '@/views/movies/MovieDetailView.vue'



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
      component: LoginView,
      meta: { requiresGuest: true }  // 비로그인 사용자만 접근 가능
    },

    {
      path: '/accounts/signup', 
      name: "Signup",
      component: SignupView,
      meta: { requiresGuest: true }  // 비로그인 사용자만 접근 가능
    },

    {
      path: '/accounts/update', 
      name: "Update",
      component: UpdateView,
      meta: { requiresAuth: true } // 로그인 사용자만 접근 가능
    },
    
    {
      path: '/accounts/profile',
      name:"Profile",
      component: ProfileView,
      meta: { requiresAuth: true } // 로그인 사용자만 접근 가능
    },

    // 영화
    {
      path: '/mycode',
      name:"MyCode",
      component: MyCodeView,
      meta: { requiresAuth: true }   
    },

    {
      path: '/codeshare',
      name:"CodeShare",
      component: CodeShareView
    },
    {
      path: '/movies/:id',
      name: 'MovieDetail',
      component: MovieDetailView
    },
  ],
})

// 네비게이션 가드
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // 인증이 필요한 페이지에 대한 처리
  if (to.meta.requiresAuth && !authStore.isLogin) {
    next({ name: 'Login' })
    return
  }
  
  // 비로그인 사용자만 접근 가능한 페이지에 대한 처리
  if (to.meta.requiresGuest && authStore.isLogin) {
    next({ name: 'Home' })  // 로그인된 사용자는 홈으로 리다이렉트
    return
  }

  next()
})

export default router
