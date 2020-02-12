import Vue from 'vue'
import Router from 'vue-router'
import CaseListContent from './views/content/CaseListContent/CaseList.vue'
import WindMap from './views/content/wind/windMap.vue'
import CurrentMap from './views/content/current/currentMap.vue'
import RescueMap from './views/content/rescue/rescueContent.vue'
import OilMap from './views/content/oilspilling/oilSpillingMap.vue'
import OilMapNew from './views/content/oilspilling/oilSpillingMap2.vue'
import OilMapMerge from './views/content/oilspilling/oilSpillingMap3.vue'
import Login from './views/home/login.vue'
import Content from './views/home/content.vue'
// import Home from "./views/Home.vue";
// 由于加入了未认证和已认证的方法，需要访问store
import store from './store/index'
// 注意此处需要定义两个方法，分别用来处理未认证和已经认证
const requireAuthenticated = (to, from, next) => {
    // 通过store.dipatch 触发 vuex的action方法
    // 注意此处有问题，由于initizlize方法并不返回promise，所以不要使用then
    // store.dispatch('auth/initialize').then(() => {
    //     if (!store.getters['auth/isAuthenticated']) {
    //         next('/login')
    //     } else {
    //         next()
    //     }
    // })

    store.dispatch('auth/initialize').then(() => console.log('执行了初始化认证的操作'))
    if (!store.getters['auth/isAuthenticated']) {
        next('/login')
    } else {
        next()
    }
}

const requireUnauthenticated = (to, from, next) => {
    // store.dispatch('auth/initialize').then(() => {
    //     if (store.getters['auth/isAuthenticated']) {
    //         next('/home')
    //     } else {
    //         next()
    //     }
    // })
    store.dispatch('auth/initialize')
    if (store.getters['auth/isAuthenticated']) {
        next('/home')
    } else {
        next()
    }
}

Vue.use(Router)

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            // 注意以/ 开头的嵌套路径会被当做根路径
            path: '/content',
            component: Content,
            children: [
                {
                    // 嵌套路径需要去掉 / (不然会被当做根路径)
                    path: 'caselist',
                    name: 'caselist',
                    component: CaseListContent,
                    // 开始加入了需要判断是否登录的验证(只有登录的才让访问该页面)
                    beforeEnter: requireAuthenticated
                },
                {
                    path: 'windmap',
                    name: 'windmap',
                    component: WindMap
                },
                {
                    path: 'currentmap',
                    name: 'currentmap',
                    component: CurrentMap
                },
                {
                    path: 'rescuemap',
                    name: 'rescuemap',
                    component: RescueMap
                },
                {
                    path: 'oilmap',
                    name: 'oilmap',
                    component: OilMap
                },
                {
                    path: 'newoilmap',
                    name: 'newoilmap',
                    component: OilMapNew
                },
                {
                    path: 'mergeoilmap',
                    name: 'mergeoilmap',
                    component: OilMapMerge
                }
            ]
        },
        {
            path: '/login',
            name: 'login',
            component: Login,
            // 注意此处需要加入判定是否为未登陆的验证，若未登录才跳转
            beforeEnter: requireUnauthenticated
        },
        {
            path: '/home',
            redirect: '/content/caselist'
        }
        // {
        //   path: "/about",
        //   name: "about",
        //   // route level code-splitting
        //   // this generates a separate chunk (about.[hash].js) for this route
        //   // which is lazy-loaded when the route is visited.
        //   component: () =>
        //     import(/* webpackChunkName: "about" */ "./views/About.vue")
        // }
    ]
})
