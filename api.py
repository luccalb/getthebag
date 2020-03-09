import flask
from flask import request, jsonify, Response
from flask_cors import CORS
from pymongo import MongoClient
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
from datetime import datetime
from dateutil.relativedelta import *
from mongostring import mongostring

def mongores(payload):
    return Response(
        dumps(payload),
        mimetype='application/json'
    )

client = MongoClient(mongostring)
db = client.moneymanager

app = flask.Flask(__name__)
cors = CORS(app)

## TRANSACTIONS ##

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the api"

@app.route('/api/transactions/all', methods=['GET'])
def api_all():
    return mongores(db.transactions.find())

@app.route('/api/transactions/<string:id>', methods=['GET'])
def api_trans_id(id):
    return mongores(db.transactions.find({'_id': ObjectId(id)}))

@app.route('/api/transactions/review', methods=['GET'])
def api_all_review():
    return mongores(db.transactions.find({'toBeReviewed': True}))

@app.route('/api/transactions/<int:year>')
def api_all_year(year):
    start = datetime(year, 1, 1)
    end = start + relativedelta(years=+1, days=+1)
    return mongores(db.transactions.find({'date': {'$lt': end, '$gte': start}}))

@app.route('/api/transactions/<int:year>/<int:month>')
def api_all_month(year, month):
    start = datetime(year, month, 1)
    end = start + relativedelta(months=+1)
    return mongores(db.transactions.find({'date': {'$lt': end, '$gte': start}}))

@app.route('/api/transactions/update', methods=['PUT'])
def api_update_transact():
    print(request.json['_id'])
    db.transactions.update_one({'_id': ObjectId(request.json['_id'])}, {'$set': {'category': request.json['category']}})
    return mongores({})

## MONTHS ##

@app.route('/api/months/all', methods=['GET'])
def api_all_months():
    return mongores(db.months.find())

@app.route('/api/months/<int:year>/<int:month>', methods=['GET'])
def api_month(year, month):
    return mongores(db.months.find_one({'year': year, 'month': month}))

## YEARS ##

@app.route('/api/years/all', methods=['GET'])
def api_all_years():
    return mongores(db.years.find())

app.run()