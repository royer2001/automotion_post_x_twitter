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

# URL del endpoint de la API de Twitter para publicar un tweet
url = "https://api.twitter.com/2/tweets"

def post_to_twitter(content):
    """
    Función para publicar un tweet en Twitter usando OAuth 1.0a.
    """
    payload = {
        "text": content
    }

    auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)
    response = requests.post(url, json=payload, auth=auth)

    if response.status_code == 201:
        return {"message": "Tweet publicado correctamente.", "data": response.json()}
    else:
        return {"error": f"Error al publicar el tweet. Código de estado: {response.status_code}", "data": response.json()}
