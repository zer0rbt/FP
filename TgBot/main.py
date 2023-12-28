import configparser

import requests
import telebot
import json
from json import dumps
import base64
from PIL import Image
from io import BytesIO

config = configparser.ConfigParser()
config.read('config.ini')

bot = telebot.TeleBot(config['DEFAULT']['TELEGRAM_TOKEN'])
telebot.logger.setLevel(telebot.logging.DEBUG)


@bot.message_handler(commands=['weather'])
def weather(message: telebot.types.Message):
    data = requests.get(
        'https://api.open-meteo.com/v1/forecast?latitude=59.93&longitude=30.31&current=temperature_2m,weather_code,wind_speed_10m').json()[
        'current']

    temperature, weather_code, wind_speed = data['temperature_2m'], data['weather_code'], data['wind_speed_10m']

    weather_conditions = {
        0: 'Clear sky',
        1: 'Mainly clear',
        2: 'Partly cloudy',
        3: 'Overcast',
        45: 'Fog',
        48: 'Rime',
        51: 'Rain',
        53: 'Rain',
        55: 'Rain',
        56: 'Rain',
        61: 'Rain',
        63: 'Rain',
        65: 'Rain',
        66: 'Rain',
        67: 'Rain',
        77: 'Snow',
        80: 'Shower',
        81: 'Shower',
        82: 'Shower',
        85: 'Snow shower',
        86: 'Snow shower'
    }

    description = weather_conditions.get(weather_code, '')

    bot.send_message(
        message.chat.id,
        f'Temperature: {temperature}°C\nWind: {wind_speed}km/h\n{description}')


@bot.message_handler(commands=['exchange'])
def exchange_rate(message: telebot.types.Message):
    data = requests.get(
        'https://iss.moex.com/iss/statistics/engines/currency/markets/selt/rates.json?iss.meta=off').json()

    usd = data['cbrf']['data'][0][3]
    eur = data['cbrf']['data'][0][6]

    bot.send_message(message.chat.id, f'RUB - USD: {usd}\nRUB - EUR: {eur}')


@bot.message_handler(commands=['gen'])
def gen(message: telebot.types.Message):
    prompt = (message.text or '').removeprefix('/gen ')

    url = "https://stablediffusionapi.com/api/v3/text2img"

    payload = json.dumps({

        "key": "", # Put here an api-key
        "prompt": f"{prompt}",
        "negative_prompt": None,
        "width": "512",
        "height": "512",
        "samples": "1",
        "num_inference_steps": "20",
        "seed": None,
        "guidance_scale": 7.5,
        "safety_checker": "yes",
        "multi_lingual": "no",
        "panorama": "no",
        "self_attention": "no",
        "upscale": "no",
        "embeddings_model": None,
        "webhook": None,
        "track_id": None
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    your_string = response.text.split('proxy_links":["')[1].split('"],')[0]


    # Декодирование строки JSON
    decoded_string = json.loads(f'"{your_string}"')

    # Извлечение ссылки
    url = decoded_string.replace('\\', '')
    print(url)
    bot.send_photo(message.chat.id, url)



@bot.message_handler(commands=['joke'])
def get_random_joke(message: telebot.types.Message):
    jokeapi_url = 'https://v2.jokeapi.dev/joke/Any'

    response = requests.get(jokeapi_url)
    data = response.json()

    if data['type'] == 'twopart':
        out = f"{data['setup']}\n{data['delivery']}"
    elif data['type'] == 'single':
        out = data['joke']
    else:
        out = "Не удалось получить шутку."

    bot.send_message(message.chat.id, out)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    bot.send_message(
        message.chat.id,
        '/weather        - Current weather\n' +
        '/gen {prompt} - Generate image w/ Stable Diffusion\n' +
        '/joke    - Random joke')


if __name__ == '__main__':
    bot.infinity_polling()
