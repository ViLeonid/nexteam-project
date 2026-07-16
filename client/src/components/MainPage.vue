<template>

<div class="home-page">


    <div class="home-header">

        <h1>
            Главная
        </h1>

        <p>
            Ваша подготовка и текущие цели
        </p>

    </div>



    <div class="dashboard">


        <!-- Цель -->

        <div class="main-target">

            <div v-if="goal" class="overlay">

                <div class="glass-card">

                    <p class="label">
                        Главная цель
                    </p>


                    <h2 class="title">
                        {{ goal.title }}
                    </h2>



                    <div class="counter">


                        <div class="remaining-title">
                            Осталось:
                        </div>


                        <div class="time-block">
                            <span class="num">
                                {{ goal.days }}
                            </span>
                            <span class="lbl">
                                д
                            </span>
                        </div>


                        <div class="time-block">
                            <span class="num">
                                {{ goal.hours }}
                            </span>
                            <span class="lbl">
                                ч
                            </span>
                        </div>


                        <div class="time-block">
                            <span class="num">
                                {{ goal.minutes }}
                            </span>
                            <span class="lbl">
                                м
                            </span>
                        </div>


                        <div class="time-block">
                            <span class="num">
                                {{ goal.seconds }}
                            </span>
                            <span class="lbl">
                                с
                            </span>
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




        <!-- AI -->

        <div class="ai-card">
            <div style="display: flex;">
                <div class="ai-title">
                Ежедневные задания от ИИ
            </div>
            <button @click="getAIanalytics">
                <span>⟳</span>
            </button>
            </div>



            <div class="ai-text" v-for="sentence in ai_response">
                <label v-if="sentence.text">
                    <input type="checkbox" v-model="sentence.checked">
                    <span :class="{ 'is_done': sentence.checked }">{{ sentence.text }}</span>
                </label>
            </div>




        </div>



    </div>





    <!-- Аналитика -->

    <div class="analytics-wrapper">


        <div class="chart-card donut">

            <todays_time_donut />

        </div>



        <div class="focus-card">

            <div class="focus-day">
                Сегодня
            </div>

            <div class="focus-time">

                {{ workedTime }}

                <span>/ 3ч</span>

            </div>

            <div class="progress">

                <div
                    class="progress-fill"
                    :class="{ completed: progress >= 100 }"
                    :style="{ width: progress + '%' }"
                ></div>

            </div>

            <div class="progress-percent">

                {{ progress }}%

            </div>


            <button
                class="focus-button"
                @click="$router.push('/focus')"
            >
                Начать Focus
            </button>
            <div class="sessions">

                <span class="sessions-icon">
                   <svg viewBox="0 0 24 24" fill="none"> <path d="M13 2L4 14h6l-1 8 9-12h-6l1-8z" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" /> </svg>









                </span>

                <span>
                    {{ sessions }} Focus-сессий
                </span>

            </div>


        </div>



        <div class="chart-card">

            <last_days_hours_of_todos />

        </div>



    </div>



</div>


</template>
<script setup>
import todays_time_donut from '@/components/ChartsForAnalytics/todays_time_donut.vue'
import last_days_hours_of_todos from './ChartsForAnalytics/last_days_hours_of_todos.vue';
import { ref, onMounted, computed, onBeforeUnmount } from 'vue'
import api from '@/api';

const now = ref(Date.now())

const workedSeconds = ref(0)
const goalSeconds = ref(10800)
const sessions = ref(0)
const progress = ref(0)

const goalName = ref();
const goalDate = ref();
const ai_response = ref();
let interval

onMounted(() => {
    interval = setInterval(() => {
        now.value = Date.now()
    }, 1000);
    getFocusToday();
})

onBeforeUnmount(() => {
    clearInterval(interval);
})

// загрузка событий пользователя
const fetchGoal = async () => {
    const res = await api.get('/api/profile');
    goalName.value = res.data.goal_name;
    goalDate.value = res.data.goal_date;
}

onMounted(() => {
    fetchGoal();
})
const goal = computed(() => {
    const currentTime = now.value

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
const getAIanalytics = async () => {

    const res = await api.get("/api/profile/ai_analytics")

    ai_response.value = res.data.output
}

const getFocusToday = async () => {
    const res = await api.get("/api/analytics/focus-today")

    workedSeconds.value = res.data.worked_seconds
    goalSeconds.value = res.data.goal_seconds
    sessions.value = res.data.sessions_count
    progress.value = res.data.progress
}
const workedTime = computed(() => {
    const hours = Math.floor(workedSeconds.value / 3600)
    const minutes = Math.floor((workedSeconds.value % 3600) / 60)

    return `${hours}ч ${minutes}м`
})
</script>

<style scoped>
.is_done {
  text-decoration: line-through;
  color: #888; /* Опционально: делает текст блеклым */
}

.sessions-icon{
    width:28px;
    height:28px;

    display:flex;
    align-items:center;
    justify-content:center;

    color:#f5f5f5;

    filter:drop-shadow(0 0 8px rgba(255,255,255,.35));
}

.sessions-icon svg{
    width:100%;
    height:100%;
}
.focus-card{

    width:290px;

    display:flex;
    flex-direction:column;
    align-items:center;

}

.focus-day{

    color:#8c8c8c;
    font-size:14px;
    letter-spacing:2px;
    padding-top:20px;

}

.focus-time{

    margin-top:6px;

    font-size:26px;
    font-weight:700;

}

.focus-time span{

    color:#777;
    font-size:18px;

}

.progress{

    width:100%;
    height:10px;

    margin-top:10px;

    background:#232323;

    border-radius:100px;

    overflow:visible;

}
.progress-fill{




    height:100%;

    background:#bbbbbb;

    border-radius:100px;

    position:relative;

    transition:.4s;

    /* постоянное мягкое свечение */
    box-shadow:
        0 0 10px rgba(255,255,255,.45),
        0 0 22px rgba(255,255,255,.25),
        0 0 40px rgba(255,255,255,.12);

    overflow:hidden;
    fill: drop-shadow(0 0 8px rgba(255, 255, 255, 0.6)) drop-shadow(0 0 18px rgba(255, 255, 255, 0.25))
}
.progress-fill::after{

    content:'';

    position:absolute;
    inset:0;

    background:linear-gradient(
        120deg,
        transparent 0%,
        rgba(255,255,255,.9) 45%,
        transparent 100%
    );

    transform:translateX(-120%);

    animation:progressShine 2.5s linear infinite;
}

@keyframes progressShine{

    to{
        transform:translateX(120%);
    }
}


.progress-fill.completed{

    background:#ffd86b;

    box-shadow:
        0 0 12px rgba(255,216,107,.8),
        0 0 35px rgba(255,200,70,.45),
        0 0 70px rgba(255,180,50,.25);
}

.progress-percent{

    margin-top:10px;

    color:#a0a0a0;

    font-size:14px;

}

.divider{

    width:100%;

    height:1px;

    background:#2a2a2a;

    margin:26px 0;

}

.sessions{

    font-size:20px;

    font-weight:600;
    margin: 30px;
    display:flex;
    gap:10px;
    align-items:center;

}

.sessions-icon{

    font-size:26px;

}

.focus-button{

    margin-top:30px;

}
.home-page{

    min-height:100vh;

    background:#080808;

    color:#f5f5f5;

    padding-left: 40px;
    padding-right: 40px;
}

.analytics-card{
    height: 250px;
    padding: 0;
    margin: 10px;
}
.donut .analytics-card{
    width:200px
}
/* HEADER */

.home-header{
    margin-bottom:40px;
    padding-top: 30px;
    margin-left: 10px;
}


.home-header h1{

    margin:0;

    font-size:56px;

    font-weight:800;

    letter-spacing:-2px;

}


.home-header p{

    margin-top:8px;

    color:#888;

    font-size:18px;

}



/* TOP */

.dashboard{

    display:grid;

    grid-template-columns:1.8fr 1.2fr;

    gap:28px;

}





/* ==========================
        GOAL BLOCK
========================== */


.main-target{

    height:320px;

    position:relative;

    overflow:hidden;

    border-radius:40px;

    background-image:

    linear-gradient(
        90deg,
        rgba(0,0,0,.25),
        rgba(0,0,0,.10),
        rgba(0,0,0,.01)
    ),

    url('@/assets/MainTarget/olympus.png');


    background-position:center;

    background-size:cover;



    border: 3px solid rgba(208,208,208,.9);


    box-shadow:

    0 0 20px rgba(136,136,136,.55),

    inset 0 0 20px rgba(0,0,0,.5);



}


.main-target .title{
    font-size: 32px;
}


.overlay{

    position:absolute;

    inset:0;

    display:flex;

    align-items:center;

    justify-content:center;

}



.glass-card{


    padding:32px 40px;


    border-radius:28px;


    height:200px;


    min-width:460px;



    background:

    rgba(25,25,25,.35);



    border:

    1px solid rgba(255,255,255,.22);



    backdrop-filter:blur(18px);



    margin-right:auto;

    margin-left:40px;



    color:white;


    text-align:center;



}




.label{


    font-size:13px;

    opacity:.75;

    margin-bottom:8px;

    letter-spacing:.6px;


}




.title{


    font-size:22px;

    margin-bottom:14px;

    font-weight:600;


}




.remaining-title{


    font-size:24px;

    letter-spacing:1.5px;

    opacity:.8;

    margin-bottom:4px;


}



.counter{


    display:flex;

    justify-content:center;

    align-items:center;


    margin-top:14px;

    flex-wrap:wrap;


}



.time-block{


    display:flex;

    align-items:baseline;


    gap:5px;


    min-width:58px;

    padding:6px 9px;


}



.num{


    font-size:26px;

    font-weight:700;


    color:#ffd36a;


    line-height:1;


}



.lbl{


    font-size:14px;

    opacity:.85;

    letter-spacing:1.4px;


}



.empty-goal{


    display:flex;

    flex-direction:column;


    align-items:center;

    justify-content:center;


    min-height:180px;


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





/* ==========================
        AI CARD
========================== */


.ai-card{

    position: relative;
    height:320px;


    padding:20px;


    background:#070707;


    border: 3px solid rgba(208,208,208,.9);


    border-radius:28px;



    box-shadow:


    0 0 20px rgba(136,136,136,.55),


    inset 0 0 20px rgba(136,136,136,.15);



    display:flex;

    flex-direction:column;


    transition:.25s;


}



.ai-card:hover{


    transform:translateY(-4px);



    box-shadow:


    0 0 35px rgba(255,255,255,.35),


    inset 0 0 25px rgba(255,255,255,.15);


}




.ai-title{


    font-size:28px;

    font-weight:700;
    margin-bottom: 10px;

}



.ai-text{


    margin:0px;


    flex:1;
    font-size: 15px;

    line-height:1.4;


    color:#bbb;


}




.ai-footer{
    position: absolute;
    bottom: 0;
    left: 14;
    padding:10px;
    width: 90%;

    border-top:

    1px solid #333;
    font-size: 12px;
    text-align: center;
    color:#777;


}






/* ==========================
        ANALYTICS
========================== */


.analytics-wrapper{


    margin-top:35px;


    display:flex;


    gap:28px;


    align-items:center;


}



.chart-card{


    background:#070707;


    border:

    3px solid rgba(208,208,208,.9);


    border-radius:28px;


    padding:20px;


    box-shadow:


    0 0 20px rgba(136,136,136,.55),


    inset 0 0 20px rgba(136,136,136,.15);



}



.chart-card:first-child{


    flex:0 0;


}



.chart-card:last-child{


    flex:1;


}




.focus-button{


    width:260px;

    height:80px;


    border-radius:24px;


    border:none;


    background:white;


    color:black;


    font-size:20px;


    font-weight:700;


    cursor:pointer;


    transition:.25s;


}



.focus-button:hover{


    transform:translateY(-4px);


    box-shadow:

    0 0 25px white;


}





@media(max-width:1000px){


.dashboard{

    grid-template-columns:1fr;

}



.analytics-wrapper{

    flex-direction:column;

}


}
/* ==========================
        AI REFRESH BUTTON
========================== */

.ai-card button {

    width:40px;
    height:40px;

    display:flex;
    align-items:center;
    justify-content:center;

    margin-left:auto;

    border-radius:20px;

    border:1px solid rgba(255,255,255,.25);

    background:
    rgba(255,255,255,.06);

    color:#fff;

    font-size:22px;

    padding:0;

    cursor:pointer;

    backdrop-filter:blur(10px);

    transition:.25s;

    box-shadow:
    0 0 12px rgba(255,255,255,.15),
    inset 0 0 10px rgba(255,255,255,.08);

}




.ai-card button span {

    display:flex;

    align-items:center;
    justify-content:center;

    line-height:1;

    transform:translateY(-2px);

}

.ai-card button:active {

    transform:rotate(180deg) scale(.95);

}



/* ==========================
        AI CHECKBOX
========================== */


.ai-text label {

    display:flex;

    align-items:flex-start;

    gap:12px;

    cursor:pointer;

    margin-bottom:6px;

    color:#c5c5c5;

    transition:.25s;

}



.ai-text label:hover {

    color:white;

}



/* скрываем стандартный checkbox */

.ai-text input {

    appearance:none;

    -webkit-appearance:none;

    width:20px;

    height:20px;

    flex-shrink:0;

    margin-top:2px;

    border-radius:7px;

    border:1px solid rgba(255,255,255,.35);

    background:#111;

    cursor:pointer;

    position:relative;

    transition:.25s;

}



/* состояние hover */

.ai-text input:hover {

    border-color:white;

    box-shadow:
    0 0 10px rgba(255,255,255,.35);

}



/* галочка */

.ai-text input:checked {

    background:#ffd86b;

    border-color:#ffd86b;

    box-shadow:

    0 0 12px rgba(255,216,107,.7),

    0 0 25px rgba(255,216,107,.35);

}



.ai-text input:checked::after {

    content:"";

    position:absolute;

    left:50%;
    top:50%;

    width:5px;

    height:10px;

    border-right:2px solid #111;

    border-bottom:2px solid #111;

    transform:
        translate(-50%, -60%)
        rotate(45deg);

}



/* текст выполненной цели */

.ai-text span {

    transition:.3s;

}



.ai-text .is_done {

    color:#666;

    text-decoration:line-through;

    opacity:.7;

}


</style>

