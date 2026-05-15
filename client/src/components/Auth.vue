<template>
  <div class="auth-wrapper">

    <div class="auth-container">
      <div class="auth-header">
        <h2>{{ isLogin ? 'Вход в систему' : 'Регистрация' }}</h2>
        <p class="subtitle">
          {{ isLogin ? 'Добро пожаловать назад! Пожалуйста, войдите.' : 'Создайте аккаунт для начала работы.' }}
        </p>
      </div>

      <form @submit.prevent="handleAuth" class="auth-form">
        <div class="input-group">
          <label for="username">Имя пользователя</label>
          <div class="input-wrapper">
            <input 
              id="username"
              v-model="username" 
              type="text" 
              placeholder="Введите ваш логин" 
              required 
            />
          </div>
        </div>

        <div class="input-group">
          <label for="password">Пароль</label>
          <div class="input-wrapper">
            <input 
              id="password"
              v-model="password" 
              type="password" 
              placeholder="••••••••" 
              required 
            />
          </div>
        </div>

        <transition name="fade">
          <div v-if="error" class="error-msg">
            <span class="error-icon"></span>
            {{ error }}
          </div>
        </transition>

        <button type="submit" class="submit-btn">
          {{ isLogin ? 'Войти' : 'Создать аккаунт' }}
        </button>
      </form>

      <div class="auth-footer">
        <p @click="isLogin = !isLogin" class="toggle-link">
          {{ isLogin ? 'Еще нет аккаунта? Зарегистрируйся' : 'Уже есть аккаунт? Войти' }}
        </p>
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
/* Импорт шрифта Inter для премиального вида */
@import url('https://googleapis.com');

/* Общие настройки контейнера */
.auth-wrapper {
  font-family: 'Inter', sans-serif;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #0f172a; /* Глубокий темный фон */
  position: relative;
  overflow: hidden;
  padding: 20px;
}

/* Элементы заднего фона (сферы) */
.bg-sphere {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  z-index: 1;
  opacity: 0.4;
  animation: float 8s ease-in-out infinite alternate;
}
.sphere-1 {
  width: 300px;
  height: 300px;
  background: #6366f1; /* Индиго */
  top: -50px;
  right: -50px;
}
.sphere-2 {
  width: 400px;
  height: 400px;
  background: #3b82f6; /* Синий */
  bottom: -100px;
  left: -100px;
  animation-delay: -4s;
}

@keyframes float {
  0% { transform: translateY(0px) scale(1); }
  100% { transform: translateY(30px) scale(1.1); }
}

/* Карточка формы (Glassmorphism) */
.auth-container {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 420px;
  background: rgba(30, 41, 59, 0.7);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

/* Заголовок */
.auth-header {
  text-align: center;
  margin-bottom: 32px;
}
.auth-header h2 {
  color: #ffffff;
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 8px 0;
  letter-spacing: -0.5px;
}
.subtitle {
  color: #94a3b8;
  font-size: 14px;
  margin: 0;
}

/* Поля ввода */
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.input-group label {
  color: #cbd5e1;
  font-size: 13px;
  font-weight: 500;
  padding-left: 4px;
}
.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}
.input-icon {
  position: absolute;
  left: 16px;
  font-size: 16px;
  opacity: 0.7;
}
.input-wrapper input {
  width: 100%;
  padding: 14px 16px 14px 20px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #ffffff;
  font-size: 15px;
  transition: all 0.3s ease;
  box-sizing: border-box;
}
.input-wrapper input:focus {
  outline: none;
  border-color: #6366f1;
  background: rgba(15, 23, 42, 0.8);
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15);
}
.input-wrapper input::placeholder {
  color: #64748b;
}

/* Кнопка */
.submit-btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  border: none;
  border-radius: 12px;
  color: #ffffff;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
  margin-top: 8px;
}
.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
}
.submit-btn:active {
  transform: translateY(0);
}

/* Ошибка */
.error-msg {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
}

/* Ссылка переключения */
.auth-footer {
  text-align: center;
  margin-top: 24px;
}
.toggle-link {
  color: #94a3b8;
  font-size: 14px;
  cursor: pointer;
  display: inline-block;
  transition: color 0.2s ease;
  user-select: none;
}
.toggle-link:hover {
  color: #6366f1;
  text-decoration: underline;
}

/* Анимации для плавного появления ошибок (Vue Transitions) */
.fade-enter-active, .fade-leave-active {
  transition: all 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* Адаптивность для мобильных */
@media (max-width: 480px) {
  .auth-container {
    padding: 32px 24px;
  }
}
</style>
