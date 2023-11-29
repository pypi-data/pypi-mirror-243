import time
import requests

link = "https://docs.google.com/forms/d/e/1FAIpQLSeilmK7No6KI1pmKf8V4Q71MPWTm6FbtIpEDDBturBbdTkauQ/formResponse?usp=pp_url&entry.450933019=XUNWEN&entry.1661957685=TIME&entry.402674929=CHANGE"


def record(code,change):
    newlink=link.replace("XUNWEN", code)
    newlink=newlink.replace("TIME", time.ctime(time.time()))
    newlink=newlink.replace("CHANGE", change)
    print(requests.post(newlink))
