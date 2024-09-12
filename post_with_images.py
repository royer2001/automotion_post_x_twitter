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

# Lista de rutas a las imágenes que quieres subir
image_paths = ["C:/Users/ADMIN/Desktop/x_post/2.jpg",
               "C:/Users/ADMIN/Desktop/x_post/3.jpg"]

# URL del endpoint para subir medios
media_url = "https://upload.twitter.com/1.1/media/upload.json"

# Lista para almacenar los media_ids
media_ids = []

# Subir cada imagen y almacenar el media_id
for image_path in image_paths:
    with open(image_path, "rb") as image_file:
        files = {"media": image_file}
        response = requests.post(media_url, files=files, auth=auth)

    # Verificar si la imagen se subió correctamente
    if response.status_code == 200:
        media_id = response.json().get("media_id_string")
        media_ids.append(media_id)
        print(f"Imagen subida correctamente. Media ID: {media_id}")
    else:
        print(f"Error al subir la imagen {image_path}. Código de estado: {response.status_code}")
        print(response.json())
        exit()

# 2. Publicar un tweet con múltiples imágenes
tweet_url = "https://api.twitter.com/2/tweets"
tweet_payload = {
    "text": "¡Este es un tweet con varias imágenes 2! :)",
    "media": {
        "media_ids": media_ids
    }
}

response = requests.post(tweet_url, json=tweet_payload, auth=auth)

# Verificar si el tweet se publicó correctamente
if response.status_code == 201:
    print("Tweet con varias imágenes publicado correctamente.")
    print(response.json())
else:
    print(f"Error al publicar el tweet. Código de estado: {response.status_code}")
    print(response.json())
