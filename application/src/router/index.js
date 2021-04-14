import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Download from '../views/Download.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/:download',
    name: 'download',
    component: Download
  },
  {
    path: '/',
    name: 'Home',
    component: Home
  },

]

const router = new VueRouter({
  routes
})

export default router
