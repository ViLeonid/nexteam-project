<template>
  <div class="auth-wrapper">
    <div class="auth-container">
      <div class="auth-header">
        <h2 class="title">{{ isLogin ? 'Вход' : 'Регистрация' }}</h2>
      </div>

      <form @submit.prevent="handleAuth" class="auth-form">
        <div class="input-group">
          <label class="txt" for="username">Введите логин:</label>
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
          <label class="txt" for="password">Введите пароль:</label>
          <div class="input-wrapper"  style="margin-bottom: -0.8rem;">
            <input 
              id="password"
              v-model="password" 
              type="password" 
              placeholder="Password" 
              required 
            />
          </div>
          <div class="password-hint" v-show="!isLogin">Пароль состоит из не менее 10 символов, содержит заглавную букву, строчную букву, цифру</div>
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
import { ref } from 'vue';
import api from '@/api';
import { useRouter } from 'vue-router';


const router = useRouter()
const username = ref('')
const password = ref('')
const isLogin = ref(true)
const error = ref('')

const handleAuth = async () => {
  error.value = ''
  const url = isLogin.value ? '/api/login' : '/api/register'
  
  try {
    const response = await api.post(url, {
      username: username.value,
      password: password.value
    })
    
    if (isLogin.value) {
      sessionStorage.setItem('isLoggedIn', 'true')
      sessionStorage.setItem('username', response.data.username)
      router.push('/todos') 
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
  background-image: url('@/assets/bg2.png');
  background-size: cover;
  background-position: center;
  box-sizing: border-box;
}

.auth-container {
  width: 90vw;
  max-width: 400px;
  padding: 40px 20px;
  border-radius: 2em;
  background: rgba(31, 31, 31, 0.7); 
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 2px solid rgba(123, 123, 123, 0.4);
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  box-sizing: border-box;
}

.auth-header {
  width: 100%;
  text-align: center;
}
.password-hint[style*="display: none"] {
  display: block !important; /* Отменяем скрытие через display */
  visibility: hidden; /* Делаем элемент полностью невидимым, но сохраняем его место */
}
.title {
  text-align: center;
  font-size: 2.5em;
  font-family: 'Gill Sans', sans-serif;
  margin-top: 0;
  margin-bottom: 20px;
  color: #ffffff;
}
.password-hint {
  width: 85%; /* Точная ширина инпута */
  font-size: 0.75rem; /* Читаемый мелкий шрифт вместо 0.5rem */
  color: #666666; /* Нейтральный серый цвет */
  text-align: left; /* Выравнивание по левому краю инпута */
  margin-top: 0.1rem; /* Небольшой отступ сверху от инпута */
  padding-left: 0.5rem;
  margin-bottom: 1rem; /* Отступ снизу до кнопки/ошибки */
  white-space: normal; /* Разрешение переноса текста */
  word-wrap: break-word; /* Защита от выламывания длинных слов */
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
  color: #d9d9d9;
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
  color: #9c9c9c !important;
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
