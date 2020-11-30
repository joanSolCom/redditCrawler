fd = open("reddit_twitter_mapping.tsv","r")
raw = fd.read()
fd.close()

lines = raw.split("\n")
alreadyHave = []
cleanLines = []
for line in lines:
    userTuple = line.split("\t")
    if userTuple not in alreadyHave:
        cleanLines.append(line)
        alreadyHave.append(userTuple)
    else:
        print("repeated",userTuple)

rawClean = "\n".join(cleanLines)
fd = open("reddit_twitter_mapping_clean.tsv","w")
fd.write(rawClean)
fd.close()