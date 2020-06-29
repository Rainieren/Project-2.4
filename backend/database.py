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

    def setServingStatus(self, orderID, recipeID, quantity, state):
        cur = self.mysql.connection.cursor()
        select_statement = '''SELECT count(*) AS aantal from orderdetails 
            WHERE orderID = %(emp_orderID)s && recipeID = %(emp_recipeID)s && quantity = %(emp_quantity)s && servingStatus = %(emp_state)s'''
        cur.execute(select_statement, {'emp_orderID': orderID, 'emp_recipeID': recipeID, 'emp_quantity': quantity, 'emp_state': state})
        check_value = cur.fetchall()
        if check_value[0]['aantal'] != 0:
            update_statement = '''UPDATE orderdetails SET servingStatus = %(emp_state)s
                        WHERE orderID = %(emp_orderID)s && recipeID = %(emp_recipeID)s && quantity = %(emp_quantity)s
                        LIMIT 1'''
            cur.execute(update_statement, {'emp_orderID': orderID, 'emp_recipeID': recipeID, 'emp_quantity': quantity, 'emp_state': state})
            self.mysql.connection.commit()

    def setOrderStatus(self, ID, status):
        cur = self.mysql.connection.cursor()
        select_statement = '''UPDATE orders SET orderStatus = %(emp_status)s WHERE orderID = %(emp_id)s;'''
        cur.execute(select_statement, {'emp_status': status, 'emp_id': ID})
        self.mysql.connection.commit()

    def insertRecipe(self, name, price, type, focus):
        cur = self.mysql.connection.cursor()
        select_statement = '''INSERT INTO recipes(recipeName, recipePrice, recipeType, recipeFocus) VALUES (%(emp_name)s, %(emp_price)s, %(emp_type)s, %(emp_focus)s)'''
        cur.execute(select_statement, {'emp_name': name, 'emp_price': price, 'emp_type': type, 'emp_focus': focus})
        self.mysql.connection.commit()

    def insertOrder(self, table):
        cur = self.mysql.connection.cursor()
        select_statement = '''INSERT INTO orders(orderDate, tableID, orderStatus) VALUES (curdate(),  %(emp_no)s, "open")'''
        cur.execute(select_statement, {'emp_no': table})
        self.mysql.connection.commit()
        orderID = cur.lastrowid
        return orderID

    def addToOrder(self, recipeID, orderID, quantity):
        cur = self.mysql.connection.cursor()
        select_statement = '''INSERT INTO orderdetails(orderID, quantity, recipeID, servingStatus) VALUES (%(emp_orderid)s, %(emp_quantity)s, %(emp_recipeid)s, "open")'''
        cur.execute(select_statement, {'emp_orderid': orderID, 'emp_quantity': quantity, 'emp_recipeid': recipeID})
        self.mysql.connection.commit()

    def getResults(self, table):
        cur = self.mysql.connection.cursor()
        select_statement = '''SELECT * FROM %(emp_no)s)'''
        cur.execute(select_statement, {'emp_no': table})
        results = cur.fetchall()
        if (len(results) == 0):
            return [{}]
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
        if (len(results) == 0):
            return [{}]
        return results

    def getServingsOfTableByTableID(self, tableID, state):
        cur = self.mysql.connection.cursor()
        select_statement = '''SELECT recipes.recipeName, tables.tableID, orders.orderID,  orderdetails.recipeID, orderdetails.quantity, orderdetails.servingStatus from orders
        INNER JOIN tables on orders.tableID = tables.tableID
        INNER JOIN orderdetails on orders.orderID = orderdetails.orderID
        INNER JOIN recipes on orderdetails.recipeID = recipes.recipeID
        WHERE tables.tableID = %(emp_tabid)s && orderdetails.servingStatus = %(emp_state)s
        order by orderdetails.servingStatus ASC'''
        cur.execute(select_statement, {'emp_tabid': tableID, 'emp_state': state})
        results = cur.fetchall()
        if (len(results) == 0):
            results = [{}]
        return results

    def getServingsByOrderID(self, orderID, focus, state):
        cur = self.mysql.connection.cursor()
        if(focus == 'all'):
            select_statement = '''SELECT orderdetails.recipeID, orderdetails.quantity, servingStatus, recipeFocus FROM orderdetails 
            LEFT JOIN recipes ON orderdetails.recipeID = recipes.recipeID
            WHERE orderID = %(emp_oid)s && servingStatus = %(emp_state)s'''
            cur.execute(select_statement, {'emp_oid': orderID, 'emp_state': state})
        elif(orderID == 0):
            select_statement = '''SELECT orderdetails.recipeID, orderdetails.quantity, servingStatus, recipeFocus FROM orderdetails 
                        LEFT JOIN recipes ON orderdetails.recipeID = recipes.recipeID
                        WHERE orderID = %(emp_oid)s && servingStatus = %(emp_state)s'''
            cur.execute(select_statement, {'emp_oid': orderID, 'emp_state': state})
        else:
            select_statement = '''SELECT orderdetails.recipeID, orderdetails.quantity, servingStatus, recipeFocus FROM orderdetails 
            LEFT JOIN recipes ON orderdetails.recipeID = recipes.recipeID
            WHERE orderID = %(emp_oid)s && recipes.recipeFocus = %(emp_focus)s && servingStatus = %(emp_state)s'''
            cur.execute(select_statement, {'emp_oid': orderID, 'emp_focus': focus, 'emp_state': state})
        results = cur.fetchall()
        if (len(results) == 0):
            return [{}]
        return results

    def getRecipes(self):
        cur = self.mysql.connection.cursor()
        select_statement = "SELECT * FROM recipes"
        cur.execute(select_statement)
        results = cur.fetchall()
        if (len(results) == 0):
            results = [{}]
        return results

    def getRecipesByName(self, name):
        cur = self.mysql.connection.cursor()
        select_statement = "SELECT * FROM recipes WHERE recipeName LIKE %(emp_no)s"
        cur.execute(select_statement, {'emp_no': "%" + name + "%"})
        results = cur.fetchall()
        if (len(results) == 0):
            results = [{}]
        return results

    def getRecipeByRecipeID(self, recipeID):
        cur = self.mysql.connection.cursor()
        select_statement = "SELECT * FROM recipes WHERE recipeID = %(emp_recipeID)s"
        cur.execute(select_statement, {'emp_recipeID': recipeID})
        results = cur.fetchall()
        if (len(results) == 0):
            results = [{}]
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
        if (len(results) == 0):
            return [{}]
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
        if (len(results) == 0):
            return [{}]
        return results


    def getTables(self):
        cur = self.mysql.connection.cursor()
        select_statement = '''SELECT * FROM tables ORDER BY tableID ASC'''
        cur.execute(select_statement)
        results = cur.fetchall()
        if (len(results) == 0):
            return [{}]
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
        if (len(results) == 0):
            return [{}]
        return results

    def getPriceOfOrder(self, ID):
        cur = self.mysql.connection.cursor()
        select_statement = '''SELECT x.orderID, orders.orderStatus, SUM(x.TotalCost) as 'TotalCost' FROM (SELECT orderID, recipes.recipeID, SUM(quantity) AS quantity, SUM(quantity)*recipes.recipePrice as TotalCost from orderdetails
        JOIN recipes on orderdetails.recipeID = recipes.recipeID
        GROUP BY orderID, recipes.recipeID) x
        JOIN orders on x.orderID = orders.orderID
        WHERE x.orderID = %(emp_ID)s
        GROUP BY x.orderID'''
        cur.execute(select_statement, {'emp_ID': ID})
        results = cur.fetchall()
        if(len(results) == 0):
            return [{"TotalCost": 0, "orderID": ID, "orderStatus": "unknown"}]
        return results

    def getTableByID(self, ID):
        cur = self.mysql.connection.cursor()
        select_statement = '''SELECT tables.tableID, tables.tableStatus as orderID FROM tables
        WHERE tables.tableID = %(emp_ID)s'''
        cur.execute(select_statement, {'emp_ID': ID})
        results = cur.fetchall()
        if (len(results) == 0):
            return [{}]
        return results

