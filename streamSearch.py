
# import libraries
import sys
import json
import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
import couchdb

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

    # connect to Twitter using Streaming API
    l = StdOutListener()
    stream = Stream(auth, l)
    stream.filter(locations=[112.467, -55.050, 168.000, -9.133])

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    # connect to couchdb
    couchserver = couchdb.Server("http://admin:admin@172.26.132.222:5984/")
    dbname = "mydb"
    if dbname in couchserver:
        db = couchserver[dbname]
    else:
        db = couchserver.create(dbname)

    tweetCount = 0

    def on_data(self, data):
        tweet = json.loads(data)
        self.tweetCount += 1
        try: 
            self.db[str(tweet["id"])] = tweet
        except Exception:
            pass
        print ("stream downloaded {0} tweets".format(self.tweetCount))
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    main()


