<template>
  <el-scrollbar height="100%" style="width: 100%;">

  <!-- 标题和搜索框 -->
  <div style="margin-top: 20px; margin-left: 40px; font-size: 2em; font-weight: bold;">
      个人用户信息
  </div>
  <div class = "infoBox" >
    <p style="font-weight: bold;font-size: larger;margin: 10px" >用户ID : {{user_info.user_id}}</p>
    <p style="font-weight: bold;font-size: larger;margin: 10px" >用户名 : {{user_info.user_name}}</p>
    <p style="font-weight: bold;font-size: larger;margin: 10px" >电话号码 : {{user_info.phone_num}}</p>
  </div>
  <!-- 存款操作 -->

  <!-- 存款记录 -->
  <!-- <div class="cashierBox" v-for="record in records" :key="record.deposit_record_id"> -->
  <!-- </div> -->


    <div style="display: flex;flex-wrap: wrap; justify-content: start;">
    <!-- 借书证卡片 -->
    <div class="cardBox" v-for="card in cards"  :key="card.account_id">
      <div>
        <!-- 卡片标题 -->
        <div style="font-size: 25px; font-weight: bold;">卡号/账户ID： {{ card.account_id }}</div>

        <el-divider />

        <!-- 卡片内容 -->
        <div style="margin-left: 10px; text-align: start; font-size: 16px;">
          <p style="padding: 2.5px;"><span style="font-weight: bold;font-size: larger">账户余额：{{ card.balance }} </span></p>
          <p style="padding: 2.5px;"><span style="font-weight: bold;">卡片类型：</span>{{ card.card_type }}</p>
          <p style="padding: 2.5px;"><span style="font-weight: bold;">是否冻结：</span>{{ card.is_frozen }}</p>
          <p style="padding: 2.5px;"><span style="font-weight: bold;">是否挂失：</span>{{ card.is_lost }}</p>
        </div>

        <el-divider />
        <!-- 卡片操作 -->
        <div style="margin-top: 10px;">
        <!--   挂失操作     -->
          <el-button type="info" :icon="DocumentDelete" circle :disabled="card.is_lost==='已挂失'"
                     @click="this.toReportLost.account_id = card.account_id, this.toReportLost.to_lost = true, this.reportLostVisible = true"
                     style="margin-left: 30px;" />
          <el-button type="primary" :icon="DocumentChecked" circle :disabled="card.is_lost==='未挂失'"
                     @click="this.toReportLost.account_id = card.account_id, this.toReportLost.to_lost = false, this.reportLostVisible = true"
                     style="margin-left: 30px;" />
        </div>


      </div>
    </div>

      <el-button class="newCardBox"
                 @click="newCardInfo.account_id = '', newCardInfo.identity_card = '', newCardInfo.password = '', newCardInfo.phone_num = '',newCardVisible = true">
        <el-icon style="height: 50px; width: 50px;">
          <Plus style="height: 100%; width: 100%;" />
        </el-icon>
      </el-button>

      <!-- 新建借书证对话框 -->
      <el-dialog v-model="newCardVisible" title="绑定新账户" width="30%" align-center>
        <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          卡号：
          <el-input v-model="newCardInfo.account_id" style="width: 12.5vw;" clearable />
        </div>
        <div style="margin-left: 2vw;   font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          账户（卡片）密码：
          <el-input v-model="newCardInfo.password" style="width: 12.5vw;" clearable />
        </div>
        <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          对应身份证号：
          <el-input v-model="newCardInfo.identity_card" style="width: 12.5vw;" clearable />
        </div>
        <div style="margin-left: 2vw;   font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          对应手机号：
          <el-input v-model="newCardInfo.phone_num" style="width: 12.5vw;" clearable />
        </div>

        <template #footer>
                <span>
                    <el-button @click="newCardVisible = false">取消</el-button>
                    <el-button type="primary" @click="ConfirmNewCard"
                               :disabled="newCardInfo.identity_card.length === 0 || newCardInfo.phone_num.length === 0 || newCardInfo.account_id.length === 0 || newCardInfo.password.length === 0">确定</el-button>
                </span>
        </template>
      </el-dialog>


      <!-- 挂失账户对话框 -->
      <el-dialog v-model="reportLostVisible" title="挂失账户" width="30%">
        <span>确定<span v-show="!toReportLost.to_lost">取消</span>挂失<span style="font-weight: bold;">卡号为{{ toReportLost.account_id }}的账户</span>吗？</span>

        <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          挂失账户密码：
          <el-input v-model="toReportLost.password" style="width: 12.5vw;" clearable />
        </div>
        <template #footer>
                <span class="dialog-footer">
                    <el-button @click="reportLostVisible = false">取消</el-button>
                    <el-button type="danger" @click="ReportLostCard">
                        确认
                    </el-button>
                </span>
        </template>
      </el-dialog>


    </div>

  </el-scrollbar>


</template>

<script>
import axios from 'axios';
import {Delete, DocumentChecked, DocumentDelete, Edit, Plus, Search} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { ref } from 'vue'

const DemandDepositVisible = ref(false)
const TimeDepositVisible = ref(false)
const TotalDepositVisible = ref(false)

export default{
  components: {Plus},
  computed: {
    DocumentChecked() {
      return DocumentChecked
    },
    DocumentDelete() {
      return DocumentDelete
    },
    Delete() {
      return Delete
    },
    Edit() {
      return Edit
    }
  },
  data(){
    return{
      toReportLost:{
        account_id:100,
        password:"",
        to_lost:true
      },
      reportLostVisible:false,
      user_info:{
        user_id:1,
        user_name:"wenhao",
        phone_num:"124141412413"
      },
      user_id:null,
      newCardVisible:false,
      newCardInfo:{
        account_id:1,
        phone_num:"12312314",
        identity_card:"333330001",
        password:"12313",
      },
      cards:[
        {
          account_id: 1,
          balance: 100.00,
          card_type:"可贷款",
          is_frozen:"未冻结",
          is_lost:"未挂失"
        },
        {
          account_id: 2,
          balance: 102.00,
          card_type: "不可贷款",
          is_frozen: "未冻结",
          is_lost: "未挂失"
        }
      ]
    }
  },
  methods: {
    ConfirmNewCard(){
      // 发出POST请求
      axios.post("http://127.0.0.1:8000/user/bind_card",
          { // 请求体
            account_id: this.newCardInfo.account_id,
            identity_card: this.newCardInfo.identity_card,
            phone_num: this.newCardInfo.phone_num,
            user_id: this.user_id,
            password: this.newCardInfo.password
          })
          .then(response => {
            ElMessage.success("绑定成功") // 显示消息提醒
            this.newCardVisible = false // 将对话框设置为不可见
            this.QueryCards() // 重新查询借书证以刷新页面
          }).catch(error=>{
            ElMessage.error(error.response.data.error);
      })
    },
    ReportLostCard(){
      axios.post("http://127.0.0.1:8000/user/card_lost/",
          { // 请求体
            account_id: this.toReportLost.account_id,
            password: this.toReportLost.password,
            to_lost: this.toReportLost.to_lost
          })
          .then(response => {
            ElMessage.success("操作成功") // 显示消息提醒
            this.newCardVisible = false // 将对话框设置为不可见
            this.QueryCards() // 重新查询借书证以刷新页面
          }).catch(error=>{
        ElMessage.error(error.response.data.error);
      })
    },
    QueryCards(){
      this.cards = [];
      let response = axios.get('http://127.0.0.1:8000/user/list_cards',
          { params:{ user_id: this.user_id } } )
          .then(response=> {
            let cards = response.data
            cards.forEach(card => {
              this.cards.push({
                account_id: card.account_id,
                balance: card.balance,
                card_type: card.card_type?"可贷款":"不可贷款",
                is_frozen: card.is_frozen?"冻结":"未冻结",
                is_lost: card.is_lost?"已挂失":"未挂失"
              })
            })
      })
    },
    GetInfo(){
      let response = axios.get('http://127.0.0.1:8000/user/user_info',
          {params:{user_id: this.user_id}})
          .then(response=> {
            this.user_info.user_name = response.data.user_name;
            this.user_info.phone_num = response.data.phone_num;
          }).catch(error=>{
            ElMessage.error(error.response.data.error);
          })
    }
  },
  mounted() {
    this.user_id = 1;//this.$route.query.user_id;
    this.QueryCards();
    this.GetInfo();
  }
}


</script>

<style scoped>

.infoBox {
  height: 150px;
  width:100%;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  text-align: left;
  margin-top: 40px;
  margin-left: 27.5px;
  margin-right: 10px;
  padding: 7.5px;
  padding-left: 30px;
  padding-right: 10px;
  padding-top: 15px;
}

.cardBox {
  height: 300px;
  width: 400px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  text-align: center;
  margin-top: 40px;
  margin-left: 27.5px;
  margin-right: 10px;
  padding: 7.5px;
  padding-right: 10px;
  padding-top: 15px;
}

.newCardBox {
  height: 300px;
  width: 400px;
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