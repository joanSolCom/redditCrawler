import json
import os
path="data/reddit_twitter_mapping_clean.tsv"
fd = open(path,"r")
raw = fd.read()
fd.close()
lines = raw.split("\n")[1:]
rawPath = "data/postsAndCommentsPerAuthor/"
userList = []
fd = open("data/clean/reddit_content.tsv","w")
fd.write("username\ttext\n")


for line in lines:
    username = line.split("\t")[0]
    userList.append(username)

for user in userList:
    commentPath = rawPath + user +"_comments.json"
    postPath = rawPath + user + "_posts.json"
    if os.path.isfile(commentPath):
        with open(commentPath, 'r', encoding='utf-8') as f:
            comments = json.load(f)
            for comment in comments:
                text = comment["body"]
                text = " ".join(text.split())
                fd.write(user+"\t"+text+"\n")
    
    if os.path.isfile(postPath):
        with open(postPath, 'r', encoding='utf-8') as f:
            posts = json.load(f)
            for post in posts:
                text = post["selftext"]
                text = " ".join(text.split())
                fd.write(user+"\t"+text+"\n")

fd.close()