from celery import chain
from base import app , socketio
from flask import request, Response , render_template , jsonify
from . import coins
from base.apps.coin_app.models import coin , price
from .tasks import getCoins , addCoinsToDb , getAllPricesTask , getRealTimePriceTask
import json
from base.apps.coin_app import coins

@socketio.on('connect')
def connect():
    print('Client connected!!!!')

@socketio.on('disconnect')
def disconnect():
    print('client disconnected!!!')

@socketio.on('RealTimePrice')
def handle_realtimeprice(data):
    # Send data to event wich name as coin currency name
    this_coin = coin.query.filter_by(currency=data['currency']).first()
    if this_coin:
        task = getRealTimePriceTask.apply_async((data['currency'],),routing_key='high.coin')
        price , this_time = task.get()
        if task.state == 'SUCCESS':
            socketio.emit(data['currency'] , {'value':price ,'time':this_time})
    else:
        socketio.emit(data['currency'] , {'value':0     ,})

@coins.route('/')
def home():
    coins = coin.query.all()
    return render_template('home.html' , coins=coins)

@coins.route('/price/<string:currency>/')
def getPrice(currency):
    """
        Details Page for every coin
        send coin details & All prices for this coin (in json for create a chart) 
    """
    this_coin = coin.query.filter_by(currency=currency).first_or_404()
    print(this_coin.fullName , this_coin.id)

    data = {str(price.date):price.price for price in this_coin.prices}

    return render_template('price.html' , this_coin=this_coin , data=json.dumps(data))



@coins.route('/getAllCoin' , methods=['POST'])
def getAllCoin():
    task = chain(getCoins.s() , addCoinsToDb.s()).apply_async(routing_key='low.coin')
    result = task.get()
    if task.state == 'SUCCESS':
        return jsonify({"result": result , "task_id":task.id}), 202
    else:
        return jsonify({"error":"Error in Fetch data"}) , 500

@coins.route('/getAllPrices' , methods=['POST'])
def getAllPrices():
    task = getAllPricesTask.apply_async()
    result = task.get()
    if task.state == 'SUCCESS':
        return jsonify({"result": f"{result} updated prices for all coins", "task_id":task.id}), 202
    else:
        return jsonify({"result":"Error in Fetch data", "task_id":task.id}) , 500

