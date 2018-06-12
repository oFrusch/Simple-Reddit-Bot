
import praw
import pdb
import re
import os
import smtplib
from email.mime.text import MIMEText

FROM = "assortedjam@gmail.com"
TO = "assortedjam@gmail.com"
PASS= "pythonemailscriptpassword"

# Creating Reddit instance
reddit = praw.Reddit('FNBR bot1')

# Having bot enter Fortnite sub
subreddit = reddit.subreddit('FortNiteBR')


'''
# Create text file to store posts that have already been observed
if not os.path.isfile("previous_read_posts"):
    previous_read_posts = []

# Add to list after it is created for the first time
else:
    with open("previous_read_posts", "r") as f:
        previous_read_posts = f.read()
        previous_read_posts = previous_read_posts.split("\n")
        previous_read_posts = list(filter(None, previous_read_posts))
        previous_read_posts = list(previous_read_posts)

'''

# Searchs through top 50 posts in Fortnite subreddit every [time interval - set by task scheduler] and adds their ids and titles to text document
id_title = dict()
for submission in subreddit.hot(limit = 50):
    #if submission.title not in previous_read_posts:
    if re.search(r'\bSkin\b | \bIQ\b | \bPatch\b, \bUpdate\b | \bGuitar\b | \bDowntime\b | \bSolo\b | \bState\b', submission.title, re.IGNORECASE):
            #previous_read_posts.append(submission.title)
        id_title.update({submission.title : submission.url})
        with open("previous_read_posts", "w") as f:
            for post_id in id_title:
                f.write(post_id + ": " + id_title[post_id] + "\n")

# Send Email with latest news from FNBR subreddit
msg = ""
msg_list = []
for title in id_title:
    msg_list.append("\n" + title + ": " + id_title[title] + "\n")
msg = ''.join(msg_list)
str(msg)
print(msg)

try:
    print("1")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    print("2")
    server.set_debuglevel(1)
    print("3")
    server.ehlo()
    print("4")
    server.starttls()
    print("5")
    server.login(FROM, PASS)
    print("6")
    server.sendmail(FROM, TO, msg)
    print("7")
    server.quit()
    print("Mail Sent Successfully")
except:
    print("Failed to Send Mail")

