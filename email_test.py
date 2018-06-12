import smtplib

FROM = "assortedjam@gmail.com"
TO = "assortedjam@gmail.com"
PASS = "pythonemailscriptpassword"

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
    server.sendmail(FROM, TO, "Hi, from Task Scheduler")
    print("7")
    server.quit()
    print("Mail Sent Successfully")
except:
    print("Failed to Send Mail")