#!/usr/bin/env python
"""
    A small bot for learning praw

    Usage:
        bot.py [-l <level> | --level <level>]

    Options:
        -h --help               Show this screen
        -l --level=<level>      [default: info]

    Be sure to export envars first:
        export REDDIT_REDDIT_CLIENT_ID=''
        export REDDIT_REDDIT_CLIENT_SECRET=''
        export REDDIT_REDDIT_USERNAME=''
        export REDDIT_REDDIT_PASSWORD=''

"""
import os
import sys
import logging
from logging import StreamHandler
from docopt import docopt
import praw


def logging_setup():
    ''' Setup the logging '''
    argument = docopt(__doc__, version='1.0.0')
    if '--level' in argument and argument.get('--level'):
        level = getattr(logging, argument.get('--level').upper())
    else:
        level = logging.info
    handlers = [StreamHandler()]

    # Use Randy's custom format to get rid of comma
    logging.basicConfig(level=level,
                        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                        datefmt="%Y-%m-%d %H:%M:%S",
                        handlers=handlers)

    logger = logging.getLogger('bot')

    return logger


def get_envars():
    """ check if envars are set """

    if os.environ.get('REDDIT_CLIENT_ID') is None:
        LOG.error("export REDDIT_CLIENT_ID=''")
        sys.exit(1)
    else:
        client_id = os.environ['REDDIT_CLIENT_ID']

    if os.environ.get('REDDIT_CLIENT_SECRET') is None:
        LOG.error("export REDDIT_CLIENT_SECRET=''")
        sys.exit(1)
    else:
        client_secret = os.environ['REDDIT_CLIENT_SECRET']

    if os.environ.get('REDDIT_USERNAME') is None:
        LOG.error("export REDDIT_USERNAME=''")
        sys.exit(1)
    else:
        username = os.environ['REDDIT_USERNAME']

    if os.environ.get('REDDIT_PASSWORD') is None:
        LOG.error("export REDDIT_PASSWORD=''")
        sys.exit(1)
    else:
        password = os.environ['REDDIT_PASSWORD']

    return client_id, client_secret, username, password


def main():
    ''' main '''

    client_id, client_secret, username, password = get_envars()
    LOG.debug('%s', client_id)
    LOG.debug('%s', client_secret)
    LOG.debug('%s', username)
    LOG.debug('%s', password)

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent='uselessbots:v0.0.1 (by /u/uselessbots)',
                         username=username,
                         password=password)

    LOG.info('Read only?: %s', reddit.read_only)  # Output: True

    for submission in reddit.subreddit('botwatch').hot(limit=10):
        LOG.info(submission.title)


if __name__ == '__main__':

    LOG = logging_setup()

    main()
