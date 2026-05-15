# Nexteam

Nexteam — это fullstack productivity/web planner приложение с системой задач, событий и AI-интеграцией.

## Возможности

- Авторизация и регистрация пользователей
- Session-based authentication
- CRUD для задач
- Календарь и события
- AI-функции через GigaChat API
- Защита пользовательских данных
- Responsive UI
- Backend API на Flask
- Frontend на Vue

---

# Стек технологий

## Frontend

- Vue.js
- Vue Router
- Bootstrap
- Fetch API

## Backend

- Flask
- SQLAlchemy
- Flask-CORS
- Werkzeug Security
- SQLite

## Безопасность

- Password hashing
- Session authentication
- SameSite cookies
- Ownership validation
- XSS protection
- CSRF protection

---

# Структура проекта

```bash
project/
│
├── client/              # Vue frontend
│   ├── src/
│   └── public/
│
├── server/              # Flask backend
│   ├── app.py
│   ├── models.py
│   └── database.db
│
├── requirements.txt
└── README.md
```

---

# Установка

## 1. Клонировать репозиторий

```bash
git clone <your-repository-url>
cd nexteam
```

---

# Backend setup

## 2. Создать virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Установить зависимости

```bash
pip install -r requirements.txt
```

---

## 4. Создать `.env`

Пример:

```env
SECRET_KEY=your_secret_key
GIGACHAT_CREDENTIALS=your_credentials
DEBUG=False
```

---

## 5. Запустить backend

```bash
cd server
python app.py
```

Backend будет доступен:

```text
http://localhost:5000
```

---

# Frontend setup

## 6. Установить npm dependencies

```bash
cd client
npm install
```

---

## 7. Запустить frontend

```bash
npm run dev
```

Frontend будет доступен:

```text
http://localhost:5173
```

---

# API

## Authentication

### Register

```http
POST /api/register
```

### Login

```http
POST /api/login
```

### Logout

```http
POST /api/logout
```

---

## Todos

### Получить задачи

```http
GET /api/todos
```

### Создать задачу

```http
POST /api/todos
```

### Обновить задачу

```http
PUT /api/todos/<id>
```

### Удалить задачу

```http
DELETE /api/todos/<id>
```

---

## Events

### Получить события

```http
GET /api/events
```

### Создать событие

```http
POST /api/events
```

---

# Безопасность

Проект включает:

- Password hashing
- Session-based authentication
- Access control
- Secure cookie flags
- XSS mitigation
- CSRF protection
- Validation checks

---

# Production рекомендации

Для production deployment рекомендуется:

- PostgreSQL вместо SQLite
- HTTPS
- Reverse proxy (Nginx)
- Docker deployment
- CSP headers
- Rate limiting
- Monitoring/logging

---

