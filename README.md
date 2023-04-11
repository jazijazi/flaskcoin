# FLASK COIN

### A web app written in python (with flask framework)

> * Get All Cryptocurrencies datails & prices from [FREE API](https://docs.kucoin.com/) then store them in local Database
> * Create a Chart for every coin with [chart.js](https://www.chartjs.org/)
> * Get real time price from api and send it with [SocketIO](https://socket.io)
> * All api http requests run asynchronous with [CELERY](https://docs.celeryq.dev/en/stable/)

---

### How to run 
`cd <directory>`
1. create a env `python -m virtualenv venv`
2. active virtual environment `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. run docker `docker compose up -d`
5. run flask `flask run`
6. run celery `celery -A base.celery worker -l info`