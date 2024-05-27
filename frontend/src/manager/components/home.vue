<template>
  <el-scrollbar height="100%" style="width: 100%; height: 100%">
    <!--出纳员信息显示卡片-->
    <div style="margin-left:20px; display: flex;flex-wrap: wrap; justify-content: start;">
      <div class="cashierBox" v-for="cashier in cashiers" :key="cashier.id">
        <div>
          <!-- 卡片标题 -->
          <div style="font-size: 25px; font-weight: bold;">No. {{cashier.id}}</div>

          <el-divider />

          <!-- 卡片内容 -->
          <div style="margin-left: 10px; text-align: start; font-size: 16px;">
            <p style="padding: 2.5px;"><span style="font-weight: bold">姓名：</span>{{cashier.name}}</p>
            <p style="padding: 2.5px;"><span style="font-weight: bold">身份证：</span>{{ cashier.identity_card }}</p>
            <p style="padding: 2.5px;"><span style="font-weight: bold">账户名：</span>{{cashier.account}}</p>
            <p style="padding: 2.5px;"><span style="font-weight: bold">性别：</span>{{cashier.sex}}</p>
            <p style="padding: 2.5px;"><span style="font-weight: bold">电话：</span>{{cashier.phone}}</p>
            <p style="padding: 2.5px;">
              <el-tag v-if="cashier.ifTrade">账户交易权限</el-tag>
              <el-tag v-if="cashier.ifManage" style="margin-left: 10px">账户管理权限</el-tag>
            </p>
          </div>
          <el-divider />
          <!-- 卡片操作 -->
          <div style="margin-top: 10px; display:flex">
            <el-button type="primary" @click="this.modBaseCashierVisible = true, this.modBaseCashierInfo.id = cashier.id,
              this.modBaseCashierInfo.account = cashier.account, this.modBaseCashierInfo.password = cashier.password,
              this.modBaseCashierInfo.name = cashier.name, this.modBaseCashierInfo.phone = cashier.phone,
              this.modBaseCashierInfo.identity_card = cashier.identity_card, this.modBaseCashierInfo.sex = cashier.sex">
              修改信息
            </el-button>
            <el-button type="success" @click="this.modAuthorityCashierVisible = true, this.modAuthorityCashierInfo.id = cashier.id,
              this.modAuthorityCashierInfo.ifManage = cashier.ifManage, this.modAuthorityCashierInfo.ifTrade = cashier.ifTrade">
              修改权限
            </el-button>
            <el-button type="danger" @click="this.deleteCashierID = cashier.id, this.deleteCashierVisible = true">
              删除
            </el-button>
          </div>
        </div>
      </div>
      <el-button class="newCashierBox" @click="newCashierVisible = true">
        <el-icon style="height: 50px; width: 50px;">
          <Plus style="height: 100%; width: 100%;" />
        </el-icon>
      </el-button>
    </div>

    <!--添加出纳员对话框-->
    <el-dialog v-model = "newCashierVisible" title = "添加出纳员" width = "30%" align-center>
      <!--各类输入框-->
      <div style = "margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
        姓名：
        <el-input v-model="newCashierInfo.name" style="width: 12.5vw; margin-left: 2rem" clearable/>
      </div>
      <div style = "margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
        身份证：
        <el-input v-model="newCashierInfo.identity_card" style="width: 12.5vw; margin-left: 1rem" clearable/>
      </div>
      <div style = "margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
        账户名：
        <el-input v-model="newCashierInfo.account" style="width: 12.5vw; margin-left: 1rem" clearable/>
      </div>
      <div style = "margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
        密码：
        <el-input type="password" v-model="newCashierInfo.password" style="width: 12.5vw; margin-left: 2rem" clearable/>
      </div>
      <div style = "margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
        电话：
        <el-input v-model="newCashierInfo.phone" style="width: 12.5vw; margin-left: 2rem" clearable/>
      </div>
      <div style = "margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
        性别：
        <el-select v-model="newCashierInfo.sex" size="default" style="width: 5vw; margin-left: 2rem">
          <el-option v-for="type in sexTypes" :key="type.value" :label="type.label" :value="type.value" />
        </el-select>
      </div>
      <div style = "margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
        权限：
        <el-checkbox v-model="newCashierInfo.ifManage" label="账户管理" size="large" style="margin-left: 1.2rem"/>
        <el-checkbox v-model="newCashierInfo.ifTrade" label="账户交易" size="large" />
      </div>

      <!--底部按钮-->
      <template #footer>
              <span>
                  <el-button @click="newCashierVisible = false">取消</el-button>
                  <el-button type="primary" @click="ConfirmNewCashier"
                             :disabled="newCashierInfo.name.length === 0 || newCashierInfo.account.length === 0
                             || newCashierInfo.identity_card.length === 0 || newCashierInfo.password.length === 0
                             || newCashierInfo.phone === 0">确定</el-button>
              </span>
      </template>
    </el-dialog>

    <!-- 修改出纳员信息对话框 -->
    <el-dialog v-model = "modBaseCashierVisible" title = "修改出纳员信息" width = "30%" align-center>
      <!--各类输入框-->
      <div style = "margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
        姓名：
        <el-input v-model="modBaseCashierInfo.name" style="width: 12.5vw; margin-left: 2rem" clearable/>
      </div>
      <div style = "margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
        身份证：
        <el-input v-model="modBaseCashierInfo.identity_card" style="width: 12.5vw; margin-left: 1rem" clearable/>
      </div>
      <div style = "margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
        账户名：
        <el-input v-model="modBaseCashierInfo.account" style="width: 12.5vw; margin-left: 1rem" clearable/>
      </div>
      <div style = "margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
        密码：
        <el-input type="password" v-model="modBaseCashierInfo.password" style="width: 12.5vw; margin-left: 2rem" clearable/>
      </div>
      <div style = "margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
        电话：
        <el-input v-model="modBaseCashierInfo.phone" style="width: 12.5vw; margin-left: 2rem" clearable/>
      </div>
      <div style = "margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
        性别：
        <el-select v-model="modBaseCashierInfo.sex" size="default" style="width: 5vw; margin-left: 2rem">
          <el-option v-for="type in sexTypes" :key="type.value" :label="type.label" :value="type.value" />
        </el-select>
      </div>

      <!--底部按钮-->
      <template #footer>
              <span>
                  <el-button @click="modBaseCashierVisible = false">取消</el-button>
                  <el-button type="primary" @click="ConfirmModBaseCashier"
                             :disabled="modBaseCashierInfo.name.length === 0 || modBaseCashierInfo.account.length === 0
                             || modBaseCashierInfo.identity_card.length === 0 || modBaseCashierInfo.password.length === 0
                             || modBaseCashierInfo.phone === 0">确定</el-button>
              </span>
      </template>
    </el-dialog>
    <!-- 修改出纳员权限对话框 -->
    <el-dialog v-model = "modAuthorityCashierVisible" title = "修改出纳员权限" width = "30%" align-center>
      <div style = "margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
        权限：
        <el-checkbox v-model="modAuthorityCashierInfo.ifManage" label="账户管理" size="large" style="margin-left: 1.2rem"/>
        <el-checkbox v-model="modAuthorityCashierInfo.ifTrade" label="账户交易" size="large" />
      </div>
      <template #footer>
              <span>
                  <el-button @click="modAuthorityCashierVisible= false">取消</el-button>
                  <el-button type="primary" @click="ConfirmModAuthorityCashier">确定</el-button>
              </span>
      </template>
    </el-dialog>
    <!-- 删除出纳员确认框 -->
    <el-dialog v-model="deleteCashierVisible" title="删除出纳员" width="30%">
      <span>确定删除<span style="font-weight: bold;">{{ deleteCashierID }}号出纳员</span>吗？</span>

      <template #footer>
                <span class="dialog-footer">
                    <el-button @click="deleteCashierVisible = false">取消</el-button>
                    <el-button type="danger" @click="ConfirmDeleteCashier">
                        删除
                    </el-button>
                </span>
      </template>
    </el-dialog>
  </el-scrollbar>

</template>
<script>
import axios from "axios";
import { ElMessage } from 'element-plus'
export default{
  data(){
    return{
      sexTypes: [ // 性别类型·
        {
          value: '男',
          label: '男',
        },
        {
          value: '女',
          label: '女',
        }
      ],
      cashiers: [
        {
          id: 1,
          account: '炸毛的王昊元',
          password: '1231231',
          name: '王昊元',
          identity_card: '123213213',
          sex: '男',
          phone:'18962391106',
          ifTrade: true,
          ifManage: true
        },
        {
          id: 2,
          account: '飞翔的猪',
          password: '',
          name: '王元豪',
          identity_card: '',
          sex: '男',
          phone:'18962391107',
          ifTrade: true,
          ifManage: false
        },
      ],
      newCashierVisible: false,
      newCashierInfo: {
          id: 0,
          name: '',
          identity_card: '',
          account: '',
          password: '',
          sex: '男',
          phone:'',
          ifTrade: false,
          ifManage: false
      },
      modBaseCashierVisible: false,
      modBaseCashierInfo: {
          id: 0,
          name: '',
          identity_card: '',
          account: '',
          password: '',
          sex: '男',
          phone:'',
      },
      modAuthorityCashierVisible: false,
      modAuthorityCashierInfo: {
          id: 0,
          ifTrade: false,
          ifManage: false
      },
      deleteCashierVisible: false,
      deleteCashierID: 0,
    }
  },
  methods: {
    ConfirmNewCashier() {
      axios.post('/manager/add/',
        {
            name: this.newCashierInfo.name,
            identity_card: this.newCashierInfo.identity_card,
            account: this.newCashierInfo.account,
            password: this.newCashierInfo.password,
            sex: this.newCashierInfo.sex,
            phone: this.newCashierInfo.phone,
            manage_authority: this.newCashierInfo.ifManage,
            trade_authority: this.newCashierInfo.ifTrade,
      })
      .then(response => {
            ElMessage.success("出纳员添加成功")
            this.newCashierVisible = false
            this.QueryCashiers()
      })
    },
    ConfirmModBaseCashier() {
      axios.post('/manager/modify-base/',
          {
            id: this.modBaseCashierInfo.id,
            name: this.modBaseCashierInfo.name,
            identity_card: this.modBaseCashierInfo.identity_card,
            account: this.modBaseCashierInfo.account,
            password: this.modBaseCashierInfo.password,
            sex: this.modBaseCashierInfo.sex,
            phone:this.modBaseCashierInfo.phone,
        }).then(response => {
          ElMessage.success("出纳员信息修改成功")
          this.modBaseCashierVisible = false
          this.QueryCashiers()
      })
    },
    ConfirmModAuthorityCashier(){
      axios.post('manager/modify-authority/',
          {
            id: this.modAuthorityCashierInfo.id,
            ifManage: this.modAuthorityCashierInfo.ifManage,
            ifTrade: this.modAuthorityCashierInfo.ifTrade,
        }).then(response => {
        ElMessage.success("出纳员权限修改成功")
        this.modAuthorityCashierVisible = false
        this.QueryCashiers()
      })
    },
    ConfirmDeleteCashier(){
      axios.post('manager/delete/',
          {
            id: this.deleteCashierID,
          }).then(response => {
            ElMessage.success("出纳员删除成功")
            this.deleteCashierVisible = false
            this.QueryCashiers()
          }
      )
    },
    QueryCashiers() {
      this.cashiers = []
      axios.get('/manager/all-cashier/')
          .then(response => {
            let cashiers = response.data
            cashiers.forEach(cashier => {
              this.cashiers.push(cashier)
            })
          })
    },
  },
  mounted() { // 当页面被渲染时
    this.QueryCashiers()
  }
}
</script>

<style scoped>
.cashierBox {
  height:380px;
  width: 275px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  text-align: center;
  margin-top: 40px;
  margin-left: 27.5px;
  margin-right: 10px;
  padding: 7.5px;
  padding-right: 10px;
  padding-top: 15px;
}
.newCashierBox {
  height: 380px;
  width: 275px;
  margin-top: 40px;
  margin-left: 27.5px;
  margin-right: 10px;
  padding: 7.5px;
  padding-right: 10px;
  padding-top: 15px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  text-align: center;
}
</style>