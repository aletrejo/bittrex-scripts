import argparse
from common import db_connect, market_summaries as ms, PATH_HELP, DEBUG_HELP

from sqlalchemy import select


def main(args):
  # Initialize database
  path = "sqlite:///{}".format(args.database_path)
  conn = db_connect(path, args.debug)

  # query SQL
  s = select([ms.c.Last, ms.c.PrevDay, ms.c.MarketName])
  rp = conn.execute(s)

  # show report
  for record in rp:
    daily_return = record.Last / record.PrevDay - 1
    daily_return = format(daily_return, '.2f')
    print("{} {}%".format(record.MarketName, daily_return))


USAGE = '''
This script displays the daily return for different Bitcoin markets from a SQLite database.
'''

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=USAGE, formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument("database_path", help=PATH_HELP, type=str)
  parser.add_argument("-d", "--debug", help=DEBUG_HELP, action="store_true")
  main(parser.parse_args())
