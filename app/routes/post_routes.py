from flask import Blueprint, jsonify, request
from ..models.post import Post
from .. import db
from ..services.twitter_service import post_to_twitter  # Importar el servicio

post_bp = Blueprint('post_bp', __name__)

# Obtener todos los productos
@post_bp.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([
        {
            "id": p.id,
            "content": p.content,
            "images": p.images,
            "created_at": p.created_at
        }
        for p in posts
    ])

# Crear un nuevo producto
@post_bp.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()

    content = data.get('content', None)
    images = data.get('images', None)

    # Llamar a la API de Twitter usando el servicio de Twitter
    if content:
        result = post_to_twitter(content)
        if "error" in result:
            return jsonify(result), 400

    new_post = Post(content=content, images=images)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({"message": "Post created", "twitter_response": result}), 201
