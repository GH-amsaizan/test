from flask import Flask, jsonify, Response
import requests
import json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import pdb


app = Flask(__name__)

# Grabbing environment variables to represent the
# Database User, Password and Name
pg_user = os.getenv('POSTGRES_DB_USER')
pg_password = os.getenv('POSTGRES_DB_PASSWORD')
db_name = os.getenv('POSTGRES_DB_NAME')
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{}:{}@localhost:5432/{}".format(pg_user, pg_password, db_name)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Testing route. Should return a simple 'Hello world' string
@app.route('/test', methods=['GET'])
def hello_world() -> str:
    return 'hello world'


# Request this route to generate a row of data in our postgres database
@app.route('/items', methods=['GET', 'POST'])
def add_item() -> str:
    # set url to a REST API
    url = ''
    response = json.loads(requests.get(url).text)
    # example parameters of response
    name = response["name"]
    information = response["information"]
    new_item = Item(name, information)
    db.session.add(new_item)
    db.session.commit()
    return response

# Request this route to see a list of all rows in our postgres database
@app.route('/items_database', methods=['GET'])
def show_items_from_database() -> Response:
    items = Item.query.all()
    results = [{
                "name": item.name,
                "information": item.information
            } for item in items]
    return jsonify(results)


# Describes the model in our postgres database
# along with each column name and data type
class Item(db.Model): # type: ignore
    __tablename__ = 'items'
    sourceid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    information = db.Column(db.String())

    def __init__(self, name: str, information: str) -> None:
        self.name = name
        self.information = information


    def __repr__(self) -> str:
        return '<Name %r>' % self.name


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)