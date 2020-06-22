from backend.database import *
from flask import Flask, request, Response
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'restaurantdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

state = "startup";
mysql = MySQL(app)

database = Database(app, mysql)

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
    cur.execute('''CREATE TABLE `restaurantdb`.`orderdetails` (
            `orderID` INT UNSIGNED NOT NULL,
            `recipeID` INT UNSIGNED NOT NULL,
            `quantity` DECIMAL(6,2) NOT NULL,
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


#Returns information about all recipes matching partially with the given name.
@app.route('/database/recipes_results/<string:name>', methods=['GET'])
def recipes_results(name):
    results = database.getRecipesByName(name)
    return str(results)


#Returns information of all recipes.
@app.route('/database/recipes', methods=['GET'])
def recipes():
    results = database.getRecipes()
    return str(results)


#Returns a more in dept information about an order such as ID, DATE, TableID and corresponding recipes with RecipeID and quanitity.
#If order has no recipes added returns nothing.
@app.route('/database/order_overview/<string:ID>', methods=['GET'])
def order_overview(ID):
    results = database.getOrderOverviewByID(ID)
    return str(results)


#Returns all orders with more in dept information such as ID, DATE, TableID and corresponding recipes with RecipeID and quanitity.
#If order has no recipes doesn't show up in list.
@app.route('/database/orders_overview', methods=['GET'])
def orders_overview():
    results = database.getOrdersOverview()
    return str(results)


#Returns all orders with basic information such as ID, DATE and TableID
@app.route('/database/orders', methods=['GET'])
def orders():
    results = database.getOrders()
    return str(results)


#make a new order by using link/neworder?table=number
@app.route('/database/new_order', methods=['GET'])
def new_order():
    table = request.args.get('table')
    database.insertOrder(table)
    return str("Order has been made!")


#http://127.0.0.1:5000/database/order/NUMBER
#Returns basic order information such as ID, DATE and TableID
@app.route('/database/order/<string:ID>', methods=['GET'])
def order(ID):
    results = database.getOrderByID(ID)
    return str(results)

#http://127.0.0.1:5000/database/new_recipe?name=NAAM&price=GETAL&type=SOORT
@app.route('/database/new_recipe')
def new_recipe():
    name = request.args.get('name')
    price = request.args.get('price')
    type = request.args.get('type')
    database.insertRecipe(name, price, type)
    return recipes_results(name)

#http://127.0.0.1:5000/database/add_to_order?recipeid=NUMBER&orderid=NUMBER&quantity=NUMBER
@app.route('/database/add_to_order')
def add_to_order():
    recipeID = request.args.get('recipeid')
    orderID = request.args.get('orderid')
    quantity = request.args.get('quantity')
    database.addToOrder(recipeID, orderID, quantity)
    return order_overview(orderID)

#http://127.0.0.1:5000/database/change_table_status?status=STATUS&tableid=NUMBER
@app.route('/database/change_table_status')
def change_table_status():
    tableID = request.args.get('tableid')
    status = request.args.get('status')
    database.setTableStatus(tableID, status)
    return tables()

@app.route('/database/tables')
def tables():
    return str(database.getTables())



'''SELECT * FROM orders o JOIN orderdetails details ON o.orderID = details.orderID

INSERT INTO orderdetails(orderID, quantity, recipeID) VALUES
                (1, 20, 1);

SELECT orders.orderID, orderDate, tableID, orderdetails.quantity, orderdetails.recipeID
FROM orders
INNER JOIN orderdetails 
   ON orderdetails.orderID = orders.orderID'''

if __name__ == "__main__":
    app.run(debug=True)