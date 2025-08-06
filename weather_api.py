#!/usr/bin/env python3
"""
Альтернативная версия получения данных о погоде через OpenWeatherMap API
Требует регистрации на openweathermap.org для получения API ключа
"""

import requests
import json
import sys
from datetime import datetime

class OpenWeatherMapAPI:
    def __init__(self, api_key="demo"):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.city = "Saint Petersburg"
        self.country_code = "RU"
        
    def get_weather_data(self):
        """Получает данные о погоде через OpenWeatherMap API"""
        if self.api_key == "demo":
            print("⚠️  Используется демо-режим. Для реальных данных:")
            print("   1. Зарегистрируйтесь на https://openweathermap.org/api")
            print("   2. Получите бесплатный API ключ")
            print("   3. Замените 'demo' на ваш ключ в коде\n")
            return self._get_demo_data()
        
        try:
            params = {
                'q': f"{self.city},{self.country_code}",
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'ru'
            }
            
            print("🌐 Получение данных через OpenWeatherMap API...")
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self._format_weather_data(data)
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка при запросе к API: {e}")
            print("📝 Используем демо-данные...")
            return self._get_demo_data()
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {e}")
            return self._get_demo_data()
    
    def _format_weather_data(self, api_data):
        """Форматирует данные из API в нужный формат"""
        try:
            return {
                'city': 'Санкт-Петербург',
                'country': 'Россия',
                'temperature': round(api_data['main']['temp']),
                'feels_like': round(api_data['main']['feels_like']),
                'condition': api_data['weather'][0]['description'].title(),
                'wind_speed': round(api_data['wind']['speed'] * 3.6),  # м/с в км/ч
                'wind_direction': self._get_wind_direction(api_data['wind'].get('deg', 0)),
                'pressure': round(api_data['main']['pressure'] * 0.75),  # гПа в мм рт.ст.
                'humidity': api_data['main']['humidity'],
                'timestamp': datetime.now().isoformat(),
                'source': 'OpenWeatherMap API'
            }
        except KeyError as e:
            print(f"❌ Ошибка в структуре данных API: {e}")
            return self._get_demo_data()
    
    def _get_wind_direction(self, degrees):
        """Конвертирует градусы в направление ветра"""
        directions = ['С', 'ССВ', 'СВ', 'ВСВ', 'В', 'ВЮВ', 'ЮВ', 'ЮЮВ', 
                     'Ю', 'ЮЮЗ', 'ЮЗ', 'ЗЮЗ', 'З', 'ЗСЗ', 'СЗ', 'ССЗ']
        index = round(degrees / 22.5) % 16
        return directions[index]
    
    def _get_demo_data(self):
        """Возвращает демонстрационные данные"""
        import random
        
        conditions = ['Ясно', 'Переменная облачность', 'Облачно', 'Небольшой дождь', 'Снег']
        directions = ['С', 'СВ', 'В', 'ЮВ', 'Ю', 'ЮЗ', 'З', 'СЗ']
        
        return {
            'city': 'Санкт-Петербург',
            'country': 'Россия',
            'temperature': random.randint(-10, 15),
            'feels_like': random.randint(-15, 10),
            'condition': random.choice(conditions),
            'wind_speed': random.randint(5, 25),
            'wind_direction': random.choice(directions),
            'pressure': random.randint(740, 780),
            'humidity': random.randint(60, 90),
            'timestamp': datetime.now().isoformat(),
            'source': 'Demo Data'
        }
    
    def print_weather_data(self, data):
        """Красиво выводит данные о погоде"""
        if not data:
            print("❌ Нет данных для отображения")
            return
        
        print("\n" + "="*50)
        print(f"🌤️  ПОГОДА В {data['city'].upper()}")
        print("="*50)
        print(f"📅 Время: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        print(f"📡 Источник: {data['source']}")
        print("-"*50)
        
        print(f"🌡️  Температура: {data['temperature']}°C (ощущается как {data['feels_like']}°C)")
        print(f"☁️  Состояние: {data['condition']}")
        print(f"💨 Ветер: {data['wind_direction']} {data['wind_speed']} км/ч")
        print(f"🌡️  Давление: {data['pressure']} мм рт. ст.")
        print(f"💧 Влажность: {data['humidity']}%")
        
        print("="*50)
    
    def save_to_json(self, data, filename='weather_api_data.json'):
        """Сохраняет данные в JSON файл"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ Данные сохранены в {filename}")
        except Exception as e:
            print(f"❌ Ошибка при сохранении: {e}")

def main():
    """Основная функция"""
    print("🌤️ Получение погоды через OpenWeatherMap API")
    print("-" * 50)
    
    # Здесь можно указать ваш API ключ
    api_key = "demo"  # Замените на ваш ключ
    
    weather_api = OpenWeatherMapAPI(api_key)
    weather_data = weather_api.get_weather_data()
    
    if weather_data:
        weather_api.print_weather_data(weather_data)
        weather_api.save_to_json(weather_data)
        return weather_data
    else:
        print("❌ Не удалось получить данные о погоде")
        return None

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Программа прервана пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)