from flask_jwt_extended import JWTManager
from flask import jsonify

jwt = JWTManager()


def configure_jwt(app):
    jwt.init_app(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({
            'message': 'The token has expired',
            'error': 'token_expired'
        }), 401
