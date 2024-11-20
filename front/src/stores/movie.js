import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const router = useRouter()
  const defaultMovies = ref([])

  // 초기 영화 데이터 요청
  const getDefaultMovies = function () {
    axios({
      method: 'get',
      url: `${API_URL}/movies/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then((res) => {
      console.log(res)
      defaultMovies.value = res.data
    })
    .catch((err) => {
      console.log(err)
    })
  }

  return { API_URL, token, isLogin, defaultMovies, getDefaultMovies }
}, {persist : true})
