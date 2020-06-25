from flask import Flask, request, Response, jsonify
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

    def setOrderStatus(self, ID, status):
        cur = self.mysql.connection.cursor()
        select_statement = '''UPDATE orders SET orderStatus = %(emp_status)s WHERE orderID = %(emp_id)s;'''
        cur.execute(select_statement, {'emp_status': status, 'emp_id': ID})
        self.mysql.connection.commit()

    def insertRecipe(self, name, price, type):
        cur = self.mysql.connection.cursor()
        select_statement = '''INSERT INTO recipes(recipeName, recipePrice, recipeType) VALUES (%(emp_name)s, %(emp_price)s, %(emp_type)s)'''
        cur.execute(select_statement, {'emp_name': name, 'emp_price': price, 'emp_type': type})
        self.mysql.connection.commit()

    def insertOrder(self, table):
        cur = self.mysql.connection.cursor()
        select_statement = '''INSERT INTO orders(orderDate, tableID, orderStatus) VALUES (curdate(),  %(emp_no)s, "open")'''
        cur.execute(select_statement, {'emp_no': table})
        self.mysql.connection.commit()
        orderID = cur.lastrowid
        return orderID


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

    def getAllOrders(self):
        cur = self.mysql.connection.cursor()
        select_statement = '''SELECT orders.orderID, orders.orderDate, SUM(orderdetails.quantity)*recipes.recipePrice as TotalCost, orders.orderStatus
                    FROM orders
                    LEFT JOIN orderdetails 
                    ON orderdetails.orderID = orders.orderID
                    LEFT JOIN recipes
                    ON recipes.recipeID = orderdetails.recipeID
                    GROUP BY orderID;'''
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

    def getOpenOrders(self):
        cur = self.mysql.connection.cursor()
        select_statement = '''SELECT orders.orderID, orders.orderDate, SUM(orderdetails.quantity)*recipes.recipePrice as TotalCost, orders.orderStatus
            FROM orders
            INNER JOIN orderdetails 
            ON orderdetails.orderID = orders.orderID
            INNER JOIN recipes
            ON recipes.recipeID = orderdetails.recipeID
            WHERE orders.orderStatus = "open"
            GROUP BY orderID;'''
        cur.execute(select_statement)
        results = cur.fetchall()
        return results

    def getOrderByID(self, ID):
        cur = self.mysql.connection.cursor()
        select_statement = '''SELECT orders.orderID, orders.orderDate, SUM(orderdetails.quantity)*recipes.recipePrice as TotalCost, orders.orderStatus
            FROM orders
            INNER JOIN orderdetails 
            ON orderdetails.orderID = orders.orderID
            INNER JOIN recipes
            ON recipes.recipeID = orderdetails.recipeID
            WHERE orders.orderID = %(emp_orderID)s
            GROUP BY orderID;'''
        cur.execute(select_statement, {'emp_orderID': ID})
        results = cur.fetchall()
        print(results)
        return results


    def getTables(self):
        cur = self.mysql.connection.cursor()
        select_statement = '''SELECT * FROM tables'''
        cur.execute(select_statement)
        results = cur.fetchall()
        return results

    def getOrderDetails(self, ID):
        cur = self.mysql.connection.cursor()
        select_statement = '''SELECT recipes.recipeID, recipes.recipePrice, CAST(sum(quantity) AS unsigned) as Quantity, sum(quantity)*recipes.recipePrice as Cost
            FROM orders
            INNER JOIN orderdetails 
            ON orderdetails.orderID = orders.orderID
            INNER JOIN recipes
            ON recipes.recipeID = orderdetails.recipeID
            WHERE orders.orderID = %(emp_no)s
            GROUP BY recipes.recipeID'''
        cur.execute(select_statement, {'emp_no': ID})
        results = cur.fetchall()
        return results

    def getPriceOfOrder(self, ID):
        cur = self.mysql.connection.cursor()
        select_statement = '''SELECT SUM(orderdetails.quantity)*recipes.recipePrice as TotalCost
            FROM orders
            INNER JOIN orderdetails 
            ON orderdetails.orderID = orders.orderID
            INNER JOIN recipes
            ON recipes.recipeID = orderdetails.recipeID
            WHERE orders.orderID = %(emp_ID)s'''
        cur.execute(select_statement, {'emp_ID': ID})
        results = cur.fetchall()
        return results

    def getTableByID(self, ID):
        cur = self.mysql.connection.cursor()
        select_statement = '''SELECT * FROM tables WHERE tableID = %(emp_ID)s'''
        cur.execute(select_statement, {'emp_ID': ID})
        results = cur.fetchall()
        return results

