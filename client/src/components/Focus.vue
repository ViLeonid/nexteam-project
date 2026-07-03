<template>
  <div class="focus-page">
    <div class="focus-header">
      <h1>Фокус</h1>
      <button class="fullscreen-btn" @click="toggleFullscreen"> Полный экран </button>
    </div>



    <div class="focus-card">

      <div class="subject">

        <label style="margin: 10px;">Предмет: </label>

        <select v-model="subject">
          <option>Физика</option>
          <option>Математика</option>
          <option>Информатика</option>
        </select>

      </div>
      <div class="timer">
        {{ formattedTime }}
      </div>
      <div class="mode">
        {{ isRunning ? "Сессия идет..." : "Готов к работе" }}
      </div>

      <div class="buttons">
        <button class="start" @click="startSession" v-if="!isRunning">
          Старт
        </button>
        <button class="pause" @click="pauseSession" v-if="isRunning">
          Пауза
        </button>
        <button class="finish" @click="finishSession" v-if="isRunning">
          Завершить
        </button>
      </div>
    </div>
    <div class="fs-history">
        <div v-if="allFS!=[]">
            <div v-for='fs in allFS' :key="fs.id" >
                Начало: {{ fs.start_time }} 
                Конец: {{ fs.end_time }}
                Предмет: {{ fs.subject }}
                Реальное время: {{ fs.real_time }}
            </div>
        </div>
        <div v-else>
            <div>Пока фокус-сессий нет</div>
        </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onUnmounted, onMounted } from "vue"
import api from '@/api';

const subject = ref("Физика");

let seconds = ref(0);

const isRunning = ref(false);
let start_time = null;
let end_time = null;
const allFS = ref([]);
let interval = null;
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
  console.log({start_time: start_time.toISOString().slice(0, 19), end_time: end_time.toISOString().slice(0, 19), real_time: seconds.value, subject: subject.value});
  api.post('/api/add_fs', {start_time: start_time.toISOString().slice(0, 19), end_time: end_time.toISOString().slice(0, 19), real_time: seconds.value, subject: subject.value}).then(() => {
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

.focus-page{

    min-height:100vh;
    background:#0f172a;
    color:white;
    padding:40px;

}

.focus-header{

    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:40px;

}

.focus-header h1{

    font-size:42px;
    font-weight:700;

}

.focus-header p{

    color:#94a3b8;

}

.fullscreen-btn{

    background:#2563eb;
    color:white;
    border:none;
    padding:12px 20px;
    border-radius:12px;
    cursor:pointer;

}

.focus-card{

    max-width:700px;
    margin:auto;

    background:#1e293b;

    border-radius:24px;

    padding:50px;

    text-align:center;

}

.subject{

    margin-bottom:40px;

}

.subject select{

    margin-top:10px;

    width:250px;

    padding:12px;

    border-radius:12px;

    background:#0f172a;

    color:white;

}

.timer{

    font-size:96px;

    font-weight:700;

    margin-bottom:10px;

    letter-spacing:3px;

}

.mode{

    color:#94a3b8;

    margin-bottom:40px;

}

.buttons{

    display:flex;

    justify-content:center;

    gap:20px;

}

.buttons button{

    border:none;

    padding:15px 28px;

    border-radius:14px;

    color:white;

    cursor:pointer;

    font-size:16px;

}

.start{

    background:#22c55e;

}

.pause{

    background:#eab308;

}

.finish{

    background:#ef4444;

}

.quote{

    margin-top:60px;

    text-align:center;

}

.quote img{

    width:420px;

    max-width:90%;

    border-radius:20px;

    margin-bottom:20px;

}

.quote p{

    color:#94a3b8;

    font-size:18px;

}

</style>