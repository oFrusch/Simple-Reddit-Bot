import praw
import smtplib
import time

FROM = "fnbr.reddit.bot1@gmail.com"
TO = "owenc343@gmail.com"
PASS = "fortniteredditbot"

# Creating Reddit instance
reddit = praw.Reddit('FNBR bot1')

# Having bot enter Fortnite sub
# subreddit = reddit.subreddit('FortNiteBR')

# Different way to access multiple subreddits
multi_subs = reddit.subreddit('FortNiteBR+darksouls+Fitness+books')


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

previous_read_posts = []
# Searchs through top 50 posts in Fortnite subreddit every hour and adds their ids and titles to text document
# Would prefer to have this scheduled by Task Scheduler. However, does not run properly when scheduled by the Task Scheduler. Although my simple email script runs fine with Task Scheduler. Is it an issue with PRAW?
while True:
    id_title = dict()
    for submission in multi_subs.hot(limit=5):
        if submission.title not in previous_read_posts:
            previous_read_posts.append(submission.title)
            id_title.update({submission.title: submission.url})
            # if re.search(r'\bSkin\b | \bPatch\b | \bUpdate\b | \bGuitar\b | \bDowntime\b | \bSolo\b | \bState\b', submission.title, re.IGNORECASE):
            #     previous_read_posts.append(submission.title)
            #     id_title.update({submission.title : submission.url})

# Send Email with latest news from FNBR subreddit or multireddit
    msg = ""
    msg_list = []
    for title in id_title:
        msg_list.append("\n" + title + ": " + id_title[title] + "\n")
    msg = ''.join(msg_list)
    str(msg)
    print(msg)

    email_interval = 14440
    amt_hrs = int(email_interval / 3600)

    if msg == "":
        msg = "No news to report, I'll get back to you in " + str(amt_hrs) + (" hours." if (amt_hrs > 1) else " hour.") + "\n - Reddit Bot"

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

    id_title.clear()  #Emptying dictionary so the list doesn't just continuously grow alongside 'previous_read_posts'

    year, month, day, hour, minute = time.strftime("%Y,%m,%d,%H,%M").split(',')
    int_hour = int(hour) #Non-military hours
    if int_hour > 12:
        int_hour = int_hour - 12
        hour = str(int_hour)
    print(month + "/" + day + "/" + year + " " + hour + ":" + minute)

    time.sleep(email_interval)
