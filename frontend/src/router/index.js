import { createRouter, createWebHistory } from 'vue-router'
import AuthToken from '../views/AuthToken.vue'
import MainPage from '@/views/MainPage.vue'
const routes = [

 
  {
    path:'/auth_token',
    name:'auth_token',
    component:AuthToken
  },
  {
    path:'/',
    name:'main',
    component:MainPage

  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
