import { createRouter, createWebHistory} from 'vue-router'
//import 自定义组件名 from 路径
import Personal from '@/online_user/components/personal.vue'
//E:\vue_project\FSE-B1-master\frontend\src\online_user\components\personal.vue
import Black from '@/online_user_administrator/components/black.vue'
import Permission from '@/online_user_administrator/components/permission.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/online_manager'
        },
        {
            path: '/online_manager/black',
            component: Black,
        },
        {
            path: '/online_manager/permission',
            component: Permission,
        }
    ]
})

export default router