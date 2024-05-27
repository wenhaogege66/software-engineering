<template>
    <el-scrollbar height="100%" style="width: 100%;">

    <!-- 标题和搜索框 -->
    <div style="margin-top: 20px; margin-left: 40px; font-size: 2em; font-weight: bold;">
        账户转账
        <el-input v-model="toSearch" :prefix-icon="Search"
            style=" width: 15vw;min-width: 150px; margin-left: 30px; margin-right: 30px; float: right; ;"
            clearable />
    </div>

    <!-- 转账操作 -->
    <div style="width:30%;margin-left:30px; padding-top:5vh;">
        <el-button style="margin-left: 10px;" type="primary" @click="this.TransferVisible = true">转账服务</el-button>
    </div>

    <!-- 转账记录 -->
    <div class="cashierBox" v-for="record in records" :key="record.deposit_record_id">
        <el-table v-if="isShow" :data="fitlerTableData" height="600"
            :default-sort="{ prop: 'transfer_record_id', order: 'ascending' }" :table-layout="'auto'"
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
        <el-dialog v-model="TransferVisible" title="转账服务" width="30%" align-center>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                转入账户ID：
                <el-input v-model="newTransferInfo.account_in_id" style="width: 12.5vw;" clearable />
            </div>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                转出账户ID：
                <el-input v-model="newTransferInfo.account_out_id" style="width: 12.5vw;" clearable />
            </div>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                密码：
                <el-input v-model="newTransferInfo.password" style="width: 12.5vw;" clearable />
            </div>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                转账金额：
                <el-input v-model="newTransferInfo.transfer_amount" style="width: 12.5vw;" clearable />
            </div>
            

            <template #footer>
                <span>
                    <el-button @click="TransferVisible = false">取消</el-button>
                    <el-button type="primary" @click="setNewTransfer"
                        :disabled="newTransferInfo.account_in_id.length === 0 || newTransferInfo.account_out_id.length === 0 || newTransferInfo.password.length === 0">确定</el-button>
                </span>
            </template>
        </el-dialog>



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
            isShow: false, // 结果表格展示状态
            records: [{ // 列表项
                transfer_record_id: 1,
                account_in_id: 1,
                account_out_id: 1,
                transfer_date: 1,
                transfer_amount : 100.00,
                cashier_id: 1
            }],
            TransferVisible:false,
            Search,
            toSearch: '', // 搜索内容
            newTransferInfo: { // 待新建存款信息
                account_in_id: '',
                account_out_id: '',
                password: '',
                transfer_amount: 0
            }
        }
    },
    computed: {
        fitlerTableData() { // 搜索规则
            return this.records.filter(
                (tuple) =>
                    (this.toSearch == '') || // 搜索框为空，即不搜索
                    tuple.bookID == this.toSearch || // 图书号与搜索要求一致
                    tuple.borrowTime.toString().includes(this.toSearch) || // 借出时间包含搜索要求
                    tuple.returnTime.toString().includes(this.toSearch) // 归还时间包含搜索要求
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
        QueryTransfers() {
            this.records = []   
            axios.get('/cashier/all-transfers/')
            .then(response => {
                let records = response.data
                console.log(response.data)
                records.forEach(record => {
                this.records.push(record)
                })
            }).catch(error => {
                console.error('There was an error!', error);
                // 可以在这里处理错误，例如显示错误消息
            });
            this.isShow = true // 显示结果列表
        },
        setNewTransfer() {
            axios.post("/cashier/transfer/",
                { // 请求体
                    account_in_id: this.newTransferlInfo.account_in_id,
                    account_out_id: this.newTransferlInfo.account_out_id,
                    password: this.newTransferInfo.password,
                    transfer_amount : this.newTransferInfo.transfer_amount,
                    cashier_id: this.cashierID
                    
                })
                .then(response => {
                    ElMessage.success("转账成功") // 显示消息提醒
                    this.TransferVisible = false // 将对话框设置为不可见
                    this.QueryTransfers() // 重新查询存款记录以刷新页面
                })
        },
    },
    mounted() { // 当页面被渲染时
        this.QueryTransfers() // 查询转账记录
    }

}
</script>

<style scoped>

</style>