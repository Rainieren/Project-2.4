import jwt
import datetime
import jwt
import datetime
from flask_cors import CORS

from backend.database import *
from flask import Flask, request, Response, jsonify, make_response
from flask_mysqldb import MySQL
import json
import time
import requests

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'restaurantdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

state = "startup";
mysql = MySQL(app)
# JWT
app.config['SECRET_KEY'] = 'thisistheverysecretkeythatnooneshouldeverfind'  # nog te veranderen
database = Database(app, mysql)

users = [
    {'id': 1, 'role': 'counter', 'password': 'counter'},
    {'id': 2, 'role': 'keuken', 'password': 'keuken'},
    {'id': 3, 'role': 'serveerder', 'password': 'serveerder'},
]

@app.route('/database/startup')
def startup():
    cur = mysql.connection.cursor()
    cur.execute('''CREATE TABLE `recipes` (
            `recipeID` int(11) unsigned NOT NULL AUTO_INCREMENT,
            `recipeName` varchar(45) NOT NULL,
            `recipePrice` varchar(45) NOT NULL,
            PRIMARY KEY (`recipeID`),
            UNIQUE KEY `recipeName_UNIQUE` (`recipeName`));
            ''')
    cur.execute('''ALTER TABLE `restaurantdb`.`recipes` ADD COLUMN `recipeFocus` VARCHAR(45) NULL AFTER `recipeType`;''')
    cur.execute('''ALTER TABLE `restaurantdb`.`recipes` 
            ADD COLUMN `recipeType` VARCHAR(45) NULL AFTER `recipePrice`;''')
    cur.execute('''CREATE TABLE `restaurantdb`.`tables` (
            `tableID` int(11) unsigned NOT NULL AUTO_INCREMENT,
            `tableStatus` varchar(45) NOT NULL,
            PRIMARY KEY (`tableID`));''')
    cur.execute('''CREATE TABLE `restaurantdb`.`orders` (
            `orderID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
            `orderDate` DATE NOT NULL,
            `tableID` INT UNSIGNED NOT NULL,
            PRIMARY KEY (`orderID`),
            FOREIGN KEY (`tableID`) references tables(`tableID`));''')
    cur.execute('''ALTER TABLE `restaurantdb`.`orders` 
            ADD COLUMN `orderStatus` VARCHAR(45) NOT NULL AFTER `tableID`;''')
    cur.execute('''CREATE TABLE `restaurantdb`.`orderdetails` (
            `orderID` INT UNSIGNED NOT NULL,
            `recipeID` INT UNSIGNED NOT NULL,
            `quantity` INT(10) NOT NULL,
            `servingStatus` varchar(45) DEFAULT NULL,
            FOREIGN KEY (`orderID`) references orders(`orderID`),
            FOREIGN KEY (`recipeID`) references recipes(`recipeID`));''')

@app.route('/database/insert', methods=['PUT'])
def initialize():
    cur = mysql.connection.cursor()
    cur.execute('''INSERT INTO tables(tableID, tableStatus) VALUES 
                (1, "FREE"),
                (2, "FREE"),
                (3, "FREE"),
                (4, "FREE"),
                (5, "FREE")''')
    cur.execute('''INSERT INTO recipes(recipeName, recipePrice, recipeType) VALUES 
                ("Pizza Hawai", 3.50, "Pizza"),
                ("Pizza Salami", 4.50, "Pizza"),
                ("Pizza Pepperoni", 3.50, "Pizza"),
                ("Pizza Tonijn", 4.25, "Pizza"),
                ("Pizza Kebab", 3.00, "Pizza"),
                ("Pizza Shoarma", 3.75, "Pizza"),
                ("Pizza Kip", 5.00, "Pizza"),
                ("Broodje Kip", 3.50, "Broodje"),
                ("Broodje Warmvlees", 3.50, "Broodje"),
                ("Broodje Gehaktbal", 3.50, "Broodje"),
                ("Broodje Shoarma", 3.50, "Broodje"),
                ("Broodje Jam", 3.50, "Broodje"),
                ("Broodje Hotdog", 3.50, "Broodje")        
                ''')
    cur.execute('''INSERT INTO orders(orderDate, tableID) VALUES
                (curdate(),  (SELECT tableID from tables WHERE tableID = '1')),
                (curdate(),  (SELECT tableID from tables WHERE tableID = '4')),
                (curdate(),  (SELECT tableID from tables WHERE tableID = '2')),
                (curdate(),  (SELECT tableID from tables WHERE tableID = '3')),
                (curdate(),  (SELECT tableID from tables WHERE tableID = '2')),
                (curdate(),  (SELECT tableID from tables WHERE tableID = '3')),
                (curdate(),  (SELECT tableID from tables WHERE tableID = '1')),
                (curdate(),  (SELECT tableID from tables WHERE tableID = '2'))
                ''')
    mysql.connection.commit()

#RECIPES
#RECIPES

#http://127.0.0.1:5000/database/recipe
@app.route('/database/recipe', methods=['POST'])
def new_recipe():
    data = request.get_json()
    name = data['name']
    price = data['price']
    type = data['type']
    focus = data['focus']
    database.insertRecipe(name, price, type, focus)
    return "succes"

@app.route('/database/recipe/<string:recipeID>', methods=['GET'])
def recipe(recipeID):
    results = database.getRecipeByRecipeID(recipeID)
    return jsonify(results)

#Returns information of all recipes.
@app.route('/database/recipes', methods=['GET', 'POST'])
def recipes():
    if(request.method == "GET"):
        response = jsonify({'recipes': database.getRecipes()})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    if(request.method == "POST"):
        data = request.get_json()
        searchterm = data['searchterm']
        results = database.getRecipesByName(searchterm)
        response = jsonify(results)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

#ORDERS
#ORDERS

#Returns basic order information such as ID, DATE and TableID
@app.route('/database/order/<string:ID>', methods=['GET'])
def order(ID):
    results = database.getOrderByID(ID)
    return jsonify(results)

#make a new order by using link/order
@app.route('/database/order', methods=['POST'])
def new_order():
    data = request.get_json()
    tableid = data['tableid']
    orderid = database.insertOrder(tableid)
    return jsonify({"orderid": orderid})

#Returns all orders with basic information such as ID, DATE and TableID
@app.route('/database/orders', methods=['GET'])
def orders():
    results = database.getAllOrders()
    return jsonify(results)

#Returns all orders with more in dept information such as ID, DATE, TableID and corresponding recipes with RecipeID and quanitity.
#If order has no servings doesn't show up in list.
@app.route('/database/orders/overview', methods=['GET'])
def orders_overview():
    results = database.getOpenOrders()
    return jsonify(results)

@app.route('/database/order/<string:orderid>/price', methods=['GET'])
def get_price_order(orderid):
    results = database.getPriceOfOrder(orderid)
    return jsonify(results)

#SERVINGS
#SERVINGS

#Returns a more in dept information about an order such as ID, DATE, TableID and corresponding recipes with RecipeID and quanitity.
#If order has no recipes added returns nothing.
@app.route('/database/order/<string:orderID>/servings', methods=['GET', 'POST'])
def order_servings(orderID):
    if(request.method == "GET"):
        results = database.getOrderDetails(orderID)
        print(results)
        return jsonify(results)
    if(request.method == "POST"):
        data = request.get_json()
        recipeID = data['recipeID']
        quantity = data['quantity']
        database.addToOrder(recipeID, orderID, quantity)

@app.route('/database/order/<string:orderID>/servings/<string:state>', methods=['GET', 'POST', 'PUT'])
def open_order_servings(orderID, state):
    if(request.method == "PUT"):
        data = request.get_json()
        recipeID = data['recipeID']
        quantity = data['quantity']
        database.setServingStatus(orderID, recipeID, quantity, state)
        return "succes"
    if(request.method == "POST"):
        data = request.get_json()
        focus = data['focus']
        results = database.getServingsByOrderID(orderID, focus, state)
        return jsonify({"orders": results})
    if(request.method == "GET"):
        results = database.getServingsByOrderID(orderID, 'all', state)
        return jsonify({"orders": results})

#TABLES
#TABLES

@app.route('/database/tables', methods=['GET'])
def tables():
    response = jsonify({'tables':database.getTables()})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/database/table/<string:tableid>', methods=['GET', 'PUT'])
def table(tableid):
    if(request.method == "GET"):
        result = database.getTableByID(tableid)
        return jsonify(result)
    if(request.method == "PUT"):
        data = request.get_json()
        tableStatus = data['tableStatus']
        database.setTableStatus(tableid, tableStatus)
        return tables()

@app.route('/database/table/<string:tableid>/servings/<string:state>', methods=['GET'])
def get_servings_table(tableid, state):
    results = database.getServingsOfTableByTableID(tableid, state)
    return jsonify(results)

#JWT
#JWT

@app.route('/database/auth', methods=['GET', 'POST'])
def auth():
    # checking if request contains JSON
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    # setting role
    role = request.json.get('role', None)

    # searching if user exists
    for i, j in enumerate(users):
        if (role == j['role']):
            # when user existst, store user in 'user'
            user = users[i]
            # check if password is correct
            if user['password'] == request.json.get('password', None):
                # if so, generate and return token
                token = jwt.encode({'id': user['id'], 'role': role,
                                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                                   app.config['SECRET_KEY'])
                return jsonify({'token': token.decode('UTF-8')})

    # else, return error
    return make_response('Could not verify', 401)




'''SELECT * FROM orders o JOIN orderdetails details ON o.orderID = details.orderID

INSERT INTO orderdetails(orderID, quantity, recipeID) VALUES
                (1, 20, 1);

SELECT orders.orderID, orderDate, tableID, orderdetails.quantity, orderdetails.recipeID
FROM orders
INNER JOIN orderdetails 
   ON orderdetails.orderID = orders.orderID'''

if __name__ == "__main__":
    app.run(debug=True)