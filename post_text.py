import os
import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener las credenciales de la API desde las variables de entorno
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

# Configurar la autenticación OAuth 1.0a
auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)

# URL del endpoint de la API de Twitter para publicar un tweet
url = "https://api.twitter.com/2/tweets"

# El contenido del tweet
payload = {
    "text": "¡Este es un tweet automatizado usando requests test 3"
}

# Realizar la solicitud POST a la API de Twitter con OAuth 1.0a
response = requests.post(url, json=payload, auth=auth)

# Verificar la respuesta
if response.status_code == 201:
    print("Tweet publicado correctamente.")
    print(response.json())
else:
    print(f"Error al publicar el tweet. Código de estado: {response.status_code}")
    print(response.json())
