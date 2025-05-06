<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('')
const email = ref('')
const password1 = ref('')
const password2 = ref('')
const error = ref('')
const router = useRouter()

const register = async () => {
  try {
    const res = await axios.post('http://localhost:8000/accounts/signup/', {
      username: username.value,
      email: email.value,
      password1: password1.value,
      password2: password2.value,
    })
    console.log('✅ 회원가입 성공:', res.data)
    error.value = ''
    router.push('/')  // 로그인 페이지로 이동
  } catch (err) {
    console.error(err)
    if (err.response && err.response.data) {
      const data = err.response.data
      error.value = Object.entries(data)
        .map(([field, messages]) => `${field}: ${messages.join(', ')}`)
        .join('\n')  // 줄바꿈 유지
    } else {
      error.value = '❌ 알 수 없는 오류가 발생했습니다.'
    }
  }
}
</script>

<template>
  <div class="form">
    <input v-model="username" placeholder="아이디" />
    <input v-model="email" placeholder="이메일" />
    <input v-model="password1" type="password" placeholder="비밀번호" />
    <input v-model="password2" type="password" placeholder="비밀번호 확인" />
    <button @click="register">회원가입</button>
    
    <!-- 여러 줄 에러 출력 -->
    <p v-if="error" style="color: red; white-space: pre-line;">
      ❌ 회원가입 실패:
      {{ error }}
    </p>
  </div>
</template>

<style scoped>
.form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
input {
  padding: 8px;
  border: 1px solid #ccc;
}
button {
  background-color: skyblue;
  padding: 8px;
  border: none;
  cursor: pointer;
}
</style>
