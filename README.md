# Restaurant Booking API

REST API для системы бронирования столиков в ресторане. API позволяет управлять столиками и бронированиями, включая проверку доступности и конфликтов времени.

## Технологии

- Python 3.11+
- FastAPI
- SQLModel (SQLAlchemy + Pydantic)
- PostgreSQL
- Docker & Docker Compose
- Poetry (управление зависимостями)
- Pytest (тестирование)

## Функциональность

### Управление столиками

- Создание столиков с указанием количества мест и расположения
- Получение списка всех столиков
- Получение информации о конкретном столике
- Обновление информации о столике
- Удаление столика

### Управление бронированиями

- Создание бронирований с проверкой доступности столика
- Проверка конфликтов времени при бронировании
- Получение списка всех бронирований
- Получение информации о конкретном бронировании
- Обновление информации о бронировании
- Удаление бронирования

## Установка и запуск

### Предварительные требования

- Docker и Docker Compose
- Python 3.11 или выше
- Poetry (опционально, для локальной разработки)

### Запуск с помощью Docker

1. Клонируйте репозиторий:

```bash
git clone https://github.com/yourusername/restaurant-booking.git
cd restaurant-booking
```

2. Запустите приложение:

```bash
docker-compose up --build
```

Приложение будет доступно по адресу: http://localhost:8000

### Локальная разработка

1. Создайте виртуальное окружение и установите зависимости:

```bash
python -m venv .venv
source .venv/bin/activate  # для Linux/Mac
# или
.venv\Scripts\activate  # для Windows
poetry install
```

2. Запустите тесты:

```bash
pytest
```

## API Endpoints

### Столики

- `POST /api/v1/tables/` - Создание столика
- `GET /api/v1/tables/` - Получение списка столиков
- `GET /api/v1/tables/{table_id}` - Получение информации о столике
- `PUT /api/v1/tables/{table_id}` - Обновление информации о столике
- `DELETE /api/v1/tables/{table_id}` - Удаление столика

### Бронирования

- `POST /api/v1/reservations/` - Создание бронирования
- `GET /api/v1/reservations/` - Получение списка бронирований
- `GET /api/v1/reservations/{reservation_id}` - Получение информации о бронировании
- `PUT /api/v1/reservations/{reservation_id}` - Обновление информации о бронировании
- `DELETE /api/v1/reservations/{reservation_id}` - Удаление бронирования

## Тестирование

Проект включает набор тестов, охватывающих:

- Создание и управление столиками
- Создание и управление бронированиями
- Проверку конфликтов времени
- Валидацию данных

Запуск тестов:

```bash
pytest
```

## Структура проекта

```
restaurant-booking/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── reservations.py
│   │       │   └── tables.py
│   │       └── api.py
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   ├── db/
│   │   └── session.py
│   ├── models/
│   │   ├── reservation.py
│   │   └── table.py
│   ├── schemas/
│   │   ├── reservation.py
│   │   └── table.py
│   ├── services/
│   │   ├── reservation.py
│   │   └── table.py
│   └── main.py
├── tests/
│   ├── api/
│   │   ├── test_reservations.py
│   │   └── test_tables.py
│   ├── test_api.py
│   ├── test_models.py
│   └── conftest.py
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── poetry.lock
├── pyproject.toml
└── README.md
```

## Лицензия

MIT

## Автор

Ivan Foksha
