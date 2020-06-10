from flask import Flask, render_template, request, json
from flask import jsonify
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL

import sys
import random

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

order_id_counter = 1

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
    {'item_id': 0, 'name': 'Pizza Hawai', 'price': 3.50, 'type': "pizza", 'focus': 'kitchen'},
    {'item_id': 1, 'name': 'Pizza Salami', 'price': 4.50, 'type': "pizza", 'focus': 'kitchen'},
    {'item_id': 2, 'name': 'Pizza Pepperoni', 'price': 5.50, 'type': "pizza", 'focus': 'kitchen'},
    {'item_id': 3, 'name': 'Pizza Tonijn', 'price': 5.00, 'type': "pizza", 'focus': 'kitchen'},
    {'item_id': 4, 'name': 'Pizza Shoarma', 'price': 4.00, 'type': "pizza", 'focus': 'kitchen'},
    {'item_id': 5, 'name': 'Pizza Kebab', 'price': 4.75, 'type': "pizza", 'focus': 'kitchen'},
    {'item_id': 6, 'name': 'Broodje Kip', 'price': 2.25, 'type': "brood", 'focus': 'kitchen'},
    {'item_id': 7, 'name': 'Broodje Warmvlees', 'price': 3.00, 'type': "brood", 'focus': 'kitchen'},
    {'item_id': 8, 'name': 'Broodje Gehaktbal', 'price': 2.50, 'type': "brood", 'focus': 'kitchen'},
    {'item_id': 9, 'name': 'Broodje Shoarma', 'price': 2.75, 'type': "brood", 'focus': 'kitchen'},
    {'item_id': 10, 'name': 'Broodje Kaas', 'price': 1.75, 'type': "brood", 'focus': 'kitchen'},
    {'item_id': 11, 'name': 'Broodje Vis', 'price': 3.00, 'type': "brood", 'focus': 'kitchen'},
    {'item_id': 12, 'name': 'Broodje Hotdog', 'price': 2.50, 'type': "brood", 'focus': 'kitchen'},
    {'item_id': 13, 'name': 'Broodje Jam', 'price': 1.50, 'type': "brood", 'focus': 'kitchen'},
    {'item_id': 14, 'name': 'Koffie', 'price': 1.50, 'type': "drinken", 'focus': 'counter'},
    {'item_id': 15, 'name': 'Thee', 'price': 1.50, 'type': "drinken", 'focus': 'counter'},
]

quarks = [{'name': 'up', 'charge': '+2/3'},
          {'name': 'down', 'charge': '-1/3'},
          {'name': 'charm', 'charge': '+2/3'},
          {'name': 'strange', 'charge': '-1/3'}]

orders = []


def get_orders(table_number):
    for table in tables:
        if table['tableNumber'] == table_number:
            return table['orders']

    return []


# get the total price of a table
def get_total_price_of_table(table_number):
    price = 0
    for table in tables:
        if table['tableNumber'] == table_number:
            for orders in table['orders']:
                for item in orders:
                    if item['amount'] != 0:
                        for amount in range(0, item['amount']):
                            price += get_price(item['itemId'])

    return price


def get_price(item_id):
    for item in recipes:
        if item_id == item['item_id']:
            return item['price']

          
# add the order to the tables list
def add_order(table_number, order):

    for table in tables:
        if int(table['tableNumber']) == table_number:
            if len(table['orders']) == 0:
                table['orders'].append(order)

            else:
                for new_order in order:
                    for old_order in table['orders']:
                        for item in old_order:
                            if item['itemId'] == new_order['itemId']:
                                item['amount'] += new_order['amount']


def get_table_has_order(table_number):
    for order in orders:
        if int(order['table']) == int(table_number):
            return True

    return False


def serve_order_from_list(order_id):
    for order in orders:
        if order['order_id'] == order_id:
            orders.remove(order)


def get_waiting_order(table_number):
    for order in orders:
        if order['table'] == table_number:
            return order

    return []


@app.route('/api/get_table_info', methods=['POST'])
def return_table_info():
    data = request.get_json()

    try:
        table_number = data['table_number']
        response = jsonify({'has_order': get_table_has_order(int(table_number)),
                            'price': get_total_price_of_table(int(table_number)),
                            'waiting_orders': get_waiting_order(int(table_number)),
                            'all_orders': get_orders(int(table_number))
                           })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except NameError:
        return jsonify({'message': 'ERROR'})


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


@app.route('/api/get_current_orders', methods=['GET'])
def get_current_orders():
    response = jsonify({'orders': orders})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/api/serve_order', methods=['POST'])
def serve_order():

    data = request.get_json()

    serve_order_from_list(data['order_id'])

    response = jsonify({'message': 'OK'})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/api/get_price_of_table', methods=['POST'])
def get_price_of_table():
    data = request.get_json()

    response = jsonify({'price': get_total_price_of_table(data['table_number'])})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/api/add_new_order', methods=['POST'])
@cross_origin()
def add_new_order():
    global order_id_counter

    data = request.get_json()

    # order_id = order_id_counter + 1
    data['order_id'] = order_id_counter
    order_id_counter += 1

    orders.append(data)

    add_order(int(data['table']), data['orders'])

    response = jsonify({'message': 'OK'})
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

if __name__ == "__main__":
    app.run(debug=True)
    str = "Messi is the best soccer player"
