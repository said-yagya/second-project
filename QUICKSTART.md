# 🚀 Быстрый старт

## 1️⃣ Веб-приложение (самый простой способ)
```bash
# Откройте index.html в браузере
# Или запустите локальный сервер:
python3 -m http.server 8000
# Затем откройте: http://localhost:8000
```

## 2️⃣ Python-скрипты

### Установка зависимостей (один раз)
```bash
sudo apt install -y python3-requests python3-bs4 python3-lxml
```

### Запуск
```bash
# Автоматический выбор режима
./run.sh

# Или напрямую:
python3 weather_scraper.py    # Парсинг AccuWeather
python3 weather_api.py        # OpenWeatherMap API
```

## 3️⃣ Что получите
- 🌡️ Температура и ощущается как
- 💨 Скорость и направление ветра  
- 🌡️ Атмосферное давление
- 💧 Влажность воздуха
- ☁️ Состояние погоды

## 4️⃣ Файлы с данными
- `weather_data.json` - данные от AccuWeather
- `weather_api_data.json` - данные от OpenWeatherMap

---
📖 Подробная документация: [README.md](README.md)