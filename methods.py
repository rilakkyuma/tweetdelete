import csv
import tweepy
import codecs

tweets = []
# keep track of all the VALID tweet ids, aka those that the user owns and not anyone else's

all_tweet_ids = []
# maps of ids and tweets both ways
tweet_id_map = {}
id_tweet_map = {}

# authentication and api objects
auth = None
api = None

# a list of all marked tweets
marked_tweets = []

consumer_key = ''
consumer_secret = ''
access_key = ''
access_secret = ''
archive_path = ''

# authenticated boolean set to False by default
authenticated = False


# read in the csv file into a multidimensional list using the global archive_path string
def read_csv():
    global tweets
    # reads a CSV file into a list of lists
    with codecs.open(archive_path, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        tweets = []
        for line in reader:
            row_data = []
            for element in line:
                row_data.append(element)
            if row_data != []:
                tweets.append(row_data)
    tweets.pop(0)
    print('csv successfully read')
    fill_in_tweet_ids()
    fill_in_maps()


# methods to be automatically called by readcsb()
def fill_in_maps():
    global tweet_id_map
    for tweet in tweets:
        tweet_id_map[tweet[5]] = int(tweet[0])
        tweet_id_map[tweet[0]] = tweet[5]
    print('filled in tweet->id and id->tweet map')


# searches through every tweet that includes a certain hashtag and marks it for deletion
def list_by_hashtag(hashtag):
    # modify hashtag string to include the '#'
    hashtag = '#' + hashtag
    for tweet in tweets:
        if hashtag in tweet[5]:
            print(tweet[0] + ' ' + tweet[3][0:10] + ' ' + tweet[5])


# lists every tweet in the account that was a Retweet of someone else's tweet
def list_retweets(userid=''):
    for tweet in tweets:
        if userid == '':
            if tweet[5][0:3] == 'RT ':
                print(tweet[0] + ' ' + tweet[3][0:10] + ' ' + tweet[5])
        else:
            rtstring = 'RT @' + userid
            if rtstring in tweet[5][0:]:
                print(tweet[0] + ' ' + tweet[3][0:10] + ' ' + tweet[5])


# lists every tweet in the account if it contains a certain keyword
def list_by_keyword(keyword):
    for tweet in tweets:
        if keyword in tweet[5]:
            print(tweet[0] + ' ' + tweet[3][0:10] + ' ' + tweet[5])


# searches through every tweet in the account that was a reply to another user
def list_replies(userid=''):
    global marked_tweets
    for tweet in tweets:
        if userid == '':
            if tweet[5][0] == '@':
                print(tweet[0] + ' ' + tweet[3][0:10] + ' ' + tweet[5])
        else:
            mention = '@' + userid
            if mention in tweet[5] and 'RT ' not in tweet[5][0:3]:
                print(tweet[0] + ' ' + tweet[3][0:10] + ' ' + tweet[5])

# lists every tweet that is in the year-months specified
def list_by_yr_month(month_list):
    for tweet in tweets:
        if tweet[3][0:7] in month_list:
            print(tweet[0] + ' ' + tweet[3][0:10] + ' ' + tweet[5])


# lists all tweets in the archive in "tweetid tweetdate tweetcontents" format
def list_all():
    if not tweets:
        print('list of tweets is empty. try reading in another csv file')
    else:
        for tweet in tweets:
            print(tweet[0] + ' ' + tweet[3][0:19] + ' ' + tweet[5])


# searches through every tweet that includes a certain keyword and marks it
def mark_by_keyword(keyword):
    global marked_tweets
    # check every tweet in the archive and if it includes the specified hashtag, add it to the list
    # of tweets to delete
    count = 0
    for tweet in tweets:
        if keyword in tweet[5]:
            marked_tweets.append(tweet[0])
            count += 1
    print('marked ' + str(count) + ' tweets')


# marks every tweet in the account that was a Retweet of someone else's tweet
def mark_retweets(userid=''):
    global marked_tweets
    count = 0
    for tweet in tweets:
        if userid == '':
            if tweet[5][0:3] == 'RT ':
                marked_tweets.append(tweet[0])
                count += 1
        else:
            rtstring = 'RT @' + userid
            if rtstring in tweet[5][0:]:
                marked_tweets.append(tweet[0])
                count += 1
    print('marked ' + str(count) + ' tweets')


# searches through every tweet that includes a certain hashtag and marks it for deletion
def mark_by_hashtag(hashtag):
    # modify hashtag string to include the '#'
    hashtag = '#' + hashtag
    global marked_tweets
    count = 0
    # check every tweet in the archive and if it includes the specified hashtag, add it to the list
    # of tweets to delete
    for tweet in tweets:
        if hashtag in tweet[5]:
            marked_tweets.append(tweet[0])
            count += 1
    print('marked ' + str(count) + ' tweets')


# marks replies. if no argument is passed, then all replies are marked. otherwise,
# specify a user to mark replies froma
def mark_replies(userid=''):
    global marked_tweets
    count = 0
    for tweet in tweets:
        if userid == '':
            if tweet[5][0] == '@':
                marked_tweets.append(tweet[5])
                count += 1
        else:
            mention = '@' + userid
            if mention in tweet[5] and 'RT ' not in tweet[5][0:3]:
                marked_tweets.append(tweet[0])
                count += 1
    print('marked ' + str(count) + ' tweets')


# searches through every tweet in the account according to its year and month of publication and adds it to the list
# of tweets to delete
def mark_by_yr_month(month_list):
    global marked_tweets
    count = 0
    for tweet in tweets:
        if tweet[3][0:7] in month_list:
            marked_tweets.append(tweet[0])
            count += 1
    print('marked ' + str(count) + ' tweets')


# marks a specific tweet for deletion based on its inputted tweet id
def mark_tweet_by_id(id):
    global marked_tweets
    global all_tweet_ids
    if id in all_tweet_ids:
        marked_tweets.append(id)
        print('marked tweet ' + str(id))
    else:
        print('tweet id ' + str(id) + ' not valid. make sure you are the owner of the tweet/retweet')


# deletes every single marked tweet. however this requires authentication first
def delete_markeds():
    # use the global marked_tweets list
    global marked_tweets
    if len(marked_tweets) == 0:
        print('there is nothing marked for deletion')
    else:
        # if user is not authenticated before deleting tweets, authenticate them
        if not authenticated:
            authenticate()
        to_delete_ids = []
        delete_count = 0
        # checks if a delete failed. it can be any one, not just all of them
        delete_failed = False
        for tweet in marked_tweets:
            to_delete_ids.append(tweet)

        # delete marked tweets by status ID
        for status_id in to_delete_ids:
            try:
                api.destroy_status(status_id)
                print(status_id, 'deleted!')
                delete_count += 1
            except:
                delete_failed = True
                print(status_id, 'could not be deleted')
        print(delete_count, 'tweets deleted')
        # clear the list of marked tweets
        marked_tweets.clear()
        print('list of marked tweets cleared')
        if delete_failed:
            print('failed to delete one or more tweets. make sure your tweet archive is up-to-date')


# utility method
def list_tweet_ids():
    for i in all_tweet_ids:
        print(i)


# lists all tweets that are marked in the format 'tweetid tweetcontents'
def list_marked_tweets():
    for i in marked_tweets:
        print(i + ' ' + str(tweet_id_map[i]))


# clears the list of marked tweets without deleting them
def clear_marked_tweets():
    global marked_tweets
    marked_tweets.clear()


# unmarks a certain tweet based on inputted tweet id
def clear_tweet(tweetid):
    try:
        marked_tweets.remove(tweetid)
        print('unmarked tweet #' + str(tweetid))
    except:
        print('invalid format or id')


# to be called automatically by readcsv()
def fill_in_tweet_ids():
    global all_tweet_ids
    endindex = len(tweets)
    for i in range(0, endindex):
        all_tweet_ids.append(tweets[i][0])
    print('filled in tweet ids')


# sets the absolute path of the tweet archive
def set_archive_path(path):
    if path != '':
        global archive_path
        archive_path = str(path)
    else:
        print('you must specify a path')


# prints to the console the currently saved archive path, which may not be valid
def output_archive_path():
    if archive_path != '':
        print(archive_path)
    else:
        print('archive path not specified')


# sets consumer_key
def set_consumer_key(input):
    global consumer_key
    consumer_key = input
    print('changed consumer_key to ' + str(input))


## sets consumer_secret
def set_consumer_secret(input):
    global consumer_secret
    consumer_secret = input
    print('changed consumer_secret to ' + str(input))


# sets access_key
def set_access_key(input):
    global access_key
    access_key = input
    print('changed access_key to ' + str(input))


# sets access_secret
def set_access_secret(input):
    global access_secret
    access_secret = input
    print('changed access_secret to ' + str(input))


# outputs to the console the four keys used in authentication
def list_keys():
    print('consumer_key = ' + str(consumer_key))
    print('consumer_secret = ' + str(consumer_secret))
    print('access_key = ' + str(access_key))
    print('access_secret = ' + str(access_secret))


# authenticates the user using the four currently saved keys
def authenticate():
    global authenticated
    if not authenticated:
        print('authenticating')
        global auth, api
        try:
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_key, access_secret)
            api = tweepy.API(auth)
            # verify that the credentials are correct. will throw an error if not which will be caught
            api.verify_credentials()
            # modify the global authenticated variable as such
            authenticated = True
            print("authenticated as @%s" % api.me().screen_name)
        except:
            print('one or more of the keys appears to be invalid or there is no connection. authentication failed')
    else:
        print('already authenticated')

# utility method for now...might expand on later
def showinfo():
    try:
        print(api.rate_limit_status())
    except:
        print('ruh-roh')