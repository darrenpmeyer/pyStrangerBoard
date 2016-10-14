from configparser import ConfigParser
from tweetstranger import TweetStranger
from tweetsearch import TweetSearch
from strangerboard import StrangerBoard

import sys
import time

configfile = 'strangertweets.ini'
config = ConfigParser(interpolation=None)
config.read(configfile)

try:

    if not config.has_section('Twitter'):
        raise RuntimeError("Config file lacks a 'Twitter' section")

    if not config.has_section('board'):
        raise RuntimeError("Config file lacks a 'board' section")

    twitter = None
    if not config.has_option('Twitter', 'bearer'):
        print("No Bearer token, getting one", file=sys.stderr)
        api_key = config.get('Twitter', 'api_key')
        api_secret = config.get('Twitter', 'api_secret')

        if not (api_key and api_secret):
            raise RuntimeError("Config file doesn't have api_key and api_secret in Twitter section")

        twitter = TweetSearch((api_key, api_secret))
        config.set('Twitter', 'bearer', twitter.token)

        with open(configfile, 'w') as fp:
            config.write(fp)
    else:
        twitter = TweetSearch(config.get('Twitter', 'bearer'))

    if not config.has_option('board', 'port'):
        raise RuntimeError("No port specified for board")
    board = StrangerBoard(port=config.get('board', 'port'))

    ts = TweetStranger(board, twitter)

    while True:
        if ts.cycle(splain=True):
            time.sleep(3)
        else:
            print("No results, trying again in 10s")
            time.sleep(10)

except Exception as e:
    print("Unhandled exception: {}".format(e.args), file=sys.stderr)
    with open(configfile, 'w') as fp:
        config.write(fp)
    sys.exit(127)
except SystemExit as e:
    with open(configfile, 'w') as fp:
        config.write(fp)
    sys.exit(e.code)
