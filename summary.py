import argparse
from common import dal, ht
from sqlalchemy import (MetaData, create_engine, Table, select)

def display_summaries(data):
	s = select([data.c.Last, data.c.PrevDay, data.c.MarketName])
	rp = dal.connection.execute(s)

	for record in rp:
		daily_return = record.Last/record.PrevDay - 1
		daily_return = format(daily_return, '.2f')
		print("{} {}%".format(record.MarketName, daily_return))


def main():
	#Command line arguments configuration 
	parser = argparse.ArgumentParser(description = "This script displays the daily return for different Bitcoin markets from a SQLite database.", formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("database_path", help=ht.path_help, type=str)
	parser.add_argument("-d", "--debug", help=ht.debug_help, action = "store_true")
	args = parser.parse_args()
	path = "sqlite:///{}".format(args.database_path)

	#Initialize database
	if args.debug:
		echo = True
		dal.db_init(path, echo)
	else:
		echo = False
		dal.db_init(path, echo)

	display_summaries(dal.market_summaries)

if __name__ == '__main__':
	main()
