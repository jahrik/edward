Build and test with docker-compose
```
make test
```

Build and deploy to docker swarm
```
make deploy

docker stack services edward
ID                  NAME                MODE                REPLICAS            IMAGE               PORTS
i3laoiilqi76        edward_mongo        replicated          1/1                 mongo:latest        *:27017->27017/tcp
qyio6ac50xyt        edward_bot          replicated          1/1                 bot:latest
```
## Module defs
#### `bot_on_bot()`

make bot talk to another bot.
https://www.tolearnenglish.com/free/celebs/audreyg.php

#### `bot_sploit()`

Search for other bots on reddit
Talk to the other bots on reddit

#### `chat_bot()`

* https://github.com/gunthercox/ChatterBot
* Create default bot
* return chatbot

#### `emoji_preprocessor(bot, statement)`

input emojis to chatterbot
http://chatterbot.readthedocs.io/en/stable/preprocessors.html
http://www.unicode.org/emoji/charts/full-emoji-list.html
https://github.com/gunthercox/ChatterBot/issues/911

#### `english_training()`

* get base bot [chat_bot()](#chat_bot)
* train basic english with
* [chatterbot.corpus.english](https://github.com/gunthercox/chatterbot-corpus/tree/master/chatterbot_corpus/data/english)

#### `export(filename=None)`

export the database
mongoexport -d bot_db -c statements

#### `feedback_bot()`

Present input_statement and response to user
Ask if it makes sense
If no, fix
Train bot

#### `get_gitter_envars()`

* get Gitter room and api token from envars
* you can obtain an api token at:
* https://developer.gitter.im/apps
* return gitter_room, gitter_api_token

#### `get_hipchat_envars()`

* get HipChat host, room, and api token from envars
* you can obtain an api token at:
* https://hipchat.com/admin/api
* return hipchat_host, hipchat_room, hipchat_access_token

#### `get_reddit()`

* obtain client_id, client_secret, username, password from [get_reddit_envars()](#get_reddit_envars)
* set reddit to praw.Reddit
* return reddit

#### `get_reddit_envars()`

* get Reddit creds from envars
* return client_id, client_secret, username, password

#### `get_sub_comments(comment)`

* get sub comments from a reddit comment object as a list
* generate a list of sub_comments from all replies
* return sub_comments

#### `get_twitter_envars()`

* get Twitter creds from envars
* return twitter_key, twitter_secret, twitter_token, twitter_token_secret

#### `gitter_bot()`

Gitter bot

https://gitter.im/jahrik/edward


#### `hipchat_bot()`

See the HipChat api documentation for how to get a user access token.
https://developer.atlassian.com/hipchat/guide/hipchat-rest-api/api-access-tokens

#### `logging_setup()`

* setup logging
* return logger

#### `loop_trainer(input_s)`

loop through input_statements

#### `main()`

main

#### `reddit_training(sub, lim)`

- **`sub`** `str` `optional` `default = 'all'`

   Which subreddit to use

- **`lim`** `int` `optional` `default = 9`

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

#### `twitter_training()`

Train bot using data from Twitter.

#### `ubuntu_training()`

* *THIS IS BROKEN RIGHT NOW*
* get base bot [chat_bot()](#chat_bot)
* train with ubuntu corpus
* [chatterbot.corpus.ubuntu](https://github.com/gunthercox/ChatterBot/blob/b611cbd0629eb2aed9f840b50d1b3f8869c2589e/chatterbot/trainers.py#L236)
* see [Training with the Ubuntu dialog corpus](http://chatterbot.readthedocs.io/en/stable/training.html#training-with-the-ubuntu-dialog-corpus)

#### `voice_bot()`

Voice bot

#### `word_list_training()`

take word list
train bot word in list for loop amount
