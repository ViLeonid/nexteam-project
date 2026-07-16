<template>
<div class="profile-page">

    <div class="page-header">
        <h1>ПРОФИЛЬ</h1>
        <p>Настройки аккаунта и подготовки</p>
    </div>

    <div class="settings-grid">

        <!-- Цель -->

        <section class="settings-card">

            <h2>Цель подготовки</h2>

            <template v-if="!editGoalMode">

                <div class="info-block">

                    <span class="label">
                        Текущая цель
                    </span>

                    <div class="goal_value" v-if="!goalName">
                        Поставьте себе цель, чтобы знать, куда двигаться
                    </div>
                    <div class="value">
                        {{ goalName }}
                    </div>

                    <div class="secondary">
                        {{ goalDate }}
                    </div>
                </div>

                <button @click="EditGoal">
                    Изменить цель
                </button>

            </template>

            <template v-else>

                <div class="field">

                    <label>Название цели</label>

                    <input
                        v-model="goalName"
                        class="password-input"
                        placeholder="Например: ВСОШ 2027"
                    >

                </div>

                <div class="field">

                    <label>Дата</label>

                    <input
                        type="date"
                        v-model="goalDate"
                        class="password-input"
                    >

                </div>

                <div class="goal-buttons">

                    <button @click="SaveGoal">
                        Сохранить
                    </button>

                    <button
                        class="cancel-btn"
                        @click="CancelGoalEdit"
                    >
                        Отмена
                    </button>

                </div>

            </template>

        </section>
        <!-- Предметы -->

        <section class="settings-card">

            <h2>Предметы</h2>

            <div
                v-if="loadingSubjects"
                class="loading"
            >
                Загрузка...
            </div>

            <template v-else>

                <div
                    v-if="subjects.length"
                    class="subjects"
                >

                    <div
                        class="subject"
                        v-for="item in subjects"
                        :key="item.id"
                    >

                        <span>
                            {{ item.name }}
                        </span>

                        <button
                            class="delete-btn"
                            @click="DeleteSubject(item.id)"
                        >
                            ✕
                        </button>

                    </div>

                </div>

                <div
                    v-else
                    class="empty"
                >
                    Пока нет добавленных предметов
                </div>

            </template>

            <div class="add-subject">
                <select v-model="newSubject">
                    <option
                        v-for="s in all_subjects"
                        :key="s.id"
                        :value="s.name"
                    >
                        {{ s.name }}
                    </option>
                </select>


                <button
                    class="add-btn"
                    @click="AddSubject"
                >
                    +
                </button>

            </div>

        </section>

        <!-- Focus -->

        <section class="settings-card">

            <h2>Настройки Focus</h2>

            <div class="setting-row">

                <span>
                    Время работы
                </span>

                <input
                    type="number"
                    min="1"
                    v-model="focusTime"
                    class="small-input"
                >

            </div>

            <div class="setting-row">

                <span>
                    Перерыв
                </span>

                <input
                    type="number"
                    min="1"
                    v-model="breakTime"
                    class="small-input"
                >

            </div>

            <div class="setting-row">

                <span>
                    Автозапуск
                </span>

                <div
                    class="toggle"
                    :class="{ active: autoStart }"
                    @click="autoStart = !autoStart"
                >
                    <div class="circle"></div>
                </div>

            </div>

            <button
                class="save-btn"
                @click="SaveFocus"
            >
                Сохранить
            </button>

        </section>

        <!-- Аккаунт -->

        <section class="settings-card">
            <h2>Аккаунт</h2>
            <div class="account-wrapper">


                <div>


                    <div class="field">

                        <label>Логин</label>

                        <div>
                            {{ login }}
                        </div>

                    </div>

                    <div class="field">

                        <label>Пароль</label>

                        <div class="password-preview">
                            ••••••••••••
                        </div>

                    </div>
                    <button
                        @click="ChangePassword"
                    >
                        {{ changePasswordMode ? "Отмена" : "Изменить пароль" }}
                    </button>
                </div>



                <div v-if="changePasswordMode">

                    <div class="field">

                        <label>
                            Текущий пароль
                        </label>

                        <input
                            type="password"
                            v-model="currentPassword"
                            placeholder="Введите текущий пароль"
                            class="password-input"
                        >

                    </div>


                    <div class="field">

                        <label>
                            Новый пароль
                        </label>

                        <input
                            type="password"
                            v-model="newPassword"
                            placeholder="Введите новый пароль"
                            class="password-input"
                        >

                    </div>


                    <button @click="SavePassword">
                        Сохранить пароль
                    </button>

                </div>
            </div>



        </section>

    </div>

</div>
</template>
<script setup>
import { ref, onMounted } from "vue";
import { useToast } from "vue-toastification"
import api from "@/api";

/* -------------------- Данные -------------------- */

const loadingSubjects = ref(false);

const subjects = ref([]);
const all_subjects = ref([]);
const newSubject = ref("");
const toast = useToast();
const changePasswordMode = ref(false);

const currentPassword = ref("");
const newPassword = ref("");
const login = ref("");

const focusTime = ref(25);
const breakTime = ref(5);
const autoStart = ref(true);
const editGoalMode = ref(false);

const goalName = ref();
const goalDate = ref();

/* -------------------- Загрузка профиля -------------------- */

const GetProfile = async () => {

    try {

        const res = await api.get("/api/profile");

        goalName.value = res.data.goal_name;

        goalDate.value = res.data.goal_date;

        console.log(goalDate.value)

        login.value = res.data.login;
        focusTime.value = res.data.focus_time ?? focusTime.value;
        breakTime.value = res.data.break_time ?? breakTime.value;
        autoStart.value = res.data.auto_start ?? autoStart.value;

    }
    catch (err) {

        console.error("Ошибка загрузки профиля", err);

    }

};

const EditGoal = () => {
    editGoalMode.value = true;
};

const CancelGoalEdit = () => {
    editGoalMode.value = false;
};

const SaveGoal = () => {
    api.post("/api/profile/change_goal", {name: goalName.value, date: goalDate.value}).then(() =>{
        GetProfile();
        CancelGoalEdit();
    })
}
/* -------------------- Предметы -------------------- */

const GetSubjects = async () => {

    loadingSubjects.value = true;

    try {

        const res = await api.get("/api/profile/get_subjects");

        subjects.value = Array.isArray(res.data.subjects)
            ? res.data.subjects
            : [];

    }
    catch (err) {

        console.error("Ошибка получения предметов", err);

        subjects.value = [];

    }
    finally {

        loadingSubjects.value = false;

    }

};

const AddSubject = async () => {

    const value = newSubject.value.trim();

    if (!value)
        return;


    const exists = subjects.value.some(
        item => item.name.toLowerCase() === value.toLowerCase()
    );


    if (exists) {
        toast.error("Такой предмет уже добавлен!", {
            toastClassName: "nexteam-toast",
            bodyClassName: "nexteam-toast-body",
            hideProgressBar: false,
        });
        return;
    }


    try {

        const res = await api.post(
            "/api/profile/add_subject",
            {
                subject: value
            }
        );


        subjects.value.push(res.data.subject);


        newSubject.value = "";

    }
    catch (err) {

        console.error(
            "Ошибка добавления предмета",
            err
        );

    }

};

const DeleteSubject = async (id) => {

    try {

        await api.delete(`/api/profile/delete_subject/${id}`);

        subjects.value = subjects.value.filter(
            item => item.id !== id
        );

    }
    catch (err) {

        console.error("Ошибка удаления предмета", err);

    }

};

/* -------------------- Focus -------------------- */

const SaveFocus = async () => {

    try {

        await api.post("/api/profile/save_focus", {

            focus_time: Number(focusTime.value),

            break_time: Number(breakTime.value),

            auto_start: autoStart.value

        });

    }
    catch (err) {

        console.error("Ошибка сохранения Focus", err);

    }

};

/* -------------------- Заглушки -------------------- */


const ChangePassword = () => {
    changePasswordMode.value = !changePasswordMode.value;
};




const SavePassword = async () => {
  try {
    const response = await api.post('/api/profile/change_password', {
      currentPassword: currentPassword.value,
      newPassword: newPassword.value
    })
    ChangePassword();
    toast.success("Пароль изменён", {
            toastClassName: "nexteam-toast",
            bodyClassName: "nexteam-toast-body",
            hideProgressBar: false,
        });
  } catch (err) {
    toast.error(err.response?.data?.error || 'Произошла ошибка', {
            toastClassName: "nexteam-toast",
            bodyClassName: "nexteam-toast-body",
            hideProgressBar: false,
        });
  }
}

const getAllSubjects = () => {
    api.get('/api/get_all_subjects').then(res => {
        all_subjects.value = res.data.subjects
    })
}

/* -------------------- Init -------------------- */

onMounted(async () => {

    await Promise.all([
        GetProfile(),
        GetSubjects(),
        getAllSubjects()
    ]);

});
</script>
<style scoped>
.goal-buttons{
    gap: 20px;
    display: flex;
}
.goal_value{
    margin-top:16px;
    padding:18px 20px;

    border:2px dashed rgba(255,255,255,.18);
    border-radius:16px;

    background:linear-gradient(
        180deg,
        rgba(255,255,255,.03),
        rgba(255,255,255,.01)
    );

    color:#a7a7a7;
    font-size:16px;
    line-height:1.6;
    text-align:center;

    transition:.25s;
}


.profile-page{
    min-height:100vh;
    background:#080808;
    color:#f5f5f5;
    padding:40px;
}

.page-header{
    margin-bottom:40px;
}

.page-header h1{
    margin:0;
    font-size:56px;
    font-weight:800;
    letter-spacing:-2px;
}

.page-header p{
    margin-top:8px;
    color:#8b8b8b;
    font-size:18px;
}

.settings-grid{
    display:grid;
    grid-template-columns:repeat(2,1fr);
    gap:28px;
}

.settings-card{
    padding:32px;
    background:#070707;

    border:3px solid rgba(208,208,208,.9);
    border-radius:28px;

    box-shadow:
        0 0 20px rgba(136,136,136,.65),
        inset 0 0 20px rgba(136,136,136,.25);
}

.settings-card h2{
    margin:0 0 28px;
    font-size:22px;
    font-weight:600;
}

.info-block{
    margin-bottom:28px;
}

.label{
    color:#777;
    font-size:14px;
}

.value{
    margin-top:12px;
    font-size:26px;
    font-weight:600;
}

.secondary{
    margin-top:8px;
    color:#999;
}

/* ---------------- Кнопки ---------------- */

button{
    background:#fff;
    color:#111;
    border:none;
    padding:14px 22px;
    border-radius:12px;
    cursor:pointer;
    font-size:15px;
    transition:.25s;
}

button:hover{
    opacity:.9;
    transform:translateY(-2px);
}

/* ---------------- Предметы ---------------- */

.subjects{
    display:flex;
    flex-direction:column;
    gap:14px;
    margin-bottom:22px;
}

.subject{
    display:flex;
    justify-content:space-between;
    align-items:center;

    padding:16px;

    border:2px solid rgba(105,105,105,.8);
    border-radius:14px;

    transition:.25s;
}

.subject:hover{
    border-color:white;
    transform:translateY(-2px);
}

.delete-btn{
    width:34px;
    height:34px;

    padding:0;

    border:none;

    background:transparent;

    color:#888;

    font-size:18px;

    border-radius:8px;
}

.delete-btn:hover{
    background:#181818;
    color:#ff6666;
}

/* ---------------- Добавление предмета ---------------- */

.add-subject{
    display:flex;
    gap:12px;
    margin-top:10px;
}

.add-subject select{
    flex:1;

    background:#0b0b0b;
    color:white;

    border:2px solid rgba(105,105,105,.8);

    border-radius:14px;

    padding:14px 16px;

    outline:none;

    font-size:15px;

    cursor:pointer;

    appearance:none;

    transition:.25s;

    background-image:
        linear-gradient(45deg, transparent 50%, white 50%),
        linear-gradient(135deg, white 50%, transparent 50%);

    background-position:
        calc(100% - 20px) 50%,
        calc(100% - 15px) 50%;

    background-size:
        6px 6px,
        6px 6px;

    background-repeat:no-repeat;
}


.add-subject select:hover{
    border-color:white;
}


.add-subject select:focus{
    border-color:white;
    box-shadow:0 0 10px rgba(255,255,255,.25);
}


.add-subject option{
    background:#0b0b0b;
    color:white;
    padding:12px;
}
.add-btn{
    width:68px;
    height:68px;

    display:flex;
    align-items:center;
    justify-content:center;

    padding-top: 6px;

    font-size:42px;
    font-weight:500;

    line-height:1;

}

/* ---------------- Focus ---------------- */

.setting-row{
    display:flex;
    justify-content:space-between;
    align-items:center;

    padding:18px 0;

    border-bottom:1px solid #222;
}

.setting-row:last-child{
    border-bottom:none;
}

.small-input{
    width:90px;

    background:#0b0b0b;
    color:white;

    border:2px solid rgba(105,105,105,.8);

    border-radius:12px;

    padding:10px;

    text-align:center;
}

.small-input:focus{
    outline:none;
    border-color:white;
}

.save-btn{
    margin-top:24px;
    width:100%;
}

/* ---------------- Toggle ---------------- */

.toggle{
    width:54px;
    height:28px;

    background:#333;

    border-radius:999px;

    cursor:pointer;

    position:relative;

    transition:.25s;
}

.circle{
    position:absolute;

    left:3px;
    top:3px;

    width:22px;
    height:22px;

    border-radius:50%;
    background:white;

    transition:.25s;
}

.toggle.active{
    background:rgb(173, 173, 173);
}

.toggle.active .circle{
    left:29px;
}

/* ---------------- Аккаунт ---------------- */

/* ---------------- Аккаунт ---------------- */

.account-wrapper{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:40px;
    align-items:start;
}


.account-wrapper > div{
    min-width:0;
}


.field{
    margin-bottom:20px;
}


.field label{
    display:block;
    margin-bottom:8px;
    color:#777;
    font-size:14px;
    font-weight:500;
}


.field div{

    font-size:18px;

    color:#eee;

    padding:6px 0;

    font-weight:500;

}


/* визуально показываем пароль как скрытое значение */

.password-preview{
    color:#888;
    font-size:24px;
    letter-spacing:4px;
}
/* пароль скрытый блок */

.account-wrapper .field div:not(:last-child){

    letter-spacing:1px;

}


/* поля ввода */


.password-input{

    width:100%;

    height:46px;

    box-sizing:border-box;


    background:#0b0b0b;

    color:white;


    border:1px solid rgba(255,255,255,.15);

    border-radius:12px;


    padding:0 14px;

    font-size:14px;

    letter-spacing:2px;
}


.password-input:focus{

    outline:none;

    border-color:white;

}



/* кнопки аккаунта */

.account-wrapper button{

    width:100%;

    margin-top:5px;

}


/* адаптация */

@media(max-width:900px){

    .account-wrapper{

        grid-template-columns:1fr;

        gap:25px;

    }

}

/* ---------------- Loading ---------------- */

.loading{
    text-align:center;
    color:#999;
    padding:25px;
}

/* ---------------- Empty ---------------- */

.empty{
    text-align:center;

    padding:28px;

    color:#777;

    border:2px dashed #444;

    border-radius:14px;

    margin-bottom:20px;
}

/* ---------------- Scroll ---------------- */

::-webkit-scrollbar{
    width:8px;
}

::-webkit-scrollbar-thumb{
    background:#444;
    border-radius:10px;
}

/* ---------------- Responsive ---------------- */

@media(max-width:900px){

    .settings-grid{
        grid-template-columns:1fr;
    }

    .page-header h1{
        font-size:42px;
    }

    .profile-page{
        padding:22px;
    }

}

</style>