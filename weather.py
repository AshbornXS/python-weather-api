import requests
from flask import Flask, request

app = Flask(__name__)

weather_icons = {
    "céu limpo": "",
    "algumas nuvens": "",
    "nuvens dispersas": "",
    "nublado": "",  # "broken clouds" geralmente se refere a céu parcialmente nublado
    "chuva leve": "",  # "shower rain" é chuva rápida e intermitente
    "chuva forte": "",
    "trovoadas": "",
    "neve": "",
    "névoa": "",
    "nublado encoberto": "",  # "overcast clouds" refere-se a céu totalmente nublado
    "chuva moderada": "",
}

@app.route('/weather', methods=['GET'])
def get_weather():
    api_key = requests.args.get('key', default='', type=str)
    city = request.args.get('city', default='', type=str)  # Obtém a cidade da URL do request

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=pt_br"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather_description = data['weather'][0]['description']
        temp = int(data['main']['temp'])

        weather_icon = weather_icons.get(weather_description, "🌈")

        weather_info = f"Current weather:{weather_description} {weather_icon}  {temp}°Cend1"
        return weather_info
    else:
        return "City not found"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8089)
