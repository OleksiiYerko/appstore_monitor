# App Store Monitor

Мониторинг позиций приложения в App Store по ключевым словам и чартам.

## Структура проекта

```
appstore_monitor/
├── src/                    # Исходный код
│   ├── scrapers/          # Скрипты для парсинга App Store
│   │   ├── appstore_scraper.py
│   │   ├── charts_scraper.py
│   │   └── search_appStore.py
│   ├── utils/             # Утилиты
│   │   ├── country_utils.py
│   │   ├── telegram_utils.py
│   │   └── state_manager.py
│   └── analyzers/         # Анализаторы данных
│       └── get_suggestions.py
├── data/                  # Данные
│   ├── config/           # Конфигурационные файлы
│   │   ├── keywords.json
│   │   ├── table_config.json
│   │   └── message_ids.json
│   ├── results/          # Результаты анализа
│   └── logs/             # Логи
├── tests/                # Тесты
├── main.py               # Главный скрипт
└── README.md
```

## Установка

1. Клонируйте репозиторий
2. Установите зависимости:
```bash
npm install
```

## Использование

### Главный скрипт

```bash
# Поиск по ключевым словам
python3 main.py search

# Проверка чартов
python3 main.py charts --country us

# Анализ поисковых подсказок
python3 main.py suggestions

# Запуск тестов
python3 main.py test
```

### Отдельные скрипты

```bash
# Поиск по ключевым словам
python3 src/scrapers/search_appStore.py

# Анализ подсказок
python3 src/analyzers/get_suggestions.py

# Тесты
python3 tests/test_suggestions.py
```

## Конфигурация

### keywords.json
```json
{
  "video translator": ["us", "gb"],
  "ai translator": ["us", "gb"],
  "photo translator": ["us", "gb"]
}
```

## Функциональность

### 1. Поиск по ключевым словам
- Мониторинг позиций приложения по ключевым словам
- Поддержка множественных стран
- Сохранение результатов в JSON

### 2. Анализ чартов
- Проверка позиций в топ-чартах
- Поддержка различных типов чартов
- Анализ по категориям

### 3. Поисковые подсказки
- Получение автодополнения поиска
- Анализ популярных запросов
- Сравнение по странам

### 4. Утилиты
- Конвертация кодов стран в названия
- Интеграция с Telegram
- Управление состоянием

## Логирование

Логи сохраняются в `data/logs/appstore_monitor.log`

## Результаты

Результаты анализа сохраняются в `data/results/` в формате JSON 