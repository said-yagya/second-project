#!/usr/bin/env python3
"""
Скрипт для получения данных о погоде в Санкт-Петербурге с AccuWeather
Получает: температуру, скорость и направление ветра, давление, влажность
"""

import requests
import json
import time
import re
from bs4 import BeautifulSoup
from datetime import datetime
import sys

class AccuWeatherScraper:
    def __init__(self):
        self.base_url = "https://www.accuweather.com"
        self.city_url = "https://www.accuweather.com/ru/ru/saint-petersburg/295212/weather-forecast/295212"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_weather_data(self):
        """Получает данные о погоде с AccuWeather"""
        try:
            print("Получение данных о погоде из AccuWeather...")
            
            # Делаем запрос к странице
            response = self.session.get(self.city_url, timeout=10)
            response.raise_for_status()
            
            # Парсим HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Извлекаем данные
            weather_data = self._extract_weather_data(soup)
            
            if weather_data:
                print("✅ Данные успешно получены!")
                return weather_data
            else:
                print("❌ Не удалось извлечь данные о погоде")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка при запросе: {e}")
            return None
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {e}")
            return None

    def _extract_weather_data(self, soup):
        """Извлекает данные о погоде из HTML"""
        try:
            weather_data = {
                'city': 'Санкт-Петербург',
                'country': 'Россия',
                'timestamp': datetime.now().isoformat(),
                'source': 'AccuWeather'
            }
            
            # Температура
            temp_element = soup.find('span', class_='temp')
            if temp_element:
                temp_text = temp_element.get_text().strip()
                temperature = re.search(r'(-?\d+)', temp_text)
                if temperature:
                    weather_data['temperature'] = int(temperature.group(1))
            
            # Ощущается как
            feels_like_element = soup.find('div', class_='real-feel')
            if feels_like_element:
                feels_text = feels_like_element.get_text().strip()
                feels_like = re.search(r'(-?\d+)', feels_text)
                if feels_like:
                    weather_data['feels_like'] = int(feels_like.group(1))
            
            # Состояние погоды
            condition_element = soup.find('span', class_='phrase')
            if condition_element:
                weather_data['condition'] = condition_element.get_text().strip()
            
            # Детали погоды
            details = self._extract_weather_details(soup)
            weather_data.update(details)
            
            return weather_data
            
        except Exception as e:
            print(f"Ошибка при извлечении данных: {e}")
            return None

    def _extract_weather_details(self, soup):
        """Извлекает детальную информацию о погоде"""
        details = {}
        
        try:
            # Ищем блок с деталями
            details_section = soup.find('div', class_='current-weather-details')
            if not details_section:
                # Альтернативный поиск
                details_section = soup.find('div', class_='current-weather-card')
            
            if details_section:
                # Ветер
                wind_element = details_section.find('span', string=re.compile(r'Ветер|Wind'))
                if wind_element:
                    wind_parent = wind_element.find_parent()
                    if wind_parent:
                        wind_text = wind_parent.get_text()
                        # Извлекаем скорость ветра
                        wind_speed = re.search(r'(\d+)\s*км/ч', wind_text)
                        if wind_speed:
                            details['wind_speed'] = int(wind_speed.group(1))
                        
                        # Извлекаем направление ветра
                        wind_dir = re.search(r'([СЮВЗ]{1,3})', wind_text)
                        if wind_dir:
                            details['wind_direction'] = wind_dir.group(1)
                
                # Давление
                pressure_element = details_section.find('span', string=re.compile(r'Давление|Pressure'))
                if pressure_element:
                    pressure_parent = pressure_element.find_parent()
                    if pressure_parent:
                        pressure_text = pressure_parent.get_text()
                        pressure = re.search(r'(\d+)\s*мм', pressure_text)
                        if pressure:
                            details['pressure'] = int(pressure.group(1))
                
                # Влажность
                humidity_element = details_section.find('span', string=re.compile(r'Влажность|Humidity'))
                if humidity_element:
                    humidity_parent = humidity_element.find_parent()
                    if humidity_parent:
                        humidity_text = humidity_parent.get_text()
                        humidity = re.search(r'(\d+)%', humidity_text)
                        if humidity:
                            details['humidity'] = int(humidity.group(1))
            
            # Если не нашли через основной метод, пробуем альтернативный
            if not details:
                details = self._extract_details_alternative(soup)
                
        except Exception as e:
            print(f"Ошибка при извлечении деталей: {e}")
        
        return details

    def _extract_details_alternative(self, soup):
        """Альтернативный метод извлечения деталей"""
        details = {}
        
        try:
            # Ищем все элементы с данными
            all_text = soup.get_text()
            
            # Ветер
            wind_match = re.search(r'Ветер[:\s]*([СЮВЗ]{1,3})[:\s]*(\d+)\s*км/ч', all_text, re.IGNORECASE)
            if wind_match:
                details['wind_direction'] = wind_match.group(1)
                details['wind_speed'] = int(wind_match.group(2))
            
            # Давление
            pressure_match = re.search(r'Давление[:\s]*(\d+)\s*мм', all_text, re.IGNORECASE)
            if pressure_match:
                details['pressure'] = int(pressure_match.group(1))
            
            # Влажность
            humidity_match = re.search(r'Влажность[:\s]*(\d+)%', all_text, re.IGNORECASE)
            if humidity_match:
                details['humidity'] = int(humidity_match.group(1))
                
        except Exception as e:
            print(f"Ошибка в альтернативном методе: {e}")
        
        return details

    def save_to_json(self, data, filename='weather_data.json'):
        """Сохраняет данные в JSON файл"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ Данные сохранены в {filename}")
        except Exception as e:
            print(f"❌ Ошибка при сохранении: {e}")

    def print_weather_data(self, data):
        """Красиво выводит данные о погоде"""
        if not data:
            print("❌ Нет данных для отображения")
            return
        
        print("\n" + "="*50)
        print(f"🌤️  ПОГОДА В {data.get('city', 'Неизвестно').upper()}")
        print("="*50)
        print(f"📅 Время: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        print(f"📡 Источник: {data.get('source', 'Неизвестно')}")
        print("-"*50)
        
        # Температура
        if 'temperature' in data:
            temp_str = f"🌡️  Температура: {data['temperature']}°C"
            if 'feels_like' in data:
                temp_str += f" (ощущается как {data['feels_like']}°C)"
            print(temp_str)
        
        # Состояние
        if 'condition' in data:
            print(f"☁️  Состояние: {data['condition']}")
        
        # Ветер
        if 'wind_speed' in data or 'wind_direction' in data:
            wind_str = "💨 Ветер: "
            if 'wind_direction' in data:
                wind_str += f"{data['wind_direction']} "
            if 'wind_speed' in data:
                wind_str += f"{data['wind_speed']} км/ч"
            print(wind_str)
        
        # Давление
        if 'pressure' in data:
            print(f"🌡️  Давление: {data['pressure']} мм рт. ст.")
        
        # Влажность
        if 'humidity' in data:
            print(f"💧 Влажность: {data['humidity']}%")
        
        print("="*50)

def main():
    """Основная функция"""
    print("🌤️ Парсер погоды AccuWeather для Санкт-Петербурга")
    print("-" * 50)
    
    scraper = AccuWeatherScraper()
    
    # Получаем данные
    weather_data = scraper.get_weather_data()
    
    if weather_data:
        # Выводим данные
        scraper.print_weather_data(weather_data)
        
        # Сохраняем в JSON
        scraper.save_to_json(weather_data)
        
        return weather_data
    else:
        print("❌ Не удалось получить данные о погоде")
        # Возвращаем тестовые данные для демонстрации
        demo_data = {
            'city': 'Санкт-Петербург',
            'country': 'Россия',
            'temperature': 5,
            'feels_like': 2,
            'condition': 'Переменная облачность',
            'wind_speed': 15,
            'wind_direction': 'СЗ',
            'pressure': 760,
            'humidity': 75,
            'timestamp': datetime.now().isoformat(),
            'source': 'Demo Data'
        }
        
        print("\n📝 Показываем демонстрационные данные:")
        scraper.print_weather_data(demo_data)
        scraper.save_to_json(demo_data, 'demo_weather_data.json')
        
        return demo_data

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Программа прервана пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)