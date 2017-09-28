# Edward
* A small bot that utilizes praw and chatterbot to connect to multiple services
* chatterbot: https://github.com/gunthercox/ChatterBot
* PRAW: https://praw.readthedocs.io/en/latest/

## Dependencies
* python 3.5+
* Be sure to export envars first:
```
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
```

## TOC
   * [Edward](#edward)
      * [Dependencies](#dependencies)
      * [Usage](#usage)
      * [Module defs](#module-defs)
            * [bot_on_bot()](#bot_on_bot)
            * [bot_sploit()](#bot_sploit)
            * [chat_bot()](#chat_bot)
            * [emoji_preprocessor(bot, statement)](#emoji_preprocessorbot-statement)
            * [english_training()](#english_training)
            * [export(filename=None)](#exportfilenamenone)
            * [feedback_bot()](#feedback_bot)
            * [get_gitter_envars()](#get_gitter_envars)
            * [get_hipchat_envars()](#get_hipchat_envars)
            * [get_reddit()](#get_reddit)
            * [get_reddit_envars()](#get_reddit_envars)
            * [get_sub_comments(comment)](#get_sub_commentscomment)
            * [get_twitter_envars()](#get_twitter_envars)
            * [gitter_bot()](#gitter_bot)
            * [hipchat_bot()](#hipchat_bot)
            * [logging_setup()](#logging_setup)
            * [loop_trainer(input_s)](#loop_trainerinput_s)
            * [main()](#main)
            * [reddit_training()](#reddit_training)
            * [twitter_training()](#twitter_training)
            * [ubuntu_training()](#ubuntu_training)
            * [voice_bot()](#voice_bot)
            * [word_list_training()](#word_list_training)
## Usage
```
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
```
## Module defs
#### `bot_on_bot()`

make bot talk to another bot.
https://www.tolearnenglish.com/free/celebs/audreyg.php

#### `bot_sploit()`

Search for other bots on reddit
Talk to the other bots on reddit

#### `chat_bot()`

https://github.com/gunthercox/ChatterBot

#### `emoji_preprocessor(bot, statement)`

input emojis to chatterbot
http://chatterbot.readthedocs.io/en/stable/preprocessors.html
http://www.unicode.org/emoji/charts/full-emoji-list.html
https://github.com/gunthercox/ChatterBot/issues/911

#### `english_training()`

Train basic english

#### `export(filename=None)`

export the database
mongoexport -d bot_db -c statements

#### `feedback_bot()`

Present input_statement and response to user
Ask if it makes sense
If no, fix
Train bot

#### `get_gitter_envars()`

* Set Gitter room and api token.
* You can obtain an api token at:
* https://developer.gitter.im/apps
returns gitter_room, gitter_api_token

#### `get_hipchat_envars()`

Set HipChat room and api token.
You can obtain an api token at:
https://hipchat.com/admin/api

#### `get_reddit()`

Get praw.Reddit

#### `get_reddit_envars()`

Reddit creds

#### `get_sub_comments(comment)`

get sub comments from a reddit comment object as a list

#### `get_twitter_envars()`

Set Twitter creds

#### `gitter_bot()`

Gitter bot

https://gitter.im/jahrik/edward


#### `hipchat_bot()`

See the HipChat api documentation for how to get a user access token.
https://developer.atlassian.com/hipchat/guide/hipchat-rest-api/api-access-tokens

#### `logging_setup()`

Setup logging

#### `loop_trainer(input_s)`

loop through input_statements

#### `main()`

main

#### `reddit_training()`

Grab lim comment trees from r/sub to train the bot

#### `twitter_training()`

Train bot using data from Twitter.

#### `ubuntu_training()`

This is an example showing how to train a chat bot using the
Ubuntu Corpus of conversation dialog.

#### `voice_bot()`

Voice bot

#### `word_list_training()`

take word list
train bot word in list for loop amount
