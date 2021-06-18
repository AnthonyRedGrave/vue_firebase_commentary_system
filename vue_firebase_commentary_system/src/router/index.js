import { createRouter, createWebHistory } from 'vue-router'
// import App from '@/App.vue'
import Main from '@/components/Main.vue'
import Login from '@/components/Login.vue'
import Logout from '@/components/Logout.vue'
import Registration from '@/components/Registration.vue'
import store from '@/store/index.js'

const routes = [
  {
    path: '/',
    name: 'Main',
    component: Main,
    meta:{
      requiresLogin: true
    }
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/registration',
    name: 'Registration',
    component: Registration
  },
  {
    path: '/logout',
    name: 'Logout',
    component: Logout
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next)=>{
  if(to.matched.some(record => record.meta.requiresLogin)){
    if (!store.getters.loggedIn){
      next({name: 'login'})
    }
    else{
      next()
    }
  }
  else{
    next( )
  }
})

export default router
