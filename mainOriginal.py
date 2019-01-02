#---            Official /r/MurderedByWords bot by /u/jackson1442           ---#
# This bot is now licensed with the MIT license. See the licensefile for more
# details. See more cool stuff with extremely specific applications at
# github.com/jackson1442
import praw, time, ConfigParser

Config = ConfigParser.ConfigParser()
print(Config.read("botconfig.ini"))
nextline = "\n\n"


def getstring(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

accountName = Config.get("basics", 'account name')
# import kdapi
r = praw.Reddit(accountName, user_agent="trying this garbage again")
# poltags = ['[pol]', '[political]', '[politics]', '[politician]']

def uniqid():
    return hex(int(time.time()*10000000))[2:17]

currentSubreddit = Config.get("basics", 'subreddit')
print(currentSubreddit)
logsub = Config.get("logging", 'logsub')

scoreA = Config.getint("flairing", "flair a")
scoreB = Config.getint("flairing", "flair b")

removeB = Config.getint("flairing", "remove b")
removeA = Config.getint("flairing", "remove a")

commentText = Config.get("basics", 'autocomment').decode("string-escape")
commentA = commentText + Config.get("flairing", 'flair success a').decode("string-escape")
commentB = commentText + Config.get("flairing", 'flair success b').decode("string-escape")

nameA = Config.get("flairing", 'flair a name')
classA = Config.get("flairing", 'flair a class')
nameB = Config.get("flairing", 'flair b name')
classB = Config.get("flairing", 'flair b class')

footer = Config.get("basics", 'footer').decode("string-escape") + '\n\n^bot ^by ^jackson1442 ^| ^[faq](https://jackson1442.github.io/flairbot/#faq) ^| ^[source](https://github.com/jackson1442/redditBot) ^| ^action ^#'
notice1 = Config.get("notices", 'message 1').decode("string-escape")
notice2 = Config.get("notices", 'message 2').decode("string-escape")

override = Config.getboolean("flairing", "override")
overrideClassA = Config.get("flairing", "override class a")
overrideClassB = Config.get("flairing", "override class b")


if time.time() < Config.getint("notices", "timestamp 1"):
    specialNotice = notice1
else:
    specialNotice = ""
if time.time() < Config.getint("notices", "timestamp 2"):
    specialNotice += notice2

