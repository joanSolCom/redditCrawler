import requests
import sys
from pprint import pprint
import json
import os

class RedditCrawler:

    def __init__(self, url, mode):
        self.url = url
        self.headers = {
            'User-Agent': 'python3:reddit crawler v1.0 (by u/capitanmartu)',
            'From': 'joanSolCom@github.com'
        }
        if mode == "all":
            self.getPostsAndComments()
        elif mode == "posts":
            self.getPosts()
        elif mode == "users":
            self.getUserPosts()


    def getPosts(self):
        urlAPI = self.url + "new.json?limit=100"
        response = requests.get(urlAPI, headers=self.headers)
        json_data = json.loads(response.text)

        while json_data["data"]["after"]:
            self.extractData(json_data)
            after = json_data["data"]["after"]
            nextURL = urlAPI + "&after=" + after
            print("Getting content after",after)
            json_data = requests.get(nextURL, headers=self.headers).json()

    def extractData(self, json_data):
        listPosts = json_data["data"]["children"]
        for post in listPosts:
            subreddit = post["data"]["subreddit"]
            idx = post["data"]["id"]
            name = "data/"+subreddit+"_"+idx+".json"
            if os.path.exists(name):
                print("already have", name)
            else:
                print("writing",name)
                with open(name, 'w', encoding='utf-8') as f:
                    json.dump(post, f, ensure_ascii=False, indent=4)


    def getPostsAndComments(self):
        #https://www.reddit.com/r/IAmA/comments/[POSTID].json
        #get all posts from subreddit and for each post, go get its comments
        raise Exception("TBD. Not implemented yet")

    def getUserPosts(self, path="data/reddit_twitter_mapping_clean.tsv"):
        fd = open(path,"r")
        raw = fd.read()
        fd.close()
        prefix = "http://reddit.com/user/"
        suffixComments = "/comments.json?limit=100"
        suffixPosts = "/submitted.json?limit=100"
        lines = raw.split("\n")[1:]
        outPath = "data/postsAndCommentsPerAuthor/"

        for line in lines:
            username = line.split("\t")[0]
            urlComments = prefix + username + suffixComments
            print("Getting comments from", username)
            response = requests.get(urlComments, headers=self.headers)
            json_data = json.loads(response.text)
            comments = []
            if "data" in json_data.keys():
                for comment in json_data["data"]["children"]:
                    comments.append(comment["data"])

                while json_data["data"]["after"]:
                    for comment in json_data["data"]["children"]:
                        comments.append(comment["data"])

                    after = json_data["data"]["after"]
                    nextURL = urlComments + "&after=" + after
                    print("Getting content after",after)
                    json_data = requests.get(nextURL, headers=self.headers).json()

                fname = outPath + username + "_comments.json"
                print("writing",fname)
                with open(fname, 'w', encoding='utf-8') as f:
                    json.dump(comments, f, ensure_ascii=False, indent=4)        
            

            print("Getting posts from",username)
            urlPosts = prefix + username + suffixPosts
            response = requests.get(urlPosts, headers=self.headers)
            json_data = json.loads(response.text)
            posts = []

            if "data" in json_data:
                for post in json_data["data"]["children"]:
                    posts.append(post["data"])

                while json_data["data"]["after"]:
                    for post in json_data["data"]["children"]:
                        posts.append(post["data"])

                    after = json_data["data"]["after"]
                    nextURL = urlPosts + "&after=" + after
                    print("Getting content after",after)
                    json_data = requests.get(nextURL, headers=self.headers).json()
                
                fname = outPath + username + "_posts.json"
                print("writing",fname)
                with open(fname, 'w', encoding='utf-8') as f:
                    json.dump(posts, f, ensure_ascii=False, indent=4) 
            
            else:
                print("WEIRD SHIT")
                print(json_data)
            
            print(username,"has",len(comments),"comments and",len(posts),"posts")





if __name__ == "__main__":
    
    arguments = sys.argv
    
    if len(arguments) < 3:
        mode = sys.argv[1]
        if mode == "users":
            iR = RedditCrawler(None, mode)
        else:
            print("please input the subreddit name you want to crawl and if you want only posts (posts) or posts and comments (all)")

    else:
        subreddit = sys.argv[1]
        url = "http://reddit.com/r/"+subreddit+"/"
        mode = sys.argv[2]
        if mode not in ["all", "posts"]:
            raise Exception("Please input all or posts as mode")
        else:
            iR = RedditCrawler(url, mode)
