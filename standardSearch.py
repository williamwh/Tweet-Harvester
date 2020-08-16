
# import libraries
import sys
import json
import tweepy
import couchdb
import time

def main():
    api_keys = ["6UnJWhiQFkMSxkhF7gC9UaWYE", "NwwYHYyBajzbsbdnGEpYOyVVL", 
                "TAxL8cGvXmoVJLrMOBcTNksjO", "Mv472hrlccHc74qK9OVQyxGwA"]

    api_secrets = ["EMzXIgAAIS6IiJWZZey27M5EycB6vDiO3o4cckqcGOlwWKkvUI", 
                   "j7JjLFzebON4G9g8cUE5r4p5NtGnwV8m4efkusiWch9qOs6q92",
                   "gPXB1xbvsUBungBk9DEdhBI1dMwe2PXBbf3xnLHDTu8Mjyjxad",
                   "4VYSdnCzRQEKRV1VPdwKqlGUYNfr8nz7X073NiODWm9jEdIVad"]

    access_tokens = ["957551496760979456-naiuXXqueKnW7148SK4ZntEZw2Ybads", 
                     "1255451187110912003-gcN5AEBgiAy0JJMvUtZQ9U4d8f4asd",
                     "1254263764704129024-qswKtEfZvfdN5s0t0aHkkm9cOUzjkn", 
                     "1253105446434467841-fdfWCS8r1EgH9kpgkhoByN45GfPklk"]

    access_token_secrets = ["cNW5ssTN8Fr4f5dtsGDYe5amtMx4lXxlyd33TXdNQIkls",
                            "zCUfBqZI59cng6QMVEGOhuuBK7EGUi7gdQ8Px9q3O3kla",
                            "oX6u2CBI6g0t3PRuAJNuhgzkevfVmilaRW5wj1QxTKasl",
                            "M3sR3TJsgPsrVkRpER7mYZmMgo2fcNFCyp1Z21wojqras"]

    auth = tweepy.OAuthHandler(api_keys[int(sys.argv[1])], api_secrets[int(sys.argv[1])])
    auth.set_access_token(access_tokens[int(sys.argv[1])], access_token_secrets[int(sys.argv[1])])
    standardSearch(sys.argv[2], auth)

# This method uses Twitter's standard search API to collect tweets
def standardSearch(searchQuery, auth):
    cities = ["sydney", "melbourne", "adelaide", "canberra", "brisbane", "perth", "darwin", "gold coast", "hobart"]

    # connect to couchdb
    couchserver = couchdb.Server("http://admin:admin@172.26.132.222:5984/")
    dbname = "mydb"
    if dbname in couchserver:
        db = couchserver[dbname]
    else:
        db = couchserver.create(dbname)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    # test authentication
    try:
        api.verify_credentials()
        print("Authentication OK")
    except Exception:
        print("Error during authentication")

    maxTweets = 10000000 # Some arbitrary large number
    tweetsPerQry = 100  # this is the max the API permits

    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = -1

    tweetCount = 0
    print("Downloading max {0} tweets".format(maxTweets))
    timelineCount = 0
    startTime = time.process_time()
    nQueryFollower = 0
    setTime = False
    search_count = 0
    while tweetCount < maxTweets:
        search_count += 1
        try:
            if (max_id <= 0):
                # downloading tweets
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                        geocode="-25.2743988,133.7751312,2000km")
            else:
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                        max_id=str(max_id - 1), 
                                        geocode="-25.2743988,133.7751312,2000km")
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                try: 
                    db[str(tweet._json["id"])] = tweet._json
                except Exception:
                    pass

            search_count = 0
            # if reaching rate limit, do nothing
            if timelineCount >= 100000:
                if (time.process_time() - startTime) > 86400:
                    startTime = time.process_time()
                    timelineCount = 0

            # if rate limit is not reached, retrieve other tweets from that user 
            # and also tweets from his followers
            else: 
                if setTime == True:
                    print(time.process_time() - fifteenMins_startTime)
                    if (time.process_time() - fifteenMins_startTime) > 900:
                        setTime = False
                        nQueryFollower = 0
                # if user follower API limit is reached, do nothing
                if nQueryFollower >= 15:
                    if setTime == False:
                        fifteenMins_startTime = time.process_time()
                        setTime = True
                # otherwise, retrieve tweets from his followers
                else:
                    nQueryUser = 0
                    for tweet in new_tweets:
                        screen_name = tweet._json["user"]["screen_name"]
                        user = api.get_user(screen_name)
                        IDs = [user.id]
                        IDs += api.followers_ids(screen_name = screen_name)
                        nQueryFollower += 1
                        for ID in IDs:
                            try:
                                timeline = api.user_timeline(user_id=ID, count=200)
                            except Exception:
                                continue

                            nQueryUser += 1
                            if nQueryUser >= 1500:
                                break
                            for i in timeline:
                                try:
                                    location = i._json["location"].lower()
                                except Exception:
                                        continue
                                for city in cities:
                                    if city in location:                  
                                        try: 
                                            db[str(i._json["id"])] = i._json
                                            tweetCount += 1
                                        except Exception:
                                            pass
                        if nQueryUser >= 1500:
                            nQueryFollower = 15
                            timelineCount += nQueryUser
                            break
                        if nQueryFollower >= 15:
                            break
                
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

if __name__ == '__main__':
    main()


