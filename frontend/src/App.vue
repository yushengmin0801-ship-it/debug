<template>
  <div class="login-container">
    <div class="login-box">
      <h2>登录</h2>
      <div class="input-group">
        <label>用户名:</label>
        <input v-model="username" type="text" placeholder="请输入用户名" />
      </div>
      <div class="input-group">
        <label>密码:</label>
        <input v-model="password" type="password" placeholder="请输入密码" />
      </div>
      <button @click="handleLogin">登录</button>
      <p v-if="message" :class="{ 'error': !isSuccess, 'success': isSuccess }">
        {{ message }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const username = ref('');
const password = ref('');
const message = ref('');
const isSuccess = ref(false);

const handleLogin = async () => {
  try {
    const response = await axios.post('/api/login', {
      username: username.value,
      password: password.value
    });
    
    message.value = response.data.message;
    isSuccess.value = response.data.success;
  } catch (err) {
    message.value = '服务器连接失败';
    isSuccess.value = false;
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
}
.login-box {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  width: 320px;
}
.input-group {
  margin-bottom: 20px;
  text-align: left;
}
label {
  display: block;
  margin-bottom: 8px;
}
input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}
button {
  width: 100%;
  padding: 10px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.error { color: red; }
.success { color: green; }
</style>
