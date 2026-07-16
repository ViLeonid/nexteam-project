<template>
    <div class="roadmap" ref="roadmap">
        <!-- HEADER -->
        <div class="header">
            <select v-model="subject">
                <option
                    v-for="s in subjects"
                    :key="s.id"
                    :value="s.name"
                >
                    {{ s.name }}
                </option>
            </select>
            <p>Карта подготовки</p>
        </div>
        <VueFlow
            v-model:nodes="nodes"
            v-model:edges="edges"
            :nodes-draggable="false"
            :min-zoom="0.2"
            :max-zoom="2"
        >
            <!-- NODE -->
            <template #node-subject="{ data }">
                <div
                    class="topic-card subject"
                    @click="openTopic(data)"
                >
                    <div class="title">
                        {{ data.name }}
                    </div>
                </div>
            </template>


            <template #node-section="{ data }">
                <div
                    class="topic-card section"
                    @click="openTopic(data)"
                >
                    <div class="title">
                        {{ data.name }}
                    </div>

                    <div class="hours">
                        {{ data.hours }} часов
                    </div>
                </div>
            </template>


            <template #node-topic="{ data }">
                <div
                    class="topic-card topic"
                    :class="getProgressClass(data.hours)"
                    @click="openTopic(data)"
                >
                    <div class="title">
                        {{ data.name }}
                    </div>

                    <div class="hours">
                        {{ data.hours }} часов
                    </div>

                    <div class="level">
                        Lv.{{ getLevel(data.hours) }}
                    </div>

                    <div class="progress">
                        <div
                            class="progress-fill"
                            :style="{ width:getProgress(data.hours)+'%' }"
                        />
                    </div>
                </div>
            </template>

            <template #node-subtopic="{ data }">
                <div
                    class="topic-card subtopic"
                    :class="getProgressClass(data.hours)"
                    @click="openTopic(data)"
                >
                    <div class="title">
                        {{ data.name }}
                    </div>

                    <div class="hours">
                        {{ data.hours }} часов
                    </div>

                    <div class="level">
                        Lv.{{ getLevel(data.hours) }}
                    </div>

                    <div class="progress">
                        <div
                            class="progress-fill"
                            :style="{ width:getProgress(data.hours)+'%' }"
                        />
                    </div>
                </div>
            </template>
        </VueFlow>

        <!-- SIDE PANEL -->
        <div
            v-if="selectedTopic"
            class="panel"
        >

            <div class="panel-header">

                <h3>{{ selectedTopic.name }}</h3>

                <span class="level">
                    Lv. {{ getLevel(selectedTopic.hours) }}
                </span>

            </div>

            <div class="progress-block">

                <div class="progress-header">

                    <span>Освоение</span>

                    <b>{{ Math.round(getProgress(selectedTopic.hours)) }}%</b>

                </div>

                <div class="progress">

                    <div
                        class="progress-fill"
                        :style="{ width: getProgress(selectedTopic.hours) + '%' }"
                    ></div>

                </div>

            </div>

            <div class="stats">

                <div class="stat">

                    <span class="label">
                        Время изучения
                    </span>

                    <span class="value">
                        {{ selectedTopic.hours }} часов
                    </span>

                </div>

                <div class="stat">

                    <span class="label">
                        Последняя сессия
                    </span>

                    <span class="value">
                        {{formatLastDate(selectedTopic.last_date)}}
                    </span>

                </div>

                <div class="stat">

                    <span class="label">
                        Количество занятий
                    </span>

                    <span class="value">
                        {{ selectedTopic.sessions }}
                    </span>

                </div>

            </div>

            <!-- <div class="materials">

                <div class="materials-title">
                    Материалы
                </div>

                <div class="material">
                    <span>Лекция</span>
                </div>

                <div class="material">
                    <span>Конспект</span>
                </div>

                <div class="material">
                    <span>Практические задачи</span>
                </div>

            </div> -->

            <button class="focus-btn" @click="goToFocus">

                Начать Focus

            </button>

        </div>
    </div>
</template>
<script setup>
import { ref, onMounted, watch } from "vue"
import { VueFlow, useVueFlow } from "@vue-flow/core"
import api from "@/api"
import "@vue-flow/core/dist/style.css"

import { useRouter } from 'vue-router'


const subject = ref();
const subjects = ref([]);
const roadmap = ref();
const { setViewport } = useVueFlow()
const router = useRouter()


const goToFocus = () => {
    console.log('subject:', subject.value)
    console.log('topic:', selectedTopic.value.name)

    router.push({
        path: '/focus',
        query: {
            subject: subject.value,
            topic: selectedTopic.value?.name || ''
        }
    })
}

function formatLastDate(lastDate) {
    if (!lastDate) return "-"

    const now = new Date()
    const date = new Date(lastDate)

    const diffMs = now - date

    const minutes = Math.floor(diffMs / (1000 * 60))
    const hours = Math.floor(diffMs / (1000 * 60 * 60))
    const days = Math.floor(diffMs / (1000 * 60 * 60 * 24))

    if (minutes < 1) return "Только что"
    if (minutes < 60) return `${minutes} мин назад`
    if (hours < 24) return `${hours} ч назад`
    if (days === 1) return "1 день назад"
    if (days <= 4) return `${days} дня назад`
    return `${days} дней назад`
}
async function loadGraph() {

    try {

        const res = await api.get(
            `/api/graph/${subject.value}/progress`
        )

        console.log(res)
        console.log(res.data)

        buildGraph(res.data)

    } catch (err) {

        console.error(err)

    }

}
watch(subject, () => {
    loadGraph()
})
function getLevel(hours) {

    if (hours < 5)
        return 1

    if (hours < 20)
        return 2

    if (hours < 40)
        return 3

    if (hours < 80)
        return 4

    return 5

}


function buildTree(topics) {

    const map = {}

    topics.forEach(topic => {

        map[topic.id] = {
            ...topic,
            children: []
        }

    })

    const roots = []

    topics.forEach(topic => {

        if (topic.parent_id) {

            map[topic.parent_id].children.push(
                map[topic.id]
            )

        }

        else {

            roots.push(map[topic.id])

        }

    })

    return roots

}

const selectedTopic = ref(null)


/*
========================
TEST DATA
========================
*/


const nodes = ref([])
const edges = ref([])



/*
========================
CENTER GRAPH BUILDER
========================
*/
/*
========================
RADIAL TREE LAYOUT
========================
*/


const NODE_RADIUS = {
    subject: 0,
    section: 400,
    topic: 800,
    subtopic: 1200
}



function getRadius(node){

    if(node.type === "subject")
        return NODE_RADIUS.subject

    if(node.type === "section")
        return NODE_RADIUS.section

    if(node.type === "topic")
        return NODE_RADIUS.topic

    return NODE_RADIUS.subtopic

}



function countLeaves(node){

    if(!node.children || node.children.length === 0)
        return 1


    return node.children
        .map(countLeaves)
        .reduce((a,b)=>a+b,0)

}




function createRadialLayout(
    node,
    parent=null,
    startAngle=0,
    endAngle=Math.PI*2
){


    const radius = getRadius(node)


    const angle =
        (startAngle + endAngle) / 2



    nodes.value.push({

        id:String(node.id),

        type:node.type,

        position:{

            x:
                Math.cos(angle)
                *
                radius,


            y:
                Math.sin(angle)
                *
                radius

        },


        data:node

    })





    if(parent){


        edges.value.push({

            id:`${parent}-${node.id}`,

            source:String(parent),

            target:String(node.id),

            type:"smoothstep",

            style:{

                stroke:"#64748b",

                strokeWidth:3

            }

        })

    }





    if(!node.children ||
        node.children.length===0)

        return





    const total =
        node.children
        .map(countLeaves)
        .reduce(
            (a,b)=>a+b,
            0
        )




    let current=startAngle





    node.children.forEach(child=>{


        const sector =
            (endAngle-startAngle)
            *
            countLeaves(child)
            /
            total




        createRadialLayout(

            child,

            node.id,

            current,

            current+sector

        )



        current += sector



    })

}






function buildGraph(data){


    nodes.value=[]

    edges.value=[]



    const tree =
        buildTree(data)



    tree.forEach(root=>{


        createRadialLayout(

            root,

            null,

            0,

            Math.PI*2

        )


    })
    setViewport({
        x: roadmap.value.clientWidth / 2 - 50,
        y: roadmap.value.clientHeight / 2 - 30,
        zoom: 0.5
    })

}

/*
========================
PROGRESS
========================
*/


function getProgress(hours) {

    return Math.min(hours / 40 * 100, 100)

}


function getProgressClass(hours) {

    if (hours === 0)
        return "empty"


    if (hours < 5)
        return "low"


    if (hours < 20)
        return "medium"


    return "high"

}

const getSubjects = () => {
    api.get('api/get_subjects').then(res => {
        subjects.value = res.data.subjects
        subject.value = subjects.value[0].name
    })
}

function openTopic(topic) {
    selectedTopic.value = topic
}

onMounted(() => {

    getSubjects()

})
</script>

<style scoped>
.roadmap {

    height: 100%;
    width: 100%;

    position: relative;

    background:
        radial-gradient(circle,
            #374151 1px,
            transparent 1px);

    background-size: 30px 30px;

    background-color: #111827;


    overflow: hidden;

}

.header {
    position: absolute;
    z-index: 10;
    top: 20px;
    left: 20px;
    background: #111827dd;
    padding: 15px 20px;
    border-radius: 12px;
    color: white;
}

.header h2 {
    margin: 0;
}

.header p {
    margin: 5px 0 0;
    opacity: .7;
}

.subject {
    border:2px solid #ff3131;
    background: #1f2937;
    width: 200px;
    min-height: 110px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.subject .title {
    font-size: 25px !important;
    text-align: center;
    width: 100%;
}


.section {
    border:2px solid #fff131;
    background: #1f2937;
    width: 200px;
    min-height: 110px;
}


.topic {
    background: #1f2937;
    border: 2px solid #374151;
    width: 200px;
    min-height: 110px;
}


.subtopic {
    background: #39393a;
    border: 2px solid #1d1d1d;
    font-size: 2px;
    width: 150px;
    min-height: 60px;
    opacity:.8;
}

.topic-card {
    border-radius: 12px;
    padding: 12px;
    color: white;
    cursor: pointer;
    transition: .2s;
}

.topic-card:hover {
    transform: translateY(-4px);
}

.title {

    font-weight:700;
    font-size:15px;

    white-space:normal;

    line-height:1.2;

}

.hours {
    font-size: 13px;
    margin-top: 8px;
    opacity: .8;
}

.level {
    font-size: 13px;
    margin-top: 5px;
    min-width: 30px;
}

.progress {
    height: 6px;
    background: #111;
    border-radius: 10px;
    margin-top: 12px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: #22c55e;
}

.empty {
    border-color: #484c4c;
}

.low {
    border-color: #64748b;
}

.medium {
    border-color: #38bdf8;
}

.high {
    border-color: #22c55e;
    box-shadow: 0 0 15px #22c55e55;
}
/* ===========================
   SIDE PANEL
=========================== */

.panel{

    position:absolute;

    top:20px;
    right:20px;

    width:330px;

    padding:24px;

    background:#1f2937;

    border:1px solid #374151;

    border-radius:16px;

    color:#fff;

    box-shadow:
        0 15px 35px rgba(0,0,0,.35);

    z-index:20;

}

/* ===========================
   HEADER
=========================== */

.panel-header{

    display:flex;

    justify-content:space-between;

    align-items:flex-start;

    gap:20px;

}

.panel-header h3{

    margin:0;

    font-size:22px;

    font-weight:700;

    line-height:1.3;

}

.level{

    color:#94a3b8;

    font-size:12px;

    font-weight:600;

}

/* ===========================
   PROGRESS
=========================== */

.progress-block{

    margin-top:24px;

}

.progress-header{

    display:flex;

    justify-content:space-between;

    align-items:center;

    margin-bottom:10px;

}

.progress-header span{

    color:#94a3b8;

    font-size:13px;

}

.progress-header b{

    font-size:15px;

}

.progress{

    height:8px;

    background:#111827;

    border-radius:999px;

    overflow:hidden;

}

.progress-fill{

    height:100%;

    background:#4fdd39;

    border-radius:999px;

    transition:.3s;

}

/* ===========================
   STATS
=========================== */

.stats{

    margin-top:26px;

    border-top:1px solid #374151;

}

.stat{

    display:flex;

    justify-content:space-between;

    align-items:center;

    padding:16px 0;

    border-bottom:1px solid #374151;

}

.label{

    color:#94a3b8;

    font-size:13px;

}

.value{

    font-size:15px;

    font-weight:600;

    color:#fff;

}

/* ===========================
   MATERIALS
=========================== */

.materials{

    margin-top:24px;

}

.materials-title{

    margin-bottom:14px;

    font-size:15px;

    font-weight:600;

}

.material{

    padding:12px 14px;

    margin-bottom:10px;

    background:#111827;

    border:1px solid #374151;

    border-radius:10px;

    color:#cbd5e1;

    font-size:14px;

    transition:.2s;

}

.material:hover{

    background:#172036;

    border-color:#2563EB;

}

/* ===========================
   BUTTON
=========================== */

.focus-btn{

    width:100%;

    margin-top:26px;

    height:46px;

    border:none;

    border-radius:10px;

    background:#2563EB;

    color:#fff;

    font-size:15px;

    font-weight:600;

    cursor:pointer;

    transition:.2s;

}

.focus-btn:hover{

    background:#1d4ed8;

}

.focus-btn:active{

    transform:scale(.98);

}
</style>
