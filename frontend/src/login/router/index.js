import { createRouter, createWebHistory} from 'vue-router'
//import 自定义组件名 from 路径
import User from "@/login/components/user.vue";
import Employee from "@/login/components/employee.vue";
import Signup from "@/login/components/signup.vue";
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/login'
        },
        {
            path: '/login/user',
            component: User,
        },
        {
            path: '/login/employee',
            component: Employee,
        },
        {
            path: '/login/signup',
            component: Signup,
        }
    ]
})

export default router