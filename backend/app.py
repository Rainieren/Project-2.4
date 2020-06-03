from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

recipes = [{'name': 'Pizza Hawai','price': '3,50', 'type': "pizza"},
           {'name': 'Pizza Salami','price': '4,50', 'type': "pizza"},
           {'name': 'Pizza Pepperoni','price': '5,50', 'type': "pizza"},
           {'name': 'Pizza Tonijn','price': '5,00', 'type': "pizza"},
           {'name': 'Pizza Shoarma','price': '4,00', 'type': "pizza"},
           {'name': 'Pizza Kebab','price': '4,75', 'type': "pizza"},
            {'name': 'Broodje Kip','price': '2,25', 'type': "brood"},
            {'name': 'Broodje Warmvlees','price': '3,00', 'type': "brood"},
            {'name': 'Broodje Gehaktbal','price': '2,50', 'type': "brood"},
            {'name': 'Broodje Shoarma','price': '2,75', 'type': "brood"},
            {'name': 'Broodje Kaas','price': '1,75', 'type': "brood"},
            {'name': 'Broodje Vis','price': '3,00', 'type': "brood"},
            {'name': 'Broodje Hotdog','price': '2,50', 'type': "brood"},
            {'name': 'Broodje Jam','price': '1,50', 'type': "brood"},
           ]

quarks = [{'name': 'up', 'charge': '+2/3'},
          {'name': 'down', 'charge': '-1/3'},
          {'name': 'charm', 'charge': '+2/3'},
          {'name': 'strange', 'charge': '-1/3'}]


@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({'message': 'Hello, World!'})


@app.route('/quarks', methods=['GET'])
def returnAll():
    return jsonify({'quarks': quarks})


@app.route('/quarks/<string:name>', methods=['GET'])
def returnOne(name):
    theOne = quarks[0]
    for i, q in enumerate(quarks):
        if q['name'] == name:
            theOne = quarks[i]
    return jsonify({'quarks': theOne})


@app.route('/quarks', methods=['POST'])
def addOne():
    new_quark = request.get_json()
    quarks.append(new_quark)
    return jsonify({'quarks': quarks})


@app.route('/quarks/<string:name>', methods=['PUT'])
def editOne(name):
    new_quark = request.get_json()
    for i, q in enumerate(quarks):
        if q['name'] == name:
            quarks[i] = new_quark
    qs = request.get_json()
    return jsonify({'quarks': quarks})


@app.route('/quarks/<string:name>', methods=['DELETE'])
def deleteOne(name):
    for i, q in enumerate(quarks):
        if q['name'] == name:
            del quarks[i]
    return jsonify({'quarks': quarks})

@app.route('/recipes/<string:type>', methods=['GET'])
def getRecipesByType(type):
    RecipeList = []
    for i, q in enumerate(recipes):
        if q['type'] == type:
            RecipeList.append(q)

    return jsonify({'recipes': RecipeList})

@app.route('/test/<string:name>', methods=['GET'])
def getRecipesByName(name):
    RecipeList = []
    for i, q in enumerate(recipes):
        if name.find(q['name']) > -1:
            RecipeList.append(q)

    return jsonify({'recipes': RecipeList})

@app.route('/recipes', methods=['GET'])
def getRecipes():
    return jsonify({'recipes': recipes})

if __name__ == "__main__":
    app.run(debug=True)
    str = "Messi is the best soccer player"
