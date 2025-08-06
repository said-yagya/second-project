// Конфигурация
const CONFIG = {
    // Используем OpenWeatherMap API как альтернативу AccuWeather
    // Для production нужно получить свой API ключ на openweathermap.org
    API_KEY: 'demo_key', // Замените на ваш API ключ
    CITY: 'Saint Petersburg',
    COUNTRY_CODE: 'RU',
    UNITS: 'metric'
};

// Элементы DOM
const elements = {
    loading: document.getElementById('loading'),
    weatherData: document.getElementById('weatherData'),
    error: document.getElementById('error'),
    temperature: document.getElementById('temperature'),
    feelsLike: document.getElementById('feelsLike'),
    condition: document.getElementById('condition'),
    windSpeed: document.getElementById('windSpeed'),
    windDirection: document.getElementById('windDirection'),
    pressure: document.getElementById('pressure'),
    humidity: document.getElementById('humidity'),
    lastUpdate: document.getElementById('lastUpdate'),
    refreshBtn: document.getElementById('refreshBtn')
};

// Направления ветра
const windDirections = {
    N: 'С', NNE: 'ССВ', NE: 'СВ', ENE: 'ВСВ',
    E: 'В', ESE: 'ВЮВ', SE: 'ЮВ', SSE: 'ЮЮВ',
    S: 'Ю', SSW: 'ЮЮЗ', SW: 'ЮЗ', WSW: 'ЗЮЗ',
    W: 'З', WNW: 'ЗСЗ', NW: 'СЗ', NNW: 'ССЗ'
};

// Функция для получения направления ветра по градусам
function getWindDirection(degrees) {
    const directions = ['С', 'ССВ', 'СВ', 'ВСВ', 'В', 'ВЮВ', 'ЮВ', 'ЮЮВ', 'Ю', 'ЮЮЗ', 'ЮЗ', 'ЗЮЗ', 'З', 'ЗСЗ', 'СЗ', 'ССЗ'];
    const index = Math.round(degrees / 22.5) % 16;
    return directions[index];
}

// Функция для перевода состояния погоды
function translateCondition(condition) {
    const translations = {
        'clear sky': 'Ясно',
        'few clouds': 'Малооблачно',
        'scattered clouds': 'Переменная облачность',
        'broken clouds': 'Облачно',
        'overcast clouds': 'Пасмурно',
        'shower rain': 'Ливень',
        'rain': 'Дождь',
        'thunderstorm': 'Гроза',
        'snow': 'Снег',
        'mist': 'Туман',
        'fog': 'Туман',
        'haze': 'Дымка'
    };
    return translations[condition.toLowerCase()] || condition;
}

// Функция для показа состояния загрузки
function showLoading() {
    elements.loading.style.display = 'block';
    elements.weatherData.style.display = 'none';
    elements.error.style.display = 'none';
    elements.refreshBtn.disabled = true;
}

// Функция для показа данных о погоде
function showWeatherData(data) {
    elements.loading.style.display = 'none';
    elements.weatherData.style.display = 'block';
    elements.error.style.display = 'none';
    elements.refreshBtn.disabled = false;
    
    // Обновляем данные
    elements.temperature.textContent = `${Math.round(data.main.temp)}°C`;
    elements.feelsLike.textContent = `${Math.round(data.main.feels_like)}°C`;
    elements.condition.textContent = translateCondition(data.weather[0].description);
    elements.windSpeed.textContent = Math.round(data.wind.speed * 3.6); // м/с в км/ч
    elements.windDirection.textContent = getWindDirection(data.wind.deg);
    elements.pressure.textContent = `${Math.round(data.main.pressure * 0.75)} мм рт. ст.`; // гПа в мм рт. ст.
    elements.humidity.textContent = `${data.main.humidity}%`;
    
    // Обновляем время последнего обновления
    const now = new Date();
    elements.lastUpdate.textContent = now.toLocaleTimeString('ru-RU', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Функция для показа ошибки
function showError() {
    elements.loading.style.display = 'none';
    elements.weatherData.style.display = 'none';
    elements.error.style.display = 'block';
    elements.refreshBtn.disabled = false;
}

// Функция для получения данных о погоде (демо-версия)
async function fetchWeatherData() {
    // В демо-версии возвращаем тестовые данные
    // В реальной версии здесь был бы запрос к API
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve({
                main: {
                    temp: Math.round(Math.random() * 20 - 5), // от -5 до 15°C
                    feels_like: Math.round(Math.random() * 20 - 5),
                    pressure: 1013 + Math.round(Math.random() * 40 - 20), // 993-1033 гПа
                    humidity: 50 + Math.round(Math.random() * 40) // 50-90%
                },
                weather: [{
                    description: ['clear sky', 'few clouds', 'scattered clouds', 'overcast clouds', 'rain', 'snow'][Math.floor(Math.random() * 6)]
                }],
                wind: {
                    speed: Math.round(Math.random() * 10 + 2), // 2-12 м/с
                    deg: Math.round(Math.random() * 360) // 0-360°
                }
            });
        }, 1500);
    });
}

// Альтернативная функция для получения реальных данных через OpenWeatherMap API
async function fetchRealWeatherData() {
    try {
        const url = `https://api.openweathermap.org/data/2.5/weather?q=${CONFIG.CITY},${CONFIG.COUNTRY_CODE}&appid=${CONFIG.API_KEY}&units=${CONFIG.UNITS}&lang=ru`;
        
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Ошибка при получении данных о погоде:', error);
        throw error;
    }
}

// Функция для получения данных через прокси (для обхода CORS)
async function fetchWeatherWithProxy() {
    try {
        // Используем публичный прокси для демонстрации
        const proxyUrl = 'https://api.allorigins.win/raw?url=';
        const weatherUrl = `https://api.openweathermap.org/data/2.5/weather?q=${CONFIG.CITY},${CONFIG.COUNTRY_CODE}&appid=${CONFIG.API_KEY}&units=${CONFIG.UNITS}&lang=ru`;
        
        const response = await fetch(proxyUrl + encodeURIComponent(weatherUrl));
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Ошибка при получении данных через прокси:', error);
        throw error;
    }
}

// Основная функция для загрузки погоды
async function loadWeather() {
    showLoading();
    
    try {
        // Пробуем получить реальные данные, если не получается - используем демо
        let weatherData;
        
        if (CONFIG.API_KEY !== 'demo_key') {
            // Если есть настоящий API ключ
            try {
                weatherData = await fetchRealWeatherData();
            } catch (error) {
                console.log('Не удалось получить реальные данные, используем прокси...');
                weatherData = await fetchWeatherWithProxy();
            }
        } else {
            // Демо-режим
            console.log('Демо-режим: используются тестовые данные');
            weatherData = await fetchWeatherData();
        }
        
        showWeatherData(weatherData);
        
    } catch (error) {
        console.error('Ошибка загрузки погоды:', error);
        showError();
    }
}

// Функция для автоматического обновления каждые 10 минут
function startAutoRefresh() {
    setInterval(loadWeather, 10 * 60 * 1000); // 10 минут
}

// Инициализация приложения
function init() {
    // Загружаем погоду при старте
    loadWeather();
    
    // Запускаем автообновление
    startAutoRefresh();
    
    console.log('Приложение погоды запущено!');
    console.log('Для использования реальных данных:');
    console.log('1. Получите API ключ на https://openweathermap.org/api');
    console.log('2. Замените CONFIG.API_KEY на ваш ключ');
}

// Запускаем приложение когда DOM загружен
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}