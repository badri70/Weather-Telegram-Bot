from aiogram import Bot, Dispatcher, types, executor
import requests
import json
from check_weather import map_pic_code_to_icon

BOT_TOKEN = Bot('5827305488:AAHNNCVoiZ8b0gUr9dYo1C81_HvMgyrNQvc')
API_KEY = '1bd144097b729734fec660eaf17f4a92'

dp = Dispatcher(BOT_TOKEN)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Welcome to Weather bot. Enter the name of the city where you want to know the weather.')


@dp.message_handler(content_types=['text'])
async def city_search(message: types.Message):
    city = message.text.strip().lower()
    info = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric')
    if info.status_code == 200:
        data = json.loads(info.text)
        # print(data)
        await message.reply(
            f"Currently in {message.text} {data['weather'][0]['main']}{map_pic_code_to_icon(data['weather'][0]['description'])}\nTemperature {data['main']['temp']}°C\nMin: {data['main']['temp_min']}°C\nMax: {data['main']['temp_max']}°C\nFeels like: {data['main']['feels_like']}°C"
        )
    else:
        await message.answer('Please enter correct name city')


executor.start_polling(dp)
