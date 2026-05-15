<template>
  <div class="auth-container">
    <h2>{{ isLogin ? 'Вход в систему' : 'Регистрация' }}</h2>
    <form @submit.prevent="handleAuth">
      <input v-model="username" type="text" placeholder="Имя пользователя" required />
      <input v-model="password" type="password" placeholder="Пароль" required />
      <button type="submit">{{ isLogin ? 'Войти' : 'Создать аккаунт' }}</button>
    </form>
    <p @click="isLogin = !isLogin" class="toggle-link">
      {{ isLogin ? 'Еще нет аккаунта? Зарегистрируйся' : 'Уже есть аккаунт? Войти' }}
    </p>
    <p v-if="error" class="error-msg">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router' // 1. Импортируем роутер

axios.defaults.withCredentials = true;

const router = useRouter() // 2. Инициализируем его внутри скрипта
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
      // 3. ОБЯЗАТЕЛЬНО записываем флаги ДО редиректа, чтобы Guard их увидел!
      sessionStorage.setItem('isLoggedIn', 'true')
      sessionStorage.setItem('username', response.data.username)
      
      // 4. Сама команда перехода на главную страницу задач
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