from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'restaurantdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    #cur.execute('''CREATE TABLE recipes (recipe_id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, name VARCHAR(20))''')
    #cur.execute('''INSERT INTO recipes VALUES(2, 'Pizza')''')

    #cur.execute('''INSERT INTO example VALUES (1, 'Anthony')''')
    #cur.execute('''INSERT INTO example VALUES (2, 'Billy')''')
    #mysql.connection.commit()

    cur.execute('''SELECT * FROM recipe''')
    results = cur.fetchall()
    print(results)
    return str(results)
    #return 'Done!'

if __name__ == "__main__":
    app.run(debug=True)