// src/stores/auth.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(null)

  const login = async (username, password) => {
    const res = await axios.post('http://localhost:8000/accounts/login/', {
      username,
      password,
    })
    token.value = res.data.key
    axios.defaults.headers.common['Authorization'] = `Token ${token.value}`
  }

  return { token, login }
})
