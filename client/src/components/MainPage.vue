<script setup>
// Импортируем ваш сохраненный компонент
import ChartsForAnalytics from '@/components/ChartsForAnalytics/todays_time_donut.vue'
import Last_days_hours_of_todos from './ChartsForAnalytics/last_days_hours_of_todos.vue';
import { ref, onMounted, computed, onBeforeUnmount } from 'vue'
import api from '@/api';

const now = ref(Date.now())

const goalName = ref();
const goalDate = ref();
let interval

onMounted(() => {
    interval = setInterval(() => {
        now.value = Date.now()
    }, 1000)
})

onBeforeUnmount(() => {
    clearInterval(interval)
})
const events = ref([])

// загрузка событий пользователя
const fetchEvents = async () => {
    const res = await api.get('/added_olympiads_events')
    events.value = res.data.events
}

onMounted(() => {
    fetchEvents()
})
const goal = computed(() => {
    // if (!events.value.length) return null



    // const futureEvents = events.value
    //     .map(e => ({
    //         ...e,
    //         start: new Date(e.start_time)
    //     }))
    //     .filter(e => e.start.getTime() > currentTime)
    //     .sort((a, b) => a.start - b.start)

    // if (!futureEvents.length) return null

    // const nearest = futureEvents[0]
    const currentTime = now.value
    api.get('/api/profile').then(res => {
        goalName.value = res.data.goal_name;
        goalDate.value = res.data.goal_date;
    })
    if (goalName.value && goalDate.value) {
        const diff = new Date(goalDate.value).getTime() - currentTime
        return {
            title: goalName.value,
            days: Math.floor(diff / (1000 * 60 * 60 * 24)),
            hours: Math.floor((diff / (1000 * 60 * 60)) % 24),
            minutes: Math.floor((diff / (1000 * 60)) % 60),
            seconds: Math.floor((diff / 1000) % 60)
        }
    }
})
</script>

<template>
    <h1>Главная</h1>
    <div class="main-wrapper">
        <div class="main-target">
            <div v-if="goal" class="overlay">
                <div class="glass-card">
                <p class="label">Главная цель</p>
                <h2 class="title">{{ goal.title }}</h2>
                <div class="counter">
                        <div class="remaining-title">Осталось:</div>
                        <div class="time-block">
                            <span class="num">{{ goal.days }}</span>
                            <span class="lbl">д</span>
                        </div>

                        <div class="time-block">
                            <span class="num">{{ goal.hours }}</span>
                            <span class="lbl">ч</span>
                        </div>

                        <div class="time-block seconds">
                            <span class="num">{{ goal.minutes }}</span>
                            <span class="lbl">м</span>
                        </div>
                        <div class="time-block seconds">
                            <span class="num">{{ goal.seconds }}</span>
                            <span class="lbl">с</span>
                        </div>
                    </div>
                </div>
            </div>



            <div v-else class="overlay">
                <div class="glass-card empty-goal">

                    <h2 class="title">
                        Пока нет цели
                    </h2>

                    <p class="label">
                        Добавьте цель в профиле и отслеживайте,
                        сколько времени осталось до её достижения.
                    </p>

                </div>
            </div>
        </div>
        <div class="analytics-wrapper">
            <ChartsForAnalytics />
            <Last_days_hours_of_todos />
        </div>
    </div>
</template>
<style scoped>
.empty-goal{
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;

    min-height:180px;
    text-align:center;
}

.empty-goal .title{
    margin-bottom:10px;
    font-size:28px;
}

.empty-goal .label{
    max-width:340px;
    line-height:1.6;
    font-size:15px;
    color:rgba(255,255,255,.75);
}
.main-target{
    width: 700px;

    height: 320px;
    position: relative;
    overflow: hidden;
    border-radius: 40px;
    margin-bottom: 40px;
    background-image: url('@/assets/MainTarget/mountains.png');
    background-position: center;
    background-size: cover;

    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2), 0 2px 4px -1px rgba(0,0,0,0.3);
    border: 1px solid #c1c1c1;
}
.main-wrapper{
    margin: 50px;
    width: 58vw;
}
.analytics-wrapper {
    display: flex;
    margin: 0;
    gap: 16px;
}
.overlay{
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* glass */
.glass-card{
    padding: 32px 40px;
    border-radius: 28px;
    width: 200px;
    background: rgba(25, 25, 25, 0.28);
    border: 1px solid rgba(255, 255, 255, 0.22);
    backdrop-filter: blur(18px);
    margin-right: auto;
    margin-left: 40px;
    color: white;
    text-align: center;

    min-width: 460px;
}

/* текст */
.label{
    font-size: 13px;
    opacity: 0.75;
    margin-bottom: 8px;
    letter-spacing: 0.6px;
}

.title{
    font-size: 22px;
    margin-bottom: 14px;
    font-weight: 600;
}

.remaining-title{
    font-size: 24px;
    letter-spacing: 1.5px;
    opacity: 0.8;
    margin-bottom: 4px;
}

/* ===== COUNTER (ROW STYLE) ===== */
.counter{
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 14px;
    flex-wrap: wrap;
}

/* блок времени — В РЯД */
.time-block{
    gap: 5px;
    min-width: 58px;
    padding: 6px 9px;
    border-radius: 12px;
}

.time-block:hover{
    transform: translateY(-2px);
}

/* число */
.num{
    font-size: 26px;
    font-weight: 700;
    color: #ffd36a;
    line-height: 1;
}

/* буква */
.lbl{
    font-size: 14px; /* 🔥 увеличил, иначе теряется в row */
    opacity: 0.85;
    letter-spacing: 1.4px;
    transform: translateY(-1px); /* лёгкое выравнивание по базовой линии */
}

/* секунды */
.seconds .num{
    font-size: 22px;
    color: #ffffff;
    opacity: 0.9;
}
</style>