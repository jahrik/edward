#!/usr/bin/env python
"""
    A small bot for learning praw

    Usage:
        bot.py [-l <level> | --level <level>]
               [-t <training> | --training <training>]

    Options:
        -h --help               Show this screen
        -l --level=<level>      [default: info]
        -t --training=<training>    Training level [default: training]

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
from chatterbot import ChatBot


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


def chat_bot_learn_english():
    ''' https://github.com/gunthercox/ChatterBot '''

    chatbot = ChatBot(
        'Useless Bot',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database='./bot_db.sqlite3',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch'
            },
            {
                'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                'threshold': 0.65,
                'default_response': 'I am sorry, but I do not understand.'
            }
        ],
        trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
    )

    chatbot.train("chatterbot.corpus.english")

    return chatbot


def chat_bot():
    ''' https://github.com/gunthercox/ChatterBot '''

    LOG.info('Teaching bot basic english...')
    chatbot = chat_bot_learn_english()
    chatbot = ChatBot(
        'Useless Bot',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database='./bot_db.sqlite3',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch'
            },
            {
                'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                'threshold': 0.25,
                'default_response': 'I am sorry, but I do not understand.'
            }
        ],
        trainer='chatterbot.trainers.ListTrainer'
    )

    return chatbot


def reddit_mode():
    ''' Grab the first comment from a reddit subreddit to train the bot '''

    chatbot = chat_bot()
    reddit = get_reddit()
    # reddit.read_only = True
    LOG.info('Read only?: %s', reddit.read_only)

    lim = 10
    sub = 'all'
    # sub = 'food'
    # sub = 'SubredditSimulator'
    slp = 3

    for submission in reddit.subreddit(sub).top(limit=lim):

        # easily exceeding rate limits, so we'll sleep
        sleep(slp)

        try:
            LOG.info('Title: %s', submission.title)
            LOG.info('Score: %s', submission.score)
            LOG.info('ID: %s', submission.id)
            LOG.info('URL: %s', submission.url)
            LOG.info('Author: %s', submission.author)
            LOG.info('Link karma: %s', submission.author.link_karma)

            # Comments
            submission.comments.replace_more(limit=0)
            comments_list = submission.comments.list()
            training_list = [(comment.body) for comment in comments_list]
            comment = training_list[0]

            # Train the chat bot with a few responses
            chatbot.train(training_list)

            # Get a response to an input statement
            response = chatbot.get_response(comment)
            LOG.info('Comment: %s', comment)
            LOG.info('Response: %s', response)
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


def bot_training():
    ''' talk to your bot!
        train your bot!
    '''

    chatbot = chat_bot()
    response = 'How can I help you?'

    while True:

        try:
            training = []
            response = '%s: ' % response
            comment = input(response)
            training.append(str(response))
            training.append(str(comment))
            response = chatbot.get_response(comment)
            LOG.info('Comment: %s', comment)
            LOG.info('Response: %s', response)
            LOG.info('Training bot: %s', training)
            chatbot.train(training)

        except (KeyboardInterrupt, EOFError, SystemExit):
            break

    return


def main():
    ''' main '''

    argument = docopt(__doc__, version='1.0.0')

    if '--training' in argument and argument.get('--training'):
        training = argument.get('--training')

    if training == 'training':
        bot_training()
    elif training == 'reddit':
        reddit_mode()
    else:
        LOG.error('Unknown training mode')


if __name__ == '__main__':

    LOG = logging_setup()

    main()
