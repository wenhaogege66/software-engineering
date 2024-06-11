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
      黑名单管理
    </div>
    <div style="width: 45%; margin-left: 10%; padding-top: 5vh">
      <el-button type="primary" @click="() => (DepositVisible = true)"
        >添加黑名单</el-button
      >
    </div>
    <el-table :data="blacks" style="width: 80%; margin-left: 10%">
      <el-table-column fixed prop="user_name" label="用户名" width="250" />
      <el-table-column prop="phone_num" label="手机号" width="250" />
      <el-table-column prop="id_card" label="身份证号" width="250" />
      <el-table-column fixed="right" label="Operations" width="250">
        <template #default="scope">
          <el-button
            link
            type="danger"
            size="large"
            @click="(DeletVisible = true), (delet_user_id = scope.row.user_id)"
            >Remove</el-button
          >
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      v-model="DepositVisible"
      title="添加黑名单"
      width="30%"
      align-center
      :before-close="handleClose"
    >
      <div
        style="
          margin-left: 2vw;
          font-weight: bold;
          font-size: 1rem;
          margin-top: 20px;
        "
      >
        用户名：
        <el-input
          v-model="newBlack_user_name"
          style="width: 12.5vw"
          clearable
        />
      </div>
      <div
        style="
          margin-left: 2vw;
          font-weight: bold;
          font-size: 1rem;
          margin-top: 20px;
        "
      >
        管理员账号：
        <el-input
          v-model="newBlack_manager_name"
          style="width: 12.5vw"
          clearable
        />
      </div>

      <template #footer>
        <span>
          <el-button @click="AddBlack()">确认</el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog
      v-model="DeletVisible"
      title="移除黑名单"
      width="30%"
      align-center
      :before-close="handleClose"
    >
      <template #footer>
        <span>
          <el-button type="danger" @click="DeletBlack()">确认移除</el-button>
        </span>
      </template>
    </el-dialog>
  </el-scrollbar>
</template>

<script>
import { ref } from "vue";
import axios from "axios";
import { ElMessage } from "element-plus";

export default {
  data() {
    return {
      newBlack_user_name: "",
      newBlack_manager_name: "",
      BlackInfo: {},
      blacks: [],
      DepositVisible: false,
      DeletVisible: false,
      delet_user_id: 0,
    };
  },
  methods: {
    async QueryBlack() {
      let response = await axios.get("/manager/blacklist_query/"); // 向/book发出GET请求s
      this.blacks = []; // 清空列表
      let blacks = response.data; // 接收响应负载
      blacks.forEach((black) => {
        this.blacks.push(black);
      });
      console.log("获取黑名单成功：", blacks);
    },
    async AddBlack() {
      this.DepositVisible = false;
      axios
        .post("/manager/blacklist_add/", {
          manager_name: this.newBlack_manager_name,
          user_name: this.newBlack_user_name,
        })
        .then((response) => {
          console.log(response);
          ElMessage.success("新增黑名单成功"); // 显示消息提醒
          this.QueryBlack();
        })
        .catch((error) => {
          console.log("有错误");
          ElMessage.error(error.response.data.error);
          this.password = "";
        });
    },
    async DeletBlack() {
      this.DeletVisible = false;
      console.log("删除", this.delet_user_id);
      axios
        .post("/manager/blacklist_delet/", {
          user_id: this.delet_user_id,
        })
        .then((response) => {
          console.log(response);
          ElMessage.success("删除成功"); // 显示消息提醒
          this.QueryBlack();
        })
        .catch((error) => {
          // console.log("有错误");
          ElMessage.error(error.response.data.error);
          this.password = "";
        });
    },
  },
  mounted() {
    // console.log("首次开始获取数据");
    this.QueryBlack(); // 查询借书证
  },
};
</script>
  

<style scoped>
</style>