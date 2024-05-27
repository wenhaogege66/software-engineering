<template>
  <div class="main">
    <el-container>
      <el-aside class="aside">
        <el-menu active-text-color="#ffd04b" background-color="#444444" default-active="1" text-color="#fff"
                 style="height:100%; width: 100%; overflow: hidden" :router="true">
          <div style="color: white; background-color: #181818;
          width: 100%; height: 10vh; display: flex; align-items: center; justify-content: center;">
            出纳员 #{{cashierID}}
          </div>
          <!-- 通过url参数形式传递给子组件 -->
          <el-menu-item :index="'/cashier/deposit?cashierID='+this.cashierID">
            <el-icon>
              <Avatar />
            </el-icon>
            <span>账户存款</span>
          </el-menu-item>
          <el-menu-item :index="'/cashier/withdrawal?cashierID='+this.cashierID">
            <el-icon>
              <Avatar />
            </el-icon>
            <span>账户取款</span>
          </el-menu-item>
          <el-menu-item :index="'/cashier/transfer?cashierID='+this.cashierID">
            <el-icon>
              <Avatar />
            </el-icon>
            <span>账户转账</span>
          </el-menu-item>
          <el-menu-item :index="'/cashier/query?cashierID='+this.cashierID">
            <el-icon>
              <Avatar />
            </el-icon>
            <span>查询记录</span>
          </el-menu-item>
          <el-sub-menu>
            <template #title>
              <el-icon><location /></el-icon>
              <span>账户管理</span>
            </template>
            <el-menu-item :index="'/cashier/accountManage?cashierID='+this.cashierID">
              <span>账户状态管理</span>
            </el-menu-item>
            <el-menu-item :index="'/cashier/accountOpen?cashierID='+this.cashierID">
              <span>账户开设</span>
            </el-menu-item>
          </el-sub-menu>
          <div style="height: 30px"></div>
          <a href="/manager" style="margin-left: 40px;">
            <el-button type="danger">
              退出
            </el-button>
          </a>
        </el-menu>

      </el-aside>
      <el-container>
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
export default {
  created() {
    this.fetchDataFromUrl();
  },
  data(){
    return{
      cashierID: 0
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
    }
  }
};
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
