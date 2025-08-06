#!/bin/bash

echo "🌤️ Приложение Погоды для Санкт-Петербурга"
echo "=========================================="
echo ""
echo "Выберите режим запуска:"
echo "1) Веб-приложение (откроет браузер на localhost:8000)"
echo "2) Python-скрипт (консольный вывод)"
echo "3) Установить зависимости"
echo "4) Выход"
echo ""

read -p "Введите номер (1-4): " choice

case $choice in
    1)
        echo "🌐 Запуск веб-сервера..."
        echo "Откройте браузер и перейдите по адресу: http://localhost:8000"
        python3 -m http.server 8000
        ;;
    2)
        echo "🐍 Запуск Python-скрипта..."
        python3 weather_scraper.py
        ;;
    3)
        echo "📦 Установка зависимостей..."
        sudo apt update && sudo apt install -y python3-requests python3-bs4 python3-lxml
        echo "✅ Зависимости установлены!"
        ;;
    4)
        echo "👋 До свидания!"
        exit 0
        ;;
    *)
        echo "❌ Неверный выбор. Попробуйте снова."
        ;;
esac