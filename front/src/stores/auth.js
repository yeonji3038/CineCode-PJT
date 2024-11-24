import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import router from '@/router'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const API_URL = import.meta.env.VITE_APP_URL
  const FRONT_URL = import.meta.env.VITE_APP_FRONT_URL
  const router = useRouter()

  // 사용자 인증 상태 관리 토큰
  const token = ref(null)
  const username = ref('')
  const profileImage = ref('')
  const email = ref('')

  // 로그인 상태 확인
  const isLogin = computed(() => {
    return token.value !== null
  })

  // 사용자 정보 가져오기
  const fetchUserInfo = () => {
    return axios({
      method: 'get',
      url: `${API_URL}accounts/profile/`,
      headers: {
        'Authorization': `Token ${token.value}`
      }
    })
      .then((response) => {
        // response.data를 직접 사용
        username.value = response.data.username
        email.value = response.data.email
        profileImage.value = response.data.profile_image
        return response.data  // 필요한 경우 응답 데이터 반환
      })
      .catch((error) => {
        console.error('사용자 정보 가져오기 실패:', error)
        throw error
      })
  }

  // 로그인 함수
  const login = function (payload) {
    axios({
      method: 'post',
      url: `${API_URL}accounts/login/`,
      data: {
        username: payload.login_username,
        password: payload.login_password
      }
    })
    .then((res) => {
      token.value = res.data.key
      localStorage.setItem('token', res.data.key)
      
      // 사용자 정보 가져오기
      fetchUserInfo()
      router.push({ name: 'Home' })
    })
    .catch((err) => {
      console.error('로그인 실패:', err)
    })
  }

  // 로그아웃
  const logout = () => {
    token.value = null
    username.value = ''
    email.value = ''
    profileImage.value = ''
    
    // localStorage 클리어
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    localStorage.removeItem('email')
    localStorage.removeItem('profileImage')
    
    router.push({ name: 'Login' })
  }

  // 회원정보 업데트 함수
  const updateUser = (payload) => {
    // FormData 객체 생성
    const formData = new FormData()
    
    // payload에서 데이터가 있는 경우에만 FormData에 추가
    if (payload.email) formData.append('email', payload.email)
    if (payload.password1) formData.append('password', payload.password1)
    if (payload.profile_image) formData.append('profile_image', payload.profile_image)

    // axios를 사용하여 서버에 PUT 요청
    return axios({
      method: 'put',
      url: `${API_URL}accounts/update/`,
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Token ${token.value}`
      }
    })
      .then((response) => {
        // 응답에서 이메일이 있으면 store의 email 업데이트
        if (response.data.email) {
          email.value = response.data.email
        }
        // 응답에서 프로필 이미지가 있으면 store의 profileImage 업데이트
        if (response.data.profile_image) {
          profileImage.value = response.data.profile_image
        }
        return response.data
      })
      .catch((error) => {
        // 에러 발생 시 에러 메시지 throw
        throw error.response?.data || '회원정보 업데이트에 실패했습니다.'
      })
  }

  // store에서 사용할 상태와 메서드들을 반환
  return { 
    API_URL, 
    token, 
    isLogin, 
    username, 
    profileImage, 
    email, 
    login, 
    logout, 
    fetchUserInfo, 
    updateUser 
  }
}, { 
  // Pinia persist 플러그인 설정
  // localStorage에 token, username, email, profileImage 상태를 저장
  persist: {
    key: 'auth', 
    storage: localStorage, 
    paths: ['token', 'username', 'email', 'profileImage']
  }
})
