<template>
    <el-scrollbar height="100%" style="width: 100%; height: 100%">
      <div style="margin-top: 20px; margin-left:20px; font-size: 2em; font-weight: bold;">
        密码重置
      </div>
      <div style="width:45%;margin:0 auto; padding-top:5vh;">
      <div class="loginBox">
        <!-- 卡片标题 -->
          <div style="font-size: 25px; font-weight: bold;"></div>
  
  
  
          <!-- 卡片内容 -->
        <div style="height: 20px"></div>
          <div style="margin-left: 10px; text-align: start; font-size: 16px;">
            <div style = "margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
              密码修改
            </div>
            <div style="height: 25px"></div>
            <div style = "margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
              手机号：
              <el-input v-model="phone" style="width: 12.5vw; margin-left: 1rem" maxlength="18" clearable/>
            </div>
            <div style="height: 25px"></div>
            <div style = "margin-left: 4.3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
              身份证号：
              <el-input v-model="IDCard" style="width: 12.5vw; margin-left: 1rem" type="password" maxlength="20" clearable/>
            </div>
            <div style="height: 25px"></div>
            <div style = "margin-left: 4.3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
              用户名：
              <el-input v-model="account" style="width: 12.5vw; margin-left: 1rem" type="password" maxlength="20" clearable/>
            </div>
            <div style="height: 25px"></div>
            <div style = "margin-left: 4.3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
              新密码：
              <el-input v-model="new_password" style="width: 12.5vw; margin-left: 1rem" type="password" maxlength="20" clearable/>
            </div>
            <div style="height: 40px"></div>
          </div>
          <!-- 卡片操作 -->
          <div style="margin-top: 10px; display:flex; margin-left: 10rem;">
            <el-button type="primary"  @click="handle()" >
              修改
            </el-button>
          </div>
        </div>
      </div>
  
    </el-scrollbar>
  </template>
  <script>
  export default{
methods: {
    handle (){
      axios.post('http://127.0.0.1:8000/user/change_password/',{
        user_name: this.account,
        identify_card: this.IDcard,
        phone_num: this.phone,
        new_password: this.password,
      }).then(response => {
        window.location.href = "/login";  // 函数内部进行超链接跳转
      }).catch(error => {
        ElMessage.error(error.response.data.error);
        //this.password = "";
      })
    }
  }
}
  </script>
  
  <style scoped>
  .loginBox {
    height: 340px;
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