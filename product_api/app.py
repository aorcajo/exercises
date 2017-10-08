from datetime import datetime

from flask import Flask, jsonify, abort, make_response, url_for, request
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import case
from marshmallow import Schema, fields, pre_load


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


# MODELS

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender_names = db.Column(db.Text)
    category_names = db.Column(db.Text)
    currency = db.Column(db.Text)
    size_infos = db.Column(db.Text)
    country_code = db.Column(db.Text)
    title = db.Column(db.Text)
    base_sku = db.Column(db.Text)
    _current_price_value = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)
    brand = db.Column(db.Text)
    image_urls = db.Column(db.Text)
    description_text = db.Column(db.Text)
    _original_price_value = db.Column(db.Float)
    url = db.Column(db.Text)
    color_name = db.Column(db.Text)
    identifier = db.Column(db.Text)

    @hybrid_property
    def discount(self):
        return 1 -  (self._current_price_value / self._original_price_value)

    @hybrid_property
    def discounted(self):
        return self._original_price_value - self._current_price_value


class ProductSchema(Schema):
    gender_names = fields.Str()
    category_names = fields.Str()
    currency = fields.Str()
    size_infos = fields.Str()
    country_code = fields.Str()
    title = fields.Str()
    base_sku = fields.Str()
    _current_price_value = fields.Float()
    timestamp = fields.DateTime(format='%Y-%m-%d %H:%M:%S.%f')
    brand = fields.Str()
    image_urls = fields.Str()
    description_text = fields.Str()
    _original_price_value = fields.Float()
    url = fields.Str()
    color_name = fields.Str()
    identifier = fields.Str()
    uri = fields.Method('format_uri')

    @pre_load
    def format_uri(self, product):
        return url_for('get_product', product_id=product.id, _external=True)


product_schema = ProductSchema()


# API
order_list = ('price', '-price', 'discount', '-discount', 'discounted', '-discounted')

@app.route('/product', methods=['GET'])
def get_products():
    products = Product.query#Product.id)

    # Order
    order_arg = request.args.get('order', '')
    if order_arg and order_arg in order_list:
        if order_arg == 'price':
            products = products.order_by(Product._current_price_value)

        elif order_arg == '-price':
            products = products.order_by(-Product._current_price_value)

        elif order_arg == 'discount':
            products = products.order_by(-Product.discount)

        elif order_arg == '-discount':
            products = products.order_by(Product.discount)

        elif order_arg == 'discounted':
            products = products.order_by(-Product.discounted)

        elif order_arg == '-discount':
            products = products.order_by(Product.discounted)

    # Filter by color_name
    color_arg = request.args.get('color', None)
    if color_arg is not None:
        products = products.filter(Product.color_name.like('%' + color_arg + '%'))

    # Get product count arg, by default=20
    count_arg = request.args.get('count', '20')
    products = products.limit(int(count_arg))

    return jsonify({'products': [product_schema.dump(product).data['uri'] for product in products.all()]})


@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.filter_by(id=product_id).first_or_404()
    product_result = product_schema.dump(product)
    return jsonify({'product': product_result.data})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    manager.run()
