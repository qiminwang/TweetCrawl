#path to the list of keywords
KEYWORDS_PATH = 'C:/Users/User/Desktop/keywords.txt'

#edit maxTweets depending on how many tweets you wish to crawl
maxTweets=1000000

# If results from a specific ID onwards are reqd, set sinceId to that ID.
# else default to no lower limit, go as far back as API allows
sinceId=None

# If results only below a specific ID are reqd, set maxId to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
maxId=-1

#edit the properties as required
MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "tweetsTest"
MONGODB_COLLECTION = "oldTweet"