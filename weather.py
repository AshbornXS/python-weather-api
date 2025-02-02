import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Dicionário de ícones para condições climáticas
WEATHER_ICONS = {
    "céu limpo": "",
    "algumas nuvens": "",
    "nuvens dispersas": "",
    "nublado": "",
    "chuva leve": "",
    "chuva forte": "",
    "trovoadas": "",
    "neve": "",
    "névoa": "",
    "nublado encoberto": "",
    "chuva moderada": "",
}

# URL base da API do OpenWeatherMap
OPENWEATHERMAP_API_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/weather', methods=['GET'])
def get_weather():
    """
    Endpoint para obter informações climáticas de uma cidade específica.
    """
    api_key = request.args.get('key', default='', type=str)
    city = request.args.get('city', default='', type=str)

    # Validação dos parâmetros
    if not api_key or not city:
        return jsonify({"error": "API key and city are required"}), 400

    try:
        # Faz a requisição à API do OpenWeatherMap
        response = requests.get(
            OPENWEATHERMAP_API_URL,
            params={
                "q": city,
                "appid": api_key,
                "units": "metric",
                "lang": "pt_br"
            }
        )
        response.raise_for_status()  # Lança uma exceção para códigos de status HTTP 4xx/5xx
        data = response.json()

        # Extrai informações do JSON
        weather_description = data['weather'][0]['description']
        temp = int(data['main']['temp'])

        # Obtém o ícone correspondente à condição climática
        weather_icon = WEATHER_ICONS.get(weather_description, "🌈")

        # Formata a resposta
        weather_info = f"Current weather: {weather_description} {weather_icon}  {temp}°C"
        return jsonify({"weather_info": weather_info})

    except requests.exceptions.RequestException as e:
        # Trata erros de requisição
        return jsonify({"error": f"Failed to fetch weather data: {str(e)}"}), 500
    except KeyError as e:
        # Trata erros de chave ausente no JSON
        return jsonify({"error": f"Unexpected response format: {str(e)}"}), 500

if __name__ == '__main__':
    # Configurações do Flask
    app.run(host='0.0.0.0', port=8089, debug=os.getenv('FLASK_DEBUG', 'False') == 'True')
