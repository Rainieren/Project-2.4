from flask import Flask, request
from flask import jsonify
from flask import request
from flask import make_response
import jwt
import datetime
from flask_cors import CORS, cross_origin
from backend.database import *
app = Flask(__name__)

CORS(app)
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'restaurantdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['CORS_HEADERS'] = 'Content-Type'
mysql = MySQL(app)

database = Database(app, mysql)

class Table:
    def __init__(self, tableID):
        self.tableID = tableID
        self.tableStatus = "free"
        self.order = 0

    def setStatus(self, status):
        self.tableStatus = status

    def addOrderToTable(self, order):
        self.order.append(order)
        self.tableStatus = "taken"

    def removeOrder(self):
        self.order = 0
        self.tableStatus = "free"

    def getTableID(self):
        return self.tableID

    def getOrder(self):
        return self.order

    def getTableStatus(self):
        return self.tableStatus

    def getPriceTable(self):

        if(self.order != 0):
            self.order.getOrderTotal()





class Order:
    def __init__(self, tableID, database):
        self.orderID = database.insertOrder(tableID)
        self.orderStatus = "open"
        self.database = database

    def hasBeenPaid(self):
        self.orderStatus = "paid"
        database.setOrderStatus(self.orderID, self.orderStatus)

    def addToOrder(self, recipeID, quantity):
        database.addToOrder(recipeID, self.orderID, quantity)

    def getOrderOverview(self):
        return database.getOrderDetails(self.orderID)

    def getOrderTotal(self):
        result = database.getOrderDetails(self.orderID)
        for x in result:
            print(x)
        return result

    def getOrderID(self):
        return self.orderID


@app.route('/')
def testing():
    list = []
    order = Order(5, database)
    order1 = Order(4, database)
    order2 = Order(2, database)
    order3 = Order(3, database)
    list.append(order)
    list.append(order1)
    list.append(order2)
    list.append(order3)
    print(list)


    #order.addToOrder(27, 20)
    results = order.getOrderOverview()
    return orders_overview()

@app.route('/database/orders_overview', methods=['GET'])
def orders_overview():
    results = database.getAllOrders()
    return str(results)


if __name__ == "__main__":
    app.run(debug=True)



