# Edward
* A small bot that utilizes praw and chatterbot to connect to multiple services
* [PRAW](https://praw.readthedocs.io/en/latest/)
* [ChatterBot](https://github.com/gunthercox/ChatterBot)
* train with:
  * reddit
  * twitter
  * gitter
  * hipchat
  * manual feedback

## Usage: 
```
./edward.py -h
    A small bot that uses praw and chatterbot
    Various training types include (manual, reddit, twitter, etc)

    Usage:
        bot.py [-l <level> | --level <level>]
               [-t <type> | --training <type>]

    Options:
        -h --help               Show this screen
        -l --level=<level>      [default: info]
        -t --training=<type>    Training level [default: manual]

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

```

### Manual
* train bot
* raw input mode
* bot will ask you how it can help?
* and carry on a conversation from there
* will take your response and learn from it
```
How can I help you?: hello
...
2017-09-21 05:13:45.822 INFO bot - bot_training: Comment: hello
2017-09-21 05:13:45.823 INFO bot - bot_training: Response: hello
2017-09-21 05:13:45.823 INFO bot - bot_training: Training bot: ['How can I help you?: ', 'hello']
List Trainer: [####################] 100%
hello: Good day!
...
2017-09-21 05:14:00.166 INFO bot - bot_training: Comment: Good day!
2017-09-21 05:14:00.166 INFO bot - bot_training: Response: ok :) :)
2017-09-21 05:14:00.166 INFO bot - bot_training: Training bot: ['hello: ', 'Good day!']
List Trainer: [####################] 100%
ok :) :): What are you?
...
2017-09-21 05:14:17.346 INFO bot - bot_training: Comment: What are you?
2017-09-21 05:14:17.346 INFO bot - bot_training: Response: Who? Who is but a form following the function of what
2017-09-21 05:14:17.346 INFO bot - bot_training: Training bot: ['ok :) :): ', 'What are you?']
List Trainer: [####################] 100%
Who? Who is but a form following the function of what:
...
```

### Reddit
* Specify a subreddit
* Specify limit
* bot will gather entire comment chain from limit of top posts
* bot will train with comment chain
* bot will respond to first comment
```
./bot.py -t reddit
2017-09-21 05:29:39.826 INFO bot - reddit_mode: Read only?: False
2017-09-21 05:29:44.488 INFO bot - reddit_mode: Title: Guardians of the Front Page
2017-09-21 05:29:44.490 INFO bot - reddit_mode: Score: 283484
2017-09-21 05:29:44.490 INFO bot - reddit_mode: ID: 5gn8ru
2017-09-21 05:29:44.491 INFO bot - reddit_mode: URL: http://i.imgur.com/OOFRJvr.gifv
2017-09-21 05:29:44.491 INFO bot - reddit_mode: Author: iH8myPP
2017-09-21 05:29:44.647 INFO bot - reddit_mode: Link karma: 311141
List Trainer: [####################] 100%
...
...
```

### Twitter

* cronjob runs every 10 minutes [here](https://github.com/jahrik/edward/blob/a011045b11c75d431c42511f0ec91c6799f745ec/crontab#L2)
* Training
```
docker exec -it bot bash
root@8d298baf24d5:/src# ./edward.py -t twitter
2017-09-23 08:03:31.239 INFO trainers - get_statements: Requesting 50 random tweets containing the word from
2017-09-23 08:03:34.138 INFO trainers - get_statements: Adding 8 tweets with responses
2017-09-23 08:03:34.877 INFO trainers - get_statements: Requesting 50 random tweets containing the word Trust
2017-09-23 08:03:37.857 INFO trainers - get_statements: Adding 8 tweets with responses
2017-09-23 08:03:38.631 INFO trainers - get_statements: Requesting 50 random tweets containing the word picked
2017-09-23 08:03:39.998 INFO trainers - get_statements: Adding 3 tweets with responses
...
...
2017-09-23 08:04:00.921 INFO edward - twitter_training: Trained database generated successfully!
```

### Gitter

* bot defaults to listening to gitter room
* [https://gitter.im/jahrik/edward](https://gitter.im/jahrik/edward)
* does not respond yet
