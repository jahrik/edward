# Reddit bot

[![Join the chat at https://gitter.im/jahrik/reddit_bot](https://badges.gitter.im/jahrik/reddit_bot.svg)](https://gitter.im/jahrik/reddit_bot?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
A small bot that utilizes praw and chatterbot
* [PRAW](https://praw.readthedocs.io/en/latest/)
* [ChatterBot](https://github.com/gunthercox/ChatterBot)

## Table of Contents

  * [Usage:](#usage)
     * [Training mode](#training-mode)
     * [Reddit mode](#reddit-mode)

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
```
./bot.py -t reddit
2017-09-21 05:29:28.754 INFO bot - chat_bot: Teaching bot basic english...
ai.yml Training: [####################] 100%
botprofile.yml Training: [####################] 100%
computers.yml Training: [####################] 100%
conversations.yml Training: [####################] 100%
drugs.yml Training: [####################] 100%
emotion.yml Training: [####################] 100%
food.yml Training: [####################] 100%
gossip.yml Training: [####################] 100%
greetings.yml Training: [####################] 100%
history.yml Training: [####################] 100%
humor.yml Training: [####################] 100%
literature.yml Training: [####################] 100%
money.yml Training: [####################] 100%
movies.yml Training: [####################] 100%
politics.yml Training: [####################] 100%
psychology.yml Training: [####################] 100%
science.yml Training: [####################] 100%
sports.yml Training: [####################] 100%
trivia.yml Training: [####################] 100%
2017-09-21 05:29:39.826 INFO bot - reddit_mode: Read only?: False
2017-09-21 05:29:44.488 INFO bot - reddit_mode: Title: Guardians of the Front Page
2017-09-21 05:29:44.490 INFO bot - reddit_mode: Score: 283484
2017-09-21 05:29:44.490 INFO bot - reddit_mode: ID: 5gn8ru
2017-09-21 05:29:44.491 INFO bot - reddit_mode: URL: http://i.imgur.com/OOFRJvr.gifv
2017-09-21 05:29:44.491 INFO bot - reddit_mode: Author: iH8myPP
2017-09-21 05:29:44.647 INFO bot - reddit_mode: Link karma: 311141
List Trainer: [####################] 100%
2017-09-21 05:29:54.001 INFO input_adapter - process_input_statement: Recieved input statement: Remember when the highest upvoted post you saw in a week had 5000 points?

EDIT: For those that are just getting to this post and are confused, when I posted this comment the OP was over 21,000 points. Yes, I know it currently says 11,000 total votes. As many people replied to me, reddit's algorithms fudge the votes in interesting ways to try to keep the front page changing.

EDIT 2: Yes ladies and gents, I know where it's at now. Insane.
2017-09-21 05:29:54.012 INFO input_adapter - process_input_statement: "Remember when the highest upvoted post you saw in a week had 5000 points?

EDIT: For those that are just getting to this post and are confused, when I posted this comment the OP was over 21,000 points. Yes, I know it currently says 11,000 total votes. As many people replied to me, reddit's algorithms fudge the votes in interesting ways to try to keep the front page changing.

EDIT 2: Yes ladies and gents, I know where it's at now. Insane. " is a known statement
2017-09-21 05:29:56.195 INFO best_match - process: Using "Remember when the highest upvoted post you saw in a week had 5000 points? EDIT: For those that are just getting to this post and are confused, when I posted this comment the OP was over 21,000 points. Yes, I know it currently says 11,000 total votes. As many people replied to me, reddit's algorithms fudge the votes in interesting ways to try to keep the front page changing. EDIT 2: Yes ladies and gents, I know where it's at now. Insane." as a close match to "Remember when the highest upvoted post you saw in a week had 5000 points?

EDIT: For those that are just getting to this post and are confused, when I posted this comment the OP was over 21,000 points. Yes, I know it currently says 11,000 total votes. As many people replied to me, reddit's algorithms fudge the votes in interesting ways to try to keep the front page changing.

EDIT 2: Yes ladies and gents, I know where it's at now. Insane. "
2017-09-21 05:29:56.198 INFO best_match - process: Selecting response from 1 optimal responses.
2017-09-21 05:29:56.198 INFO response_selection - get_first_response: Selecting first response from list of 1 options.
2017-09-21 05:29:56.198 INFO best_match - process: Response selected. Using "Can't wait to upvote this 17 different times later this week."
2017-09-21 05:29:56.198 INFO multi_adapter - process: BestMatch selected "Can't wait to upvote this 17 different times later this week." as a response with a confidence of 0.99
2017-09-21 05:29:58.498 INFO multi_adapter - process: LowConfidenceAdapter selected "I am sorry, but I do not understand." as a response with a confidence of 0
2017-09-21 05:29:58.500 INFO multi_adapter - process: NoKnowledgeAdapter selected "Remember when the highest upvoted post you saw in a week had 5000 points? EDIT: For those that are just getting to this post and are confused, when I posted this comment the OP was over 21,000 points. Yes, I know it currently says 11,000 total votes. As many people replied to me, reddit's algorithms fudge the votes in interesting ways to try to keep the front page changing. EDIT 2: Yes ladies and gents, I know where it's at now. Insane." as a response with a confidence of 0
2017-09-21 05:29:58.515 INFO bot - reddit_mode: Comment: Remember when the highest upvoted post you saw in a week had 5000 points?

EDIT: For those that are just getting to this post and are confused, when I posted this comment the OP was over 21,000 points. Yes, I know it currently says 11,000 total votes. As many people replied to me, reddit's algorithms fudge the votes in interesting ways to try to keep the front page changing.

EDIT 2: Yes ladies and gents, I know where it's at now. Insane.
2017-09-21 05:29:58.515 INFO bot - reddit_mode: Response: Can't wait to upvote this 17 different times later this week.
2017-09-21 05:29:58.515 INFO bot - reddit_mode: ------------------------------------------------------------
2017-09-21 05:30:01.518 INFO bot - reddit_mode: Title: Thanks, Obama.
2017-09-21 05:30:01.519 INFO bot - reddit_mode: Score: 230827
2017-09-21 05:30:01.519 INFO bot - reddit_mode: ID: 5bx4bx
2017-09-21 05:30:01.520 INFO bot - reddit_mode: URL: https://i.reddituploads.com/58986555f545487c9d449bd5d9326528?fit=max&h=1536&w=1536&s=c15543d234ef9bbb27cb168b01afb87d
2017-09-21 05:30:01.520 INFO bot - reddit_mode: Author: Itsjorgehernandez
2017-09-21 05:30:01.678 INFO bot - reddit_mode: Link karma: 14364
List Trainer: [####################] 100%
2017-09-21 05:30:11.891 INFO input_adapter - process_input_statement: Recieved input statement: ^^psst, ^^hey ^^kid, ^^want ^^some ^^[livethread](https://www.reddit.com/live/xw7ya3zdewzc)?
2017-09-21 05:30:11.895 INFO input_adapter - process_input_statement: "^^psst, ^^hey ^^kid, ^^want ^^some ^^[livethread](https://www.reddit.com/live/xw7ya3zdewzc)?" is a known statement
2017-09-21 05:30:13.971 INFO best_match - process: Using "^^psst, ^^hey ^^kid, ^^want ^^some ^^[livethread](https://www.reddit.com/live/xw7ya3zdewzc)?" as a close match to "^^psst, ^^hey ^^kid, ^^want ^^some ^^[livethread](https://www.reddit.com/live/xw7ya3zdewzc)?"
2017-09-21 05:30:13.974 INFO best_match - process: Selecting response from 1 optimal responses.
2017-09-21 05:30:13.974 INFO response_selection - get_first_response: Selecting first response from list of 1 options.
2017-09-21 05:30:13.974 INFO best_match - process: Response selected. Using "The president we needed. Now time for the one we deserve."
2017-09-21 05:30:13.974 INFO multi_adapter - process: BestMatch selected "The president we needed. Now time for the one we deserve." as a response with a confidence of 1.0
2017-09-21 05:30:15.998 INFO multi_adapter - process: LowConfidenceAdapter selected "I am sorry, but I do not understand." as a response with a confidence of 0
2017-09-21 05:30:16.000 INFO multi_adapter - process: NoKnowledgeAdapter selected "^^psst, ^^hey ^^kid, ^^want ^^some ^^[livethread](https://www.reddit.com/live/xw7ya3zdewzc)?" as a response with a confidence of 0
2017-09-21 05:30:16.000 INFO chatterbot - learn_response: Adding "^^psst, ^^hey ^^kid, ^^want ^^some ^^[livethread](https://www.reddit.com/live/xw7ya3zdewzc)?" as a response to "Can't wait to upvote this 17 different times later this week."
2017-09-21 05:30:16.014 INFO bot - reddit_mode: Comment: ^^psst, ^^hey ^^kid, ^^want ^^some ^^[livethread](https://www.reddit.com/live/xw7ya3zdewzc)?
2017-09-21 05:30:16.014 INFO bot - reddit_mode: Response: The president we needed. Now time for the one we deserve.
2017-09-21 05:30:16.014 INFO bot - reddit_mode: ------------------------------------------------------------
```
