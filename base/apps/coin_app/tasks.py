from __future__ import absolute_import , unicode_literals
from urllib import response
from base import app
from celery.utils.log import get_task_logger
from celery import shared_task
from base import celery
import time
import requests
from requests.exceptions import HTTPError
from base import db
from .models import coin , price
from base.utils import GetCoinATaskException , AddCoinsToDbTaskException , GetAllPricesTaskException , RealTimePrice

logger = get_task_logger(__name__)


@celery.task(name="GET ALL COINS" , retry_kwargs={'max_retries':4} , retry_backoff=True , retry_backoff_max=60 , retry_jitter=True)
def getCoins():
    """
        request to url
        if success return a list of coins attributes
        if fail raise a exception
    """
    logger.info("START GETING ALL COINS...")
    try:
        res = requests.get('https://api.kucoin.com/api/v1/currencies')
        res.raise_for_status()
    except HTTPError as http_err:
        logger.info("HTTP ERROR IN GETING ALL COINS !")
        raise GetCoinATaskException("HTTP ERROR IN GETING ALL COINS !")
    except Exception as err:
        logger.info("SOME ERROR IN GETING ALL COINS !")
        raise GetCoinATaskException("SOME ERROR IN GETING ALL COINS !")
    else:
        if res.json()['code'] != '200000':
            raise GetCoinATaskException(res.json()['msg'])
        else:
            data = res.json()['data']
            number_coins_geted = len(data)
            logger.info(f"{number_coins_geted} coins downloaded !")
            logger.info("GETING ALL COINS DONE")
            return data

@celery.task(bind=True , name="ADD COINS TO DATABASE",retry_kwargs={'max_retries':4} , retry_backoff=True , retry_backoff_max=60 , retry_jitter=True)
def addCoinsToDb(self , coins):
    """
        coins is a list of dictionaries wich have coin attributes
        iterate one by one and add to database if already not exist
        return string
    """
    if len(coins)==0:
        raise AddCoinsToDbTaskException('Coins is Empty')
    number_of_added_to_db = 0
    with app.app_context():
        for thiscoin in coins:
            coin_in_db = coin.query.filter_by(name = thiscoin['name']).first()
            if coin_in_db:
                continue
            else:
                new_coin = coin(currency=thiscoin["currency"],
                                    name=thiscoin["name"],
                                    fullName=thiscoin["fullName"],
                                    precision=thiscoin["precision"],
                                    confirms=thiscoin["confirms"],
                                    contractAddress=thiscoin["contractAddress"],
                                    withdrawalMinSize=thiscoin["withdrawalMinSize"],
                                    withdrawalMinFee=thiscoin["withdrawalMinFee"],
                                    isWithdrawEnabled=thiscoin["isWithdrawEnabled"],
                                    isDepositEnabled=thiscoin["isDepositEnabled"],
                                    isMarginEnabled=thiscoin["isMarginEnabled"],
                                    isDebitEnabled=thiscoin["isDebitEnabled"]
                                )
                db.session.add(new_coin)
                db.session.commit()
                number_of_added_to_db += 1

    logger.info(f'{number_of_added_to_db} NEW COIN ADDED TO DB !')
    return f'{number_of_added_to_db} NEW COIN ADDED TO DB !'

@celery.task(bind=True , name="ADD ALL PRICES TO DATABASE" , retry_kwargs={'max_retries':4} , retry_backoff=True , retry_backoff_max=60 , retry_jitter=True)
def getAllPricesTask(self):
    """
        request to url
        get new prices of coins in a dictionary
        add price to databse if coin exist
        reutrn a number
    """
    logger.info("START GETING ALL PRICES...")
    try:
        res = requests.get('https://api.kucoin.com/api/v1/prices')
        res.raise_for_status()
    except HTTPError as http_err:
        logger.info("HTTP ERROR IN GETING ALL PRICES !")
        raise GetAllPricesTaskException("HTTP ERROR IN GETING ALL PRICES !")
    except Exception as err:
        logger.info("SOME ERROR IN GETING ALL PRICES !")
        raise GetAllPricesTaskException("SOME ERROR IN GETING ALL PRICES !")
    else:
        if res.json()['code'] != '200000':
            raise GetAllPricesTaskException(res.json()['msg'])
        data = res.json()['data']
        number_prices_geted = len(data)
        logger.info(f"{number_prices_geted} price downloaded !")
        number_prices_added = 0
        with app.app_context():
            for cr , pr in data.items():
                this_coin = coin.query.filter_by(currency = cr).first()
                if this_coin:
                    new_price = price(coin_id=this_coin.id , price=pr)
                    db.session.add(new_price)
                    db.session.commit()
                    number_prices_added += 1
                else:
                    continue
        logger.info(f"{number_prices_added} price addedd !")
        return number_prices_added
        
@celery.task(bind=True , name="GET REAL TIME PRICE TASK")
def getRealTimePriceTask(self , currency):
    """
        get a Currency
        Send a request for real time price of this
    """
    logger.info(f"START GETING Price For:  {currency}")
    try:
        res = requests.get(f'https://api.kucoin.com/api/v1/prices?currencies={currency}')
        res.raise_for_status()
    except HTTPError as http_err:
        logger.info("HTTP ERROR IN GETING Real Time Price!")
        raise RealTimePrice("HTTP ERROR IN GETING Real Time Price!")
    except Exception as err:
        logger.info("SOME ERROR IN GETING Real Time Price!")
        raise RealTimePrice("SOME ERROR IN GETING Real Time Price!")
    else:
        if res.json()['code'] != '200000' or res.json()['data'] == None:
            raise RealTimePrice(res.json()['msg'])
        price = res.json()['data'][f'{currency}']
    
    logger.info(f'REAL TIME PRICE FOR {currency} is {price}')
    return price , time.strftime("%d/%m/%Y, %H:%M:%S")