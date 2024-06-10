<template>
  <el-scrollbar height="100%" style="width: 100%;">

  <!-- 标题和搜索框 -->
  <div style="margin-top: 20px; margin-left: 40px; font-size: 2em; font-weight: bold;">
      账户余额查询
  </div>

  <!-- 存款操作 -->
  <div style="width:70%;margin-left:30px; padding-top:5vh;">
      <!-- <el-input v-model="this.toQuery" style="display:inline; " placeholder="输入借书证ID"></el-input> -->
      <el-button style="margin-left: 10px;" type="primary" @click="DemandDepositVisible = true">活期存款</el-button>
      <el-button style="margin-left: 10px;" type="primary" @click="TimeDepositVisible = true">定期存款</el-button>
      <el-button style="margin-left: 10px;" type="primary" @click="TotalDepositVisible = true">累计存款</el-button>
  </div>

  <!-- 存款记录 -->
  <!-- <div class="cashierBox" v-for="record in records" :key="record.deposit_record_id"> -->
  <!-- </div> -->

      <el-dialog v-model="DemandDepositVisible" title="活期存款" width="30%" align-center :before-close="handleClose">
          <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
              账户ID：
              <!-- <el-input v-model="newDepositInfo.account_id" style="width: 12.5vw;" clearable /> -->
          </div>
          <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
              密码：
              <!-- <el-input v-model="newDepositInfo.password" style="width: 12.5vw;" show-password/> -->
          </div>
          <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
              存款金额：
              <!-- <el-input-number v-model="newDepositInfo.deposit_amount" style="width: 12.5vw;" :precision="2" :step="0.1" clearable :min="0"/> -->
          </div>

          <template #footer>
              <span>
                  <el-button @click="DemandDepositVisible = false">取消</el-button>
              </span>
          </template>
      </el-dialog>

      <el-dialog v-model="TimeDepositVisible" title="定期存款" width="30%" align-center>
          <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
              账户ID：
              <!-- <el-input v-model="newTimeDepositInfo.account_id" style="width: 12.5vw;" clearable /> -->
          </div>
          <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
              密码：
              <!-- <el-input v-model="newTimeDepositInfo.password" style="width: 12.5vw;" show-password/> -->
          </div>
          <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
              存款金额：
              <!-- <el-input-number v-model="newTimeDepositInfo.deposit_amount" style="width: 12.5vw;" :precision="2" :step="0.1" clearable :min="0"/> -->
          </div>
          <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
              存款期限：
              <!-- <el-input v-model="newTimeDepositInfo.deposit_term" style="width: 12.5vw;" clearable /> -->
          </div>
          <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
              是否自动续期：
              <!-- <el-radio-group  style="margin-left: 10px;" v-model="newTimeDepositInfo.is_auto_renew">
                  <el-radio v-model="newTimeDepositInfo.is_auto_renew" value="1">是</el-radio>
                  <el-radio v-model="newTimeDepositInfo.is_auto_renew" value="2">否</el-radio>
              </el-radio-group> -->
          </div>

          <template #footer>
              <span>
                  <el-button @click="TimeDepositVisible = false">取消</el-button>
              </span>
          </template>
      </el-dialog>

      <el-dialog v-model="TotalDepositVisible" title="累计存款" width="30%" align-center>
          <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
              账户ID：
              <!-- <el-input v-model="totalDepositInfo.account_id" style="width: 12.5vw;" clearable /> -->
          </div>
          <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
              密码：
              <!-- <el-input v-model="totalDepositInfo.password" style="width: 12.5vw;" show-password/> -->
          </div>
          <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
              累计存款：
              <!-- <el-input v-model="this.total_amount" style="width: 12.5vw;" disabled /> -->
          </div>

          <template #footer>
              <span>
                  <el-button @click="TotalDepositVisible = false">取消</el-button>
              </span>
          </template>
      </el-dialog>


  </el-scrollbar>


</template>

<script lang="ts" setup>
import axios from 'axios';
import { Delete, Edit, Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { ref } from 'vue'

const DemandDepositVisible = ref(false)
const TimeDepositVisible = ref(false)
const TotalDepositVisible = ref(false)

</script>

<style scoped>

</style>