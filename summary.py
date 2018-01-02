from sqlalchemy import (MetaData, create_engine, Table, select)

""""To DO:
- Use command line arguments 
"""


#Creating engine
metadata = MetaData()
engine = create_engine('sqlite:///marketsummaries.db', echo=True)
connection = engine.connect()

#Reflecting marketsummaries table
market_summaries = Table('marketsummaries', metadata, autoload=True, autoload_with=engine)

#Calculating summaries
s = select([market_summaries])
rp = connection.execute(s)

#Printing daily return for each market 
for record in rp:
	daily_return = record.Last/record.PrevDay - 1
	daily_return = format(daily_return, '.2f')
	print("{} {}%".format(record.MarketName, daily_return))