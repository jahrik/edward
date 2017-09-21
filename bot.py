#!/usr/bin/env python
"""
    A small bot for learning praw

    Usage:
        bot.py [-l <level> | --level <level>]

    Options:
        -h --help               Show this screen
        -l --level=<level>      [default: info]

    Be sure to export envars first:
        export REDDIT_CLIENT_ID=''
        export REDDIT_CLIENT_SECRET=''
        export REDDIT_USERNAME=''
        export REDDIT_PASSWORD=''

"""
import os
import sys
import logging
from logging import StreamHandler
from time import sleep
from docopt import docopt
import praw
# import requests


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

    logger = logging.getLogger('prawcore')

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


def get_reddit():
    ''' Get praw.Reddit '''

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
    return reddit


def main():
    ''' main '''

    reddit = get_reddit()

    LOG.info('Read only?: %s', reddit.read_only)
    # reddit.read_only = True

    for submission in reddit.subreddit('SubredditSimulator').hot(limit=10):

        # exceeding rate limits
        sleep(2)

        try:
            LOG.info('Title: %s', submission.title)
            LOG.info('Score: %s', submission.score)
            LOG.info('ID: %s', submission.id)
            LOG.info('URL: %s', submission.url)
            # if submission.author:
            LOG.info('Author: %s', submission.author)
            LOG.info('Link karma: %s', submission.author.link_karma)
            # LOG.info('Top comments: %s', list(submission.comments))
            # LOG.info('All comments: %s', submission.comments.list())
            LOG.info('------------------------------------------------------------')

        except praw.exceptions.APIException as praw_exc:
            LOG.error('APIException: %s', praw_exc)

        except praw.exceptions.ClientException as praw_exc:
            LOG.error('ClientException: %s', praw_exc)

        except praw.exceptions.PRAWException as praw_exc:
            LOG.error('PRAWException: %s', praw_exc)

        except AssertionError as exc:
            if '429' in '%s' % exc:
                LOG.warning('Exceeding rate limits: %s', exc)
                LOG.warning('sleeping for 60 seconds')
                sleep(60)


if __name__ == '__main__':

    LOG = logging_setup()

    main()
