<template>
  <div class="auth-wrapper">
    <div class="auth-container">
      <div class="auth-header">
        <h2 class="title">{{ isLogin ? 'Вход' : 'Регистрация' }}</h2>
      </div>

      <form @submit.prevent="handleAuth" class="auth-form">
        <div class="input-group">
          <label for="username">Введите логин:</label>
          <div class="input-wrapper">
            <input 
              id="username"
              v-model="username" 
              type="text" 
              placeholder="Username" 
              required 
            />
          </div>
        </div>

        <div class="input-group">
          <label for="password">Введите пароль:</label>
          <div class="input-wrapper">
            <input 
              id="password"
              v-model="password" 
              type="password" 
              placeholder="Password" 
              required 
            />
          </div>
        </div>

        <transition name="fade">
          <div v-if="error" class="error-msg">
            {{ error }}
          </div>
        </transition>

        <button type="submit" class="submit-btn">
          {{ isLogin ? 'Войти' : 'Создать аккаунт' }}
        </button>
      </form>

      <div class="auth-footer">
        <button @click="isLogin = !isLogin" class="secondary-button">
          {{ isLogin ? 'Еще нет аккаунта? Зарегистрируйся' : 'Уже есть аккаунт? Войти' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

axios.defaults.withCredentials = true;

const router = useRouter()
const username = ref('')
const password = ref('')
const isLogin = ref(true)
const error = ref('')

const handleAuth = async () => {
  error.value = ''
  const url = isLogin.value ? 'http://localhost:5000/api/login' : 'http://localhost:5000/api/register'
  
  try {
    const response = await axios.post(url, {
      username: username.value,
      password: password.value
    })
    
    if (isLogin.value) {
      sessionStorage.setItem('isLoggedIn', 'true')
      sessionStorage.setItem('username', response.data.username)
      router.push('/') 
    } else {
      alert('Регистрация успешна! Теперь выполните вход.')
      isLogin.value = true
      password.value = ''
    }
  } catch (err) {
    error.value = err.response?.data?.error || 'Произошла ошибка'
  }
}
</script>

<style scoped>
.auth-wrapper {
  margin: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100vw;
  height: 100vh;
  font-family: sans-serif;
  background-color: #000000;
  box-sizing: border-box;
}

.auth-container {
  width: 90vw;
  max-width: 400px;
  padding: 40px 20px;
  border-radius: 2em;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-sizing: border-box;
}

.auth-header {
  width: 100%;
  text-align: center;
}

.title {
  text-align: center;
  font-size: 2.5em;
  font-family: 'Gill Sans', sans-serif;
  margin-top: 0;
  margin-bottom: 20px;
  color: #000000;
}

.auth-form {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.input-group {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.input-group label {
  color: #333333;
  margin: 10px 0 5px 0;
  width: 85%;
  text-align: left;
  font-size: 1rem;
}

.input-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
}

.input-wrapper input {
  font-size: 1rem;
  margin-bottom: 15px;
  width: 85%;
  height: 50px;
  border-radius: 2em;
  padding: 0 1.2em;
  background-color: #4f4f4f;
  border: 1px solid #cccccc;
  box-sizing: border-box; 
  outline: none;
  color: #ffffff; 
}

.submit-btn {
  width: 85%;
  height: 50px;
  margin-top: 10px;
  border-radius: 2em;
  border: none;
  background-color: #000000;
  color: #ffffff;
  font-size: 1.1rem;
  cursor: pointer;
  transition: 0.3s;
}

.submit-btn:hover {
  background-color: #333333;
}

.error-msg {
  color: red;
  margin: 5%;
  text-align: center;
  font-size: 0.9rem;
}

.auth-footer {
  width: 100%;
  display: flex;
  justify-content: center;
}

.secondary-button {
  background-color: transparent !important;
  border: none;
  color: #666666 !important;
  font-size: 0.9rem !important;
  text-decoration: underline;
  margin-top: 20px;
  cursor: pointer;
}

.secondary-button:hover {
  color: #000000 !important;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
