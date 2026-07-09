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
        <div class="focus-block">
            <div class="focus-card settings-card" v-if="(status == 'notstarted')">

                <div class="focus-left">
                    <div class="info-block">
                        <div class="settings-el">
                            <label>Предмет</label>
                            <select v-model="subject">
                                <option v-for="s in subjects" :key="s.id" :value="s.name">
                                    {{ s.name }}
                                </option>
                            </select>
                        </div>

                        <div class="settings-el">
                            <label>Тема</label>
                            <select v-model="topic">
                                <option v-for="t in topics" :key="t.id" :value="t.name">
                                    {{ t.name }}
                                </option>
                            </select>
                        </div>

                        <div class="settings-el">
                            <label>Цель</label>
                            <input v-model="goal" placeholder="Что планируешь сделать?">
                        </div>


                        <div class="tasks-checkbox">
                            <input type="checkbox" v-model="is_tasks">
                            <span>Решение задач</span>
                        </div>

                    </div>
                    <div class="info-block">
                        <div class="settings-el">
                            <label>Режим таймера</label>
                            <select v-model="mode">
                                <option>Помодоро</option>
                                <option>Пробный тур</option>
                                <option>Бесконечный</option>
                            </select>
                        </div>

                        <div class="settings-el">
                            <label>Фон</label>
                            <select v-model="bg">
                                <option>-</option>
                                <option>Лес</option>
                                <option>Горы</option>
                            </select>
                        </div>

                        <div class="settings-el">
                            <label>Музыка/Шум для концентрации</label>
                            <select v-model="music">
                                <option>Дождь</option>
                                <option>-</option>
                            </select>
                        </div>


                    </div>

                </div>
            </div>
            <div class="focus-card timer-card" :style="status != 'notstarted' ? { 'background-image': backgrounds[bg] } : ''" :class="{ 'istimerfocus': !(status == 'notstarted'), 'fullscreenFocus': isfullscreen }">
                <div :class="[isfullscreen ? 'fullscreenRight' : 'focus-right']">
                    <div class="timer-circle" :style="{ height: timer_h + 'px' }">
                        <svg class="progress-ring" width="340" height="340"
                            v-if="!(status == 'notstarted') && (mode == 'Помодоро' || mode == 'Пробный тур')">

                            <!-- фон -->
                            <circle class="ring-bg" cx="170" cy="170" r="160" />

                            <!-- прогресс -->

                            <circle class="ring-progress" cx="170" cy="170" r="160" :stroke-dasharray="circumference"
                                :stroke-dashoffset="offset" />

                        </svg>



                        <div class="timer-content">

                            <div class="mode-title">
                                {{ status == "running" ? "ФОКУС" : "ГОТОВ" }}
                            </div>

                            <div class="timer">
                                {{ formattedTime }}
                            </div>
                            <div style="display: flex; justify-content: center; gap: 10px; ">

                                <div class="mode" v-if="status == 'running'">
                                    Сессия идет... {{ isbreak ? "Отдых" : "Концентрация" }}
                                </div>
                                <div class="mode" v-else-if="!(status == 'notstarted')">
                                    Пауза
                                    <div>
                                </div>
                                </div>
                            </div>

                            <div v-if="!(status == 'notstarted') && mode == 'Помодоро'" class="mode">Цикл: {{ actual_cycles }}/{{
                                cycles_count }}</div>

                        </div>

                    </div>
                    <div v-if="(status == 'notstarted') && mode == 'Помодоро'">
                        <div class="pomodoro-timer">
                            <label>Время одного цикла</label>
                            <input type="number" v-model="cycle_time">м
                        </div>
                        <div class="pomodoro-timer">
                            <label>Время одного перерыва</label>
                            <input type="number" v-model="break_time">м
                        </div>
                        <div class="pomodoro-timer">
                            <label>Количество циклов</label>
                            <input type="number" v-model="cycles_count">
                        </div>
                    </div>
                    <div v-else-if="!(status == 'running') && mode == 'Пробный тур'">
                        <div class="tour-timer">
                            <label>Время тура</label>
                            <input type="number" v-model="tour_time">
                        </div>
                    </div>
                    <div class="buttons">

                        <button class="start" @click="startSession" v-if="!(status == 'running') && (status == 'notstarted')">
                            Начать
                        </button>

                        <button class="continue" @click="continueSession" v-if="!(status == 'running') && !(status == 'notstarted')">
                            Продолжить
                        </button>

                        <button class="pause" @click="pauseSession" v-if="(status == 'running')">
                            Пауза
                        </button>

                        <button class="finish" @click="finishSession" v-if="!(status == 'notstarted')">
                            Завершить
                        </button>

                        <button class="subtractseconds" @click="addTime(-30)" v-if="(status == 'running')">
                            -30 сек
                        </button>
                        <button class="addseconds" @click="addTime(30)" v-if="(status == 'running')">
                            +30 сек
                        </button>

                    </div>

                    <div class="tasks-counter" :class="{ 'fullscreenTasks': isfullscreen }" v-if="(status == 'running') && is_tasks">

                        <div class="counter-title">
                            Решено задач
                        </div>

                        <div class="counter">

                            <button @click="addTasks(-1)">
                                −
                            </button>

                            <span>{{ count_tasks }}</span>

                            <button @click="addTasks(1)">
                                +
                            </button>
                        </div>
                    </div>

                </div>
            </div>
        </div>

        <div class="history-card">

            <div class="history-header">
                <h2>История фокус-сессий</h2>
            </div>

            <div v-if="allFS.length" class="history-table">

                <div class="table-head" style="font-size: 20px;">
                    <div>Дата</div>
                    <div>Предмет</div>
                    <div>Тема</div>
                    <div>Время</div>
                    <div>Задач</div>
                </div>

                <div class="table-row" v-for="fs in allFS" :key="fs.id">

                    <div class="date">
                        {{ fs.start_time }}
                    </div>

                    <div class="subject-cell">

                        <div class="subject-icon-small" :class="{
                            physics: fs.subject == 'Физика',
                            math: fs.subject == 'Математика',
                            informatics: fs.subject == 'Информатика'
                        }">
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

                    <div class="tasks" v-if="fs.count_tasks != 0">
                        {{ fs.count_tasks }}
                    </div>

                </div>

            </div>

            <div v-else class="empty-history">
                Пока нет завершённых сессий
            </div>

        </div>

    </div>
</template>

<script setup>
import { ref, computed, onUnmounted, onMounted, watch } from "vue"
import api from '@/api';
import infinityImg from '@/assets/infinity3.jpg'
import forestImg from '@/assets/focus_images/fi1.png'
import mountainsImg from '@/assets/focus_images/fi2.jpeg'
import { useToast } from "vue-toastification"


const subject = ref();
const subjects = ref([]);
const topics = ref([]);
const isSession = ref(false);
const backgrounds = {
    "-": 'none',
    "Лес": `url(${forestImg})`,
    "Горы": `url(${mountainsImg})`

}
let seconds = ref(0);
const topic = ref();
const goal = ref();
const is_tasks = ref();
const music = ref();
const real_time = ref(0);
const bg = ref();
const status = ref("notstarted");
const mode = ref("Помодоро");
const count_tasks = ref(0);
const isRunning = ref(false);
let work_started_at = ref();
let end_time = null;
const allFS = ref([]);
let interval = null;
let afs;
const radius = 160;
const circumference = 2 * Math.PI * radius;
let cycle_time = ref(25);
let break_time = ref(5);
let cycles_count = ref(4);
let tour_time = ref();
const toast = useToast();
const isfullscreen = ref(false);

watch(subject, () => {
    topic.value = undefined
    getTopics()
})

const progress = computed(() => {
    if (mode.value == "Помодоро") {
        if (isbreak.value) {
            return Math.min((seconds.value % ((cycle_time.value + break_time.value) * 60) - cycle_time.value * 60) / (break_time.value * 60), 1);
        }
        else {
            return Math.min(seconds.value % ((cycle_time.value + break_time.value) * 60) / (cycle_time.value * 60), 1);
        }
    }
    else if (mode.value == "Пробный тур") {
        return Math.min(seconds.value % (tour_time.value * 60) / (tour_time.value * 60), 1);
    }
    else if (mode.value == "Бесконечный") {
    }
})
const timer_h = computed(() => {
    if (!(status == 'notstarted')) {
        return 340;
    }
    return 200;
})
const isbreak = computed(() => {
    return seconds.value / 60 % (cycle_time.value + break_time.value) > cycle_time.value;
})
const actual_cycles = computed(() => {
    return 1 + Math.trunc(seconds.value / 60 / (cycle_time.value + break_time.value));
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

const addTasks = (count) => {
    api.post('/api/focus/tasks', {tasks: count});
    count_tasks.value += count;
}
const addTime = (count) => {
    real_time.value += count;
    updateTimer();
    api.post('/api/focus/time', {time: count});
}
function startSession() {
    console.log(topic.value);
    if (topic.value) {
        api.post('/api/focus/start', {
            subject: subject.value,
            is_tasks: is_tasks.value,
            topic: topic.value,
            goal: goal.value,
            bg: bg.value,
            music: music.value}).then({

        }).then(() => {
            isRunning.value = true;
            isSession.value = true;
            api.get('/api/focus/start').then(res => {
                work_started_at.value = res.data.work_started_at
                status.value = res.data.timer_status
                console.log("timer is running")
                console.log(work_started_at.value)
                clearInterval(interval);
                interval = setInterval(updateTimer, 1000);
            })
        })
    }
    else {
        toast.error("Заполните тему и предмет!", {
            toastClassName: "nexteam-toast",
            bodyClassName: "nexteam-toast-body",
            hideProgressBar: false,
        });
    }
}

function pauseSession() {
    isRunning.value = false
    clearInterval(interval)
    api.get('/api/focus/pause').then(res => {status.value = res.data.timer_status})
    const now = new Date();
    const start = new Date(work_started_at.value);
    real_time.value += Math.floor((now - start) / 1000);
}

function continueSession() {

    isRunning.value = true
    api.get('/api/focus/continue').then(res => {
        work_started_at.value = res.data.work_started_at
        status.value = res.data.timer_status
        clearInterval(interval);
        interval = setInterval(updateTimer, 1000);
    })

}


function finishSession() {

    clearInterval(interval)
    end_time = new Date();
    isRunning.value = false;
    isSession.value = false;
    api.post('/api/focus/end').then(res => {
        getFS();
        status.value = res.data.timer_status
    });
    count_tasks.value = 0;
    seconds.value = 0;
    real_time.value = 0;
}
const getFS = () => {
    api.get('/api/focus_history').then(res => {
        allFS.value = res.data.focus_sessions.sort((a, b) => {
            return new Date(b.start_time) - new Date(a.start_time);
        });
    })
}
const updateTimer = () => {
    console.log(!(status == 'notstarted') , status.value == "running" , work_started_at.value)
    if (!(status == 'notstarted') && status.value == "running" && work_started_at.value) {
        const now = new Date();
        const start = new Date(work_started_at.value);
        seconds.value = real_time.value + Math.floor((now - start) / 1000);
        console.log(seconds.value);
    }
}

const getAFS = () => {
    api.get('/api/active_focus').then(res => {
        afs = res.data.focus;
        status.value = afs.status;

        work_started_at.value = afs.work_started_at;
        count_tasks.value = afs.count_tasks;
        is_tasks.value = afs.is_tasks;
        real_time.value = afs.real_time;
        seconds.value = real_time.value;
        bg.value = afs.bg;
        music.value = afs.music;
        if(status.value == 'running'){
            clearInterval(interval);
            topic.value = afs.topic;
            goal.value = afs.goal;
            subject.value = afs.subject;
            interval = setInterval(updateTimer, 1000);
        }
        if (status.value == 'notstarted'){
            real_time.value = 0;
            seconds.value = 0;
        }
    })
}









const getTopics = () => {
    api.get(`/api/get_topics/${subject.value}`).then(res => { topics.value = res.data.topics })
}
function toggleFullscreen() {
    if (!document.fullscreenElement) {
        isfullscreen.value = true
        document.documentElement.requestFullscreen()
    } else {
        isfullscreen.value = false
        document.exitFullscreen()
    }

}
const getSubjects = () => {
    api.get('api/get_subjects').then(res => {
        subjects.value = res.data.subjects
        subject.value = subjects.value[0]
        getTopics()
    })
}

onUnmounted(() => clearInterval(interval));
onMounted(() => {
    getFS();
    getAFS();
    getSubjects();

})
</script>

<style>
.fullscreenTasks {
    margin: 20px;
}

.fullscreenRight {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;
    width: 100%;
    height: 100%;
    margin-bottom: 70px;
}

.fullscreenFocus {
    position: fixed;

    inset: 0;

    width: 100vw;
    height: 100vh;

    z-index: 99;

    border-radius: 0 !important;
    border: 0 !important;
    display: flex;
    justify-content: center;
    align-items: center;

    margin: 0;
}

.Vue-Toastification__toast.nexteam-toast {
    background-color: #121212 !important;
    border: 3px solid rgba(246, 246, 246, 0.8) !important;
    border-radius: 16px !important;
    box-shadow: 0 0 15px rgba(255, 255, 255, 0.1), 0 0 15px rgba(255, 255, 255, 0.6) !important;
}

.Vue-Toastification__progress-bar {
    background: #ffffff !important;
}
</style>


<style scoped>
.pomodoro-timer,
.tour-timer {
    display: flex;
    align-items: center;
    gap: 6px;
    margin: 5px 0;
    color: #cfcfcf;
}

.pomodoro-timer input,
.tour-timer input {
    width: 60px;
    padding: 3px 4px;

    background: #0b0b0b;
    color: #fff;

    border: 2px solid rgba(105, 105, 105, .8);
    border-radius: 10px;

    text-align: center;
    outline: none;
}

.pomodoro-timer input:focus,
.tour-timer input:focus {
    border-color: #fff;
    box-shadow: 0 0 12px rgba(255, 255, 255, .15);
}



.progress-ring {
    position: absolute;
    transform: rotate(-90deg);
    overflow: visible;
}

.progress-infinity {
    overflow: visible;
}

.neon-border {
    border: 1px solid var(--neon-border);

    box-shadow:
        0 0 10px rgba(255, 255, 255, 0.04),
        inset 0 0 0 rgba(255, 255, 255, 0);

    transition: 0.25s ease;
}

.neon-border:hover {
    border: 1px solid var(--neon-border-strong);

    box-shadow:
        0 0 18px var(--neon-glow),
        0 0 40px rgba(255, 255, 255, 0.06);
}

/* =========================
   GLOBAL RESET / BASE
========================= */

* {
    box-sizing: border-box;
    font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
}

.focus-page {
    min-height: 100vh;
    padding: 40px;
    color: #ffffff;

    background:
        radial-gradient(circle at top,
            rgba(255, 255, 255, 0.06),
            transparent 35%),

        radial-gradient(circle at bottom,
            rgba(255, 255, 255, 0.03),
            transparent 45%),

        #050505;

    overflow: hidden;
    position: relative;
}

/* subtle night glow overlay */
.focus-page::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;

    background:
        radial-gradient(circle at center,
            rgba(255, 255, 255, 0.03),
            transparent 70%);
}

/* =========================
   HEADER
========================= */

.focus-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 35px;
}

.focus-header h1 {
    font-size: 48px;
    font-weight: 800;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin: 0;

    color: #fff;

    text-shadow:
        0 0 10px rgba(255, 255, 255, 0.15);
}

.focus-header p {
    margin-top: 8px;
    color: #8a8a8a;
    letter-spacing: 1.5px;
}

/* =========================
   FULLSCREEN BUTTON
========================= */

.fullscreen-btn {
    background: #ffffff;
    position: fixed;
    right: 45px;
    border: none;
    border-radius: 14px;
    padding: 14px 24px;

    cursor: pointer;
    font-size: 14px;
    font-weight: 600;

    transition: 0.25s ease;
    z-index: 999;
    box-shadow:
        0 0 20px rgba(255, 255, 255, 0.25);
}

.fullscreen-btn:hover {
    transform: translateY(-2px);

    box-shadow:
        0 0 35px rgba(255, 255, 255, 0.45);
}

/* =========================
   LAYOUT
========================= */

.focus-block {
    display: flex;
    flex-wrap: wrap;
    gap: 30px;
}

.focus-card {

    display: flex;
    justify-content: space-between;

    background: rgba(10, 10, 10, 0.72);
    backdrop-filter: blur(28px);

    border: 3px solid rgba(208, 208, 208);
    border-radius: 28px;

    box-shadow:
        0 0 20px rgba(136, 136, 136, 0.85),
        inset 0 0 20px rgba(136, 136, 136, 0.85);

    transition: 0.3s ease;
}



/* =========================
   LEFT PANEL
========================= */

.focus-left {
    flex: 1;
    display: flex;
    flex-wrap: wrap;
    gap: 32px;
}

.settings-card {
    flex: 0 0 51vw;
    padding: 30px;
}

.info-block {
    display: flex;
    flex-direction: column;
    gap: 14px;
    width: 22vw;
}

.settings-el {
    margin: 10px;
}

/* =========================
   LABELS
========================= */

.info-block label {
    color: #bdbdbd;
    font-size: 14px;
    letter-spacing: 1px;

    margin-left: 8px;
    margin-bottom: 6px;
    display: block;
}

/* =========================
   INPUTS
========================= */

.info-block input,
.info-block select {
    width: 100%;

    background: #0b0b0b;
    color: #ffffff;

    border: 2px solid rgba(105, 105, 105, 0.8);
    border-radius: 14px;

    padding: 14px 16px;

    outline: none;

    transition: 0.25s ease;
}

.info-block input:focus,
.info-block select:focus {
    border-color: #ffffff;

    box-shadow:
        0 0 18px rgba(255, 255, 255, 0.18);
}

/* =========================
   CHECKBOX
========================= */

.tasks-checkbox {
    margin-top: 10px;
    margin-left: 30px;

    display: flex;
    align-items: center;
    gap: 12px;

    color: #cfcfcf;
}

.tasks-checkbox input {
    width: 18px;
    height: 18px;

    accent-color: #ffffff;
}

/* =========================
   RIGHT PANEL
========================= */

.timer-card {
    flex: 1;
    display: flex;
    padding: 10px;
}

.istimerfocus {
    background-position: center center;
    background-repeat: no-repeat;
    background-size: cover;
}

.focus-right {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
}

/* =========================
   TIMER CIRCLE
========================= */

.timer-circle {
    position: relative;
    width: 340px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.progress-ring {
    position: absolute;
    transform: rotate(-90deg);
}

.ring-bg {
    fill: none;

    stroke: rgba(31, 31, 31, 0.4);
    stroke-width: 10;
    filter: blur(2px);
}

.ring-progress {
    fill: none;

    stroke: #ffffff;
    stroke-width: 10;

    stroke-linecap: round;

    transition: stroke-dashoffset 0.5s linear;

    filter:
        drop-shadow(0 0 8px rgba(255, 255, 255, 0.6)) drop-shadow(0 0 18px rgba(255, 255, 255, 0.25));
}

/* =========================
   TIMER TEXT
========================= */

.timer-content {
    position: relative;
    z-index: 5;

    text-align: center;
}

.mode-title {
    color: #e5e5e5;
    font-size: 20px;
    letter-spacing: 3px;

    margin-bottom: 15px;
}

.timer {
    font-size: 68px;
    font-weight: 700;

    letter-spacing: 4px;

    color: #ffffff;

    text-shadow:
        0 0 12px rgba(255, 255, 255, 0.15);
}

.mode {
    color: #e5e5e5;
}

/* =========================
   BUTTONS
========================= */

.buttons {
    display: flex;
    gap: 18px;
    flex-wrap: wrap;
    justify-content: center;

    margin-top: 20px;
}

.buttons button {
    border: none;

    padding: 15px 28px;

    border-radius: 14px;

    font-size: 14px;
    font-weight: 600;

    cursor: pointer;

    transition: 0.25s ease;
}

/* START */
.start {
    background: #ffffff;
    color: #000000;

    box-shadow:
        0 0 20px rgba(255, 255, 255, 0.25);
}

.start:hover {
    transform: translateY(-3px);

    box-shadow:
        0 0 45px rgba(255, 255, 255, 0.55);
}

/* PAUSE */
.pause {
    background: #ffffff;
    color: #000000;

    box-shadow:
        0 0 20px rgba(255, 255, 255, 0.25);
}
.continue {

    background: #ffffff;
    color: #000000;

    box-shadow:
        0 0 20px rgba(255, 255, 255, 0.25);
}

/* FINISH */
.finish {
    background: #0e0e0e;
    color: #ffffff;

    border: 1px solid rgba(255, 255, 255, 0.12);
}

/* =========================
   TASK COUNTER
========================= */

.tasks-counter {
    position: absolute;
    left: 20px;
    bottom: 20px;
    margin-top: 35px;
    width: 260px;

    background: #0b0b0b;

    border-radius: 18px;

    padding: 22px;

    border: 2px solid rgba(255, 255, 255, 0.8);
}

.counter-title {
    color: #cfcfcf;
    margin-bottom: 16px;
    text-align: center;
}

.counter {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.counter span {
    font-size: 32px;
    font-weight: 700;
    color: #ffffff;
}

.counter button {
    width: 48px;
    height: 48px;

    border: none;
    border-radius: 14px;

    background: #ffffff;
    color: #000000;

    font-size: 20px;

    cursor: pointer;

    box-shadow: 0 0 18px rgba(255, 255, 255, 0.25);
}

/* =========================
   HISTORY CARD
========================= */

.history-card {
    margin-top: 40px;

    background: #070707;

    overflow: hidden;
    border: 3px solid rgba(208, 208, 208);
    border-radius: 28px;

    box-shadow:
        0 0 20px rgba(136, 136, 136, 0.85),
        inset 0 0 20px rgba(136, 136, 136, 0.85);
}

.history-header {
    padding: 26px 30px;

    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.history-header h2 {
    margin: 0;

    font-size: 26px;
    font-weight: 700;

    letter-spacing: 2px;

    color: #ffffff;
}

/* =========================
   TABLE
========================= */

.history-table {
    width: 100%;
}

.table-head,
.table-row {
    display: grid;

    grid-template-columns:
        2fr 1.4fr 2fr 1fr 0.8fr;

    align-items: center;
    border-radius: 10px;
    border-color: #c6c6c6;
    padding: 18px 30px;
}

.table-head {
    color: #8a8a8a;

    font-size: 13px;
    letter-spacing: 1px;
    border-bottom: 2px solid rgb(205, 205, 205);
    border-top: 2px solid rgb(205, 205, 205);
    border-radius: 0;
}

.table-row {
    border: 1px solid rgb(64, 64, 64);
    border-radius: 0;
    transition: 0.25s ease;

    color: #eaeaea;
}

.table-row:hover {
    background: rgba(255, 255, 255, 0.08);
}

/* =========================
   SUBJECT CELL
========================= */

.subject-cell {
    display: flex;
    align-items: center;
    gap: 12px;

    color: #ffffff;
}

.subject-icon-small {
    width: 38px;
    height: 38px;

    border-radius: 10px;

    display: flex;
    justify-content: center;
    align-items: center;

    font-size: 16px;

    background: #111111;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

/* neutral monochrome (no colors) */
.physics,
.math,
.informatics {
    background: #0d0d0d;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

/* =========================
   TASKS COLUMN
========================= */

.tasks {
    color: #ffffff;
    font-weight: 700;
    font-size: 16px;

    text-shadow:
        0 0 10px rgba(255, 255, 255, 0.2);
}

/* =========================
   EMPTY STATE
========================= */

.empty-history {
    padding: 50px;
    text-align: center;

    color: #777777;
    letter-spacing: 1px;
}

/* =========================
   RESPONSIVE
========================= */

@media(max-width:1100px) {

    .focus-card {
        flex-direction: column;
    }

    .focus-right {
        flex: 1 1 0;
    }

    .timer-circle {
        width: 280px;
        height: 280px;
    }

    .settings-card {
        flex: 1 1 100%;
    }

    .info-block {
        width: 100%;
    }
}

@media(max-width:700px) {

    .focus-page {
        padding: 20px;
    }

    .focus-header {
        flex-direction: column;
        gap: 20px;
        align-items: flex-start;
    }

    .timer {
        font-size: 56px;
    }

    .buttons {
        flex-direction: column;
        width: 100%;
    }

    .buttons button {
        width: 100%;
    }

    .table-head,
    .table-row {
        grid-template-columns: 1fr;
        gap: 10px;
    }

    .subject-cell {
        justify-content: flex-start;
    }
}

/* =========================
   FINAL MICRO GLOW TOUCH
========================= */

.focus-page * {
    transition: 0.2s ease;
}

.focus-card,
.history-card {
    will-change: transform;
}
</style>