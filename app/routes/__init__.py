from .product_routes import product_bp
# from .user_routes import user_bp
# from .order_routes import order_bp

def init_app(app):
    app.register_blueprint(product_bp)
    # app.register_blueprint(user_bp)
    # app.register_blueprint(order_bp)
