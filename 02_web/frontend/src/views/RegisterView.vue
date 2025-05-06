<template>
  <div class="register-container">
    <div class="register-card">
      <h2>회원가입</h2>
      <RegisterForm />
    </div>
  </div>
</template>

<script setup>
import RegisterForm from '@/components/RegisterForm.vue'
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #e6f2ff;
}
.register-card {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  width: 360px;
  text-align: center;
}
</style>
