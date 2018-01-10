import requests
import argparse
from sqlalchemy import (create_engine, MetaData, Table, Column, Integer, String, Float, insert, delete)
from common import dal, ht

def get_market_data():
    response = requests.get("https://bittrex.com/api/v1.1/public/getmarketsummaries")

    if response.status_code == 200:
        py_response = response.json()
        return py_response
    else:
        print("Something went wrong with the Bittrex API call.")
        return None 


def populate_db(data):
    #Clear database contents
    clear_db = delete(dal.market_summaries)
    result = dal.connection.execute(clear_db)

    #Insert data into database
    if data is not None:
        ins = dal.market_summaries.insert()
        result = dal.connection.execute(ins, data["result"])
        print("Success! The Bitcoin market data has been stored in the database.")
    else:
        print("Error. No data to store.")


def main():
    #Command line arguments configuration
    parser = argparse.ArgumentParser(description = "This script imports cryptocurrencies prices from the Bittrex API into a SQLite database.", formatter_class=argparse.RawTextHelpFormatter)
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

    market_data = get_market_data()
    populate_db(market_data)


if __name__ == "__main__":
    main()