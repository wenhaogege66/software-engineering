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
      <el-table-column prop="id_lost" label="是否挂失" width="120" />
      <el-table-column fixed="right" label="Operations" width="350">
        <template #default="scope">
          <el-button
            link
            type="primary"
            size="large"
            @click="(FrozenVisible = true), (Frozen_Id = scope.row.user_id)"
            >Frozen</el-button
          >
          <el-button
            link
            type="danger"
            size="large"
            @click="(LostVisible = true), (Lost_id = scope.row.user_id)"
            >Lost</el-button
          >
          <el-button
            link
            type="danger"
            size="large"
            @click="(DeleteVisible = true), (Delete_id = scope.row.user_id)"
            >Delete</el-button
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
          <el-button type="danger" @click="DeletBlack()"
            >确认冻结该用户</el-button
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
          <el-button type="danger" @click="DeletBlack()"
            >确认该用户已丢失</el-button
          >
        </span>
      </template>
    </el-dialog>

    <el-dialog
      v-model="DeleteVisible"
      title="用户注销"
      width="30%"
      align-center
      :before-close="handleClose"
    >
      <template #footer>
        <span>
          <el-button type="danger" @click="DeletBlack()"
            >确认注销该用户</el-button
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
        this.user_datas.push(user);
      });
      console.log("获取人员信息成功：", blacks);
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