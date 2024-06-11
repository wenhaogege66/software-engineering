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
      用户权限管理
    </div>
    <el-table :data="user_datas" style="width: 80%; margin-left: 10%">
      <el-table-column fixed prop="user_name" label="用户名" width="150" />
      <el-table-column prop="phone_num" label="手机号" width="200" />
      <el-table-column prop="id_card" label="身份证号" width="200" />
      <el-table-column prop="is_frozen" label="是否冻结" width="120" />
      <el-table-column prop="is_lost" label="是否挂失" width="120" />
      <el-table-column fixed="right" label="Operations" width="150">
        <template #default="scope">
          <el-button
            link
            type="primary"
            size="large"
            @click="
              (FrozenVisible = true),
                ((Frozen_Id = scope.row.user_id),
                (UnFrozen_Id = scope.row.user_id))
            "
            >Frozen</el-button
          >
          <el-button
            link
            type="danger"
            size="large"
            @click="
              (LostVisible = true),
                ((Lost_id_Id = scope.row.user_id),
                (UnLost_id = scope.row.user_id))
            "
            >Lost</el-button
          >
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      v-model="FrozenVisible"
      title="用户冻结"
      width="30%"
      align-center
      :before-close="handleClose"
    >
      <template #footer>
        <span>
          <el-button type="primary" @click="Frozen()">确认冻结该用户</el-button>
        </span>
        <span>
          <el-button type="danger" @click="UnFrozen()" style="margin-left: 15px"
            >解冻该用户</el-button
          >
        </span>
      </template>
    </el-dialog>

    <el-dialog
      v-model="LostVisible"
      title="用户挂失"
      width="30%"
      align-center
      :before-close="handleClose"
    >
      <template #footer>
        <span>
          <el-button type="primary" @click="Lost()">确认挂失用户</el-button>
        </span>
        <span>
          <el-button type="danger" @click="UnLost()" style="margin-left: 15px"
            >解除该用户挂失</el-button
          >
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
      Lost_id: 0,
      Frozen_Id: 0,
      Delete_Id: 0,
      UnLost_id: 0,
      UnFrozen_Id: 0,
      UnDelete_Id: 0,
      user_datas: [],
      LostVisible: false,
      FrozenVisible: false,
      DeleteVisible: false,
    };
  },
  methods: {
    async QueryUserData() {
      let response = await axios.get("/manager/user_data_query/"); // 向/book发出GET请求s
      this.user_datas = []; // 清空列表
      let users = response.data; // 接收响应负载
      users.forEach((user) => {
        if (user.is_frozen) user.is_frozen = "是";
        else user.is_frozen = "否";
        if (user.is_lost) user.is_lost = "是";
        else user.is_lost = "否";
        this.user_datas.push(user);
      });
      // console.log("获取人员信息成功：", blacks);
    },
    async Frozen() {
      this.FrozenVisible = false;
      axios
        .post("/manager/user_frozen/", {
          user_id: this.Frozen_Id,
        })
        .then((response) => {
          console.log(response);
          ElMessage.success("冻结成功"); // 显示消息提醒
          this.QueryUserData();
        })
        .catch((error) => {
          // console.log("有错误");
          ElMessage.error(error.response.data.error);
        });
    },
    async UnFrozen() {
      this.FrozenVisible = false;
      axios
        .post("/manager/user_unfrozen/", {
          user_id: this.UnFrozen_Id,
        })
        .then((response) => {
          console.log(response);
          ElMessage.success("解冻成功"); // 显示消息提醒
          this.QueryUserData();
        })
        .catch((error) => {
          // console.log("有错误");
          ElMessage.error(error.response.data.error);
        });
    },
    async Lost() {
      this.LostVisible = false;
      axios
        .post("/manager/user_lost/", {
          user_id: this.Lost_id,
        })
        .then((response) => {
          console.log(response);
          ElMessage.success("挂失成功"); // 显示消息提醒
          this.QueryUserData();
        })
        .catch((error) => {
          // console.log("有错误");
          ElMessage.error(error.response.data.error);
          this.password = "";
        });
    },
    async UnLost() {
      this.LostVisible = false;
      // console.log("看看这里喔：", this.UnLost_id);
      axios
        .post("/manager/user_unlost/", {
          user_id: this.UnLost_id,
        })
        .then((response) => {
          console.log(response);
          ElMessage.success("解除挂失成功"); // 显示消息提醒
          this.QueryUserData();
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
    this.QueryUserData(); // 查询借书证
  },
};
</script>
  
  <style scoped>
</style>