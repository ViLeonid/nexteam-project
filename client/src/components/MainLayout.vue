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
              <li class="nav-item">
                <router-link to="/graph" class="nav-link" active-class="active">
                  <i class="bi bi-book me-2"></i> Граф
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
                <router-link to="/profile" class="nav-link" active-class="active">
                  <i class="bi bi-book me-2"></i> Профиль
                </router-link>
              </li>
              <!-- <li class="nav-item">
                <a href="#" class="nav-link disabled"><i class="bi bi-gear me-2"></i> Настройки</a>
              </li> -->
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

<style scoped>
.sidebar{
    background:#050505 !important;

    border-right:2px solid rgba(208,208,208,.18);

    box-shadow:
        8px 0 30px rgba(0,0,0,.45),
        inset -1px 0 0 rgba(255,255,255,.05);

    overflow:hidden;
}

/* ---------------- Логотип ---------------- */

.sidebar h2{
    color:white;
    font-size:34px;
    font-weight:800;
    letter-spacing:-1px;
}

/* ---------------- Разделители ---------------- */

.sidebar hr{
    border-color:rgba(255,255,255,.08);
    opacity:1;
    margin:20px 16px;
}

/* ---------------- Заголовки ---------------- */

.sidebar-heading{

    color:#666 !important;

    font-size:11px;

    letter-spacing:2px;

    font-weight:700;

    margin-bottom:14px !important;
}

/* ---------------- Меню ---------------- */

.nav{

    gap:6px;
}

.nav-link{

    display:flex;
    align-items:center;
    gap:12px;

    height:52px;

    padding:0 18px !important;

    border-radius:16px;

    color:#8c8c8c !important;

    font-size:15px;

    font-weight:500;

    transition:.25s;
}

/* ---------------- Иконки ---------------- */

.nav-link i{

    font-size:18px;

    width:20px;

    text-align:center;

    transition:.25s;
}

/* ---------------- Hover ---------------- */

.nav-link:hover{

    background:#101010;

    color:white !important;

    transform:translateX(4px);
}

.nav-link:hover i{

    color:white;
}

/* ---------------- Активная ---------------- */

.nav-link.active{

    color:white !important;

    background:#111;

    border:2px solid rgba(208,208,208,.85);

    box-shadow:
        0 0 18px rgba(180,180,180,.35),
        inset 0 0 12px rgba(255,255,255,.06);
}

/* ---------------- Нижняя кнопка ---------------- */

.sidebar>.p-3{

    border-top:1px solid rgba(255,255,255,.08)!important;

    background:#050505 !important;
}

.btn-logout{

    height:52px;

    display:flex;
    align-items:center;

    background:#111;

    color:#ff6d6d;

    border:2px solid rgba(255,90,90,.18);

    border-radius:16px;

    font-size:15px;

    font-weight:600;

    transition:.25s;
}

.btn-logout:hover{

    background:#181818;

    color:white;

    border-color:#ff5b5b;

    box-shadow:0 0 18px rgba(255,90,90,.22);
}

.btn-logout i{

    font-size:18px;
}

/* ---------------- Контент ---------------- */

main{

    background:#080808 !important;

    min-height:100vh;
}

/* ---------------- Скролл ---------------- */

.sidebar::-webkit-scrollbar{

    width:6px;
}

.sidebar::-webkit-scrollbar-thumb{

    background:#3a3a3a;

    border-radius:999px;
}

.sidebar::-webkit-scrollbar-track{

    background:transparent;
}

/* ---------------- Responsive ---------------- */

@media(max-width:768px){

    .sidebar{

        width:260px;
    }

}
</style>
