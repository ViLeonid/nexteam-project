<template>
    <div class="analytics-page">

        <div class="analytics-header">
            <h1>Аналитика</h1>
            <p>Ваш прогресс подготовки</p>
        </div>

        <div class="dashboard">

            <!-- Hero -->
            <div class="hero-card">

                <div class="hero-value">
                    {{ analytics.total_hours }} ч
                </div>

                <div class="hero-title">
                    Всего подготовки
                </div>

                <div class="hero-subtitle">
                    +{{ analytics.week_hours }} ч за последние 7 дней
                </div>

            </div>

            <!-- Правая часть -->

            <div class="mini-card">
                <div class="mini-title">
                    Любимый предмет
                </div>
                <div class="mini-value">
                    {{ analytics.favorite_subject_hours }} ч
                </div>

                <div class="mini-sub">
                    {{ analytics.favorite_subject }}
                </div>
            </div>

            <div class="mini-card">
                <div class="mini-title">
                    Решено задач
                </div>

                <div class="mini-value">
                    {{ analytics.total_tasks }}
                </div>

                <div class="mini-sub">
                    +{{ analytics.week_tasks }} за неделю
                </div>
            </div>

            <div class="mini-card">
                <div class="mini-title">
                    Изучено тем
                </div>

                <div class="mini-value">
                    {{ analytics.topics_count }}
                </div>

                <div class="mini-sub">
                    Последняя: {{ analytics.last_topic }}
                </div>
            </div>

            <div class="mini-card">
                <div class="mini-title">
                    Средняя Focus
                </div>

                <div class="mini-value">
                    {{ analytics.average_session }} мин
                </div>

                <div class="mini-sub">
                    {{ analytics.sessions_count }} сессий
                </div>
            </div>

        </div>

        <div class="topic-card">

            <div class="topic-header">
                🔥 Самая активная тема
            </div>

            <div class="topic-name">
                {{ analytics.favorite_topic }}
            </div>

            <div class="topic-hours">
                {{ analytics.favorite_topic_hours }} часов подготовки
            </div>

        </div>

        <div class="analytics-wrapper">

            <div class="chart-first">
                <ChartsForAnalytics />
            </div>

            <div class="chart-second">
                <Last_days_hours_of_todos />
            </div>

            <div class="chart-third">
                <Bar_charts />
            </div>

        </div>

    </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'
import ChartsForAnalytics from '@/components/ChartsForAnalytics/todays_time_donut.vue'
import Last_days_hours_of_todos from './ChartsForAnalytics/last_days_hours_of_todos.vue';
import Bar_charts from './ChartsForAnalytics/bar_charts.vue';

const analytics = ref({
    total_hours: 0,
    week_hours: 0,

    favorite_subject: "-",
    favorite_subject_hours: 0,

    total_tasks: 0,
    week_tasks: 0,

    topics_count: 0,
    last_topic: "-",

    favorite_topic: "-",
    favorite_topic_hours: 0,

    average_session: 0,
    sessions_count: 0
})

async function getAnalytics() {
    try {
        const response = await api.get("/api/analytics/summary")
        analytics.value = response.data
    } catch (err) {
        console.error(err)
    }
}


onMounted(() => {
    getAnalytics()
})
</script>

<style scoped>
.analytics-page{

    min-height:100vh;

    background:#080808;

    color:#f5f5f5;

    padding:40px;

}



/* ---------------- HEADER ---------------- */


.analytics-header{

    margin-bottom:40px;

}


.analytics-header h1{

    margin:0;

    font-size:56px;

    font-weight:800;

    letter-spacing:-2px;

}


.analytics-header p{

    margin-top:8px;

    color:#8b8b8b;

    font-size:18px;

}




/* ---------------- DASHBOARD ---------------- */


.dashboard{


    display:grid;

    grid-template-columns:2fr 1fr 1fr;

    grid-template-rows:170px 170px;

    gap:28px;


}




.hero-card,
.mini-card,
.topic-card,
.analytics-card{


    background:#070707;


    border:3px solid rgba(208,208,208,.9);


    border-radius:28px;


    box-shadow:

    0 0 20px rgba(136,136,136,.55),

    inset 0 0 20px rgba(136,136,136,.15);


    transition:.25s;


}



.hero-card:hover,
.mini-card:hover,
.topic-card:hover,
.analytics-card:hover{


    transform:translateY(-4px);


    box-shadow:

    0 0 35px rgba(255,255,255,.35),

    inset 0 0 25px rgba(255,255,255,.15);


}





/* ---------------- HERO ---------------- */


.hero-card{


    grid-row:1/3;


    padding:36px;


    display:flex;

    flex-direction:column;

    justify-content:center;


}



.hero-value{


    font-size:72px;

    font-weight:800;


}



.hero-title{


    margin-top:10px;

    font-size:28px;

    font-weight:600;


}



.hero-subtitle{


    margin-top:20px;

    color:#888;


}




/* ---------------- MINI CARDS ---------------- */



.mini-card{


    padding:14px;
    padding-left: 26px;


}



.mini-value{


    font-size:38px;

    font-weight:700;


}



.mini-title{


    margin-top:14px;


    color:#888;


    font-size:15px;


}



.mini-sub{


    margin-top:10px;

    color:white;

}





/* ---------------- TOPIC ---------------- */


.topic-card{


    margin-top:28px;


    padding:30px;


}



.topic-header{


    color:#888;

    margin-bottom:14px;


}



.topic-name{


    font-size:38px;

    font-weight:700;


}



.topic-hours{


    margin-top:12px;

    color:#aaa;


}





/* ---------------- CHARTS ---------------- */





.analytics-wrapper{

    display:flex;

    flex-wrap:wrap;

    gap:28px;

    margin-top:35px;

}



/* Бублик */

.chart-first{

    flex:0 0 400px;

}



/* График задач */

.chart-second{

    flex:1;

    min-width:400px;

}



/* Нижний график */

.chart-third{

    flex:1 1 100%;

}





/* адаптация */


@media(max-width:1000px){


.dashboard{

    grid-template-columns:1fr;

    grid-template-rows:auto;

}


.hero-card{

    grid-row:auto;

}


.analytics-wrapper{

    grid-template-columns:1fr;

}


.chart-second,
.chart-third{

    grid-column:auto;

}


}



</style>
