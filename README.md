# Reddit bot
A small bot for learning praw

## Usage: 
```
./bot.py -h
    A small bot for learning praw

    Usage:
        bot.py [-l <level> | --level <level>]
               [-t <reddit> | --training <reddit>]

    Options:
        -h --help               Show this screen
        -l --level=<level>      [default: info]
        -t --training=<reddit>    Training level [default: reddit]

    Be sure to export envars first:
        export REDDIT_CLIENT_ID=''
        export REDDIT_CLIENT_SECRET=''
        export REDDIT_USERNAME=''
        export REDDIT_PASSWORD=''
```

### Training mode
* train your bot!
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

### Reddit mode
* Specify a subreddit
* Specify limit
* bot will gather entire comment chain from limit of top posts
* bot will train with comment chain
* bot will respond to first comment
