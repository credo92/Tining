%matplotlib inline

from collections import Counter
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import json
#Establishing Connection
import twitter
CONSUMER_KEY = 'XXXXXX'
CONSUMER_SECRET = 'XXXXX'
OAUTH_TOKEN = 'XXXXXX'
OAUTH_TOKEN_SECRET = 'XXXXXXXXXXX'
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)
print(twitter_api)

#trending topics using World Id,woeid available on yahoo
WORLD_WOE_ID = 1
CA_WOE_ID = 23424775

#getting world trends

world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
ca_trends = twitter_api.trends.place(_id=CA_WOE_ID)w

#output
# basic analysis
# using python sets to find common trending between world and india

world_trends_set = set([trend['name']
                      for trend in world_trends[0]['trends']
                       ])
ca_trends_sett = set([trend['name']
                   for trend in ca_trends[0]['trends']
                    ])
common_trends = world_trends_set.intersection(ca_trends_set)
print common_trends

print json.dumps(world_trends, indent=1)
print
print json.dumps(ca_trends, indent=1)

## Searching statuses

q = '#Jio'
count = 100

search_results = twitter_api.search.tweets(q=q,count=count)
statuses = search_results['statuses']

for _ in range(5):
    print "Length of statuses", len(statuses)
    try:
        next_results = search_results['search_metadata']['next_results']
    except KeyError, e: # nothin when next result null
        break
    #dictionary
    kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&")])
    search_results = twitter_api.search.tweets(**kwargs)
    statuses += search_results['statuses']


    #extracting text, screen names, and hastags
    status_texts = [ status['text']
                 for status in statuses]
    screen_names = [user_mention['screen_name']
                for status in statuses
                    for user_mention in status['entities']['user_mentions']]

    hashtags = [ hashtag['text']
            for status in statuses
                for hashtag in status['entities']['hashtags']]

    # collection of words
    words = [ w
          for t in status_texts
              for w in t.split()]

#frequency distribution from the words in tweets
for item in [words,screen_names,hashtags]:
    c=Counter(item)
    print c.most_common()[:10] #top 10
    print

retweets  = [
            (status['retweet_count'],
             status['retweeted_status']['user']['screen_name'],
             status['text'])

            for status in statuses
                if status.has_key('retweeted_status')

            ]
#pretty table to display tuples in a nice tabular format
#Data Visualization Frequency Data with Histograms
for label, data in(
                    ('Word', words),
                    ('Screen Name', screen_names),
                    ('Hashtag', hashtags)):
    counts = [count for count, _, _ in retweets]
    plt.hist(counts)
    plt.title("Retweets")
    plt.xlabel('Bins (number of times retweed)')
    plt.ylabel('Number of tweets in bin')

    print counts


    pt = PrettyTable(field_names=[label, 'Count'])
    c  = Counter(data)
    plt.hist(c.values())

    plt.title(label)
    plt.ylabel("Number of items in bin")
    plt.xlabel("Bins (number of times an item appeared)")
    plt.figure()

    [pt.add_row(kv) for kv in c.most_common()[:10]]
    pt.align[label], pt.align['Count'] = 'l', 'r' # column alignment
    print pt

    pt = PrettyTable(field_names=['Count','Screen Name', 'Text'])
    [ pt.add_row(row) for row in sorted(retweets, reverse=True)[:5]]
    pt.max_width['Text'] = 50
    pt.align= 'l'
    print pt



# lexical diversity measure for tweets

def lexical_diversity(tokens):
    return 1.0*len(set(tokens))/len(tokens)

def average_words(statuses):
    total_words = sum([len(s.split()) for s in statuses])
    return 1.0*total_words/len(statuses)

#users who have retweeted a status using statuses/retweets/:id API.
_retweets  = twitter_api.statuses.retweets(id=317127304981667841)
print [r['user']['screen_name'] for r in _retweets]








#printing lexical diversity Quantitative Measure

print lexical_diversity(words)
print lexical_diversity(screen_names)
print lexical_diversity(hashtags)
print average_words(status_texts)



#print sample search by slicing the list
print json.dumps(statuses[0], indent=1)

#print first items
print json.dumps(status_texts[0:5], indent=1)
print json.dumps(screen_names[0:5], indent =1)
print json.dumps(hashtags[0:5], indent =1)
print json.dumps(words[0:5], indent =1)
