import ConfigParser
config = ConfigParser.ConfigParser()
print ("Hello! Thanks for using flairbot by jackson1442.\nThis script will walk\
you through the creation of your configuration file.\nFirst thing's first - \
please read the README in the package before starting.")

cfgfile = open('botconfig.ini', 'w')

#-- BASICS --#

config.add_section('basics')

subreddit = raw_input('What subreddit do you plan to run this bot on? ')
config.set('basics','subreddit',subreddit)

commentText = raw_input('What do you want the bot\'s autocomment to say? ')
config.set('basics','autocomment',commentText)

footer = raw_input('Need a footer? If you do, please enter it here, otherwise, enter "\\n". ')
config.set('basics','footer',footer)

acctName = raw_input('What is the name of the account this bot will run on? Do not include the /u/. ')
config.set('basics','account name',acctName)

#-- FLAIRING --#

config.add_section('flairing')

print ('Now on to flairing! Please fill in all values unless it says otherwise. You can change these at any time. ')

nameA = raw_input('What should the text of flair A be? ')
config.set('flairing','flair a name',nameA)
classA = raw_input('What should the css class of flair A be? ')
config.set('flairing','flair a class',classA)
pointsA = input('How many points should the comment receive to set flair A? (should be positive)' )
config.set('flairing','flair a',pointsA)
successA = raw_input('What do you want the bot to append to its comment once the post has been flaired as A? (enter "\\n" to disable) ')
config.set('flairing','flair success a',successA)

nameB = raw_input('What should the text of flair B be? ')
config.set('flairing','flair b name',nameB)
classB = raw_input('What should the css class of flair B be? ')
config.set('flairing','flair b class',classB)
pointsB = input('How many points should the comment receive to set flair B? (should be negative) ')
config.set('flairing','flair b',pointsB)
successB = raw_input('What do you want the bot to append to its comment once the post has been flaired as B? (enter "\\n" to disable) ')
config.set('flairing','flair success b',successB)
report = raw_input('Should the bot report posts that are flaired as '+nameB+' for moderator attention? (enter yes or no) ')
config.set('flairing','report',report)
if report == 'yes':
    reportmessage = raw_input('What do you want that report to say? ') + ' - '
else:
    reportmessage = 'reports disabled'
config.set('flairing','reason',reportmessage)

override = raw_input('Should mods be allowed to override the bot decision? (enter yes or no) ')
config.set('flairing','override',override)
if override == 'yes':
    overrideClassA = raw_input('What should the css class of the flair override A be? \
    (this should be different than the normal one) ')
    overrideClassB = raw_input('what should the css class of the flair override B be? \
    (this should be different than the normal one, too) ')
else:
    overrideClassA = 'not set'
    overrideClassB = 'not set'
config.set('flairing','override class a',overrideClassA)
config.set('flairing','override class b',overrideClassB)

#-- LOGGING --#
config.add_section('logging')
logsub = raw_input('Please enter a logsub. Your bot must be a moderator, and this is required. Do not include r/. ')
config.set('logging','logsub',logsub)

#-- APPROVAL --#
config.add_section('approval')
approval = raw_input('Do you want to require approval for posts to pass a certain number of upvotes? (enter yes or no) ')
config.set('approval','required',approval)

if approval == 'yes':
    threshold = input('Please enter the threshold at which you\'d like unapproved posts to be tomporarily removed: ')
    comment = raw_input('Please enter the comment you\'d like to leave stickied on the post. This will be sent as modmail as well. \
    \nEnter %(author)s for the author of the post and %(link)s for the permalink of the post: \n')
else:
    threshold = 25000
    comment = ''
config.set('approval','threshold',threshold)
config.set('approval','comment',comment)

print ('\n\n That\'s it! You can add special notices at the bottom of your shiny new botconfig.ini file. Happy botting!')
config.add_section('notices')
config.set('notices','timestamp 1',0)
config.set('notices','message 1','none')
config.set('notices','timestamp 2',0)
config.set('notices','message 2','none')


config.write(cfgfile)

cfgfile.close()
exit()
