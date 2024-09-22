import os
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from ..models.post import Post
from .. import db
from ..services.twitter_service import post_to_twitter
from ..services.twitter_media_service import post_tweet_with_images
from flask_jwt_extended import jwt_required

UPLOAD_FOLDER = 'tmp/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

post_bp = Blueprint('post_bp', __name__)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@post_bp.route('/posts', methods=['GET'])
@jwt_required()
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
@jwt_required()
def create_post():
    content = request.form.get('content')

    image_paths = []

    if 'images' in request.files:
        files = request.files.getlist('images')

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                image_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(image_path)
                image_paths.append(image_path)

    if image_paths:
        result = post_tweet_with_images(content, image_paths)
    else:
        result = post_to_twitter(content)
    
    for path in image_paths:
        if os.path.exists(path):
            os.remove(path)

    new_post = Post(content=content, images=image_paths)
    db.session.add(new_post)
    db.session.commit()

    if "error" in result:
        return jsonify(result), 400

    return jsonify({"message": "Post created", "twitter_response": result}), 201
