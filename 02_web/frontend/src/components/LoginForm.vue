<!-- LoginForm.vue -->
<template>
  <div class="form">
    <!-- 아래 줄 삭제 -->
    <!-- <img src="/NewsPick.png" alt="logo" class="logo" /> -->

    <input v-model="username" placeholder="아이디" />
    <input v-model="password" type="password" placeholder="비밀번호" />
    <button @click="login">로그인</button>
    <p v-if="error" style="color: red">{{ error }}</p>

    <router-link to="/register" class="signup-link">회원가입</router-link>
  </div>
</template>



<script setup>
import { ref } from 'vue'
import axios from 'axios'

const username = ref('')
const password = ref('')
const error = ref('')

const login = async () => {
  try {
    const response = await axios.post('http://localhost:8000/accounts/login/', {
      username: username.value,
      password: password.value,
    })
    console.log('✅ 로그인 성공:', response.data)
    error.value = ''
    window.location.href = '/home' // 로그인 성공 시 이동
  } catch (err) {
    error.value = '❌ 로그인 실패: 아이디 또는 비밀번호를 확인하세요.'
    console.error(err)
  }
}
</script>

<style scoped>
.form {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

input {
  padding: 8px;
  border: 1px solid #ccc;
  width: 100%;
  max-width: 280px;
}

button {
  background-color: skyblue;
  padding: 8px;
  border: none;
  cursor: pointer;
  width: 100%;
  max-width: 280px;
}

.logo {
  width: 100px;
  margin-bottom: 16px;
}

.signup-link {
  color: #007bff;
  text-decoration: none;
  margin-top: 8px;
}

.signup-link:hover {
  text-decoration: underline;
}
</style>
