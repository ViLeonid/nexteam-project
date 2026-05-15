import 'bootstrap/dist/css/bootstrap.css'; 
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import VueKatex from 'vue3-katex';
import 'katex/dist/katex.min.css';

const app = createApp(App);
app.use(router);
app.use(VueKatex);

const autoRender = (text) => {
  if (!text) return "";

  // 1. Оборачиваем весь текст в \text{...}, чтобы сохранить пробелы и обычный шрифт
  // 2. Ищем все команды LaTeX (начинаются с \) и выводим их из-под \text{}
  // Магия регулярки: она находит \команду и превращает "\text{... \int ...}" в "\text{...} \int \text{...}"
  const processed = `\\text{${text}}`.replace(/(\\[a-z]+(?:\{.*?\})?(?:_\{?.*?\}?)?(?:\^\{?.*?\}?)?)/g, '} $1 \\text{');

  try {
    return katex.renderToString(processed, {
      throwOnError: false,
      displayMode: false // Позволяет тексту переноситься на новые строки
    });
  } catch (e) {
    return text; // Если произошла ошибка, выводим сырой текст
  }
};

app.mount('#app');
