<template>
    <el-scrollbar height="100%" style="width: 100%; height: 100%">
      <div style="margin-top: 20px; margin-left:20px; font-size: 2em; font-weight: bold;">
        黑名单管理
      </div>
      <div style="width:45%;margin:0 auto; padding-top:5vh;">
            <el-button type="primary" @click="DepositVisible = true">添加黑名单</el-button>
      </div>
      <el-table :data="tableData" style="width: 70% ;margin-left:15%">
        <el-table-column fixed prop="date" label="用户名" width="300" />
        <el-table-column prop="name" label="手机号" width="300" />
        <el-table-column prop="state" label="身份证号" width="300" />
        <el-table-column fixed="right" label="Operations" width="150">
      <template #default>
        <el-button link type="primary" size="small" @click="handleClick">
          移除
        </el-button>
      </template>
    </el-table-column>
  </el-table>


      <el-dialog v-model="DepositVisible" title="添加黑名单" width="30%" align-center :before-close="handleClose">
          <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
              用户名：
              <!-- <el-input v-model="newDepositInfo.account_id" style="width: 12.5vw;" clearable /> -->
          </div>

          <template #footer>
              <span>
                  <el-button @click="DepositVisible = false">确认</el-button>
              </span>
          </template>
      </el-dialog>
  
    </el-scrollbar>
  </template>
  <script lang="ts" setup>
import { ref } from 'vue'

const DepositVisible = ref(false)

const handleClick = () => {
  console.log('click')
}

  </script>
  
  <style scoped>

  </style>