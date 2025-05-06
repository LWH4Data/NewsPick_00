import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'       // 로그인 화면
import HomeView from '@/views/HomeView.vue'         // 홈 화면
import RegisterView from '@/views/RegisterView.vue' // 회원가입 화면

const routes = [
  { path: '/', name: 'login', component: LoginView },        // 기본 경로는 로그인
  { path: '/home', name: 'home', component: HomeView },       // 홈 화면
  { path: '/register', name: 'register', component: RegisterView }, // 회원가입 화면
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
