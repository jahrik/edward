#!/usr/bin/env python
"""
    A small bot that uses praw and chatterbot
    Various training types include (manual, reddit, twitter, etc)

    Usage:
        bot.py [-l <level> | --level <level>]
               [-t <type> | --training <type>]

    Options:
        -h --help               Show this screen
        -l --level=<level>      [default: info]
        -t --training=<type>    Training level [default: feedback]

    Be sure to export envars first:
        export REDDIT_CLIENT_ID=
        export REDDIT_CLIENT_SECRET=
        export REDDIT_USERNAME=
        export REDDIT_PASSWORD=
        export TWITTER_KEY=
        export TWITTER_SECRET=
        export TWITTER_TOKEN=
        export TWITTER_TOKEN_SECRET=
        export HIPCHAT_HOST=
        export HIPCHAT_ROOM=
        export HIPCHAT_ACCESS_TOKEN=
        export GITTER_ROOM=
        export GITTER_API_TOKEN=

"""

import os
import sys
import logging
import random
from logging import StreamHandler
from time import sleep
import multiprocessing
from docopt import docopt
import praw
from chatterbot import ChatBot
from chatterbot.utils import input_function
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import UbuntuCorpusTrainer


def logging_setup():
    ''' Setup the logging '''
    argument = docopt(__doc__, version='1.0.0')
    if '--level' in argument and argument.get('--level'):
        level = getattr(logging, argument.get('--level').upper())
    else:
        level = logging.info
    handlers = [StreamHandler()]

    logging.basicConfig(level=level,
                        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                        datefmt="%Y-%m-%d %H:%M:%S",
                        handlers=handlers)

    logger = logging.getLogger('prawcore')

    return logger


def get_gitter_envars():
    """ check if envars are set """

    if os.environ.get('GITTER_ROOM') is None:
        LOG.error("export GITTER_ROOM=''")
        sys.exit(1)
    else:
        gitter_room = os.environ['GITTER_ROOM']

    if os.environ.get('GITTER_API_TOKEN') is None:
        LOG.error("export GITTER_API_TOKEN=''")
        sys.exit(1)
    else:
        gitter_api_token = os.environ['GITTER_API_TOKEN']

    return gitter_room, gitter_api_token


def get_hipchat_envars():
    """ check if envars are set """

    if os.environ.get('HIPCHAT_HOST') is None:
        LOG.error("export HIPCHAT_HOST=''")
        sys.exit(1)
    else:
        hipchat_host = os.environ['HIPCHAT_HOST']

    if os.environ.get('HIPCHAT_ROOM') is None:
        LOG.error("export HIPCHAT_ROOM=''")
        sys.exit(1)
    else:
        hipchat_room = os.environ['HIPCHAT_ROOM']

    if os.environ.get('HIPCHAT_ACCESS_TOKEN') is None:
        LOG.error("export HIPCHAT_ACCESS_TOKEN=''")
        sys.exit(1)
    else:
        hipchat_access_token = os.environ['HIPCHAT_ACCESS_TOKEN']

    return hipchat_host, hipchat_room, hipchat_access_token


def get_twitter_envars():
    """ check if envars are set """

    if os.environ.get('TWITTER_KEY') is None:
        LOG.error("export TWITTER_KEY=''")
        sys.exit(1)
    else:
        twitter_key = os.environ['TWITTER_KEY']

    if os.environ.get('TWITTER_SECRET') is None:
        LOG.error("export TWITTER_SECRET=''")
        sys.exit(1)
    else:
        twitter_secret = os.environ['TWITTER_SECRET']

    if os.environ.get('TWITTER_TOKEN') is None:
        LOG.error("export TWITTER_TOKEN=''")
        sys.exit(1)
    else:
        twitter_token = os.environ['TWITTER_TOKEN']

    if os.environ.get('TWITTER_TOKEN_SECRET') is None:
        LOG.error("export TWITTER_TOKEN_SECRET=''")
        sys.exit(1)
    else:
        twitter_token_secret = os.environ['TWITTER_TOKEN_SECRET']

    return twitter_key, twitter_secret, twitter_token, twitter_token_secret


def get_reddit_envars():
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

    client_id, client_secret, username, password = get_reddit_envars()
    LOG.debug('%s', client_id)
    LOG.debug('%s', client_secret)
    LOG.debug('%s', username)
    LOG.debug('%s', password)

    try:

        reddit = praw.Reddit(client_id=client_id,
                             client_secret=client_secret,
                             user_agent='uselessbots:v0.0.1 (by /u/uselessbots)',
                             username=username,
                             password=password)

    except AssertionError as exc:
        if '429' in '%s' % exc:
            LOG.warning('Exceeding rate limits: %s', exc)
            LOG.warning('sleeping for 10 seconds')
            sleep(10)

    return reddit


def get_sub_comments(comment):
    ''' get sub comments from a reddit comment object as a list '''

    sub_comments = []
    sub_comments.append(comment.body)
    for _idx, child in enumerate(comment.replies):
        sub_comments.append(child.body)

    return sub_comments


def chat_bot():
    ''' https://github.com/gunthercox/ChatterBot '''

    chatbot = ChatBot(
        'Default Bot',
        storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
        database='bot_db',
        database_uri='mongodb://mongo:27017/',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch'
            }
            # {
            #   'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            #   'threshold': 0.65,
            #   'default_response': 'I am sorry, but I do not understand.'
            # },
            # {
            #   'import_path': 'chatterbot.logic.MathematicalEvaluation'
            # },
            # {
            #   'import_path': 'chatterbot.logic.TimeLogicAdapter'
            # }
        ],

        trainer='chatterbot.trainers.ListTrainer'

        )

    return chatbot


def english_training():
    ''' Train basic english '''

    LOG.info('Teaching bot basic english...')
    bot = chat_bot()

    bot.set_trainer(ChatterBotCorpusTrainer)
    bot.train("chatterbot.corpus.english")

    return


def ubuntu_training():
    '''
    This is an example showing how to train a chat bot using the
    Ubuntu Corpus of conversation dialog.
    '''

    LOG.info('Training bot with ubuntu corpus trainer')
    bot = chat_bot()

    bot.set_trainer(UbuntuCorpusTrainer)
    bot.train()

    return


def reddit_training():
    ''' Grab lim comment trees from r/sub to train the bot '''

    bot = chat_bot()
    reddit = get_reddit()
    reddit.read_only = True
    LOG.info('Read only?: %s', reddit.read_only)

    lim = 99
    sub = 'all'
    slp = 0.03

    for submission in reddit.subreddit(sub).hot(limit=lim):

        try:
            LOG.info('Title: %s', submission.title)
            LOG.info('Score: %s', submission.score)
            LOG.info('ID: %s', submission.id)
            LOG.info('URL: %s', submission.url)
            if submission.author:
                LOG.info('Author: %s', submission.author)
                LOG.info('Link karma: %s', submission.author.link_karma)

            # Comments
            submission.comments.replace_more(limit=0)
            comments_list = submission.comments.list()

            for comment in comments_list:

                sleep(slp)
                sub_comments = []
                sub_comments.append(submission.title)
                sub_comments.append(comment.body)
                for _idx, child in enumerate(comment.replies):
                    sub_comments.append(child.body)

                LOG.info('Training: %s', sub_comments)
                bot.train(sub_comments)

            LOG.info('--------------------------------------------------------')

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


def twitter_training():
    '''
    This example demonstrates how you can train your chat bot
    using data from Twitter.
    '''

    twitter_key, twitter_secret, twitter_token, twitter_token_secret = get_twitter_envars()

    bot = ChatBot(
        'Useless Bot',
        storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
        database='bot_db',
        database_uri='mongodb://mongo:27017/',
        logic_adapters=[
            "chatterbot.logic.BestMatch"
        ],
        input_adapter="chatterbot.input.TerminalAdapter",
        output_adapter="chatterbot.output.TerminalAdapter",
        twitter_consumer_key=twitter_key,
        twitter_consumer_secret=twitter_secret,
        twitter_access_token_key=twitter_token,
        twitter_access_token_secret=twitter_token_secret,
        trainer="chatterbot.trainers.TwitterTrainer"
    )

    bot.train()

    bot.logger.info('Trained database generated successfully!')


def get_feedback(input_statement, response):

    print('\n Input -> {} \n'.format(input_statement))
    print('\n Output -> {} \n'.format(response))
    print('\n Does this make sense? \n')

    text = input_function()

    if 'yes' in text.lower():
        return True
    elif 'no' in text.lower():
        return False
    else:
        print('Please type either "Yes" or "No"')
        return get_feedback()



def loop_trainer(input_s):
    ''' loop through input_statements '''

    bot = chat_bot()
    session = bot.conversation_sessions.new()
    session_id = session.id

    for i in range(3):

        try:
            input_statement = bot.input.process_input_statement(input_s)
            statement, response = bot.generate_response(input_statement, session_id)
            bot.learn_response(response, input_statement)
            bot.conversation_sessions.update(session_id, statement)
            bot.output.process_response(response)

        except (KeyboardInterrupt, EOFError, SystemExit):
            break

    return


def word_list_training():
    ''' take word list
        train bot word in list for loop amount
    '''

    filename = 'list_5000'
    word_list = open(filename, "r")
    work = [(line.strip('\n')) for line in word_list]
    random.shuffle(work)
    pool = multiprocessing.Pool(4)
    pool.map(loop_trainer, work)
    pool.close()
    pool.join()


def feedback_training():
    """
    This example shows how to create a chat bot that
    will learn responses based on an additional feedback
    element from the user.
    """

    bot = chat_bot()
    session = bot.conversation_sessions.new()
    session_id = session.id

    while True:

        try:
            comment = input('input -> ')
            input_statement = bot.input.process_input_statement(comment)
            statement, response = bot.generate_response(input_statement, session_id)

            if get_feedback(input_statement, response):
                bot.learn_response(response, input_statement)
                # bot.conversation_sessions.update(session_id, statement)

            bot.output.process_response(response)

        except (KeyboardInterrupt, EOFError, SystemExit):
            break

    return


def hipchat_bot():
    '''
    See the HipChat api documentation for how to get a user access token.
    https://developer.atlassian.com/hipchat/guide/hipchat-rest-api/api-access-tokens
    '''

    hipchat_host, hipchat_room, hipchat_access_token = get_hipchat_envars()
    # bot = chat_bot()

    bot = ChatBot(
        'Useless Bot',
        storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
        database='bot_db',
        database_uri='mongodb://mongo:27017/',
        hipchat_host=hipchat_host,
        hipchat_room=hipchat_room,
        hipchat_access_token=hipchat_access_token,
        # input_adapter="chatterbot.input.HipChat",
        input_adapter="chatterbot.input.TerminalAdapter",
        output_adapter='chatterbot.output.HipChat',
        trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
    )

    # The following loop will execute each time the user enters input
    while True:
        try:

            response = bot.get_response(None)

        # Press ctrl-c or ctrl-d on the keyboard to exit
        except (KeyboardInterrupt, EOFError, SystemExit):
            break


def gitter_bot():
    ''' gitter bot '''

    gitter_room, gitter_api_token = get_gitter_envars()

    bot = ChatBot(
        'Gitter Bot',
        storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
        database='bot_db',
        database_uri='mongodb://mongo:27017/',
        gitter_room=gitter_room,
        gitter_api_token=gitter_api_token,
        gitter_only_respond_to_mentions=False,
        input_adapter='chatterbot.input.Gitter',
        output_adapter='chatterbot.output.Gitter',
    )
    """
    {'id': '59c8097c614889d47534c2fe',
     'text': 'test',
     'html': 'test',
     'sent': '2017-09-24T19:37:32.559Z',
     'fromUser': {'id': '59c4bd8ed73408ce4f76e071',
                  'username': 'jahrik',
                  'displayName': 'jahrik',
                  'url': '/jahrik',
                  'avatarUrl': 'https://avatars-04.gitter.im/gh/uv/4/jahrik',
                  'avatarUrlSmall': 'https://avatars0.githubusercontent.com/u/3237460?v=4&s=60',
                  'avatarUrlMedium': 'https://avatars0.githubusercontent.com/u/3237460?v=4&s=128', 'gv': '4'},
     'unread': False,
     'readBy': 0,
     'urls': [],
     'mentions': [],
     'issues': [],
     'meta': [],
     'v': 1}
    """
    session_id = bot.default_session.uuid

    while True:
        try:
            data = bot.input.get_most_recent_message()
            input_s = data.get('text')
            print(input_s)
            input_statement = bot.input.process_input(input_s)
            statement, response = bot.generate_response(input_statement, session_id)
            print(response)
            # print(statement)
            # statement, response = bot.generate_response(input_statement, session_id)
            # print(statement)
            # print(response)
            # respond = bot.ouput.gitter.send_message(reponse)
            # bot.learn_response(response, input_statement)
            # bot.conversation_sessions.update(session_id, statement)
            # bot.output.process_response(response)

        # Press ctrl-c or ctrl-d on the keyboard to exit
        except (KeyboardInterrupt, EOFError, SystemExit):
            break

    return


def main():
    ''' main '''

    argument = docopt(__doc__, version='1.0.0')

    if '--training' in argument and argument.get('--training'):
        training = argument.get('--training')

    if training == 'english':
        english_training()
    elif training == 'word_list':
        word_list_training()
    elif training == 'feedback':
        feedback_training()
    elif training == 'ubuntu':
        ubuntu_training()
    elif training == 'reddit':
        reddit_training()
    elif training == 'twitter':
        twitter_training()
    elif training == 'hipchat':
        hipchat_bot()
    elif training == 'gitter':
        gitter_bot()
    else:
        LOG.error('Unknown training mode')


if __name__ == '__main__':

    LOG = logging_setup()

    main()
