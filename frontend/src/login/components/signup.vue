<template>
    <el-scrollbar height="100%" style="width: 100%; height: 100%">
      <div style="margin-top: 20px; margin-left:20px; font-size: 2em; font-weight: bold;">
        互联网个人用户
      </div>
      <div style="width:45%;margin:0 auto; padding-top:5vh;">
        <div class="loginBox">
          <!-- 卡片标题 -->

          <!-- 卡片内容 -->
          <div style="margin-left: 10px; height: 180px ;text-align: start; font-size: 16px;">
            <div style=" height: 40px;margin: auto;display: flex;align-items: center;justify-content: center">
              <div style ="font-size: 1.5rem;font-weight: bolder; margin-top: 20px;text-align: center">
                用 户 注 册
              </div>
            </div>
            <el-divider/>
            <el-form label-position="right" label-width="100px" style=" font-weight: bolder; font-size: 10px">
              <el-form-item label="用户名"  style = "margin-top: 5px;">
                <el-input v-model="account" style="width: 12.5vw; margin-left: 1rem" maxlength="18" clearable/>
              </el-form-item>
              <el-form-item label="密码" style = "margin-top: 5px;">
                <el-input v-model="password" style="width: 12.5vw; margin-left: 1rem" type="password" maxlength="20" clearable/>
              </el-form-item>
              <el-form-item label="电话号码"  style = "margin-top: 5px;">
                <el-input v-model="phone" style="width: 12.5vw; margin-left: 1rem" maxlength="18" clearable/>
              </el-form-item>
              <el-form-item label="身份证号" style = "margin-top: 5px;">
                <el-input v-model="IDCard" style="width: 12.5vw; margin-left: 1rem" type="password" maxlength="20" clearable/>
              </el-form-item>

              <!-- 卡片操作 -->
              <div style="margin-top: 30px; display:flex;justify-content: center">
                <el-button type="primary"  @click="handle()">
                  注册
                </el-button>
                <el-button :icon="Edit" @click = "login">
                  返回
                </el-button>
              </div>
            </el-form>
          </div>
        </div>
      </div>
  
    </el-scrollbar>
  </template>
  <script>
  import axios from "axios";
  import { ElMessage } from 'element-plus'
  export default{
    data(){
      return{
        account: "",  // 用户登录，还不知道用什么
        password: "",
        IDCard:"",
        phone:"",
      }
    },
    methods: {
      login(){
        window.location.href = "/login/user";
      },
      handle (){
      axios.post('http://127.0.0.1:8000/user/sign_up/',{
        user_name: this.account,
        password: this.password,
        identity_card: this.IDCard,
        phone_num: this.phone
      }).then(response => {

        window.location.href = "/login";  // 函数内部进行超链接跳转
      }).catch(error => {
        ElMessage.error(error.response.data.error);
        //this.password = "";
      })
    }
    },
    mounted() { // 当页面被渲染时
    }
  }
  </script>
  
  <style scoped>
  .loginBox {
    height: 400px;
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