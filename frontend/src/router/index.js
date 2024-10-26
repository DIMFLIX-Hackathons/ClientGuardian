import { createRouter, createWebHistory } from 'vue-router'
import AuthToken from '../views/AuthToken.vue'
import MainPage from '@/views/MainPage.vue'
import { checkToken } from '@/modules/api'


const routes = [
  {
    path:'/authorization',
    name:'auth_token',
    component:AuthToken,
    meta: { requiresAuth: false}
  },
  {
    path:'/',
    name:'main',
    component: MainPage,
    meta: { requiresAuth: true}
  }
]

export const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})


router.beforeEach(async (to, from, next) => {
	if (to.matched.some((record) => record.meta.requiresAuth)) {
	  	const isAuth = await checkToken();
	  	if (!isAuth) {
        router.push('/authorization');
	  	}
	}
	next();
});

export default router;

