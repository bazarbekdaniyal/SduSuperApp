# SDU SuperApp

**Web Platform for SDU Students and Teachers**

CSS 217 – Software Architecture and Design Patterns  
Final Project

**Year:** 2025

---

## 📋 Project Overview

SDU SuperApp is a web application combining key functions for SDU university students:

- 👨‍🏫 **Teachers Rating** — view and rate teachers
- 📅 **Schedules** — teacher and group schedules
- 🚪 **Free Rooms** — finding free classrooms in real-time
- 📰 **News** — university news and events
- 🛒 **Shop** — SDU merch and products

---

## 🏗️ Architecture

### Project Structure

```
SduSuperApp/
├── app.py                 # Main Flask file
├── config.py              # Configuration
├── requirements.txt       # Dependencies
│
├── models/                # Data Models
│   ├── teacher.py
│   ├── schedule.py
│   ├── review.py
│   ├── room.py
│   ├── news.py
│   ├── product.py
│   ├── order.py
│   └── subscriber.py
│
├── repository/            # Data Access Layer
│   ├── base_repository.py
│   ├── teacher_repository.py
│   └── ...
│
├── services/              # Business Logic
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
├── templates/             # HTML Templates (Jinja2)
├── static/                # CSS, JS, Images
└── data/                  # JSON Data Files
```

---

## 🎨 Design Patterns

### 1. Factory Method (Creational Pattern)

**Location:** `factory/`

**Description:** The Factory Method pattern defines an interface for creating objects in a superclass, but allows subclasses to alter the type of objects that will be created.

**Implementation:**
- `BaseFactory` — abstract factory with `create()` and `create_default()` methods
- `TeacherFactory` — creating teachers
- `NewsFactory` — creating news
- `ProductFactory` — creating products
- `ReviewFactory` — creating reviews

**Justification:**
- Isolation of object creation logic
- Easy to add new object types
- Uniform creation interface

```python
# Usage Example
factory = TeacherFactory()
teacher = factory.create_professor(name="John Doe", department="IT", ...)
```

---

### 2. Observer (Behavioral Pattern)

**Location:** `observer/`

**Description:** The Observer pattern defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.

**Implementation:**
- `Observer` — abstract observer interface
- `Subject` — base publisher class
- `NewsPublisher` — news publisher (Singleton)
- `EmailSubscriber` — subscriber for email notifications
- `NotificationSubscriber` — subscriber for internal notifications

**Justification:**
- Loose coupling between components
- Easy to add new subscriber types
- Automatic notifications on events

```python
# Usage Example
publisher = NewsPublisher()
subscriber = EmailSubscriber("user@gmail.com", "User")
publisher.subscribe_to_all(subscriber)
publisher.publish_news(news)  # All subscribers will receive notification
```

---

### 3. Facade (Structural Pattern)

**Location:** `facade/sdu_facade.py`

**Description:** The Facade pattern provides a unified interface to a set of interfaces in a subsystem.

**Implementation:**
- `SDUFacade` — single entry point to all services (Singleton)
- Combines: TeacherService, ScheduleService, ReviewService, RoomService, NewsService, ShopService

**Justification:**
- Simplifies usage of a complex system
- Reduces dependencies between client and subsystems
- Provides a single entry point
- Facilitates testing

```python
# Usage Example
facade = SDUFacade()

# Instead of working with 6 different services:
data = facade.get_home_page_data()
teacher_info = facade.get_teacher_full_info(teacher_id)
```

---

## 🔧 SOLID Principles

### S — Single Responsibility Principle

Each class has one responsibility:
- `Repository` — only CRUD operations with data
- `Service` — only business logic
- `Controller` — only HTTP request handling
- `Factory` — only object creation

### O — Open/Closed Principle

Classes are open for extension, closed for modification:
- New factories are added without changing `BaseFactory`
- New subscribers are added without changing `NewsPublisher`
- New repositories are added without changing `BaseRepository`

### L — Liskov Substitution Principle

Subclasses can replace base classes:
- All repositories implement `BaseRepository`
- All factories implement `BaseFactory`
- All observers implement `Observer`

### I — Interface Segregation Principle

Small specialized interfaces:
- `Observer` — minimal interface with `update()` method
- `BaseFactory` — only `create()` and `create_default()`

### D — Dependency Inversion Principle

Depend on abstractions, not on concrete implementations:
- Services accept repositories via constructor
- Controllers use Facade instead of direct services

---

## 🚀 Installation and Run

### Requirements
- Python 3.9+
- pip

### Installation

```bash
# Clone repository
cd SduSuperApp

# Create virtual environment
python -m venv .venv

# Activate (macOS/Linux)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# IMPORTANT: For automatic news translation, install:
pip install deep-translator
```

### Run

```bash
python app.py
```

The application will be available at: `http://localhost:5000`

---

## 📱 Features

### Home Page
- Top teachers by rating
- Latest news
- Popular products

### Teachers (`/teachers`)
- List of all teachers
- Filter by department
- Search by name
- Teacher page with schedule and reviews
- Adding reviews (with moderation)

### Rooms (`/rooms`)
- Search free rooms by day and time
- Filter by building
- View currently free rooms

### News (`/news`)
- News list with categories
- Search news
- Email newsletter subscription (Observer Pattern)
- Popular news

### Shop (`/shop`)
- Product catalog
- Product categories
- Cart
- Checkout

### Admin Panel (`/admin`)
- Statistics
- Review moderation
- Teacher management
- Order management

---

## 📊 Technologies

- **Backend:** Python 3.11, Flask 3.0
- **Frontend:** HTML5, CSS3, Jinja2
- **Data Storage:** JSON files
- **Icons:** Font Awesome 6
- **Fonts:** Google Fonts (Inter)

---

## 👥 Team

- Daniyal Bazarbek **Developer**
- Yerkezhan Chakenova **Designer**
- Kenshibek Assylkhan **Tester**

---

## 📄 License

Project created within the course CSS 217 – Software Architecture and Design Patterns.

© 2025 SDU University
