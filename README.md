# Sleep Tracker

Приложение для отслеживания качества сна и анализа режима сна. Позволяет пользователям записывать время сна и пробуждения, оценивать самочувствие и просматривать статистику.

## 🌟 Возможности

- 📝 Запись времени сна и пробуждения
- 😊 Оценка самочувствия после сна
- 📊 Просмотр статистики сна
- 📈 Анализ режима сна за последние 10 дней
- 👥 Поддержка нескольких пользователей
- 👨‍💼 Административная панель для просмотра общей статистики

## 🛠 Технологии

- Python
- [BeeWare](https://beeware.org/) (набор инструментов для создания нативных приложений)
- Toga (кроссплатформенный GUI фреймворк от BeeWare)
- Briefcase (инструмент для создания нативных приложений от BeeWare)
- Supabase (облачная база данных)


## 📁 Структура проекта

```
sleep_tracker/
├── src/
│   └── sleep_tracker/
│       ├── assets/           # Изображения и ресурсы
│       ├── database/         # Работа с базой данных
│       │   └── supabase_db.py
│       ├── models/          # Модели данных
│       ├── resources/       # Дополнительные ресурсы
│       ├── screens/         # Экраны приложения
│       │   ├── admin_screen.py
│       │   ├── base_screen.py
│       │   ├── history_screen.py
│       │   ├── input_screen.py
│       │   ├── login_screen.py
│       │   ├── main_menu.py
│       │   └── report_screen.py
│       ├── utils/           # Вспомогательные функции
│       ├── app.py           # Основной файл приложения
│       └── __main__.py      # Точка входа
├── tests/                   # Тесты
├── pyproject.toml          # Зависимости и метаданные проекта
└── README.md               # Документация
```

## 📋 Требования

- Python 3.8 или выше
- Зависимости из pyproject.toml
- Аккаунт Supabase для доступа к базе данных

## 🚀 Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/asdfsdafdsa/sleep_tracker.git
cd sleep_tracker
```

2. Установите зависимости:
```bash
pip install -e .
```

3. Настройте Supabase:
   - Создайте проект на [Supabase](https://supabase.com)
   - Создайте таблицы `users` и `sleep_logs`
   - Скопируйте URL и ключ API из настроек проекта
   - Обновите значения `SUPABASE_URL` и `SUPABASE_KEY` в файле `src/sleep_tracker/database/supabase_db.py`

**Пример:**
```python
# src/sleep_tracker/database/supabase_db.py
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your_supabase_api_key"
```

## 💻 Использование

1. Запустите приложение:
```bash
python -m sleep_tracker
```

2. Войдите в систему
3. Используйте меню для:
   - Ввода данных о сне
   - Просмотра истории
   - Анализа статистики

## 📱 Поддерживаемая платформа

- Android


## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробности в файле [LICENSE](LICENSE).
