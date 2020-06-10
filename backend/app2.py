from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'restaurantdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

state = "startup";
mysql = MySQL(app)

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

@app.route('/database/select/<string:name>', methods=['GET'])
def selectbyname(name):
    cur = mysql.connection.cursor()
    select_statement = "SELECT * FROM recipes WHERE recipeName LIKE %(emp_no)s"
    cur.execute(select_statement, {'emp_no': "%"+name+"%"})
    results = cur.fetchall()
    print(results)
    return str(results)

@app.route('/database/select', methods=['GET'])
def select():
    cur = mysql.connection.cursor()
    select_statement = "SELECT * FROM recipes"
    cur.execute(select_statement)
    results = cur.fetchall()
    print(results)
    return str(results)

if __name__ == "__main__":
    app.run(debug=True)