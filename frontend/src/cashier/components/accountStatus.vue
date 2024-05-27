<template>
  <el-scrollbar height="100%" style="width: 100%; height: 100%">
    <div style="margin-top: 20px; margin-left:20px; font-size: 2em; font-weight: bold;">
      账户状态管理
    </div>
    <div style="width:30%;margin:0 auto; padding-top:5vh;">

      <el-input  v-model="queryAccountID" style="display:inline; " placeholder="输入账户ID"></el-input>
      <el-button style="margin-left: 10px;" type="primary" @click="QueryAccount" :disabled="queryAccountID.length === 0">查询</el-button>
      <div class="accountBox" v-if="isShow">
        <div style="font-size: 25px; font-weight: bold;">账户ID： {{account.id}}</div>

        <el-divider />

        <p style="padding: 2.5px;"><span style="font-weight: bold">余额：￥</span>{{account.balance}}</p>
        <p style="padding: 2.5px;"><span style="font-weight: bold">定期存款：￥</span>{{account.currentDeposit}}</p>
        <p style="padding: 2.5px;"><span style="font-weight: bold">待定存款：￥</span>{{account.uncreditedDeposit}}</p>
        <p style="padding: 2.5px;"><span style="font-weight: bold">身份证：</span>{{account.identity_card}}</p>
        <p style="padding: 2.5px;">
          <el-tag type = "danger" v-if="account.isFrozen">已冻结</el-tag>
          <el-tag v-else>未冻结</el-tag>
          <span style = "padding: 10px"></span>
          <el-tag type = "danger" v-if="account.isLost" style="margin-left: 10px">已挂失</el-tag>
          <el-tag v-else>未挂失</el-tag>
        </p>

        <el-divider />

        <div style="margin-top: 10px; margin-left: 75px; display:flex">
          <el-button v-if = "account.isFrozen && !account.isLost" type="primary"
                     @click = "unfreezeAccountID = queryAccountID, unfreezeVisible = true">解冻 </el-button>
          <el-button v-if = "!account.isFrozen && !account.isLost" type="primary"
                     @click = "freezeAccountID = queryAccountID, freezeVisible = true">冻结 </el-button>
          <el-button v-if = "!account.isFrozen && account.isLost" type="primary"
                     @click = "reissueAccountID = queryAccountID, reissueVisible = true">补发 </el-button>
          <el-button v-if = "!account.isFrozen && !account.isLost" type="primary"
                     @click = "reportLossAccountID = queryAccountID, reportLossVisible = true">挂失 </el-button>
        </div>
      </div>
    </div>
    <el-dialog v-model="unfreezeVisible" title="账户解冻" width="30%">
      <span>确定解冻<span style="font-weight: bold;">{{ unfreezeAccountID }}号账户</span>吗？</span>

      <template #footer>
                <span class="dialog-footer">
                    <el-button @click="unfreezeVisible = false">取消</el-button>
                    <el-button type="danger" @click="ConfirmUnfreezeAccount">
                        确定
                    </el-button>
                </span>
      </template>
    </el-dialog>

    <el-dialog v-model="freezeVisible" title="账户冻结" width="30%">
      <span>确定冻结<span style="font-weight: bold;">{{ freezeAccountID }}号账户</span>吗？</span>

      <template #footer>
                <span class="dialog-footer">
                    <el-button @click="freezeVisible = false">取消</el-button>
                    <el-button type="danger" @click="ConfirmFreezeAccount">
                        确定
                    </el-button>
                </span>
      </template>
    </el-dialog>

    <el-dialog v-model="reportLossVisible" title="账户挂失" width="30%">
      <span>确定挂失<span style="font-weight: bold;">{{ reportLossAccountID }}号账户</span>吗？</span>

      <template #footer>
                <span class="dialog-footer">
                    <el-button @click="reportLossVisible = false">取消</el-button>
                    <el-button type="danger" @click="ConfirmReportLossAccount">
                        确定
                    </el-button>
                </span>
      </template>
    </el-dialog>

    <el-dialog v-model="reissueVisible" title="账户补发" width="30%">
      <span>确定补发<span style="font-weight: bold;">{{ reissueAccountID }}号账户</span>吗？</span>

      <template #footer>
                <span class="dialog-footer">
                    <el-button @click="reissueVisible = false">取消</el-button>
                    <el-button type="danger" @click="ConfirmReissueAccount">
                        确定
                    </el-button>
                </span>
      </template>
    </el-dialog>
  </el-scrollbar>
</template>

<script>
  import axios from "axios";
  import {ElMessage} from "element-plus";

  export default {
    created() {
      this.fetchDataFromUrl();
    },
    data() {
      return {
        cashierID: 0,
        queryAccountID: '',
        freezeAccountID: 0,
        unfreezeAccountID: 0,
        reportLossAccountID: 0,
        reissueAccountID: 0,
        unfreezeVisible: false,
        freezeVisible: false,
        reportLossVisible: false,
        reissueVisible: false,
        newReissueAccountID: 0, // 补发新账号ID
        isShow: false,
        account:
            {
              id: 3,
              password: '',
              identity_card: '330782200408076216',
              //cardType: '',
              balance: 100.00,
              currentDeposit: 44.0,
              uncreditedDeposit: 56.0,
              isFrozen: false,
              isLost: false
            }
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
      ConfirmUnfreezeAccount() {
        // this.account.isFrozen = false
        // this.unfreezeVisible = false
        axios.post('/cashier/unfreeze/',
            {
              accountID : this.unfreezeAccountID,
            }).then(response=>{
              ElMessage.success("账户解冻成功")
              this.unfreezeVisible = false
              this.account.isFrozen = false
        })
      },
      ConfirmFreezeAccount() {
        // this.account.isFrozen = true
        // this.freezeVisible = false
        axios.post('/cashier/freeze/',
            {
              accountID : this.freezeAccountID,
            }).then(response=>{
          ElMessage.success("账户冻结成功")
          this.freezeVisible = false
          this.account.isFrozen = true
        })
      },
      ConfirmReportLossAccount() {
        // this.account.isLost = true
        // this.reportLossVisible = false
        axios.post('/cashier/reportloss/',
            {
              accountID: this.reportLossAccountID,
            }).then(response=>{
              ElMessage.success("账户挂失成功")
              this.reportLossVisible = false
              this.account.isLost = true
              this.reportLossVisible = false
        })
      },
      ConfirmReissueAccount() {
        // this.reissueVisible = false
        // this.isShow = false
        // this.queryAccountID = ''
        axios.post('/cashier/reissue/',
            {
              account: this.reissueAccountID,
            }).then(response=>{
            this.newReissueAccountID = response.data.accountID;
            ElMessage.success("账户补发成功，新账户ID: "+ this.newReissueAccountID);
            this.reissueVisible = false
            this.isShow = false
            this.queryAccountID = ''
        })
      },
      QueryAccount(){
        this.account = {} // 清空账号信息
        axios.get('/cashier/queryAccount',
            {
              params: {accountID : parseInt(this.queryAccountID) }
            }).then(response => {
              this.account = response.data
              this.isShow = true;
            })
        // this.isShow = true
      }
    }
  }
</script>

<style scoped>
.accountBox {
  height:350px;
  width: 300px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  text-align: center;
  margin-top: 80px;
  margin-left: 0px;
  margin-right: 10px;
  padding: 7.5px;
  padding-right: 10px;
  padding-top: 15px;
}
</style>