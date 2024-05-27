<template>
    <el-scrollbar height="100%" style="width: 100%;">

    <!-- 标题和搜索框 -->
    <div style="margin-top: 20px; margin-left: 40px; font-size: 2em; font-weight: bold;">
        查询记录
        <el-input v-model="toSearch" :prefix-icon="Search"
            style=" width: 15vw;min-width: 150px; margin-left: 30px; margin-right: 30px; float: right; ;"
            clearable />
    </div>

    <!-- 存款操作 -->
    <div style="width:70%;margin-left: 30px; padding-top:5vh;">
        <el-input v-model="this.toQuery" style="display:inline; " placeholder="输入账户ID"></el-input>
        <!-- <el-radio style="margin-left: 10px;" v-model="deposit_checked">存款记录</el-radio>
        <el-radio style="margin-left: 10px;" v-model="withdrawl_checked">取款记录</el-radio>
        <el-radio style="margin-left: 10px;" v-model="transfer_checked">转账记录</el-radio> -->
        <el-radio-group  style="margin-left: 10px;" v-model="select">
            <el-radio :label="1">存款记录</el-radio>
            <el-radio :label="2">取款记录</el-radio>
            <el-radio :label="3">转账记录</el-radio>
        </el-radio-group>
        <el-button style="margin-left: 100px;" type="primary" @click="this.QueryRecords">查询</el-button>
    </div>

    <!-- 存款记录 -->
    <div class="cashierBox" v-for="deposit_record in deposit_records" :key="deposit_record.deposit_record_id">
        <el-table v-if="isDepositShow" :data="fitlerTableData_Deposit" height="600"
            :default-sort="{ prop: 'deposit_record_id', order: 'ascending' }" :table-layout="'auto'"
            style="width: 100%; margin-left: 50px; margin-top: 30px; margin-right: 50px; max-width: 80vw;">
            <el-table-column v-if="isDepositShow" prop="deposit_record_id" label="存款记录ID" sortable/>
            <el-table-column v-if="isDepositShow" prop="account_id" label="账户ID" sortable/>
            <el-table-column v-if="isDepositShow" prop="deposit_type" label="存款类型" />
            <el-table-column v-if="isDepositShow" prop="auto_renew_status" label="是否自动续期" />
            <el-table-column v-if="isDepositShow" prop="deposit_start_date" label="存款起始日期" />
            <el-table-column v-if="isDepositShow" prop="deposit_end_date" label="存款终止日期" />
            <el-table-column v-if="isDepositShow" prop="deposit_amount" label="存款金额" />
            <el-table-column v-if="isDepositShow" prop="cashier_id" label="出纳员ID" />
            <!-- <el-table-column label="操作">
                <template #default="scope">
                    <el-button :disabled="scope.row.returnTime !== '0' " link type="primary" size="small" @click="returnBook(scope.row)" v-model="returnBookVisible">还书</el-button>
                </template>
            </el-table-column> -->
        </el-table>
    </div>

    <!-- 取款记录 -->
    <div class="cashierBox" v-for="withdrawl_record in withdrawl_records" :key="withdrawl_record.withdrawl_record_id">
    <el-table v-if="isWithdrawlShow" :data="fitlerTableData_Withdrawl" height="600"
        :default-sort="{ prop: 'withdrawl_record_id', order: 'ascending' }" :table-layout="'auto'"
        style="width: 100%; margin-left: 50px; margin-top: 30px; margin-right: 50px; max-width: 80vw;">
        <el-table-column prop="withdrawl_record_id" label="取款记录ID" sortable/>
        <el-table-column prop="account_id" label="账户ID" sortable/>
        <el-table-column prop="withdrawl_date" label="取款日期" />
        <el-table-column prop="withdrawl_amount" label="取款金额" />
        <el-table-column prop="cashier_id" label="出纳员ID" />
        <!-- <el-table-column label="操作">
            <template #default="scope">
                <el-button :disabled="scope.row.returnTime !== '0' " link type="primary" size="small" @click="returnBook(scope.row)" v-model="returnBookVisible">还书</el-button>
            </template>
        </el-table-column> -->
    </el-table>
    </div>

    <!-- 转账记录 -->
    <div class="cashierBox" v-for="transfer_record in transfer_records" :key="transfer_record.transfer_record_id">
    <el-table v-if="isTransferShow" :data="fitlerTableData_Transfer" height="600"
        :default-sort="{ prop: 'withdrawl_record_id', order: 'ascending' }" :table-layout="'auto'"
        style="width: 100%; margin-left: 50px; margin-top: 30px; margin-right: 50px; max-width: 80vw;">
        <el-table-column prop="transfer_record_id" label="转账记录ID" sortable/>
        <el-table-column prop="account_in_id" label="转入账户ID" sortable/>
        <el-table-column prop="account_out_id" label="转出账户ID" />
        <el-table-column prop="transfer_date" label="转账日期" />
        <el-table-column prop="transfer_amount" label="转账金额" />
        <el-table-column prop="cashier_id" label="出纳员ID" />
        <!-- <el-table-column label="操作">
            <template #default="scope">
                <el-button :disabled="scope.row.returnTime !== '0' " link type="primary" size="small" @click="returnBook(scope.row)" v-model="returnBookVisible">还书</el-button>
            </template>
        </el-table-column> -->
    </el-table>
    </div>


    </el-scrollbar>


</template>

<script>
import axios from 'axios';
import { Delete, Edit, Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

export default {
    data() {
        return {
            cashierID: 1,
            isDepositShow: false, // 存款记录展示状态
            isWithdrawlShow: false, // 取款记录展示状态
            isTransferShow: false, // 转账记录展示状态
            select:0,
            deposit_records: [{ // 列表项
                deposit_record_id: 1,
                account_id: 1,
                deposit_type: "活期存款",
                auto_renew_status: "/",
                deposit_start_date: 0,
                deposit_end_date: 1,
                deposit_amount : 100.00,
                cashier_id: 1
            }],
            withdrawl_records: [{ // 列表项
                withdrawl_record_id: 1,
                account_id: 1,
                withdrawl_date: 1,
                withdrawl_amount : 100.00,
                cashier_id: 1
            }],
            transfer_records: [{ // 列表项
                transfer_record_id: 1,
                account_in_id: 1,
                account_out_id: 1,
                transfer_date: 1,
                transfer_amount : 100.00,
                cashier_id: 1
            }],
            deposit_checked:false,
            withdrawl_checked:false,
            transfer_checked:false,
            DemandDepositVisible:false,
            TimeDepositVisible:false,
            TotalDepositVisible:false,
            Search,
            toSearch: '', // 搜索内容
            toQuery:'',
            newDepositInfo: { // 待新建存款信息
                account_id: '',
                password: '',
                deposit_amount: 0
            },
            newTimeDepositInfo: {
                account_id: '',
                password: '',
                deposit_amount: 0,
                deposit_term: 0,
                is_auto_renew: false
            }
        }
    },
    computed: {
        fetchDataFromUrl() {
            // 获取当前URL
            const url = new URL(window.location);

            // 创建URLSearchParams对象
            const params = new URLSearchParams(url.search);

            // 从查询字符串中获取参数
            this.cashierID = params.get('cashierID');
        },
        fitlerTableData_Deposit() { // 搜索规则
            return this.deposit_records.filter(
                (tuple) =>
                    (this.toSearch == '')  // 搜索框为空，即不搜索
                //     tuple.bookID == this.toSearch || // 图书号与搜索要求一致
                //     tuple.borrowTime.toString().includes(this.toSearch) || // 借出时间包含搜索要求
                //     tuple.returnTime.toString().includes(this.toSearch) // 归还时间包含搜索要求
            )
        },
        fitlerTableData_Withdrawl() { // 搜索规则
            return this.withdrawl_records.filter(
                (tuple) =>
                    (this.toSearch == '')  // 搜索框为空，即不搜索
                //     tuple.bookID == this.toSearch || // 图书号与搜索要求一致
                //     tuple.borrowTime.toString().includes(this.toSearch) || // 借出时间包含搜索要求
                //     tuple.returnTime.toString().includes(this.toSearch) // 归还时间包含搜索要求
            )
        },
        fitlerTableData_Transfer() { // 搜索规则
            return this.transfer_records.filter(
                (tuple) =>
                    (this.toSearch == '')  // 搜索框为空，即不搜索
                //     tuple.bookID == this.toSearch || // 图书号与搜索要求一致
                //     tuple.borrowTime.toString().includes(this.toSearch) || // 借出时间包含搜索要求
                //     tuple.returnTime.toString().includes(this.toSearch) // 归还时间包含搜索要求
            )
        }
    },
    methods: {
        fetchDataFromUrl() {
            // 获取当前URL
            const url = new URL(window.location);

            // 创建URLSearchParams对象
            const params = new URLSearchParams(url.search);

            // 从查询字符串中获取参数
            this.cashierID = params.get('cashierID');
        },
        async QueryRecords() {
            this.deposit_records = [],
            this.withdrawl_records = [],
            this.transfer_record = []
            let response = await axios.get('/all-records/', { 
                params: { 
                    type:this.select,
                    account_id:this.toQuery
                } 
            }) 
            let records = response.data // 获取响应负载
            //存款记录
            if(this.select === 1) {
                recordss.forEach(record => { // 对于每一个借书记录
                this.deposit_records.push(record) // 将它加入到列表项中
                });
                this.isDepositShow = true // 显示结果列表
            }
            else this.isDepositShow = false

            //取款记录
            if(this.select === 2) {
                recordss.forEach(record => { // 对于每一个借书记录
                this.withdrawl_records.push(record) // 将它加入到列表项中
                });
                this.isWithdrawlShow = true // 显示结果列表
            }
            else this.isWithdrawlShow = false

            //转账记录
            if(this.select === 3) {
                recordss.forEach(record => { // 对于每一个借书记录
                this.transfer_records.push(record) // 将它加入到列表项中
                });
                this.isTransferShow = true // 显示结果列表
            }
            else this.isTransferShow = false
        },
    },
    mounted() { // 当页面被渲染时
        // this.QueryRecords() // 查询存款记录
    }

}
</script>

<style scoped>

</style>