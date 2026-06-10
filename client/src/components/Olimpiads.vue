<template>
  <div>
    <input v-model="count">
    <button @click="loadOlympiads" :disabled="loading" class="btn">
      {{ loading ? "Парсим..." : "Найти олимпиады" }}
    </button>
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
    <div v-for="olympiad in sortedOlympiads" :key="olympiad.id" class="card">
      <h2>{{ olympiad.title }}</h2>
      <p v-if="olympiad.subjects.length">
        <b>Предметы:</b>
        {{ olympiad.subjects.join(", ") }}
      </p>
      <div v-if="olympiad.dates.length">
        <h4>Этапы</h4>
        <ul>
          <li v-for="date in olympiad.dates" :key="date.stage">
            {{ date.stage }} — {{ date.date }}
          </li>
        </ul>
      </div>
      <p v-if="olympiad.classes">Классы: {{ olympiad.classes }}</p>
      <div v-if="olympiad.level_perechnya !== ''">
        <p style="color: blueviolet; font-weight: bold;">Уровень перечня: {{ olympiad.level_perechnya }}</p>
      </div>
      <div><p>id: {{ olympiad.id }}</p></div>
      <div style="display: flex; justify-content: space-between; align-items: flex-end;">
        <a v-if="olympiad.url" :href="olympiad.url" target="_blank">
          Сайт олимпиады
        </a>
        <button @click="AddInSchedule(olympiad.id)">Добавить в расписание</button>
      </div>
    </div>
  </div>
</template>


<script setup>
import axios from "axios";
import { ref, computed } from "vue";

const olympiads = ref([]);
const loading = ref(false);
const count = ref();
const sortBy = ref("id");
const selectedSubject =ref("");

const AddInSchedule = (id) => {
  axios.post(`http://localhost:5000/add_olimpiad/${id}`, id);
}

const sortedOlympiads = computed(() => {
  let arr = [...olympiads.value];
  if (selectedSubject.value) {
    arr = arr.filter(olympiads =>
      olympiads.subjects?.includes(selectedSubject.value)
    );
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

const loadOlympiads = async () => {
  loading.value = true;
  try {
    const response = await axios.post(
      "http://localhost:5000/api/olympiads/parse",
      {
        count: count.value
      },
      {
        withCredentials: true
      }
    );
    olympiads.value = response.data.olympiads || [];
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
};

</script>



<style scoped>
.btn {
  padding: 10px 20px;
  margin-bottom: 20px;
}

.card {
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
}
</style>