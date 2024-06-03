<template>
    <div class="user-profile">
        <div class="form-container">
            <h1>更新用户信息</h1>
            <form @submit.prevent="updateUser">
                <div class="form-group">
                    <label for="name">姓名:</label>
                    <input type="text" id="name" v-model="user.name" required>
                </div>
                <div class="form-group">
                    <label for="age">年龄:</label>
                    <input type="number" id="age" v-model="user.age" required>
                </div>
                <div class="form-group">
                    <label for="sex">性别:</label>
                    <select id="sex" v-model="user.sex" required>
                        <option value="male">男</option>
                        <option value="female">女</option>
                        <option value="other">其他</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="description">个人介绍:</label>
                    <textarea id="description" v-model="user.description" required></textarea>
                </div>
                <button type="submit">更新</button>
            </form>
        </div>
    </div>
</template>

<script>
import { update_info } from '@/service/authService.js'
export default {
    data() {
        return {
            user: {
                user_id: '',
                name: '',
                age: '',
                sex: 'male',
                description: ''
            }
        }
    },
    created(){
      this.user.user_id = localStorage.getItem('user_id')
    },
    methods: {
        updateUser() {
            // console.log(this.user)
            update_info(this.user).then(res => {
                // console.log("用户信息已更新:", this.user);
                alert("用户信息已更新!");
            }).catch(e => {
                console.log(e)
            })
        }
    }
}
</script>

<style scoped>
.user-profile {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    /* 调整为 flex-start 使内容靠上 */
    height: 100vh;
    /* 设置为视口高度 */
    width: 100vw;
    /* 设置为视口宽度 */
    padding-top: 50px;
    /* 添加顶部填充来调整位置 */
}

.form-container {
    width: 100%;
    max-width: 600px;
    /* 最大宽度设为600px */
    padding: 20px;
    background-color: #f9f9f9;
    /* 背景颜色 */
    border-radius: 8px;
    /* 圆角 */
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    /* 阴影 */
}

.form-group {
    margin-bottom: 15px;
    text-align: left;
    /* 使标签和输入框左对齐 */
}

label {
    display: block;
    margin-bottom: 5px;
}

input,
select,
textarea {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
}

button {
    padding: 10px 15px;
    background-color: #42b983;
    border: none;
    color: white;
    cursor: pointer;
}

button:hover {
    background-color: #38a175;
}
</style>