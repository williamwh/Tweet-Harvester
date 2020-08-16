# import libraries
import sys
import json
import couchdb
from multiprocessing import Process

# this method read tweets from a file and put into the database automatically
def main(n):

    with open(sys.argv[1]) as file:

        # remove the first line of file
        file.readline()

        couchserver = couchdb.Server("http://admin:admin@172.26.133.32:5984/")
        dbname = "mydb"
        if dbname in couchserver:
            db = couchserver[dbname]
        else:
            db = couchserver.create(dbname)

        # keep iterating to read 1000 lines of file each time and process it
        content = "{\"rows\":["
        count = 0
        nline = 0
        nTweets = 0
        for line in file:
            nline += 1
            if nline % 2 == n:
                if count < 1000:
                    content += line
                    nTweets += 1
                    count += 1
                else: 
                    print(nline)
                    if content[-2] == ",":
                        content = content[:-2] + "]}"
                    if content == "{\"rows\":[":
                        content += "]}"
                    data = json.loads(content)
                    for tweet in data["rows"]:
                        del tweet["doc"]["_rev"]
                        try:
                            db[str(tweet["doc"]["id"])] = tweet["doc"]
                        except Exception:
                            pass
                    content = "{\"rows\":["
                    count = 0
        print("done", nTweets)

if __name__ == '__main__':
    p1 = Process(target=main, args=(1,))
    p1.start()
    p2 = Process(target=main, args=(0,))
    p2.start()
    # main()