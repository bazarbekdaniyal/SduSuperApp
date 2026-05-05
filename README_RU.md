# SDU SuperApp

**Веб-платформа для студентов и преподавателей SDU**

CSS 217 – Software Architecture and Design Patterns  
Final Project

**Year:** 2025

---

## 📋 Обзор проекта

SDU SuperApp — это веб-приложение, объединяющее ключевые функции для студентов университета SDU:

- 👨‍🏫 **Рейтинг преподавателей** — просмотр и оценка преподавателей
- 📅 **Расписания** — расписания преподавателей и групп
- 🚪 **Свободные аудитории** — поиск свободных аудиторий в реальном времени
- 📰 **Новости** — университетские новости и события
- 🛒 **Магазин** — мерч и товары SDU

---

## 🏗️ Архитектура

### Структура проекта

```
SduSuperApp/
├── app.py                 # Главный файл Flask
├── config.py              # Конфигурация
├── requirements.txt       # Зависимости
│
├── models/                # Модели данных
│   ├── teacher.py
│   ├── schedule.py
│   ├── review.py
│   ├── room.py
│   ├── news.py
│   ├── product.py
│   ├── order.py
│   └── subscriber.py
│
├── repository/            # Слой доступа к данным
│   ├── base_repository.py
│   ├── teacher_repository.py
│   └── ...
│
├── services/              # Бизнес-логика
│   ├── teacher_service.py
│   ├── news_service.py
│   └── ...
│
├── controllers/           # Flask Blueprints (routes)
│   ├── main_controller.py
│   ├── teacher_controller.py
│   └── ...
│
├── factory/               # Factory Method Pattern
│   ├── base_factory.py
│   ├── teacher_factory.py
│   └── ...
│
├── observer/              # Observer Pattern
│   ├── observer.py
│   ├── subject.py
│   ├── news_publisher.py
│   └── email_subscriber.py
│
├── facade/                # Facade Pattern
│   └── sdu_facade.py
│
├── templates/             # HTML шаблоны (Jinja2)
├── static/                # CSS, JS, изображения
└── data/                  # JSON-файлы данных
```

---

## 🎨 Паттерны проектирования

### 1. Factory Method (Creational Pattern)

**Расположение:** `factory/`

**Описание:** Паттерн Factory Method определяет интерфейс для создания объектов, но позволяет подклассам решать, какой класс инстанцировать.

**Реализация:**
- `BaseFactory` — абстрактная фабрика с методами `create()` и `create_default()`
- `TeacherFactory` — создание преподавателей
- `NewsFactory` — создание новостей
- `ProductFactory` — создание товаров
- `ReviewFactory` — создание отзывов

**Обоснование:**
- Изоляция логики создания объектов
- Легко добавлять новые типы объектов
- Единообразный интерфейс создания

```python
# Пример использования
factory = TeacherFactory()
teacher = factory.create_professor(name="Иван Иванов", department="IT", ...)
```

---

### 2. Observer (Behavioral Pattern)

**Расположение:** `observer/`

**Описание:** Паттерн Observer определяет зависимость "один ко многим" между объектами. При изменении состояния Subject все Observer уведомляются автоматически.

**Реализация:**
- `Observer` — абстрактный интерфейс наблюдателя
- `Subject` — базовый класс издателя
- `NewsPublisher` — издатель новостей (Singleton)
- `EmailSubscriber` — подписчик для email-уведомлений
- `NotificationSubscriber` — подписчик для внутренних уведомлений

**Обоснование:**
- Слабая связанность между компонентами
- Легко добавлять новые типы подписчиков
- Автоматические уведомления при событиях

```python
# Пример использования
publisher = NewsPublisher()
subscriber = EmailSubscriber("user@gmail.com", "User")
publisher.subscribe_to_all(subscriber)
publisher.publish_news(news)  # Все подписчики получат уведомление
```

---

### 3. Facade (Structural Pattern)

**Расположение:** `facade/sdu_facade.py`

**Описание:** Паттерн Facade предоставляет унифицированный интерфейс к набору интерфейсов в подсистеме.

**Реализация:**
- `SDUFacade` — единая точка входа ко всем сервисам (Singleton)
- Объединяет: TeacherService, ScheduleService, ReviewService, RoomService, NewsService, ShopService

**Обоснование:**
- Упрощает использование сложной системы
- Уменьшает зависимости между клиентом и подсистемами
- Обеспечивает единую точку входа
- Облегчает тестирование

```python
# Пример использования
facade = SDUFacade()

# Вместо работы с 6 разными сервисами:
data = facade.get_home_page_data()
teacher_info = facade.get_teacher_full_info(teacher_id)
```

---

## 🔧 SOLID Принципы

### S — Single Responsibility Principle (Принцип единственной ответственности)

Каждый класс имеет одну ответственность:
- `Repository` — только CRUD операции с данными
- `Service` — только бизнес-логика
- `Controller` — только обработка HTTP-запросов
- `Factory` — только создание объектов

### O — Open/Closed Principle (Принцип открытости/закрытости)

Классы открыты для расширения, закрыты для модификации:
- Новые фабрики добавляются без изменения `BaseFactory`
- Новые подписчики добавляются без изменения `NewsPublisher`
- Новые репозитории добавляются без изменения `BaseRepository`

### L — Liskov Substitution Principle (Принцип подстановки Лисков)

Подклассы могут заменять базовые классы:
- Все репозитории реализуют `BaseRepository`
- Все фабрики реализуют `BaseFactory`
- Все наблюдатели реализуют `Observer`

### I — Interface Segregation Principle (Принцип разделения интерфейса)

Маленькие специализированные интерфейсы:
- `Observer` — минимальный интерфейс с методом `update()`
- `BaseFactory` — только `create()` и `create_default()`

### D — Dependency Inversion Principle (Принцип инверсии зависимостей)

Зависимость от абстракций, а не от конкретных реализаций:
- Сервисы принимают репозитории через конструктор
- Контроллеры используют Facade вместо прямых сервисов

---

## 🚀 Установка и запуск

### Требования
- Python 3.10+
- pip

### Установка

```bash
# Клонировать репозиторий
cd SduSuperApp

# Создать виртуальное окружение
python -m venv .venv

# Активировать (macOS/Linux)
source .venv/bin/activate

# Активировать (Windows)
.venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt

# ВАЖНО: Для работы автоматического перевода новостей установите:
pip install deep-translator
```

### Запуск

```bash
python app.py
```

Приложение будет доступно по адресу: `http://localhost:5001`

### Деплой через Docker

```bash
cp .env.example .env
# Отредактируйте .env и задайте SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD
docker compose up -d --build
```

Приложение будет доступно по адресу: `http://localhost:5001`.

JSON-файлы сохраняются в Docker volume `app_data`, поэтому заказы, отзывы, рейтинги и другие данные остаются между пересборками контейнера.

---

## 📱 Функционал

### Главная страница
- Топ преподавателей по рейтингу
- Последние новости
- Популярные товары

### Преподаватели (`/teachers`)
- Список всех преподавателей
- Фильтрация по факультету
- Поиск по имени
- Страница преподавателя с расписанием и отзывами
- Добавление отзывов (с модерацией)

### Аудитории (`/rooms`)
- Поиск свободных аудиторий по дню и времени
- Фильтрация по корпусу
- Просмотр текущих свободных аудиторий

### Новости (`/news`)
- Список новостей с категориями
- Поиск по новостям
- Подписка на email-рассылку (Observer Pattern)
- Популярные новости

### Магазин (`/shop`)
- Каталог товаров
- Категории товаров
- Корзина
- Оформление заказа

### Админ-панель (`/admin`)
- Статистика
- Модерация отзывов
- Управление преподавателями
- Управление заказами

---

## 📊 Технологии

- **Backend:** Python 3.11, Flask 3.0
- **Frontend:** HTML5, CSS3, Jinja2
- **Хранение данных:** JSON-файлы
- **Иконки:** Font Awesome 6
- **Шрифты:** Google Fonts (Inter)

---

## 👥 Команда

- Daniyal Bazarbek **Developer** 
- Yerkezhan Chakenova **Presentation (PPT)** 
- Kenshibek Assylkhan **Tester** 

---

## 📄 Лицензия

Проект создан в рамках курса CSS 217 – Software Architecture and Design Patterns.

© 2025 SDU University
