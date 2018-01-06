#!/usr/bin/env python
"""
Usage:
    ./edward.py [-l <level> | --level   <level>]
                [-t  <type> | --training <type>]
                [-b   <bot> | --bot       <bot>]
                [-e         | --export   <file>]
                [-h         | --help           ]
                [--version  ]

Options:
    -h --help               Show this screen and exit
    --version               Show version and exit
    -l --level=<level>      [default: info]
    -t --training=<type>    Training type:
                                english, word_list,
                                ubuntu, reddit, twitter
                                [default: None]

    -b --bot=<bot>          Run bot: [default: help]
                                gitter, hipchat, voice, feedback
                                [default: None]

"""

import os
import sys
import random
import logging
from logging import StreamHandler
import time
from time import sleep
import multiprocessing
from docopt import docopt
import praw
import tweepy
from chatterbot import ChatBot
from chatterbot.utils import input_function
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import UbuntuCorpusTrainer
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener

VERSION = '0.1.1'


def logging_setup():
    """
    * setup logging
    * return logger
    """
    argument = docopt(__doc__, version=VERSION)
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
    """
    * get Gitter room and api token from envars
    * obtain an api token at:
    * https://developer.gitter.im/apps
    * return gitter_room, gitter_api_token
    """

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
    """
    * get HipChat host, room, and api token from envars
    * obtain an api token at:
    * https://hipchat.com/admin/api
    * return hipchat_host, hipchat_room, hipchat_access_token
    """

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
    """
    * get Twitter creds from envars
    * return twitter_key, twitter_secret, twitter_token, twitter_token_secret
    * create app https://apps.twitter.com/
    """

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
    """
    * get Reddit creds from envars
    * return client_id, client_secret, username, password
    """

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
    """
    * obtain client_id, client_secret, username, password from [get_reddit_envars()](#get_reddit_envars)
    * set reddit to praw.Reddit
    * return reddit
    """

    client_id, client_secret, username, password = get_reddit_envars()
    LOG.debug('%s', client_id)
    LOG.debug('%s', client_secret)
    LOG.debug('%s', username)
    LOG.debug('%s', password)

    try:

        reddit = praw.Reddit(client_id=client_id,
                             client_secret=client_secret,
                             user_agent='edward:v0.1.1 (by /u/uselessbots)',
                             username=username,
                             password=password)

    except AssertionError as exc:
        if '429' in '%s' % exc:
            LOG.warning('Exceeding rate limits: %s', exc)
            LOG.warning('sleeping for 10 seconds')
            sleep(10)

    return reddit


def get_sub_comments(comment):
    """
    * get sub comments from a reddit comment object as a list
    * generate a list of sub_comments from all replies
    * return sub_comments
    """

    sub_comments = []
    sub_comments.append(comment.body)
    for _idx, child in enumerate(comment.replies):
        sub_comments.append(child.body)

    return sub_comments


def chat_bot():
    """
    * https://github.com/gunthercox/ChatterBot
    * Create default bot
    * return chatbot
    """

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
        # filters=[
        #     'chatterbot.filters.RepetitiveResponseFilter'
        # ],
        trainer='chatterbot.trainers.ListTrainer'

        )

    return chatbot


def english_training():
    """
    * get base bot [chat_bot()](#chat_bot)
    * train basic english with
    * [chatterbot.corpus.english](https://github.com/gunthercox/chatterbot-corpus/tree/master/chatterbot_corpus/data/english)
    """

    LOG.info('Teaching bot basic english...')
    bot = chat_bot()

    bot.set_trainer(ChatterBotCorpusTrainer)
    bot.train("chatterbot.corpus.english")

    return


def ubuntu_training():
    """
    * *THIS IS BROKEN RIGHT NOW*
    * get base bot [chat_bot()](#chat_bot)
    * train with ubuntu corpus
    * [chatterbot.corpus.ubuntu](https://github.com/gunthercox/ChatterBot/blob/b611cbd0629eb2aed9f840b50d1b3f8869c2589e/chatterbot/trainers.py#L236)
    * see [Training with the Ubuntu dialog corpus](http://chatterbot.readthedocs.io/en/stable/training.html#training-with-the-ubuntu-dialog-corpus)
    """

    LOG.info('Training bot with ubuntu corpus trainer')
    bot = chat_bot()

    bot.set_trainer(UbuntuCorpusTrainer)
    bot.train()

    return


def reddit_training(sub, lim):
    """
    Parameters
    ----------
    sub : str, optional, default = 'all'
        Which subreddit to use

    lim : int, optional, default = 9
        how many to grab

    Configure
    * get base bot [chat_bot()](#chat_bot)
    * get reddit from [get_reddit()](#get_reddit)
    * configure read only true/false
    * sub = the subreddit to use
    * lim = the amount of submissions to grab from a chosen subreddit
    * slp = is set to keep from reaching reddit server rate limits

    Training
    * training list starts as an empty list []
    * for every submission collect comment chains
    * for every comment in comment chains collect all replies
    * if the comment is not '[deleted]'
    * if reply is not '[removed]'
    * if reply is < 80 characters
    * append training list
    * Train the bot
    """

    bot = chat_bot()
    reddit = get_reddit()
    reddit.read_only = True
    LOG.info('Read only?: %s', reddit.read_only)

    if sub:
        sub = sub
    else:
        sub = 'all'

    if lim:
        lim = lim
    else:
        lim = 9
    slp = 0.1

    def parse_comments(comments_list):
        """
        I must have thought I needed this for something.
        """
        for comment in comments_list:
            print(comment)
        pass

    for submission in reddit.subreddit(sub).hot(limit=lim):

        try:
            LOG.debug('Title: %s', submission.title)
            LOG.debug('Score: %s', submission.score)
            LOG.debug('ID: %s', submission.id)
            LOG.debug('URL: %s', submission.url)
            # If submission.author is NoneType it means the comment was [deleted]
            if submission.author:
                LOG.debug('Author: %s', submission.author)
                LOG.debug('Link karma: %s', submission.author.link_karma)

                # Comments
                submission.comments.replace_more(limit=0)
                comments_list = submission.comments.list()

                for comment in comments_list:

                    sleep(slp)
                    sub_comments = []
                    # sub_comments.append(submission.title)
                    sub_comments.append(comment.body)
                    for _idx, rep in enumerate(comment.replies):
                        reply = rep.body.strip('/r/').strip('^')
                        # if comment is > 80:
                        #   find portion of comment that is valid and snip
                        if len(reply) < 80:
                            if not reply == '[removed]':
                                LOG.debug('Appending reply: %s', reply)
                                sub_comments.append(reply)
                        else:
                            LOG.debug('Reply is too long: {}'.format(reply))

                    # If comment chain is at least 5 long train bot.
                    if len(sub_comments) < 5:
                        LOG.debug('Skipping: %s', sub_comments)
                    else:
                        LOG.debug('Comment is %s statements long', len(sub_comments))
                        bot.train(sub_comments)
                        LOG.info('Training: %s', sub_comments)
                        LOG.info('--------------------------------------------')

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
    """
    Train bot using data from Twitter.
    """

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


def loop_trainer(input_s):
    """
    Parameters
    ----------
    input_s : str, required, default = None
        Input string

    * input string
    * process as input_statement
    * get statement and response form chat bot
    * if the response is not the same as the input string
    * train bot with conversation
    """

    bot = chat_bot()
    session = bot.conversation_sessions.new()
    session_id = session.id

    for _var in range(3):

        try:
            input_statement = bot.input.process_input_statement(input_s)
            statement, response = bot.generate_response(input_statement, session_id)
            if str(response) != str(input_s):
                bot.learn_response(response, input_statement)
                bot.conversation_sessions.update(session_id, statement)
                bot.output.process_response(response)

        except (KeyboardInterrupt, EOFError, SystemExit):
            break

    return


def word_list_training():
    """
    * word_list contains 5000 most common words in English language
    * randomize the list
    * pool 4 child processes
    * run [loop_trainer(input_s)](#loop_trainerinput_s) with word as input s 
    """

    filename = 'list_5000'
    word_list = open(filename, "r")
    work = [(line.strip('\n')) for line in word_list]
    random.shuffle(work)
    pool = multiprocessing.Pool(4)
    pool.map(loop_trainer, work)
    pool.close()
    pool.join()


def feedback_bot():
    """
    * ask for input
    * present input_statement and response to user
    * ask if it makes sense
    * if no, user can fix
    * train bot
    """

    bot = chat_bot()
    session = bot.conversation_sessions.new()
    session_id = session.id

    while True:

        try:

            comment = input('input -> ')
            input_statement = bot.input.process_input_statement(comment)
            statement, response = bot.generate_response(input_statement, session_id)
            print('\n Input -> {} \n'.format(input_statement))
            print('\n Output -> {} \n'.format(response))
            print('\n Does this make sense? \n')

            text = input_function()

            if 'y' in text.lower():
                bot.learn_response(response, input_statement)
                bot.conversation_sessions.update(session_id, statement)
            elif 'n' in text.lower():
                print('\n What should my response be? \n')
                new_response = input_function()
                print('###############################')
                print('TODO:')
                print('* Update response -> {}'.format(new_response))
                print('* Train bot with new conversation')
                print('* input -> {}'.format(statement))
                print('* output -> {}'.format(new_response))
                print('###############################')
                # new = bot.output.process_response(new_response)
                # bot.learn_response(new_response, input_statement)
                # bot.conversation_sessions.update(session_id, statement)
                chain = []
                chain.append(statement.text)
                chain.append(new_response)
                bot.train(chain)
            else:
                print('Please type either "y" or "n"')
                return # get_feedback(input_statement, response)


        except (KeyboardInterrupt, EOFError, SystemExit):
            break

    return


def hipchat_bot():
    """
    DOES NOT WORK YET
    """

    hipchat_host, hipchat_room, hipchat_access_token = get_hipchat_envars()
    print(hipchat_host, hipchat_room, hipchat_access_token)

    bot = ChatBot(
        'Hipchat Bot',
        storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
        database='bot_db',
        database_uri='mongodb://mongo:27017/',
        hipchat_host=hipchat_host,
        hipchat_room=hipchat_room,
        hipchat_access_token=hipchat_access_token,
        input_adapter='chatterbot.input.HipChat',
        output_adapter='chatterbot.output.HipChat',
        trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
    )

    while True:
        try:

            response = bot.get_response(None)

        except (KeyboardInterrupt, EOFError, SystemExit):
            break


def gitter_bot():
    """
    * get gitter_room, gitter_api_token from [get_gitter_envars()](#get_gitter_envars)

    Talk to bot with twitter or github access
    * https://gitter.im/jahrik/edward
    """

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
        trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
    )

    while True:
        try:

            response = bot.get_response(None)

        except (KeyboardInterrupt, EOFError, SystemExit):
            break

    return


def voice_bot():
    """
    * input speech to text
    * output text to speech
    """

    bot = ChatBot(
        "Voice Bot",
        storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
        database='bot_db',
        database_uri='mongodb://mongo:27017/',
        input_adapter="chatterbot_voice.VoiceInput",
        output_adapter="chatterbot_voice.VoiceOutput",
        # recognizer_instance="recognize_google_cloud",
    )

    while True:
        try:

            bot_input = bot.get_response(None)

        # Press ctrl-c or ctrl-d on the keyboard to exit
        except (KeyboardInterrupt, EOFError, SystemExit):
            break


def bot_on_bot():
    """
    * make bot talk to another bot.
    * https://www.tolearnenglish.com/free/celebs/audreyg.php
    """
    # from urllib import urlencode
    # import requests
    # params = {'search': 'hello'}
    # search_url = 'https://www.tolearnenglish.com/free/celebs/audreyg.php/submit_search/?'
    # url = search_url + urlencode(params)
    # r = requests.get(url)
    # print(r)
    # now you get your desired response.


def bot_sploit():
    """
    * Search for other bots on reddit
    * Talk to the other bots on reddit
    """
    return


# def export(filename=None):
#     """
#     * export the database
#     * mongoexport -d bot_db -c statements
#     """
#     # return filename
#     # from os.path import join
#     import pymongo
#     # from bson.json_utils import dumps
#     username = 'root'
#     password = 'root'
#     host = 'mongodb://{}:{}@127.0.0.1'.format(username, password)
#     port = 27017
#     database = 'bot_db'
#
#     def backup_db(backup_db_dir):
#         """
#         backup mongo db
#         """
#         pass
#         # client = pymongo.MongoClient(host=host, port=port)
#         # database = client['bot_db']
#         # print(authenticated = database.authenticate())
#         # assert authenticated, "Could not authenticate to database!"
#         # print(collections)
#         # collections = database.collection_names()
#         # for i, collection_name in enumerate(collections):
#             # col = getattr(database,collections[i])
#             # collection = col.find()
#             # jsonpath = collection_name + ".json"
#             # jsonpath = join(backup_db_dir, jsonpath)
#             # with open(jsonpath, 'wb') as jsonfile:
#                 # jsonfile.write(dumps(collection))
#     # bot = chat_bot()
#     # backup_db(backup_db_dir=os.environ['PWD'])
#     # if filename == None:
#         # export = 'export.yml'
#     # else:
#         # backup_db(backup_db_dir=os.environ['PWD'])


def emoji_preprocessor(bot, statement):
    """
    * input emojis to chatterbot
    * http://chatterbot.readthedocs.io/en/stable/preprocessors.html
    * http://www.unicode.org/emoji/charts/full-emoji-list.html
    * https://github.com/gunthercox/ChatterBot/issues/911
    """
    LOG.debug(bot)
    LOG.debug(statement)
    return statement


def facebook_messenger_bot():
    """
    * Connect to facebook messenger
    * API key?: 
    """


def feedback(bot, comment):
    """
    * parse comment for Master commands
    * return response
    """

    # from chatterbot.storage.mongodb import MongoDatabaseAdapter as MDA
    if 'Delete ' in comment:
        delete_this = comment.split("Delete ",1)[1]
        LOG.info('Deleting: %s', delete_this)
        return True
        bot.storage.mongodb.MongoDatabaseAdapter.remove(statement_text=delete_this)
    else:
        return False


def twitter_bot():
    """
    * Create a BotStreamListener(StreamListener) class
    * see details here: [class StreamListener(object):](https://github.com/tweepy/tweepy/blob/8373a0ab040461531c26076693cc99ecd2a7c3f1/tweepy/streaming.py#L31)
    * Start up bot on __init__()
    * watch for data
    * if 'direct_message' and not our user_id:
    * process a response for the message from the database
    * reply with response
    """

    class BotStreamListener(StreamListener):
        """
        * A listener handles private messages that are received from the stream.
        * Listener for handling direct messaging input
        """

        def __init__(self, api=None):
            self.api = api
            self.bot = chat_bot()
            self.session = self.bot.conversation_sessions.new()
            self.session_id = self.session.id

        def on_connect(self):
            LOG.info("Connection established!")

        def on_disconnect(self, notice):
            LOG.info("Connection lost!! : %s", notice)

        def on_status(self, status):
            LOG.info(status.text)
            return True

        def on_data(self, data):
            import json
            LOG.info('Entered on data')
            
            if 'direct_message' in data:
                parsed = json.loads(data)
                sender_id = parsed["direct_message"]["sender_id"]
                sender_name = parsed["direct_message"]["sender_screen_name"]
                comment = parsed["direct_message"]["text"]
                LOG.info('Message Received from: %s', sender_name)
                LOG.info('Message: %s', comment)

                if feedback(self.bot, comment):
                    return True

                else:

                    if int(api.me().id) != int(sender_id):
                        input_statement = self.bot.input.process_input_statement(comment)
                        statement, response = self.bot.generate_response(input_statement, self.session_id)
                        api.send_direct_message(sender_name, text=response)
                        self.bot.learn_response(response, input_statement)
                        self.bot.conversation_sessions.update(self.session_id, statement)

            return True

        def on_error(self, status):
            print(status)
        
        
    def limit_handled(cursor):
        """
        * Rate limit handler for twitter
        * sleep for a few minutes
        """

        while True:
            try:
                yield cursor.next()
            except tweepy.RateLimitError:
                sleep(60 * 3)

    def twitter_search(search, limit):
        """
        Search twitter for x
        """
        search_results = ()
        for tweet in tweepy.Cursor(api.search, q='#{}'.format(search)).items():
            try:
               print('Tweet by: @' + tweet.user.screen_name)
               sleep(5)

            except tweepy.TweepError as e:
                print(e.reason)

            except StopIteration:
                break
        return search_results


    def twitter_retweet(search, limit):
        """
        * twitter_search(search)
        * retweet the things
        * limit how many
        """
        search_results = twitter_search(search, 3)
        for tweet in search_resulsts:
            try:
                tweet.retweet()
            except tweepy.TweepError as e:
                LOG.error(e.reason)
                sleep(5)

        return


    twitter_key, twitter_secret, twitter_token, twitter_token_secret = get_twitter_envars()

    auth = tweepy.OAuthHandler(twitter_key, twitter_secret)
    auth.set_access_token(twitter_token, twitter_token_secret)
    api = tweepy.API(auth)
    LOG.info('Accessing API as: %s', api.me().name)

    ############################################################################
    # Auto follow followers
    ############################################################################

    def follow_daemon():
        p = multiprocessing.current_process()
        LOG.info('Starting:{} {}'.format(p.name, p.pid))

        # follow every follower of the authenticated user.
        while True:
            for follower in limit_handled(tweepy.Cursor(api.followers).items()):
                # LOG.debug('Follower: %s', follower.screen_name)
                follower.follow()
                
            # sys.stdout.flush()
            time.sleep(60 * 5)
        LOG.info('Exiting: {} {}'.format(p.name, p.pid))
        # sys.stdout.flush()

    d = multiprocessing.Process(name='follow_daemon', target=follow_daemon)
    d.daemon = True

    d.start()

    ############################################################################

    try:
        LOG.info("Starting bot_stream for %s", api.me().name)
        bot_stream_listener = BotStreamListener()
        stream = tweepy.Stream(auth=api.auth, listener=bot_stream_listener)
        stream.userstream()

    except BaseException as err:
        LOG.error("Twitter Bot Error: %s", err)


def main():
    """
    * check docopt args
    """

    args = docopt(__doc__, version=VERSION)

    if '--bot' in args and args.get('--bot'):
        bot = args.get('--bot')
    if '--training' in args and args.get('--training'):
        training = args.get('--training')
    if '--export' in args and args.get('--export'):
        exp = args.get('--export')
        export(exp)

    if training == 'english':
        english_training()
    elif training == 'word_list':
        word_list_training()
    elif training == 'ubuntu':
        ubuntu_training()
    elif training == 'reddit':
        reddit_training(sub='all', lim=99)
    elif training == 'twitter':
        twitter_training()
    else: # training:
        # exit("{0} is not a command. \nSee: './edward.py --help'".format(training))
        pass

    if bot == 'feedback':
        feedback_bot()
    if bot == 'hipchat':
        hipchat_bot()
    elif bot == 'gitter':
        gitter_bot()
    elif bot == 'twitter':
        twitter_bot()
    elif bot == 'voice':
        voice_bot()
    else: # bot:
        # exit("{0} is not a command. \nSee: './edward.py --help'".format(bot))
        pass

if __name__ == '__main__':

    LOG = logging_setup()

    main()
