from sqlalchemy import (create_engine, MetaData, Table, Column, Integer, String, Float, insert)
import requests

""""To DO:
- Update Method
- Use commandline arguments 
"""

#Metadata
metadata = MetaData()

#Creating table 
market_summaries = Table('marketsummaries', metadata, 
    Column('MarketName', String(), primary_key=True),
    Column('High', Float()),
    Column('Low', Float()),
    Column('Volume', Float()),
    Column('Last', Float()),
    Column('BaseVolume', Float()),
    Column('TimeStamp', String()), 
    Column('Bid', Float()), 
    Column('Ask', Float()),
    Column('OpenBuyOrders', Integer()),
    Column('OpenSellOrders', Integer()), 
    Column('PrevDay', Float()),
    Column('Created', String()),
    Column('DisplayMarketName', String())
)

#Creating engine and connecting it to database
engine = create_engine('sqlite:///marketsummaries.db', echo=True)
metadata.create_all(engine)
connection = engine.connect()


#Get data from the API
def get_market_data():

	response = requests.get("https://bittrex.com/api/v1.1/public/getmarketsummaries")

	print(response.status_code)

	if response.status_code == 200:
		py_response = response.json()
		return py_response
	else:
		print("Something went wrong.")
		return None 

market_data = get_market_data()

#Add DisplayMarketName to marketdata
if market_data is not None:
    for row in market_data["result"]:
        row["DisplayMarketName"] = None

#Inserting data into database
if market_data is not None:
    ins = market_summaries.insert()
    result = connection.execute(ins, market_data["result"])

