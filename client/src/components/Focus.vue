<template>
  <div class="focus-page">

    <div class="focus-header">
      <div>
        <h1>Фокус-сессия</h1>
        <p>Настрой сессию и приступай к работе</p>
      </div>

      <button class="fullscreen-btn" @click="toggleFullscreen">
        ⛶ Полный экран
      </button>
    </div>

    <div class="focus-card">

      <div class="focus-left">

        <div class="status">
          <span class="dot"></span>
          {{ isRunning ? "СЕССИЯ АКТИВНА" : "ГОТОВ К НАЧАЛУ" }}
        </div>

        <div class="subject-card">
          <div class="subject-icon">
            📚
          </div>

          <div>
            <h2>{{ subject }}</h2>
            <p>{{ topic || "Без темы" }}</p>
          </div>
        </div>

        <div class="info-block">

          <label>Тема</label>
          <input
              v-model="topic"
              placeholder="Например: Электростатика"
          >

          <label>Цель</label>
          <input
              v-model="goal"
              placeholder="Что планируешь сделать?"
          >

          <label>Предмет</label>

          <select v-model="subject">
            <option>Физика</option>
            <option>Математика</option>
            <option>Информатика</option>
          </select>

          <div class="tasks-checkbox">
            <input
                type="checkbox"
                v-model="is_tasks"
            >

            <span>Решение задач</span>
          </div>

        </div>

      </div>

      <div class="focus-right">

        <div class="timer-circle">

            <svg
                class="progress-ring"
                width="320"
                height="320"
            >

                <!-- фон -->

                <circle
                    class="ring-bg"
                    cx="160"
                    cy="160"
                    r="130"
                />

                <!-- прогресс -->

                <circle
                    class="ring-progress"
                    cx="160"
                    cy="160"
                    r="130"
                    :stroke-dasharray="circumference"
                    :stroke-dashoffset="offset"
                />

            </svg>

            <div class="timer-content">

                <div class="mode-title">
                    {{ isRunning ? "ФОКУС" : "ГОТОВ" }}
                </div>

                <div class="timer">
                    {{ formattedTime }}
                </div>

                <div class="mode">
                    {{ isRunning ? "Сессия идет..." : "Нажмите старт" }}
                </div>

            </div>

        </div>

        <div class="buttons">

          <button
              class="start"
              @click="startSession"
              v-if="!isRunning"
          >
            ▶ Начать
          </button>

          <button
              class="pause"
              @click="pauseSession"
              v-if="isRunning"
          >
            ⏸ Пауза
          </button>

          <button
              class="finish"
              @click="finishSession"
              v-if="isRunning"
          >
            ■ Завершить
          </button>

        </div>

        <div
            class="tasks-counter"
            v-if="isRunning && is_tasks"
        >

          <div class="counter-title">
            Решено задач
          </div>

          <div class="counter">

            <button @click="count_tasks--">
              −
            </button>

            <span>{{ count_tasks }}</span>

            <button @click="count_tasks++">
              +
            </button>

          </div>

        </div>

      </div>

    </div>

    <div class="history-card">

        <div class="history-header">
            <h2>История фокус-сессий</h2>
        </div>

        <div v-if="allFS.length" class="history-table">

            <div class="table-head">
                <div>Дата</div>
                <div>Предмет</div>
                <div>Тема</div>
                <div>Время</div>
                <div>Задач</div>
            </div>

            <div
                class="table-row"
                v-for="fs in allFS"
                :key="fs.id"
            >

                <div class="date">
                    {{ fs.start_time }}
                </div>

                <div class="subject-cell">

                    <div
                        class="subject-icon-small"
                        :class="{
                            physics: fs.subject=='Физика',
                            math: fs.subject=='Математика',
                            informatics: fs.subject=='Информатика'
                        }"
                    >
                        📚
                    </div>

                    {{ fs.subject }}

                </div>

                <div>
                    {{ fs.topic || "—" }}
                </div>

                <div>
                    {{ fs.real_time }} сек
                </div>

                <div class="tasks">
                    {{ fs.count_tasks }}
                </div>

            </div>

        </div>

        <div
            v-else
            class="empty-history"
        >
            Пока нет завершённых сессий
        </div>

        </div>

  </div>
</template>

<script setup>
import { ref, computed, onUnmounted, onMounted } from "vue"
import api from '@/api';

const subject = ref("Физика");

let seconds = ref(0);
const topic = ref();
const goal = ref();
const is_tasks = ref();
const count_tasks = ref(0);
const isRunning = ref(false);
let start_time = null;
let end_time = null;
const allFS = ref([]);
let interval = null;

const radius = 130
const circumference = 2 * Math.PI * radius

const progress = computed(() => {
    // пока пример: полный круг за час
    const max = 100
    return Math.min(seconds.value / max, 1)
})

const offset = computed(() => {
    return circumference * (1 - progress.value)
})

const formattedTime = computed(() => {
  const h = Math.floor(seconds.value / 3600)
  const m = Math.floor(seconds.value % 3600 / 60)
  const s = seconds.value % 60
  return [
    h.toString().padStart(2, "0"),
    m.toString().padStart(2, "0"),
    s.toString().padStart(2, "0")
  ].join(":")

})

function startSession(){
  if (seconds.value === 0) {
    start_time = new Date();
  }
  isRunning.value=true
  interval=setInterval(()=>{
    seconds.value++
  },1000)
}

function pauseSession(){

  isRunning.value=false

  clearInterval(interval)  
}

function finishSession(){

  clearInterval(interval)
  end_time = new Date();
  isRunning.value=false;
  api.post('/api/add_fs', {start_time: start_time.toISOString().slice(0, 19), end_time: end_time.toISOString().slice(0, 19), real_time: seconds.value, subject: subject.value, is_tasks: is_tasks.value, topic: topic.value, goal: goal.value, count_tasks: count_tasks.value}).then(() => {
    getFS();
  });
  seconds.value = 0;
}
const getFS = () => {
  api.get('/api/focus').then(res => { allFS.value = res.data.focus_sessions })
}

function toggleFullscreen(){
  if(!document.fullscreenElement){
    document.documentElement.requestFullscreen()
  }else{
    document.exitFullscreen()
  }
}

onUnmounted(()=>clearInterval(interval));
onMounted(getFS);
</script>
<style scoped>

*{
    box-sizing:border-box;
}

.focus-page{
    min-height:100vh;
    padding:40px;
    color:white;
    background:
        radial-gradient(circle at top,#2c1b55 0%,#111827 35%,#0b1120 100%);
}

.focus-header{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:35px;
}

.focus-header h1{
    font-size:42px;
    font-weight:700;
    margin:0;
}

.focus-header p{
    margin-top:8px;
    color:#9ca3af;
}

.fullscreen-btn{
    background:linear-gradient(135deg,#7c3aed,#5b21b6);
    color:white;
    border:none;
    border-radius:14px;
    padding:14px 24px;
    cursor:pointer;
    font-size:15px;
    transition:.25s;
    box-shadow:0 10px 30px rgba(124,58,237,.35);
}

.fullscreen-btn:hover{
    transform:translateY(-2px);
}

.focus-card{

    display:flex;
    justify-content:space-between;
    gap:60px;

    background:rgba(24,31,49,.75);
    backdrop-filter:blur(18px);

    border:1px solid rgba(255,255,255,.08);

    border-radius:28px;

    padding:45px;

    box-shadow:
    0 0 40px rgba(0,0,0,.35);

}

.focus-left{
    flex:1;
}

.focus-right{

    width:430px;

    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;

}

.status{

    display:inline-flex;
    align-items:center;
    gap:10px;

    padding:8px 16px;

    border-radius:30px;

    background:rgba(34,197,94,.12);

    color:#4ade80;

    font-weight:600;

    margin-bottom:30px;

}

.dot{

    width:10px;
    height:10px;
    border-radius:50%;
    background:#4ade80;

    box-shadow:
    0 0 12px #4ade80;

}

.subject-card{

    display:flex;
    align-items:center;
    gap:20px;

    margin-bottom:35px;

}

.subject-icon{

    width:72px;
    height:72px;

    display:flex;
    align-items:center;
    justify-content:center;

    border-radius:20px;

    font-size:34px;

    background:linear-gradient(135deg,#7c3aed,#4f46e5);

    box-shadow:0 15px 35px rgba(124,58,237,.4);

}

.subject-card h2{

    margin:0;
    font-size:34px;

}

.subject-card p{

    margin-top:6px;
    color:#b7bfd0;

}

.info-block{

    display:flex;
    flex-direction:column;
    gap:14px;

}

.info-block label{

    color:#b7bfd0;
    font-size:15px;

}

.info-block input,
.info-block select{

    width:100%;

    background:#111827;

    color:white;

    border:1px solid rgba(255,255,255,.08);

    border-radius:14px;

    padding:14px 16px;

    outline:none;

    transition:.25s;

}

.info-block input:focus,
.info-block select:focus{

    border-color:#7c3aed;
    box-shadow:0 0 15px rgba(124,58,237,.4);

}

.tasks-checkbox{

    margin-top:10px;

    display:flex;
    align-items:center;
    gap:12px;

}

.tasks-checkbox input{

    width:18px;
    height:18px;

}

.timer-circle{

    position:relative;

    width:320px;
    height:320px;

    display:flex;
    align-items:center;
    justify-content:center;

}

.progress-ring{

    position:absolute;

    transform:rotate(-90deg);

}

.ring-bg{

    fill:none;

    stroke:#3b3653;

    stroke-width:10;

}

.ring-progress{

    fill:none;

    stroke:#7c3aed;

    stroke-width:10;

    stroke-linecap:round;

    transition:stroke-dashoffset .5s linear;

    filter:drop-shadow(0 0 12px rgba(124,58,237,.7));

}

.timer-content{

    position:relative;

    z-index:5;

    text-align:center;

}

.mode-title{

    color:#d4d4d8;

    font-size:20px;

    margin-bottom:15px;

    letter-spacing:2px;

}

.timer{

    font-size:72px;
    font-weight:700;
    margin-bottom:12px;
}

.mode{

    color:#9ca3af;
}

.buttons{

    display:flex;
    gap:18px;
    flex-wrap:wrap;
    justify-content:center;

}

.buttons button{

    border:none;

    padding:15px 28px;

    border-radius:14px;

    color:white;

    font-size:16px;

    cursor:pointer;

    transition:.25s;

}

.buttons button:hover{

    transform:translateY(-3px);

}

.start{

    background:linear-gradient(135deg,#7c3aed,#5b21b6);

    box-shadow:0 10px 25px rgba(124,58,237,.35);

}

.pause{

    background:#f59e0b;

}

.finish{

    background:#dc2626;

}

.tasks-counter{

    margin-top:35px;

    width:260px;

    background:#111827;

    border-radius:18px;

    padding:22px;

    border:1px solid rgba(255,255,255,.06);

}

.counter-title{

    color:#cbd5e1;

    margin-bottom:16px;

    text-align:center;

}

.counter{

    display:flex;

    justify-content:space-between;

    align-items:center;

}

.counter span{

    font-size:32px;
    font-weight:700;

}

.counter button{

    width:48px;
    height:48px;

    border:none;

    border-radius:14px;

    background:#7c3aed;

    color:white;

    font-size:24px;

    cursor:pointer;

}

.history-card{

    margin-top:40px;

    background:rgba(22,28,44,.82);

    border-radius:22px;

    overflow:hidden;

    border:1px solid rgba(255,255,255,.06);

}

.history-header{

    padding:26px 30px;

    border-bottom:1px solid rgba(255,255,255,.05);

}

.history-header h2{

    margin:0;

    font-size:28px;

}

.history-table{

    width:100%;

}

.table-head{

    display:grid;

    grid-template-columns:
    2fr
    1.4fr
    2fr
    1fr
    .8fr;

    padding:18px 30px;

    color:#8b95a7;

    font-size:15px;

    border-bottom:1px solid rgba(255,255,255,.05);

}

.table-row{

    display:grid;

    grid-template-columns:
    2fr
    1.4fr
    2fr
    1fr
    .8fr;

    align-items:center;

    padding:22px 30px;

    transition:.25s;

    border-bottom:1px solid rgba(255,255,255,.04);

}

.table-row:hover{

    background:rgba(124,58,237,.08);

}

.subject-cell{

    display:flex;

    align-items:center;

    gap:12px;

}

.subject-icon-small{

    width:38px;

    height:38px;

    border-radius:10px;

    display:flex;

    justify-content:center;

    align-items:center;

    font-size:18px;

}

.physics{

    background:#6d28d9;

}

.math{

    background:#15803d;

}

.informatics{

    background:#2563eb;

}

.tasks{

    color:#4ade80;

    font-weight:700;

    font-size:18px;

}

.empty-history{

    padding:50px;

    text-align:center;

    color:#94a3b8;

}

@media(max-width:1100px){

.focus-card{

    flex-direction:column;

}

.focus-right{

    width:100%;

}

.timer-circle{

    width:280px;
    height:280px;

}

}

@media(max-width:700px){

.focus-page{

    padding:20px;

}

.focus-header{

    flex-direction:column;
    gap:20px;
    align-items:flex-start;

}

.timer{

    font-size:52px;

}

.subject-card{

    flex-direction:column;
    text-align:center;

}

.buttons{

    flex-direction:column;
    width:100%;

}

.buttons button{

    width:100%;

}

}

</style>