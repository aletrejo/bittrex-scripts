import requests
import argparse
from sqlalchemy import delete

from common import db_connect, market_summaries, PATH_HELP, DEBUG_HELP


def get_market_data():
  response = requests.get("https://bittrex.com/api/v1.1/public/getmarketsummaries")

  if response.status_code == 200:
    return response.json()
  else:
    print("Something went wrong with the Bittrex API call.")
    return None


def populate_db(conn, data):
  # clear database contents
  clear_db = delete(market_summaries)
  result = conn.execute(clear_db)

  # insert data into database
  if data is not None:
    ins = market_summaries.insert()
    result = conn.execute(ins, data["result"])
    print("Success! The Bitcoin market data has been stored in the database.")
  else:
    print("Error. No data to store.")


def main(args):
  # database init
  path = "sqlite:///{}".format(args.database_path)
  conn = db_connect(path, args.debug)

  market_data = get_market_data()
  populate_db(conn, market_data)


USAGE = '''This script imports cryptocurrencies prices from the Bittrex API
into a SQLite database.'''


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description=USAGE , formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument("database_path", help=PATH_HELP, type=str)
  parser.add_argument("-d", "--debug", help=DEBUG_HELP, action = "store_true")
  main(parser.parse_args())