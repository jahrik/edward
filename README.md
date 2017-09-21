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
```
./bot.py -t training
How can I help you? hello bot
2017-09-21 03:55:01.091 INFO input_adapter - process_input_statement: Recieved input statement: hello bot
2017-09-21 03:55:01.098 INFO input_adapter - process_input_statement: "hello bot" is not a known statement
2017-09-21 03:55:23.150 INFO best_match - process: Using "hello bot" as a close match to "hello"
2017-09-21 03:55:23.155 INFO best_match - process: Selecting response from 1 optimal responses.
2017-09-21 03:55:23.155 INFO response_selection - get_first_response: Selecting first response from list of 1 options.
2017-09-21 03:55:23.156 INFO best_match - process: Response selected. Using "howdy"
2017-09-21 03:55:23.156 INFO multi_adapter - process: BestMatch selected "howdy" as a response with a confidence of 0.71
2017-09-21 03:55:44.310 INFO multi_adapter - process: LowConfidenceAdapter selected "I am sorry, but I do not understand." as a response with a confidence of 0
2017-09-21 03:55:44.313 INFO multi_adapter - process: NoKnowledgeAdapter selected "hello bot" as a response with a confidence of 0
2017-09-21 03:55:44.327 INFO bot - bot_training: Comment: hello bot
2017-09-21 03:55:44.327 INFO bot - bot_training: Response: howdy
How can I help you?
```

### Reddit mode
```

```
