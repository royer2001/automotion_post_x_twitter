import os
import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)
media_url = "https://upload.twitter.com/1.1/media/upload.json"
tweet_url = "https://api.twitter.com/2/tweets"


def upload_images(image_paths):
    media_ids = []

    for image_path in image_paths:
        with open(image_path, "rb") as image_file:
            files = {"media": image_file}
            response = requests.post(media_url, files=files, auth=auth)

        # Verificar si la imagen se subió correctamente
        if response.status_code == 200:
            media_id = response.json().get("media_id_string")
            media_ids.append(media_id)
        else:
            return {
                "error": f"Error al subir la imagen {image_path}. Codigo de estado: {response.status_code}",
                "data": response.json()
            }

    return {"media_ids": media_ids}


def post_tweet_with_images(content, image_paths):

    upload_response = upload_images(image_paths)

    if "error" in upload_response:
        return upload_response
    media_ids = upload_response['media_ids']

    tweet_payload = {
        "text": content,
        "media": {
            "media_ids": media_ids
        }
    }

    response = requests.post(tweet_url, json=tweet_payload, auth=auth)

    # Verificar si el tweet se publicó correctamente
    if response.status_code == 201:
        return {
            "message": "Tweet con imagenes publicado correctamente.",
            "data": response.json()
        }
    else:
        return {
            "error": f"Error al publicar el tweet. Cogigo de estado: {response.status_code}",
            "data": response.json()
        }
