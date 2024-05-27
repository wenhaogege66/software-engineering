import { createRouter, createWebHistory} from 'vue-router'
//import 自定义组件名 from 路径
import Deposit from '@/cashier/components/deposit.vue'
import Withdrawal from '@/cashier/components/withdrawal.vue'
import Transfer from '@/cashier/components/transfer.vue'
import Query from '@/cashier/components/query.vue'
import AccountManage from "@/cashier/components/accountStatus.vue";
import AccountOpen from "@/cashier/components/accountOpen.vue";
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/cashier'
        },
        {
            path: '/cashier/accountManage',
            component: AccountManage,
        },
        {
            path: '/cashier/deposit',
            component: Deposit
        },
        {
            path: '/cashier/withdrawal',
            component: Withdrawal
        },
        {
            path: '/cashier/transfer',
            component: Transfer
        },
        {
            path: '/cashier/query',
            component: Query,
        },
        {
            path: '/cashier/accountOpen',
            component: AccountOpen,
        },
    ],
})

export default router