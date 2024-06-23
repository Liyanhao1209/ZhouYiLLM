<template>
  <div class="top-div">
    <el-button @click="logout()" type="info">登出</el-button>
  </div>
  <div class="user-list">
    <!-- 查询当前注册的用户 -->
    <div class="user-list-container">
      <h2>当前注册的用户</h2>
      <ul>
        <li v-for="user in users" :key="user.id" class="user-item">
          <div class="user-info">
            <span><strong>名字：</strong>{{ user.name }}</span>
            <span><strong>邮箱：</strong>{{ user.email }}</span>
            <span><strong>性别：</strong>{{ user.sex }}</span>
            <span><strong>年龄：</strong>{{ user.age }}</span>
            <span><strong>帐号状态：</strong>{{ user.is_active ? '正常' : '封禁' }}</span>
          </div>
          <div class="user-button">
            <el-button type="success" @click="to_user_conv_history(user)">查看对话历史记录</el-button>
            <button @click="user.is_active ? methodOne(user) : methodTwo(user)"
              :class="user.is_active ? 'normal-button' : 'error-button'">
              {{ user.is_active ? '封禁' : '解封' }}
            </button>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { getuser, block_user, relive_user } from '@/service/administor.js'
import { ElMessage } from 'element-plus';
export default {
  data() {
    return {
      users: []
    }
  },
  methods: {
    logout() {
      this.$router.back();
      localStorage.removeItem('token')
    },
    getUsers() {
      getuser().then(res => {
        if (res.data.code === 200) {
          this.users = res.data.data.user_list;
          ElMessage({
            message: '查询成功',
            type: 'success'
          })
        }
      })
    },
    methodOne(user) {
      //console.log('Method One for user:', user);
      let form = {
        id: "",
        username: user.name,
        user_id: user.id
      }
      block_user(form).then(res => {
        if (res.data.code === 200) {
          user.is_active = false;
          ElMessage({
            message: '封禁成功',
            type: 'success'
          })
        }
      })
    },
    methodTwo(user) {
      let form = {
        id: "",
        username: user.name,
        user_id: user.id
      }
      relive_user(form).then(res => {
        if (res.data.code === 200) {
          user.is_active = true;
          ElMessage({
            message: '解封成功',
            type: 'success'
          })
        }
      })
    },
    to_user_conv_history(user){
      let user_id = user.id
      this.$router.push({
        path: '/admin_history_chat',
        query: {
          user_id: user_id
        }
      })
    }
  },


  created() {
    console.log('admin create');
    this.getUsers();
  }
}
</script>

<style scoped>
.user-list {
  font-family: Arial, sans-serif;
}

.user-list-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: #333;
}

ul {
  list-style-type: none;
  padding: 0;
}

.user-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-info span {
  margin-bottom: 5px;
}

.normal-button {
  background-color: red;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.normal-button:hover {
  background-color: darkred;
}

.error-button {
  background-color: green;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.error-button:hover {
  background-color: darkgreen;
}

.top-div {
  text-align: start;
  width: 100%;
  margin-left: 30px;
  margin-top: 30px;
}

.user-button{
  display: flex;
  align-items: center;
  justify-content:space-around;
  width: 250px;
}
</style>
