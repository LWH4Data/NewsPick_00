<template>
  <div class="login-container">
    <div class="login-card">
      <!-- 절대 경로로 이미지 사용 (public 폴더 기준) -->
      <img src="/NewsPick.png" alt="logo" class="logo" />
      <LoginForm />
    </div>
  </div>
</template>

<script setup>
import LoginForm from '@/components/LoginForm.vue'
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #e6f2ff;
}

.login-card {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  width: 360px;
  text-align: center;
}

.logo {
  width: 120px;
  margin-bottom: 24px;
}
</style>
