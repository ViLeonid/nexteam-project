<template>
<div class="landing">

    <!-- HERO -->
    <section class="hero">

        <div class="overlay"></div>

        <div class="hero-content">

            <div class="badge">
                Олимпиады • ЕГЭ • ОГЭ
            </div>

            <h1>
                Побеждают не самые умные.
                <br>
                Побеждают самые системные.
            </h1>

            <p>
                NexTeam — персональная система подготовки.
                Планируй, отслеживай прогресс, проходи фокус-сессии,
                развивайся каждый день.
            </p>

            <div class="hero-buttons">
                <button class="primary" @click="$router.push({path: '/auth', query: { isLogin: 'false' } })">
                    Регистрация
                </button>

                <button class="secondary" @click="$router.push({path: '/auth', query: { isLogin: 'true' } })">
                    Вход
                </button>
            </div>

        </div>
        <div class="hero-image">
            <img src="@/assets/landing_photo3.png" alt="NexTeam preview">
        </div>

    </section>





    <!-- STATS -->

    <section class="stats">

        <div class="stat">
            <h2>24/7</h2>
            <span>Доступность</span>
        </div>

        <div class="stat">
            <h2 class="infinity">
                <svg viewBox="0 0 100 50">
                    <path d="M50 25 C35 5,10 5,10 25 C10 45,35 45,50 25 C65 5,90 5,90 25 C90 45,65 45,50 25"
                    fill="none"
                    stroke="white"
                    stroke-width="8"
                    stroke-linecap="round"/>
                </svg>
            </h2>
            <span>Количество целей</span>
        </div>

        <div class="stat">
            <h2>100%</h2>
            <span>Контроль подготовки</span>
        </div>

        <div class="stat">
            <h2>1</h2>
            <span>Главная цель — победа</span>
        </div>

    </section>






    <!-- FEATURES -->

    <section class="features">

        <h2>
            Всё для подготовки
        </h2>

        <div class="cards">

            <div class="card">
                <div class="icon">🎯</div>

                <h3>Умные цели</h3>

                <p>
                    Разбей подготовку на реальные задачи и двигайся к победе каждый день.
                </p>
            </div>

            <div class="card">
                <div class="icon">🔥</div>

                <h3>Фокус-сессии</h3>

                <p>
                    Таймер, статистика, режим концентрации и контроль времени.
                </p>
            </div>

            <div class="card">
                <div class="icon">📈</div>

                <h3>Аналитика</h3>

                <p>
                    Следи за количеством часов,
                    продуктивностью и прогрессом.
                </p>
            </div>

            <div class="card">
                <div class="icon">🧠</div>

                <h3>Карта подготовки</h3>

                <p>
                    Огромное дерево тем с твоим прогрессом.
                </p>
            </div>

            <div class="card">
                <div class="icon">📅</div>

                <h3>Календарь олимпиад</h3>

                <p>
                    Все важные даты автоматически появляются в расписании.
                </p>
            </div>

            <div class="card">
                <div class="icon">🏆</div>

                <h3>Главная цель</h3>

                <p>
                    Каждый день напоминаем,
                    ради чего ты начал.
                </p>
            </div>

        </div>

    </section>







    <!-- TIMELINE -->

    <section class="timeline">

        <h2>
            Путь к диплому
        </h2>

        <div class="steps">

            <div class="step">
                <div class="circle">1</div>

                <h3>Поставь цель</h3>

                <p>
                    Выбери олимпиаду и предмет.
                </p>
            </div>

            <div class="step">
                <div class="circle">2</div>

                <h3>Построй маршрут</h3>

                <p>
                    NexTeam автоматически разобьёт подготовку.
                </p>
            </div>

            <div class="step">
                <div class="circle">3</div>

                <h3>Учись ежедневно</h3>

                <p>
                    Фокус-сессии и аналитика будут вести тебя вперёд.
                </p>
            </div>

            <div class="step">
                <div class="circle">4</div>

                <h3>Побеждай</h3>

                <p>
                    Когда остальные теряют мотивацию —
                    ты продолжаешь расти.
                </p>
            </div>

        </div>

    </section>








    <!-- CTA -->

    <section class="cta">

        <h2>
            Каждый день без подготовки —
            день, который работает против тебя.
        </h2>

        <p>

            Начни сегодня.
            Через несколько месяцев ты скажешь себе спасибо.

        </p>

        <button class="primary" @click="$router.push({path: '/auth', query: { isLogin: 'false' } })">
            Начать подготовку →
        </button>

    </section>

</div>
</template>

<style scoped>

*{
    box-sizing:border-box;
    font-family:Inter,sans-serif;
}
.card h3{
    color: #bdbdbd;
}
.landing{

    background:#040404;
    color:white;

}

.hero{

    height:100vh;

    position:relative;

    display:flex;
    align-items:center;

    justify-content:space-between;
    padding:0 120px;
    gap: 20px;

    background:url("@/assets/landing.jpg") center/cover;

}

.overlay{

    position:absolute;
    inset:0;

    background:
    linear-gradient(to right,
    rgba(0,0,0,.88),
    rgba(0,0,0,.45));

}
.hero-image{

    position:relative;

    width:60vw;

    display:flex;

    justify-content:center;

    align-items:center;

}


.hero-image img{

    width:100%;
    transform: translateY(-50px);
    transform: translateX(50px);

    border-radius:30px;

    box-shadow:
    0 40px 80px rgba(0,0,0,.7);

    -webkit-mask-image: linear-gradient(
        to bottom,
        black 75%,
        transparent 100%
    );

    mask-image: linear-gradient(
        to bottom,
        black 75%,
        transparent 100%
    );
}



.hero-content{

    position:relative;

    width:50vw;

}

.infinity svg{

    width:80px;
    height:70px;

}

.badge{

    display:inline-block;

    padding:8px 18px;

    border-radius:40px;

    background:rgba(255,255,255,.15);

    backdrop-filter:blur(10px);

    margin-bottom:25px;

    font-size: 14px;

    font-weight: 600;
}

.hero h1{

    font-size:72px;

    line-height:1.1;

    margin-bottom:30px;

}

.hero p{

    font-size:22px;

    color:#d7d7d7;

    line-height:1.6;

    width:620px;

}

.hero-buttons{

    display:flex;

    gap:20px;

    margin-top:45px;

}

.primary{

    background:white;

    color:black;

    padding:18px 34px;

    border:none;

    border-radius:16px;

    font-size:18px;

    cursor:pointer;

}

.secondary{

    background:transparent;

    color:white;

    border:2px solid white;

    padding:18px 34px;

    border-radius:16px;

}

.stats{

    display:flex;

    justify-content:center;

    gap:80px;

    padding:80px;

}

.stat{

    text-align:center;

}

.stat h2{

    font-size:64px;

    margin-bottom:10px;

}

.stat span{

    color:#9e9e9e;

}

.features{

    padding:120px;

}

.features h2{

    text-align:center;

    font-size:56px;

    margin-bottom:70px;

}

.cards{

    display:grid;

    grid-template-columns:repeat(3,1fr);

    gap:35px;

}

.card{

    background:#111;

    border-radius:25px;

    padding:35px;

    transition:.3s;

    border:1px solid #2d2d2d;

}

.card:hover{

    transform:translateY(-12px);

    box-shadow:0 20px 60px rgba(255,255,255,.08);

}

.icon{

    font-size:45px;

    margin-bottom:25px;

}

.card h3{

    font-size:28px;

    margin-bottom:20px;

}

.card p{

    color:#bdbdbd;

    line-height:1.7;

}

.timeline{

    padding:120px;

    background:#090909;

}

.timeline h2{

    text-align:center;

    font-size:54px;

    margin-bottom:80px;

}

.steps{

    display:flex;

    justify-content:space-between;

}

.step{

    width:250px;

    text-align:center;

}

.circle{

    width:80px;

    height:80px;

    border-radius:50%;

    background:white;

    color:black;

    margin:auto;

    display:flex;

    justify-content:center;

    align-items:center;

    font-size:34px;

    font-weight:bold;

    margin-bottom:30px;

}

.step h3{

    margin-bottom:15px;

}

.step p{

    color:#bfbfbf;

}

.cta{

    text-align:center;

    padding:150px 20px;

}

.cta h2{

    font-size:58px;

    width:1000px;

    margin:auto;

}

.cta p{

    margin-top:30px;

    color:#b8b8b8;

    font-size:22px;

}

.cta button{

    margin-top:50px;

    padding:22px 60px;

    border:none;

    border-radius:18px;

    font-size:22px;

    cursor:pointer;

    background:white;

    color:black;

}

</style>