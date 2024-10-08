from flask import Blueprint, jsonify, request
from ..models.product import Product
from .. import db

product_bp = Blueprint('product_bp', __name__)

# Obtener todos los productos
@product_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "price": p.price} for p in products])

# Crear un nuevo producto
@product_bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product created"}), 201
