from flask import Flask, request, Response
from flask_mysqldb import MySQL

class Database:
    def __init__(self, app, mysql):
        self.app = app
        self.mysql = mysql

    def setTableStatus(self, table, status):
        cur = self.mysql.connection.cursor()
        select_statement = '''UPDATE tables SET tableStatus = %(emp_status)s WHERE tableID = %(emp_tableid)s;'''
        cur.execute(select_statement, {'emp_status': status, 'emp_tableid': table})
        self.mysql.connection.commit()

    def insertRecipe(self, name, price, type):
        cur = self.mysql.connection.cursor()
        select_statement = '''INSERT INTO recipes(recipeName, recipePrice, recipeType) VALUES (%(emp_name)s, %(emp_price)s, %(emp_type)s)'''
        cur.execute(select_statement, {'emp_name': name, 'emp_price': price, 'emp_type': type})
        self.mysql.connection.commit()

    def insertOrder(self, table):
        cur = self.mysql.connection.cursor()
        select_statement = '''INSERT INTO orders(orderDate, tableID) VALUES (curdate(),  %(emp_no)s)'''
        cur.execute(select_statement, {'emp_no': table})
        self.mysql.connection.commit()

    def updateDatabase(self):
        return False

    def addToOrder(self, recipeID, orderID, quantity):
        cur = self.mysql.connection.cursor()
        select_statement = '''INSERT INTO orderdetails(orderID, quantity, recipeID) VALUES (%(emp_orderid)s, %(emp_quantity)s, %(emp_recipeid)s)'''
        cur.execute(select_statement, {'emp_orderid': orderID, 'emp_quantity': quantity, 'emp_recipeid': recipeID})
        self.mysql.connection.commit()

    def getResults(self, table):
        cur = self.mysql.connection.cursor()
        select_statement = '''SELECT * FROM %(emp_no)s)'''
        cur.execute(select_statement, {'emp_no': table})
        results = cur.fetchall()
        return results

    def getOrders(self):
        cur = self.mysql.connection.cursor()
        select_statement = '''SELECT * FROM orders'''
        cur.execute(select_statement)
        results = cur.fetchall()
        return results

    def getRecipes(self):
        cur = self.mysql.connection.cursor()
        select_statement = "SELECT * FROM recipes"
        cur.execute(select_statement)
        results = cur.fetchall()
        return results

    def getRecipesByName(self, name):
        cur = self.mysql.connection.cursor()
        select_statement = "SELECT * FROM recipes WHERE recipeName LIKE %(emp_no)s"
        cur.execute(select_statement, {'emp_no': "%" + name + "%"})
        results = cur.fetchall()
        return results

    def getOrdersOverview(self):
        cur = self.mysql.connection.cursor()
        select_statement = '''SELECT orders.orderID, orderDate, tableID, orderdetails.quantity, orderdetails.recipeID
            FROM orders
            INNER JOIN orderdetails 
            ON orderdetails.orderID = orders.orderID'''
        cur.execute(select_statement)
        results = cur.fetchall()
        return results

    def getOrderOverviewByID(self, ID):
        cur = self.mysql.connection.cursor()
        select_statement = '''SELECT orders.orderID, orderDate, tableID, orderdetails.quantity, orderdetails.recipeID
            FROM orders
            INNER JOIN orderdetails 
            ON orderdetails.orderID = orders.orderID
            WHERE orders.orderID = %(emp_orderID)s'''
        cur.execute(select_statement, {'emp_orderID': ID})
        results = cur.fetchall()
        return results

    def getTables(self):
        cur = self.mysql.connection.cursor()
        select_statement = '''SELECT * FROM tables'''
        cur.execute(select_statement)
        results = cur.fetchall()
        return results

    def getOrderByID(self, ID):
        cur = self.mysql.connection.cursor()
        select_statement = "SELECT * FROM orders WHERE orderID LIKE %(emp_no)s"
        cur.execute(select_statement, {'emp_no': ID})
        results = cur.fetchall()
        return results


