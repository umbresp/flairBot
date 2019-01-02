#---            FlairBot by /u/jackson1442           ---#
# This bot is now licensed with the MIT license. See the licensefile for more
# details. See more cool stuff with extremely specific applications at
# github.com/jackson1442

#---            Python3 Port by /u/Umbresp           ---#
# I have more shit too. github.com/umbresp

import configparser
import praw
import time
from utils import *


NEXTLINE = '\n\n'
config = configparser.RawConfigParser()

print(config.read('botconfig.ini'))

account_name = config.get('basics', 'account name')
reddit_instance = praw.Reddit(account_name, user_agent='flairBot.py')
current_subreddit = config.get('basics', 'subreddit')

# print(current_subreddit)

logsub = config.get("logging", 'logsub')
upvote_flair_limit = config.getint("flairing", 'flair a')
downvote_flair_limit = config.getint("flairing", 'flair b')
upvote_remove_limit = config.getint("flairing", 'remove a')
downvote_remove_limit = config.getint("flairing", 'remove b')

# print(type(config.get('basics', 'autocomment')))

comment_body = config.get("basics", 'autocomment')
upvote_flaired = comment_body + config.get("flairing", 'flair success a')
downvote_flaired = comment_body + config.get("flairing", 'flair success b')

upvote_flair_name = config.get("flairing", 'flair a name')
upvote_flair_class = config.get("flairing", 'flair a class')
downvote_flair_name = config.get("flairing", 'flair b name')
downvote_flair_class = config.get("flairing", 'flair b class')

footer = config.get("basics", 'footer') + '\n\n^bot ^by ^umbresp and jackson1442 ^| ^[faq](https://jackson1442.github.io/flairbot/#faq) ^| ^[source](https://github.com/jackson1442/redditBot) ^| ^action ^#'
notice1 = config.get("notices", 'message 1')
notice2 = config.get("notices", 'message 2')

override = config.getboolean("flairing", 'override')
overrideClassA = config.get("flairing", 'override class a')
overrideClassB = config.get("flairing", 'override class b')

if time.time() < config.getint("notices", "timestamp 1"):
    special_notice = notice1
else:
    special_notice = ""
if time.time() < config.getint("notices", "timestamp 2"):
    special_notice += notice2

f = open("logfile.txt", "a+")

print(unique_id())

# END variable declaration

#--- comment on new posts, hide from /new ---#

for post in reddit_instance.subreddit(current_subreddit).new():
    # get an id
    action_id = unique_id()

    # post on logsub then lock
    logpost = reddit_instance.subreddit(logsub).submit(action_id + ' - Commented on post "' + post.title[:50] + '"', url='https://www.reddit.com' + post.permalink)
    logpost.mod.lock() 
    logpost.mod.approve()

    # if more than a day old, stop
    if time.time() - post.created_utc > 86400: 
        break
    
    # reply to the post and sticky the comment
    comment = post.reply(comment_body + special_notice + footer + '['+action_id+']('+logpost.permalink+')')
    comment.mod.distinguish(how='yes', sticky=True)
    comment.clear_vote() 

    # save the comment and hide the post
    comment.save()
    post.hide()

    # logging
    print('Commented on post id ' + post.id)
    f.write('\nCommented on post ' + post.permalink + ' - ' + action_id)

#--- check for unapproved posts beyond threshold ---#
if config.getboolean("approval", "required") == 'yes':
    for u in reddit_instance.subreddit(current_subreddit).mod.unmoderated():
        if u.score > config.getint("approval", "threshold"):

            # get post details
            link = u.permalink
            author = str(u.author)
            action_id = unique_id()

            # post in logsub
            logpost = reddit_instance.subreddit(logsub).submit(action_id + ' - Temporarily removed post "' + u.title[:50] + '"', url='https://reddit.com' + u.permalink)
            logpost.mod.lock()
            logpost.mod.approve()
            temp_removal_message = config.get("approval", 'comment')

            # modmail
            reddit_instance.subreddit(current_subreddit).modmail.create('Post temporarily removed', temp_removal_message + footer + '['+action_id+']('+logpost.permalink+')', str(u.author))
            
            # reply and sticky
            comment = u.reply(temp_removal_message + footer + '['+action_id+']('+logpost.permalink+')')
            comment.mod.distinguish(how='yes', sticky=True)
            
            # remove the post
            u.mod.remove()
            u.report("Temporarily removed due to upvotes with no approval. Please verify.")

            # logging
            print('temporarily removed post ' + u.permalink)
            f.write('\nRemoved post ' + u.permalink + ' temporarily for review - ' + action_id)
            

time.sleep(10)

#--- Sort through previously made comments, flair/edit accordingly. ---#

for comment in reddit_instance.redditor(account_name).saved():
    current_comment = comment.body.split('#')[0]
    action_id = unique_id()
    print(comment.parent().permalink)

    # ~ 5 days. weird flex, but ok
    if time.time() - comment.created_utc > 423000:
        # flair as if the comment were downvoted
        comment.parent().mod.flair(text=downvote_flair_name, css_class=downvote_flair_class)
        comment.parent().mod.approve()
        print('removed comment id ' + comment.permalink + ' because of oldeness')
        reddit_instance.subreddit(logsub).submit(action_id + ' - Flaired post "' + comment.parent().title[:50] + '" as ' + downvote_flair_name + ' (auto-old)', url='https://reddit.com' + comment.parent().permalink).mod.lock()
        comment.delete()
        continue

    # another mod overrode the sticky
    if comment.stickied != True: 
        comment.delete()
        continue

    # shouldn't ever happen, but just in case reddit breaks
    if comment.author != account_name: 
        continue

    # parent post was deleted
    if comment.parent().author == '[deleted]': 
        comment.delete()
        continue

    # comment was upvoted
    if comment.score > upvote_flair_limit:
        # comment has not already been edited
        if current_comment != upvote_flaired + special_notice + footer[:-1]:
            # post in logsub
            logpost = reddit_instance.subreddit(logsub).submit(action_id + ' - Flaired post "' + comment.parent().title[:50] + '"... as ' + upvote_flair_name, url='https://reddit.com' + comment.parent().permalink)
            logpost.mod.lock()
            logpost.mod.approve()
            # edit comment
            comment.edit(upvote_flaired + special_notice + footer + '['+action_id+']('+logpost.permalink+')')
            comment.parent().mod.flair(text=upvote_flair_name, css_class=upvote_flair_class)
            # logging
            print('edited comment ' + comment.permalink)            
            f.write('\nFlaired post ' + comment.parent().permalink + ' as ' + upvote_flair_name + ' - ' + action_id)
            
        if comment.score > upvote_remove_limit: 
            comment.delete()

    # comment was downvoted
    elif comment.score < downvote_flair_limit:
        # comment has not already been upvoted
        if current_comment != downvote_flaired + special_notice + footer[:-1]:
            # post in logsub
            logpost = reddit_instance.subreddit(logsub).submit(action_id + ' - Flaired post "' + comment.parent().title[:50] + '"... as ' + downvote_flair_name, url='https://reddit.com' + comment.parent().permalink)
            logpost.mod.lock()
            logpost.mod.approve()
            # edit comment
            comment.edit(downvote_flaired + special_notice + footer + '['+action_id+']('+logpost.permalink+')')
            comment.parent().mod.flair(text=downvote_flair_name, css_class=downvote_flair_class)
            # logging
            print('edited comment id ' + comment.permalink)
            f.write('\nFlaired post ' + comment.parent().permalink + ' as ' + downvote_flair_name + ' - ' + action_id)
            
        # the downvotes are too much
        if (comment.score < downvote_remove_limit) and config.getboolean("flairing", "report"):
            comment.parent().report(config.get("flairing", 'reason') + action_id)
            comment.delete()
            f.write('\nReported post ' + comment.parent().permalink + ' as potential low quality - ' + action_id)
            reddit_instance.subreddit(logsub).submit(action_id + ' - Reported post "' + comment.parent().title[:50] + '" as potential LQ', url='https://reddit.com' + comment.parent().permalink).mod.lock()
    
    # ???      
    else: 
        continue
    print(comment.parent().permalink)
    
f.close()
exit()
