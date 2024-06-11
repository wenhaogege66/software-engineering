<template>
  <el-scrollbar height="100%" style="width: 100%">
    <!-- 标题和搜索框 -->
    <div
      style="
        margin-top: 20px;
        margin-left: 40px;
        font-size: 2em;
        font-weight: bold;
      "
    >
      查询记录
      <el-input
        v-model="toSearch"
        :prefix-icon="Search"
        style="
          width: 15vw;
          min-width: 150px;
          margin-left: 30px;
          margin-right: 30px;
          float: right;
        "
        clearable
      />
    </div>

    <!-- 存款操作 -->
    <div style="width: 70%; margin-left: 30px; padding-top: 5vh">
      <!-- <el-input v-model="this.toQuery" style="display:inline; " placeholder="输入银行卡号"></el-input> -->
      <!-- <el-radio style="margin-left: 10px;" v-model="deposit_checked">存款记录</el-radio>
      <el-radio style="margin-left: 10px;" v-model="withdrawl_checked">取款记录</el-radio>
      <el-radio style="margin-left: 10px;" v-model="transfer_checked">转账记录</el-radio> -->
      <el-radio-group style="margin-left: 10px" v-model="select">
        <el-radio :label="1">存款记录</el-radio>
        <el-radio :label="2">取款记录</el-radio>
        <el-radio :label="3">转账记录</el-radio>
      </el-radio-group>
      <el-button
        style="margin-left: 100px"
        type="primary"
        @click="this.QueryRecords"
        >查询</el-button
      >
    </div>

    <!-- 存款记录 -->
    <el-table
      v-for="deposit_record in deposit_records"
      :data="fitlerTableData_Deposit"
      :v-show="this.isDepositShow"
      height="600"
      :default-sort="{ prop: 'deposit_start_date', order: 'ascending' }"
      :table-layout="'auto'"
      :key="deposit_record"
      style="
        width: 100%;
        margin-left: 50px;
        margin-top: 30px;
        margin-right: 50px;
        max-width: 80vw;
      "
    >
      <el-table-column prop="account_id" label="账户ID" />
      <el-table-column prop="deposit_type" label="存款类型" sortable />
      <el-table-column prop="deposit_amount" lable="存款金额" sortable />
      <el-table-column prop="deposit_start_date" label="存款时间" sortable />
      <el-table-column prop="deposit_end_date" label="存款结束时间" sortable />
      <el-table-column prop="cashier_id" label="操作账户" sortable />
    </el-table>
    <!--取款-->
    <el-table
      :v-show="this.isWithdrawlShow"
      v-for="withdrawl_record in withdrawl_records"
      :data="fitlerTableData_Withdrawl"
      :key="withdrawl_record"
      height="600"
      :default-sort="{ prop: 'withdrawl_date', order: 'ascending' }"
      :table-layout="'auto'"
      style="
        width: 100%;
        margin-left: 50px;
        margin-top: 30px;
        margin-right: 50px;
        max-width: 80vw;
      "
    >
      <el-table-column prop="account_id" label="账户ID" />
      <el-table-column prop="withdrawl_amount" lable="取款金额" sortable />
      <el-table-column prop="withdrawl_date" label="取款时间" sortable />

      <el-table-column prop="cashier_id" label="操作账户" sortable />
    </el-table>
    <!--交易-->
    <el-table
      :v-show="this.isTransferShow"
      v-for="transfer_record in transfer_records"
      :data="fitlerTableData_Transfer"
      :key="transfer_record"
      height="600"
      :default-sort="{ prop: 'deposit_start_date', order: 'ascending' }"
      :table-layout="'auto'"
      style="
        width: 100%;
        margin-left: 50px;
        margin-top: 30px;
        margin-right: 50px;
        max-width: 80vw;
      "
    >
      <el-table-column prop="account_in_id" label="收款账户ID" />
      <el-table-column prop="account_out_id" label="转款账户ID" sortable />
      <el-table-column prop="transfer_amount" lable="交易金额" sortable />
      <el-table-column prop="transfer_date" label="交易时间" sortable />
      <el-table-column prop="cashier_id" label="操作账户" sortable />
    </el-table>
  </el-scrollbar>
</template>

<script>
import axios from "axios";
import { Delete, Edit, Search } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";

export default {
  data() {
    return {
      nowdate: "",
      cashierID: 1,
      isDepositShow: false, // 存款记录展示状态
      isWithdrawlShow: false, // 取款记录展示状态
      isTransferShow: false, // 转账记录展示状态
      select: 0,
      deposit_records: [
        {
          // 列表项
          deposit_record_id: 1,
          account_id: 1,
          deposit_type: "活期存款",
          auto_renew_status: "/",
          deposit_start_date: 0,
          deposit_end_date: 1,
          deposit_amount: 100.0,
          cashier_id: 1,
        },
      ],
      withdrawl_records: [
        {
          // 列表项
          withdrawl_record_id: 1,
          account_id: 1,
          withdrawl_date: 1,
          withdrawl_amount: 100.0,
          cashier_id: 1,
        },
      ],
      transfer_records: [
        {
          // 列表项
          transfer_record_id: 1,
          account_in_id: 1,
          account_out_id: 1,
          transfer_date: 1,
          transfer_amount: 100.0,
          cashier_id: 1,
        },
      ],
      deposit_checked: false,
      withdrawl_checked: false,
      transfer_checked: false,
      DemandDepositVisible: false,
      TimeDepositVisible: false,
      TotalDepositVisible: false,
      AutoEditVisible: false,
      Search,
      toSearch: "", // 搜索内容
      toQuery: "",
      newDepositInfo: {
        // 待新建存款信息
        account_id: "",
        password: "",
        deposit_amount: 0,
      },
      newTimeDepositInfo: {
        account_id: "",
        password: "",
        deposit_amount: 0,
        deposit_term: 0,
        is_auto_renew: false,
      },
    };
  },
  computed: {
    fetchDataFromUrl() {
      // 获取当前URL
      const url = new URL(window.location);

      // 创建URLSearchParams对象
      const params = new URLSearchParams(url.search);

      // 从查询字符串中获取参数
      this.cashierID = params.get("cashierID");
    },
    fitlerTableData_Deposit() {
      // 搜索规则
      return this.deposit_records.filter(
        (tuple) => this.toSearch == "", // 搜索框为空，即不搜索
        tuple.deposit_record_id === this.toSearch ||
          tuple.cashier_id === this.toSearch ||
          tuple.deposit_amount >= this.toSearch ||
          tuple.deposit_start_date.toString().includes(this.toSearch) ||
          tuple.deposit_end_date.toString().includes(this.toSearch)
      );
    },
    fitlerTableData_Withdrawl() {
      // 搜索规则
      return this.withdrawl_records.filter(
        (tuple) => this.toSearch == "", // 搜索框为空，即不搜索
        tuple.withdrawl_record_id === this.toSearch ||
          tuple.cashier_id === this.toSearch ||
          tuple.withdrawl_amount >= this.toSearch ||
          tuple.withdrawl_date.toString().includes(this.toSearch)
      );
    },
    fitlerTableData_Transfer() {
      // 搜索规则
      return this.transfer_records.filter(
        (tuple) => this.toSearch == "",
        tuple.transfer_record_id === this.toSearch ||
          tuple.cashier_id === this.toSearch ||
          tuple.transfer_amount >= this.toSearch ||
          tuple.transfer_date.toString().includes(this.toSearch)
      );
    },
  },
  methods: {
    fetchDataFromUrl() {
      // 获取当前URL
      const url = new URL(window.location);

      // 创建URLSearchParams对象
      const params = new URLSearchParams(url.search);

      // 从查询字符串中获取参数
      this.cashierID = params.get("cashierID");
    },
    async QueryRecords() {
      // console.log(this.deposit_records)
      (this.deposit_records = []),
        (this.withdrawl_records = []),
        (this.transfer_records = []);
      let response = await axios.get("/online_user/all-records/", {
        params: {
          account_id: this.toQuery,
          record_type: this.select,
        },
      });
      let records = response.data; // 获取响应负载
      //存款记录
      if (this.select === 1) {
        records.forEach((record) => {
          this.deposit_records.push(record); // 将它加入到列表项中
        });
        this.isDepositShow = true; // 显示结果列表
      } else this.isDepositShow = false;

      //取款记录
      if (this.select === 2) {
        records.forEach((record) => {
          this.withdrawl_records.push(record); // 将它加入到列表项中
        });
        this.isWithdrawlShow = true; // 显示结果列表
      } else this.isWithdrawlShow = false;

      //转账记录
      if (this.select === 3) {
        records.forEach((record) => {
          this.transfer_records.push(record); // 将它加入到列表项中
        });
        this.isTransferShow = true; // 显示结果列表
      } else this.isTransferShow = false;
    },
    //   editAuto(data) {
    //       console.log(data)
    //       axios.post("/cashier/update-auto-renew/",
    //           { // 请求体
    //               record_id: data
    //           })
    //           .then(response => {
    //               ElMessage.success("更改成功") // 显示消息提醒
    //               this.QueryRecords() // 重新查询存款记录以刷新页面
    //           })
    //   }
  },
  mounted() {
    // 当页面被渲染时
    this.QueryRecords(); // 查询存款记录
    this.date = new Date();
    console.log(this.date);
  },
};
</script>

<style scoped>
</style>