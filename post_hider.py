# MIT License
#
# Copyright 2018 umbresp
#
# Permission is hereby granted, free of charge, to any 
# person obtaining a copy of this software and 
# associated documentation files (the "Software"), to 
# deal in the Software without restriction, including 
# without limitation the rights to use, copy, modify, 
# merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom
# the Software is furnished to do so, subject to the 
# following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all copies or substantial portions
# of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF 
# ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT 
# SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR 
# ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN 
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

# post_hider.py
# Purpose: Hides all posts currently posted in a subreddit.
# Notes: This is useful if you want to run something else
# but don't want all legacy submissions to be considered.
# Just hide them!

# REMEMBER TO FILL OUT subreddit!

import praw
import datetime
import configparser as ConfigParser

subreddit = "Badfaketexts"  # CASE SENSITIVE, don't include the /r/

config = ConfigParser.ConfigParser()
config.read('botconfig.ini')
username = config.get('basics', 'account name')
config.read('praw.ini')
password = config.get(username, 'password')
client_id = config.get(username, 'client_id')
client_secret = config.get(username, 'client_secret')
user_agent = f'{username} running post_hider.py'

r = praw.Reddit(client_id=client_id, client_secret=client_secret, password=password, user_agent=user_agent, username=username)
print(r)
for i in r.user.moderator_subreddits(limit=None): # TODO: Add compatability for non-mod subs
    if i.display_name == subreddit:
        print(i.display_name)
        for p in i.new():
            print(p)
            p.hide()