FROM python:3

# copy all the files to the container
ADD standardSearch.py /
#ADD streamSearch.py /

# install dependencies
RUN pip3 install tweepy
RUN pip3 install couchdb
#RUN pip3 install searchtweets

ENTRYPOINT ["python", "./standardSearch.py"]
#ENTRYPOINT ["python", "./streamSearch.py"]

# run the command
#CMD ["python", "./standardSearch.py"]