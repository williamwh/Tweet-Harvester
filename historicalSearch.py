
# import libraries
import sys
import json
import yaml
from searchtweets import load_credentials
from searchtweets import gen_rule_payload
from searchtweets import ResultStream
import couchdb
from multiprocessing import Process


# This method uses Twitter's 30 days search API to collect tweets
def thirtyDaysSearch(searchQuery, API_KEY, API_SECRET):

	# assign configuration variables
    config = dict(
        search_tweets_api = dict(
            account_type = 'premium',
            endpoint = 'https://api.twitter.com/1.1/tweets/search/30day/dev.json',
            consumer_key = API_KEY,
            consumer_secret = API_SECRET
        )
    )

    # put configuration variables to a yaml file
    with open('twitter_keys_30day.yaml', 'w') as config_file:
        yaml.dump(config, config_file, default_flow_style=False)

    # load credential arguments
    premium_search_args = load_credentials("twitter_keys_30day.yaml",
                                       yaml_key="search_tweets_api",
                                       env_overwrite=False)

    maxTweets = 10000000 # Some arbitrary large number

    # connect to couchdb
    couchserver = couchdb.Server("http://admin:admin@172.26.133.32:5984/")
    dbname = "mydb"
    if dbname in couchserver:
        db = couchserver[dbname]
    else:
        db = couchserver.create(dbname)

    tweetCount = 0
    print("Downloading max {0} tweets".format(maxTweets))

    while tweetCount < maxTweets:
    	# specify the search keyword and number of tweet per request
        rule = gen_rule_payload(searchQuery, results_per_call=100)
        # downloading tweets
        new_tweets = ResultStream(rule_payload=rule, max_results=100, **premium_search_args)
        if not new_tweets:
            print("No more tweets found")
            break

        # put tweets into couchdb
        for tweet in new_tweets.stream():
            try: 
                db[str(tweet["id"])] = tweet
                tweetCount += 1
            except Exception:
                pass
        print("Downloaded {0} tweets".format(tweetCount))


# This method uses Twitter's full archieve search API to collect tweets
def fullArchieveSearch(searchQuery, from_date, to_date, API_KEY, API_SECRET):

	# assign configuration variables
    config = dict(
        search_tweets_api = dict(
            account_type = 'premium',
            endpoint = 'https://api.twitter.com/1.1/tweets/search/fullarchive/dev.json',
            consumer_key = API_KEY,
            consumer_secret = API_SECRET
        )
    )

    # put configuration variables to a yaml file
    with open('twitter_keys_fullarchive.yaml', 'w') as config_file:
        yaml.dump(config, config_file, default_flow_style=False)
    
    # load credential arguments
    premium_search_args = load_credentials("twitter_keys_fullarchive.yaml",
                                       yaml_key="search_tweets_api",
                                       env_overwrite=False)
    maxTweets = 10000000 # Some arbitrary large number

    # connect to couchdb
    couchserver = couchdb.Server("http://admin:admin@172.26.133.32:5984/")
    dbname = "mydb"
    if dbname in couchserver:
        db = couchserver[dbname]
    else:
        db = couchserver.create(dbname)

    tweetCount = 0
    print("Downloading max {0} tweets".format(maxTweets))
    time = 0
    while tweetCount < maxTweets:
    	# specify the search keyword and number of tweet per request
        rule = gen_rule_payload(searchQuery, results_per_call=100, from_date=from_date,
                                to_date=to_date)
        # downloading tweets
        new_tweets = ResultStream(rule_payload=rule, max_results=100, **premium_search_args)
        if not new_tweets:
            print("No more tweets found")
            break

        # put tweets into couchdb
        for tweet in new_tweets.stream():
            try: 
                db[str(tweet["id"])] = tweet
                tweetCount += 1
            except Exception:
                pass
        print("Downloaded {0} tweets".format(tweetCount))

if __name__ == '__main__':

    api_keys = ["6UnJWhiQFkMSxkhF7gC9UaWYE", "NwwYHYyBajzbsbdnGEpYOyVVL", 
                "TAxL8cGvXmoVJLrMOBcTNksjO", "Mv472hrlccHc74qK9OVQyxGwA"]

    api_secrets = ["EMzXIgAAIS6IiJWZZey27M5EycB6vDiO3o4cckqcGOlwWKkvUI", 
                   "j7JjLFzebON4G9g8cUE5r4p5NtGnwV8m4efkusiWch9qOs6q92",
                   "gPXB1xbvsUBungBk9DEdhBI1dMwe2PXBbf3xnLHDTu8Mjyjxad",
                   "4VYSdnCzRQEKRV1VPdwKqlGUYNfr8nz7X073NiODWm9jEdIVad"]

    full_p1 = Process(target=fullArchieveSearch, 
    	args=("place:sydney place_country:AU", "202004030000", "202004100000", api_keys[0], api_secrets[0],))
    full_p1.start()
    thirty_p1 = Process(target=thirtyDaysSearch, args=("place:sydney place_country:AU", api_keys[0], api_secrets[0],))
    thirty_p1.start()

    full_p2 = Process(target=fullArchieveSearch, 
    	args=("place:sydney place_country:AU", "202004030000", "202004100000", api_keys[1], api_secrets[1],))
    full_p2.start()
    thirty_p2 = Process(target=thirtyDaysSearch, args=("place:sydney place_country:AU", api_keys[1], api_secrets[1],))
    thirty_p2.start()

    full_p3 = Process(target=fullArchieveSearch, 
    	args=("place:sydney place_country:AU", "202004030000", "202004100000", api_keys[2], api_secrets[2],))
    full_p3.start()
    thirty_p3 = Process(target=thirtyDaysSearch, args=("place:sydney place_country:AU", api_keys[2], api_secrets[2],))
    thirty_p3.start()

    full_p4 = Process(target=fullArchieveSearch, 
    	args=("place:sydney place_country:AU", "202004030000", "202004100000", api_keys[3], api_secrets[3],))
    full_p4.start()
    thirty_p4 = Process(target=thirtyDaysSearch, args=("place:sydney place_country:AU", api_keys[3], api_secrets[3],))
    thirty_p4.start()


