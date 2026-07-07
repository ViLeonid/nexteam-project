<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router';
import api from '@/api';

const router = useRouter()

const isFullscreen = ref(false)

const updateFullscreen = () => {
  isFullscreen.value = !!document.fullscreenElement
}

onMounted(() => {
  document.addEventListener('fullscreenchange', updateFullscreen)
})

onUnmounted(() => {
  document.removeEventListener('fullscreenchange', updateFullscreen)
})
// Функция для выхода из аккаунта
const handleLogout = async () => {
  try {
    // Отправляем запрос на разлогин во Flask (порт 5000)
    await api.post('/api/logout')
  } catch (e) {
    console.error('Ошибка при удалении сессии на сервере', e)
  } finally {
    // В любом случае очищаем локальные данные, чтобы сработал роутер
    sessionStorage.clear()
    // Перенаправляем пользователя на форму входа
    router.push('/auth')
  }
}
</script>

<template>
  <div class="container-fluid">
    <div class="row">
      <!-- БОКОВАЯ ПАНЕЛЬ -->
      <!-- ДОБАВЛЕНО: классы d-flex flex-column для управления вертикальным пространством -->
      <nav v-if="!isFullscreen" class="col-md-3 col-lg-2 d-md-block bg-dark sidebar p-0 shadow min-vh-100 position-fixed d-flex flex-column justify-content-between">
        <div class="position-sticky pt-3 w-100">
          <div class="px-4 py-3 text-white">
            <h2 class="m-0">OnOlympUs</h2>
          </div>
          
          <hr class="text-secondary mx-3">

          <div class="px-3">
            <!-- Секция 1: Основное -->
            <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-secondary text-uppercase small">
              Основные
            </h6>
            <ul class="nav flex-column mb-3">
              <li class="nav-item">
                <router-link to="/" class="nav-link" exact-active-class="active">
                  <i class="bi bi-book me-2"></i> Главная
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/todos" class="nav-link" exact-active-class="active">
                  <i class="bi bi-book me-2"></i> Задачи
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/schedule" class="nav-link" active-class="active">
                  <i class="bi bi-book me-2"></i> Расписание
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/analytics" class="nav-link" active-class="active">
                  <i class="bi bi-book me-2"></i> Аналитика
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/olympiads" class="nav-link" active-class="active">
                  <i class="bi bi-book me-2"></i> Олимпиады
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/focus" class="nav-link" active-class="active">
                  <i class="bi bi-book me-2"></i> Фокус
                </router-link>
              </li>
            </ul>

            <hr class="text-secondary mx-3">

            <!-- Секция 2: Аккаунт -->
            <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-secondary text-uppercase small">
              Пользователь
            </h6>
            <ul class="nav flex-column">
              <li class="nav-item">
                <a href="#" class="nav-link disabled"><i class="bi bi-person me-2"></i> Профиль</a>
              </li>
              <li class="nav-item">
                <a href="#" class="nav-link disabled"><i class="bi bi-gear me-2"></i> Настройки</a>
              </li>
            </ul>
          </div>
        </div>

        <!-- ДОБАВЛЕНО: Нижняя секция с кнопкой Выйти -->
        <div class="p-3 w-100 border-top border-secondary border-opacity-10 bg-dark">
          <button @click="handleLogout" class="btn btn-logout w-100 text-start py-2 px-3 d-flex align-items-center gap-2">
            <i class="bi bi-box-arrow-left"></i>
            <span>Выйти из системы</span>
          </button>
        </div>
      </nav>

      <!-- КОНТЕНТ СТРАНИЦЫ -->
      <!-- ДОБАВЛЕНО: Сдвиг контента offset-md-3, чтобы sidebar фиксировано стоял слева и не перекрывал контент -->
      <main :class="['min-vh-100 p-0', isFullscreen ? 'col-12' : 'col-md-9 ms-sm-auto col-lg-10 offset-md-3 offset-lg-2']">
        <router-view />
      </main>
    </div>
  </div>
</template>

<style>
.sidebar .nav-link {
  color: #adb5bd;
  border-radius: 8px;
  margin-bottom: 5px;
  padding: 10px 15px;
}

.sidebar .nav-link:hover {
  background-color: rgba(255, 255, 255, 0.05);
  color: white;
}

.sidebar .nav-link.active {
  background-color: #0d6efd !important;
  color: white !important;
}

.sidebar-heading {
  font-size: 0.75rem;
  font-weight: 700;
}

hr {
  opacity: 0.1;
}

/* ИСПРАВЛЕНО: Белый/светлый фон вместо черного, чтобы текст карточек задач был читаемым */
main {
  background-color: #f8f9fa !important;
}

/* ДОБАВЛЕНО: Стили для кнопки выхода */
.btn-logout {
  color: #dc3545;
  background: transparent;
  border: 1px solid transparent;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-logout:hover {
  background-color: rgba(220, 53, 69, 0.1);
  border-color: rgba(220, 53, 69, 0.2);
  color: #ea868f;
}
</style>
