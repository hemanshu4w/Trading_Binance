from flask import Flask, render_template,request
from flask_restful import Resource,Api,reqparse
from binance import Client
from binance.enums import *

import config
import json 
app = Flask(__name__)
app.secret_key = 'Himanshu'
api = Api(app)
client = Client(config.API_KEY, config.API_SECRET, tld='com',testnet=False)

def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
    try:
        
        print(f"sending order {order_type} - {side} {quantity} {symbol}")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        #print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False



    return order



@app.route('/')
def hello_world():
    return render_template('dashboard.html')


@app.route('/webhook',methods = ['POST'])
def webhook():
    data = json.loads(request.data)
    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return {
            'code':'error',
            'message':"Nice try, Invalid phrase"
        }
    #
    side = data['strategy']['order_action'].upper()
    quantity = data['strategy']['order_contracts']
    order_response = order(side,quantity,"DOGEUSDT")
    #print(order_response)
    return {
        "code":"success",
        "message":data
    } 
    

    

