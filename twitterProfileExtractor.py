import os
import json
import re

path = "data/"
URL_REGEX = r"""((?:(?:https|ftp|http)?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|org|uk)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|uk|ac)\b/?(?!@)))"""
toInvestigate = []

print("Reddit Username\tTwitter Username")
for fname in os.listdir(path):
    fpath = path + fname
    with open(fpath) as json_file:
        data = json.load(json_file)
        text = data["data"]["selftext"]
        usernameReddit = data["data"]["author"]
        links = re.findall(URL_REGEX, text)
        found = False
        for link in links:
            if "twitter.com/" in link:
                twitterUsername = link.split("twitter.com/")[1].split("/")[0].replace("\\","").split("?")[0]
                #print(usernameReddit+"\t"+twitterUsername)
                found = True
                break
        
        if not found:
            toInvestigate.append(fpath)

for fname in toInvestigate:
    with open(fname) as json_file:
        data = json.load(json_file)
        text = data["data"]["selftext"]
        title = data["data"]["title"]
        print("------------------------------------------")
        print(title)
        print(text)
        usernameReddit = data["data"]["author"]
    