<template>
  <el-scrollbar height="100%" style="width: 100%; height: 100%">
    <div
      style="
        margin-top: 20px;
        margin-left: 20px;
        font-size: 2em;
        font-weight: bold;
      "
    >
      银行职员登录
    </div>
    <div style="width: 45%; margin: 0 auto; padding-top: 5vh">
      <div class="loginBox">
        <!-- 卡片标题 -->
        <div style="font-size: 25px; font-weight: bold"></div>

        <!-- 卡片内容 -->
        <div style="height: 20px"></div>
        <div style="margin-left: 10px; text-align: start; font-size: 16px">
          <div
            style="
              margin-left: 3vw;
              font-weight: bold;
              font-size: 1rem;
              margin-top: 5px;
            "
          >
            职员类型：
            <el-select
              v-model="employee.type"
              size="default"
              style="width: 11vw; margin-left: 0rem"
            >
              <el-option
                v-for="type in Types"
                :key="type.value"
                :label="type.label"
                :value="type.value"
              />
            </el-select>
          </div>
          <div style="height: 25px"></div>
          <div
            style="
              margin-left: 3vw;
              font-weight: bold;
              font-size: 1rem;
              margin-top: 5px;
            "
          >
            账户名：
            <el-input
              v-model="account"
              style="width: 12.5vw; margin-left: 1rem"
              maxlength="18"
              clearable
            />
          </div>
          <div style="height: 25px"></div>
          <div
            style="
              margin-left: 4.3vw;
              font-weight: bold;
              font-size: 1rem;
              margin-top: 5px;
            "
          >
            密码：
            <el-input
              v-model="password"
              style="width: 12.5vw; margin-left: 1rem"
              type="password"
              maxlength="20"
              clearable
            />
          </div>
          <div style="height: 40px"></div>
        </div>
        <!-- 卡片操作 -->
        <div style="margin-top: 10px; display: flex; margin-left: 10rem">
          <el-button
            type="primary"
            @click="employeeLogin"
            :disabled="
              account.length === 0 ||
              password.length === 0 ||
              employee.type.length === 0
            "
          >
            登录
          </el-button>
        </div>
      </div>
    </div>
  </el-scrollbar>
</template>
<script>
import axios from "axios";
import { ElMessage } from "element-plus";
export default {
  data() {
    return {
      account: "",
      password: "",
      Types: [
        {
          value: "系统管理员",
          label: "系统管理员",
        },
        {
          value: "出纳员",
          label: "出纳员",
        },
        {
          value: "贷款审核员",
          label: "贷款审核员",
        },
        {
          value: "贷款部门经理",
          label: "贷款部门经理",
        },
        {
          value: "外汇操作员",
          label: "外汇操作员",
        },
        {
          value: "外汇管理员",
          label: "外汇管理员",
        },
        {
          value: "信用卡审查员",
          label: "信用卡审查员",
        },
        {
          value: "互联网用户管理员",
          label: "互联网用户管理员",
        },
      ],
      employee: {
        id: "", // 对应职员id，如：出纳员返回出纳员id，系统管理员返回管理员id
        type: "系统管理员", // 银行职员类型
      },
    };
  },
  methods: {
    employeeLogin() {
      switch (this.employee.type) {
        case "系统管理员":
          // console.log(666);
          this.getSysManagerID();
          break;
        case "出纳员":
          // console.log(555);

          this.getCashierID();
          break;
        /*
          case "...":
            ...
          break;
          *
          */
        case "互联网用户管理员":
          this.getOnlineUserAdministratorID();
          break;
        default:
          // console.log(33);

          break;
      }
    },
    getOnlineUserAdministratorID() {
      // console.log(666);
      axios
        .post("/manager/sign_in/", {
          account: this.account,
          password: this.password,
        })
        .then((response) => {
          console.log(444);

          console.log(response.data.id);
          this.employee.id = response.data.id;
          // console.log(this.employee.id);
          window.location.href =
            "/online_manager?managerID=" + this.employee.id; // 函数内部进行超链接跳转/
        })
        .catch((error) => {
          console.log("有错误");
          ElMessage.error(error.response.data.error);
          this.password = "";
        });
    },
    getSysManagerID() {
      axios
        .post("/login/sysManager/", {
          account: this.account,
          password: this.password,
        })
        .then((response) => {
          this.employee.id = response.data.id;
          window.location.href = "/manager?managerID=" + this.employee.id; // 函数内部进行超链接跳转
        })
        .catch((error) => {
          ElMessage.error(error.response.data.error);
          this.password = "";
        });
    },
    getCashierID() {
      axios
        .post("/login/cashier/", {
          account: this.account,
          password: this.password,
        })
        .then((response) => {
          this.employee.id = response.data.id;
          window.location.href = "/cashier?cashierID=" + this.employee.id; // 函数内部进行超链接跳转
        })
        .catch((error) => {
          ElMessage.error(error.response.data.error);
          this.password = "";
        });
    },
  },
  mounted() {
    // 当页面被渲染时
  },
};
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