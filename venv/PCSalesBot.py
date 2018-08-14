import praw
import smtplib
import time
import re

FROM = "ifindpcsalesbot@gmail.com"
TO = "owenc343@gmail.com"
PASS = "findpcsales"

# Creating Reddit instance
reddit = praw.Reddit('FNBR bot1')

# Having bot enter Fortnite sub
# subreddit = reddit.subreddit('FortNiteBR')

# Different way to access multiple subreddits
multi_subs = reddit.subreddit('buildapcsales')


previous_read_posts = []
# Searchs through top posts related to specified keywords and finds deals in the buildapcsales subreddit
while True:
    id_title = dict()
    for submission in multi_subs.hot(limit=20):
        if submission.title not in previous_read_posts:
            if re.search(r'\bMONITOR\b | \bSSD\b', submission.title, re.IGNORECASE):
                previous_read_posts.append(submission.title)
                id_title.update({submission.title : submission.url})

# Send Email with latest deals from buildapcsales
    msg = ""
    msg_list = []
    for title in id_title:
        msg_list.append("\n" + title + ": " + id_title[title] + "\n")
    msg = ''.join(msg_list)
    str(msg)
    print(msg)

    email_interval = 7220
    amt_hrs = int(email_interval / 3600)

    if msg == "":
        msg = "No new deals found, I'll get back to you in " + str(amt_hrs) + (" hours." if (amt_hrs > 1) else " hour.") + "\n - Reddit Bot"

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

    id_title.clear()  # Emptying dictionary so the list doesn't just continuously grow alongside 'previous_read_posts'

    year, month, day, hour, minute = time.strftime("%Y,%m,%d,%H,%M").split(',')
    int_hour = int(hour) # Non-military hours
    if int_hour > 12:
        int_hour = int_hour - 12
        hour = str(int_hour)
    print(month + "/" + day + "/" + year + " " + hour + ":" + minute)

    time.sleep(email_interval)
