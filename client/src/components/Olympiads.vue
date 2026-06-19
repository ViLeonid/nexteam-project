<template>
  <div class="page">

    <div class="controls">
      <input
        v-model="searchQuery"
        type="text"
        class="count-input"
        placeholder="Поиск по названию..."
      >

      <select v-model="selectedSubject">
        <option value="">Все предметы</option>
        <option value="Математика">Математика</option>
        <option value="Информатика">Информатика</option>
        <option value="Физика">Физика</option>
        <option value="Химия">Химия</option>
      </select>

      <select v-model="sortBy">
        <option value="id">По ID</option>
        <option value="level">По уровню перечня</option>
        <option value="title">По названию</option>
      </select>
      <select v-model="selectedClass">
        <option value="">Все классы</option>
        <option value="5">5 класс</option>
        <option value="6">6 класс</option>
        <option value="7">7 класс</option>
        <option value="8">8 класс</option>
        <option value="9">9 класс</option>
        <option value="10">10 класс</option>
        <option value="11">11 класс</option>
      </select>
      <label class="checkbox">
        <input type="checkbox" v-model="showOnlyAdded">
        Только добавленные
      </label>
      <div class="results-counter">
        Найдено
        <span>{{ sortedOlympiads.length }}</span>
        из
        <span>{{ olympiads.length }}</span>
        олимпиад
      </div>
    </div>

    <div class="olympiads-grid">

      <div
        v-for="olympiad in sortedOlympiads"
        :key="olympiad.id"
        :class="
          addedOlympiads.includes(String(olympiad.id))
            ? 'olympiad-card-added'
            : 'olympiad-card-active'
        "
      >
        <div class="card-top">
          <div class="icon-box">🏆</div>
          <div>
            <h2>{{ olympiad.title }}</h2>
            
            <span class="subtitle">
              Олимпиада школьников
            </span>
          </div>

        </div>
        <div v-if="olympiad.subjects?.length" class="subjects">
          <span v-for="subject in olympiad.subjects" :key="subject" class="subject-tag">
            {{ subject }}
          </span>
        </div>

        <div v-if="olympiad.dates?.length" class="section">
          <h3>Этапы</h3>

          <ul class="stages">
            <li v-for="date in olympiad.dates" :key="date.stage">
              {{ date.stage }} — {{ date.date }}
            </li>
          </ul>
        </div>

        <div class="bottom">

          <div class="info">

            <div>
              Классы: {{ olympiad.classes }}
            </div>

            <div>
              ID: {{ olympiad.id }}
            </div>

            <a v-if="olympiad.url" :href="olympiad.url" target="_blank" class="site-link">
              🌐 Сайт олимпиады
            </a>

          </div>

          <div class="actions">

            <div v-if="olympiad.level_perechnya" class="level">
              ⭐ Уровень {{ olympiad.level_perechnya }}
            </div>
            <div v-if="olympiad.dates.length">
              <button
              v-if="!addedOlympiads.includes(String(olympiad.id))"
                class="schedule-btn"
                @click="AddInSchedule(olympiad.id)"
              >
                Добавить в расписание
              </button>

              <button
                v-else
                class="remove-btn"
                @click="RemoveFromSchedule(olympiad.id)"
              >
                Удалить из расписания
              </button>
            </div>
          </div>

        </div>

      </div>

    </div>

  </div>
</template>


<script setup>
import api from '@/api';
import { ref, computed, onMounted } from "vue";

const olympiads = ref([]);
const loading = ref(false);
const start_limit = ref();
const end_limit = ref();
const sortBy = ref("id");
const selectedSubject = ref("");
const selectedClass = ref("");
const addedOlympiads = ref([]);
const searchQuery = ref("");
const showOnlyAdded = ref(false);


const AddInSchedule = async (id) => {
  try {
    await api.post(`/add_olympiad/${id}`);

    if (!addedOlympiads.value.includes(String(id))) {
      addedOlympiads.value.push(String(id));
    }
  } catch (error) {
    console.error(error);
  }
};

const GetAddedOlympiads = async () => {
  try {
    const res = await api.get('/added_olympiads');

    addedOlympiads.value =
      res.data.olympiads.map(id => String(id));

  } catch (error) {
    console.error(error);
  }
};

const RemoveFromSchedule = async (id) => {
  try {
    await api.delete(`/remove_olympiad/${id}`);

    addedOlympiads.value =
      addedOlympiads.value.filter(
        olympiadId => olympiadId !== String(id)
      );

  } catch (error) {
    console.error(error);
  }
};

const GetOlympiads = () => {
    api.get('/olympiads').then(res => { olympiads.value = res.data.olympiads })
}

const sortedOlympiads = computed(() => {
  let arr = [...olympiads.value];

  if (showOnlyAdded.value) {
    arr = arr.filter(olympiad =>
      addedOlympiads.value.includes(String(olympiad.id))
    );
  }

  if (searchQuery.value.trim()) {
    const words = searchQuery.value
      .toLowerCase()
      .split(/\s+/);

    arr = arr.filter(olympiad =>
      words.every(word =>
        olympiad.title.toLowerCase().includes(word)
      )
    );
  }

  if (selectedSubject.value) {
    arr = arr.filter(olympiad =>
      olympiad.subjects?.includes(selectedSubject.value)
    );
  }



  if (selectedSubject.value) {
    arr = arr.filter(olympiads =>
      olympiads.subjects?.includes(selectedSubject.value)
    );
  }
    if (selectedClass.value) {
        arr = arr.filter(olympiad => {
            if (!olympiad.classes) return false;

            const nums =
            olympiad.classes.match(/\d+/g)?.map(Number) || [];

            const current = Number(selectedClass.value);

            if (nums.length === 1) {
            return nums[0] === current;
            }

            if (nums.length >= 2) {
            return current >= nums[0] &&
                    current <= nums[nums.length - 1];
            }

            return false;
        });
    }
  switch (sortBy.value) {
    case "title":
      return arr.sort((a, b) =>
        a.title.localeCompare(b.title, "ru")
      );

    case "level":
      return arr.sort((a, b) => {
        const levelA = a.level_perechnya
          ? Number(a.level_perechnya)
          : 999;

        const levelB = b.level_perechnya
          ? Number(b.level_perechnya)
          : 999;

        return levelA - levelB;
      });

    case "id":
    default:
      return arr.sort((a, b) => Number(a.id) - Number(b.id));
  }
});

onMounted(() => {
  GetOlympiads();
  GetAddedOlympiads();
});
</script>
<style scoped>

* {
  box-sizing: border-box;
}

.page {
  min-height: 100vh;
  background: #050b17;
  padding: 24px;
}

/* ---------- Верхняя панель ---------- */

.controls {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 30px;
}

.controls input,
.controls select {
  height: 48px;

  background: #0f1b34;
  border: 1px solid #243456;

  border-radius: 12px;

  color: white;

  padding: 0 14px;

  font-size: 15px;

  outline: none;

  transition: .2s;
}

.controls input:focus,
.controls select:focus {
  border-color: #5865f2;
}

.controls select option {
  background: #0f1b34;
}
.results-counter {
  margin-left: auto;

  display: flex;
  align-items: center;
  gap: 6px;

  padding: 0 18px;

  height: 48px;

  border-radius: 12px;

  background: #0f1b34;
  border: 1px solid #243456;

  color: rgba(255,255,255,.8);

  font-weight: 500;
}

.results-counter span {
  color: white;
  font-weight: 700;
}
.search-btn {
  height: 48px;

  border: none;

  padding: 0 18px;

  border-radius: 12px;

  background: linear-gradient(
    135deg,
    #5865f2,
    #7c5cff
  );

  color: white;

  font-weight: 600;

  cursor: pointer;

  transition: .2s;
}

.search-btn:hover {
  transform: translateY(-2px);
}

.remove-btn {
  border: none;

  background: #4d1f1f;
  color: #ff6b6b;

  padding: 12px 18px;

  border-radius: 14px;

  font-size: 1rem;
  font-weight: 700;

  cursor: pointer;

  transition: .2s;
}

.remove-btn:hover {
  background: #6a2a2a;
  transform: translateY(-2px);
}

/* ---------- Сетка ---------- */

.olympiads-grid {
  max-width: 1800px;

  margin: 0 auto;

  display: grid;

  grid-template-columns: repeat(3, 1fr);

  gap: 20px;
}



.olympiad-card-active {
  background: #0f1b34;

  border: 1px solid #243456;

  border-radius: 22px;

  padding: 20px;

  color: white;
  opacity: 1;
  transition: .25s;

  box-shadow:
    0 10px 30px rgba(0,0,0,.35);
}

.olympiad-card-added {
  background: #0f1b34;

  border: 1px solid #243456;

  border-radius: 22px;

  padding: 20px;

  color: white;
  opacity: 0.4;
  transition: .25s;

  box-shadow:
    0 10px 30px rgba(0,0,0,.35);
}

.olympiad-card:hover {
  transform: translateY(-4px);

  border-color: #5865f2;

  box-shadow:
    0 20px 40px rgba(0,0,0,.45);
}

.card-top {
  display: flex;
  gap: 14px;

  align-items: flex-start;

  margin-bottom: 18px;
}

.icon-box {
  width: 52px;
  height: 52px;

  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 14px;

  background: #1f2a52;

  font-size: 24px;
}

.card-top h2 {
  margin: 0;

  font-size: 1.4rem;
  line-height: 1.2;

  color: white;
}

.subtitle {
  color: rgba(255,255,255,.55);

  font-size: .95rem;
}

/* ---------- Предметы ---------- */

.subjects {
  display: flex;
  flex-wrap: wrap;

  gap: 8px;

  margin-bottom: 18px;
}

.subject-tag {
  background: #20295a;

  color: white;

  padding: 8px 12px;

  border-radius: 999px;

  font-size: .9rem;
  font-weight: 600;
}

/* ---------- Этапы ---------- */

.section {
  border-top: 1px solid rgba(255,255,255,.08);
  border-bottom: 1px solid rgba(255,255,255,.08);

  padding: 18px 0;

  margin-bottom: 18px;
}

.section h3 {
  margin: 0 0 12px;

  font-size: 1.3rem;
}

.stages {
  margin: 0;
  padding-left: 20px;
}

.stages li {
  margin-bottom: 8px;

  color: rgba(255,255,255,.85);

  line-height: 1.4;
}

/* ---------- Низ ---------- */

.bottom {
  display: flex;

  justify-content: space-between;

  gap: 20px;
}

.info {
  display: flex;
  flex-direction: column;

  gap: 8px;

  color: rgba(255,255,255,.7);

  font-size: .95rem;
}

.site-link {
  margin-top: 8px;

  color: white;

  text-decoration: none;

  font-weight: 600;
}

.site-link:hover {
  text-decoration: underline;
}

.actions {
  display: flex;
  flex-direction: column;

  align-items: flex-end;

  gap: 12px;
}

.level {
  background: #24295d;

  color: white;

  padding: 10px 14px;

  border-radius: 14px;

  font-weight: 700;

  font-size: 1rem;
}

.schedule-btn {
  border: none;

  background: #0b4a52;

  color: #00d26a;

  padding: 12px 18px;

  border-radius: 14px;

  font-size: 1rem;
  font-weight: 700;

  cursor: pointer;

  transition: .2s;
}

.schedule-btn:hover {
  background: #0e5f69;

  transform: translateY(-2px);
}

/* ---------- Number Input ---------- */

input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  opacity: 1;
  filter: invert(1);
}
.checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  background: #0f1b34;
  padding: 0 12px;
  border-radius: 12px;
  height: 48px;
  border: 1px solid #243456;
}

/* ---------- Адаптив ---------- */

@media (max-width: 1500px) {
  .olympiads-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 900px) {
  .olympiads-grid {
    grid-template-columns: 1fr;
  }

  .bottom {
    flex-direction: column;
  }

  .actions {
    align-items: stretch;
  }

  .schedule-btn {
    width: 100%;
  }
}

</style>