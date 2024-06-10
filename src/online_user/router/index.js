import { createRouter, createWebHistory} from 'vue-router'
//import 自定义组件名 from 路径
import Personal from '@/online_user/components/personal.vue'
//E:\vue_project\FSE-B1-master\frontend\src\online_user\components\personal.vue
import Account from '@/online_user/components/account.vue'
import Record from '@/online_user/components/record.vue'
import Home from '@/online_user/components/home.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/online_user'
        },
        {
            path: '/online_user/personal',
            component: Personal,
        },
        {
            path: '/online_user/account',
            component: Account,
        },
        {
            path: '/online_user/record',
            component: Record,
        },
        {
            path: '/online_user/home',
            component: Home,
        }
    ]
})

export default router