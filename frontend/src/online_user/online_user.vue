<template>
  <div class="main">
    <el-container>
      <el-aside class="aside">
        <el-menu
          active-text-color="#ffd04b"
          background-color="#444444"
          default-active="1"
          text-color="#fff"
          style="height: 100%; width: 100%; overflow: hidden"
          :router="true"
        >
          <div
            style="
              color: white;
              background-color: #181818;
              width: 100%;
              height: 10vh;
              display: flex;
              align-items: center;
              justify-content: center;
            "
          >
            互联网个人银行
          </div>

            <el-menu-item v-model:index="index.home">
              <el-icon>
                <Avatar />
              </el-icon>
              <span>首页</span>
            </el-menu-item>
            <el-menu-item v-model:index="index.personal">
              <el-icon>
                <User />
              </el-icon>
              <span>密码修改</span>
            </el-menu-item>
            <el-menu-item v-model:index="index.account">
              <el-icon>
                <User />
              </el-icon>
              <span>用户信息</span>
            </el-menu-item>
            <el-menu-item v-model:index="index.record">
              <el-icon>
                <User />
              </el-icon>
              <span>交易记录</span>
            </el-menu-item>
            <el-menu-item @click="Exit">
              <el-icon>
                <SwitchButton />
              </el-icon>
              <span>退出</span>
            </el-menu-item>
            <div style="height: 30px"></div>
  <!--          <a href="/" style="margin-left: 40px;">-->
  <!--            <el-button type="danger">-->
  <!--              退出-->
  <!--            </el-button>-->
  <!--          </a>-->
          </el-menu>
  
        </el-aside>
        <el-container>
          <el-header style="height: 0vh;"></el-header>
          <el-main style="height: 100%; width: 100%; ">
            <el-scrollbar height="100%">
              <RouterView class="content" style="height: 100vh; max-height: 100%; background-color: white; color: black;" />
            </el-scrollbar>
          </el-main>
        </el-container>
      </el-container>
    </div>
  </template>

  <script>
  import {SwitchButton} from "@element-plus/icons-vue";

  export default {
    components: {SwitchButton},

    data() {
      return {
        index:{
          home: "/online_user/home",
          personal: "/online_user/personal",
          account: "/online_user/account",
          record: "/online_user/record",
        },
        user_id:0
      }
    },
    methods: {
      Exit() {
        window.location.href = "/login";
      }
    },
    mounted() { // 当页面被渲染时
      // 获取 URL 中的查询字符串
      console.log(this.$route)
      let search = window.location.search;
      if(search!==undefined)
      {
        let urlParams = new URLSearchParams(search);
        let obj = JSON.parse(urlParams.get('user_id'));
        this.user_id = obj;
        console.log(this.user_id);
      }
      this.index={
        home: "/online_user/home" + "?user_id=" + JSON.stringify(this.user_id),
        personal: "/online_user/personal" + "?user_id=" + JSON.stringify(this.user_id),
        account: "/online_user/account" + "?user_id=" + JSON.stringify(this.user_id),
        record: "/online_user/record" + "?user_id=" + JSON.stringify(this.user_id),
      }
    }
  }
  </script>

  <style scoped>
#app {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background-color: #dcdcdc;
  width: 100vw;
  height: 100vh;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  width: 100%;
  min-height: 100%;
  height: auto;
  background-color: #dcdcdc;
}

.title {
  background-color: #ffffff;
  height: 60px;
}

.aside {
  min-height: 100vh;
  width: 200px;
  background-color: black;
}
</style>
  