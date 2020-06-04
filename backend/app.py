from flask import Flask, json
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin
import sys

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

tables = [
    {'tableNumber': 1, 'orders': []},
    {'tableNumber': 2, 'orders': []},
    {'tableNumber': 3, 'orders': []},
    {'tableNumber': 4, 'orders': []},
    {'tableNumber': 5, 'orders': []},
    {'tableNumber': 6, 'orders': []},
    {'tableNumber': 7, 'orders': []},
    {'tableNumber': 8, 'orders': []},
    {'tableNumber': 9, 'orders': []},
    {'tableNumber': 10, 'orders': []},
]

recipes = [
    {'name': 'Pizza Hawai', 'price': 3.50, 'type': "pizza"},
    {'name': 'Pizza Salami', 'price': 4.50, 'type': "pizza"},
    {'name': 'Pizza Pepperoni', 'price': 5.50, 'type': "pizza"},
    {'name': 'Pizza Tonijn', 'price': 5.00, 'type': "pizza"},
    {'name': 'Pizza Shoarma', 'price': 4.00, 'type': "pizza"},
    {'name': 'Pizza Kebab', 'price': 4.75, 'type': "pizza"},
    {'name': 'Broodje Kip', 'price': 2.25, 'type': "brood"},
    {'name': 'Broodje Warmvlees', 'price': 3.00, 'type': "brood"},
    {'name': 'Broodje Gehaktbal', 'price': 2.50, 'type': "brood"},
    {'name': 'Broodje Shoarma', 'price': 2.75, 'type': "brood"},
    {'name': 'Broodje Kaas', 'price': 1.75, 'type': "brood"},
    {'name': 'Broodje Vis', 'price': 3.00, 'type': "brood"},
    {'name': 'Broodje Hotdog', 'price': 2.50, 'type': "brood"},
    {'name': 'Broodje Jam', 'price': 1.50, 'type': "brood"},
    {'name': 'Koffie', 'price': 1.50, 'type': "drinken"},
    {'name': 'Thee', 'price': 1.50, 'type': "drinken"},
]

quarks = [{'name': 'up', 'charge': '+2/3'},
          {'name': 'down', 'charge': '-1/3'},
          {'name': 'charm', 'charge': '+2/3'},
          {'name': 'strange', 'charge': '-1/3'}]

orders = []


@app.route('/api/get_all_products', methods=['GET'])
def return_all():
    response = jsonify({'products': recipes})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/api/get_all_tables', methods=['GET'])
def return_all_tables():
    response = jsonify({'tables': tables})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


'''
@app.route('/api/get_one_product/<string:name>', methods=['GET'])
def return_one(name):
    the_one = quarks[0]
    for i, q in enumerate(quarks):
        if q['name'] == name:
            the_one = quarks[i]
    return jsonify({'quarks': the_one})


@app.route('/api/add_product', methods=['POST'])
def add_one():
    new_quark = request.get_json()
    quarks.append(new_quark)
    return jsonify({'quarks': quarks})


@app.route('/api/edit_product/<string:name>', methods=['PUT'])
def edit_one(name):
    new_quark = request.get_json()
    for i, q in enumerate(quarks):
        if q['name'] == name:
            quarks[i] = new_quark
    qs = request.get_json()
    return jsonify({'quarks': quarks})


@app.route('/api/delete_product/<string:name>', methods=['DELETE'])
def delete_one(name):
    for i, q in enumerate(quarks):
        if q['name'] == name:
            del quarks[i]
    return jsonify({'quarks': quarks})


@app.route('/api/get_products_by_type/<string:type>', methods=['GET'])
def get_recipes_by_type(type):
    recipe_list = []
    for i, q in enumerate(recipes):
        if q['type'] == type:
            recipe_list.append(q)

    return jsonify({'recipes': recipe_list})


@app.route('/api/get_product_by_name/<string:name>', methods=['GET'])
def get_recipes_by_name(name):
    recipe_list = []
    for i, q in enumerate(recipes):
        if name.find(q['name']) > -1:
            recipe_list.append(q)

    return jsonify({'recipes': recipe_list})


@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    return jsonify({'recipes': recipes})

'''
@app.route('/api/add_new_order', methods=['POST'])
@cross_origin()
def add_new_order():
    data = request.get_json()
    print(data)
    orders.append(data)
    response = jsonify({'message': 'OK'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    app.run(debug=True)
    str = "Messi is the best soccer player"
