import VueRouter from 'vue-router'
import Vue from 'vue'
import Index from '../components/index'
import Editor from '../components/editor'
import Viewer from '../components/viewer'

Vue.use(VueRouter)

var router = new VueRouter({
  routes: [
    {
      path: '/',
      name: 'index',
      component: Index
    }, {
      path: '/editor',
      name: 'newEditor',
      component: Editor
    }, {
      path: '/editor/:id',
      name: 'updateEditor',
      component: Editor
    }, {
      path: '/viewer/:id',
      name: 'viewer',
      component: Viewer
    }
  ]
})

export default router
