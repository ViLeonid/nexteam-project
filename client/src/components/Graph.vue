<template>
    <div class="roadmap">
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
        <VueFlow v-model:nodes="nodes" v-model:edges="edges" fit-view :fit-view-options="{padding: 0.25}" :default-viewport="{
            x: 700,
            y: 100,
            zoom: 0.8
        }">
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
        <div v-if="selectedTopic" class="panel">
            <h3>{{ selectedTopic.name }}</h3>
            <div class="info">
                <p>Всего времени: <b>{{ selectedTopic.hours }} часов</b></p>
                <p>Последняя сессия: <br>3 дня назад</p>
                <p>Количество занятий: <br>8</p>
            </div>
            <button>Начать Focus по этой теме</button>
        </div>
    </div>
</template>
<script setup>
import { ref, onMounted, watch } from "vue"
import { VueFlow } from "@vue-flow/core"
import api from "@/api"
import "@vue-flow/core/dist/style.css"


const subject = ref();
const subjects = ref([]);


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
TREE LAYOUT
========================
*/


const NODE_WIDTH = 200
const NODE_HEIGHT = 120

const GAP_X = 20
const GAP_Y = 180



function calculateWidth(node) {

    if (!node.children || node.children.length === 0) {
        return NODE_WIDTH
    }


    return node.children.reduce(
        (sum, child) => sum + calculateWidth(child),
        0
    )
        +
        GAP_X * (node.children.length - 1)

}





function createGraphLayout(
    node,
    parent = null,
    depth = 0,
    left = 0
) {


    const width = calculateWidth(node)



    const x =
        left + width / 2 - NODE_WIDTH / 2


    const y =
        depth * NODE_HEIGHT * 2



    nodes.value.push({

        id: String(node.id),

        type: node.type ,

        position: {
            x,
            y
        },

        data: node

    })



    if (parent) {


        edges.value.push({

            id: `${parent}-${node.id}`,

            source: String(parent),

            target: String(node.id),

            type: "smoothstep",

            style: {
                stroke: "#64748b",
                strokeWidth: 3
            }

        })

    }



    if (node.children) {


        let childLeft = left


        node.children.forEach(child => {


            createGraphLayout(
                child,
                node.id,
                depth + 1,
                childLeft
            )


            childLeft += calculateWidth(child) + GAP_X


        })


    }


}




function buildGraph(data) {

    nodes.value = []
    edges.value = []

    const tree = buildTree(data)

    tree.forEach(root => {

        const totalWidth = calculateWidth(root)

        createGraphLayout(

            root,

            null,

            0,

            -totalWidth / 2

        )

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

onMounted (() => {
    getSubjects()
})
</script>

<style scoped>
.roadmap {

    height: 85vh;
    width: 100%;

    position: relative;

    background:
        radial-gradient(circle,
            #374151 1px,
            transparent 1px);

    background-size: 30px 30px;

    background-color: #111827;

    border-radius: 14px;

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
    min-height: 110px;}


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
    opacity: .45;
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

.panel {
    position: absolute;
    right: 20px;
    top: 20px;
    width: 280px;
    background: #1f2937;
    color: white;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 10px 30px #0008;
}

.panel button {
    width: 100%;
    padding: 12px;
    margin-top: 15px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
}
</style>
