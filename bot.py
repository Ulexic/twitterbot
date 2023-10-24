import csv
import json
import random
import os

from requests_oauthlib import OAuth1Session

import config

token_url = "https://api.twitter.com/2/oauth2/token"

# Get the bearer token
def get_access_token():
   request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
   oauth = OAuth1Session(config.api_key, client_secret=config.api_key_secret)

   try:
      fetch_response = oauth.fetch_request_token(request_token_url)
   except ValueError:
      print(
         "There may have been an issue with the config.api_key or config.api_key_secret you entered."
      )

   resource_owner_key = fetch_response.get("oauth_token")
   resource_owner_secret = fetch_response.get("oauth_token_secret")
   print("Got OAuth token: %s" % resource_owner_key)

   base_authorization_url = "https://api.twitter.com/oauth/authorize"
   authorization_url = oauth.authorization_url(base_authorization_url)
   print("Please go here and authorize: %s" % authorization_url)
   verifier = input("Paste the PIN here: ")

   # Get the access token
   access_token_url = "https://api.twitter.com/oauth/access_token"
   oauth = OAuth1Session(
      config.api_key,
      client_secret=config.api_key_secret,
      resource_owner_key=resource_owner_key,
      resource_owner_secret=resource_owner_secret,
      verifier=verifier,
   )
   oauth_tokens = oauth.fetch_access_token(access_token_url)

   with open('config.py', "w") as file:
      file.write("api_key = " + "\"" + config.api_key + "\"\n")
      file.write("api_key_secret = " + "\"" + config.api_key_secret + "\"\n")
      file.write("access_token = " + "\"" + oauth_tokens["oauth_token"] + "\"\n")
      file.write("access_token_secret = " + "\"" + oauth_tokens["oauth_token_secret"] + "\"\n")

   return (oauth_tokens["oauth_token"], oauth_tokens["oauth_token_secret"])

# Send a tweet with a random lyric
def send_tweet(lyric):
   if config.access_token == "" or config.access_token_secret == "":
      get_access_token()

   oauth = OAuth1Session(
      config.api_key,
      client_secret=config.api_key_secret,
      resource_owner_key=config.access_token,
      resource_owner_secret=config.access_token_secret,
   )

   response = oauth.post(
      "https://api.twitter.com/2/tweets",
      json={"text": lyric},
   )

   if response.status_code != 201:
      raise Exception(
         "Request returned an error: {} {}".format(response.status_code, response.text)
      )

   print("Response code: {}".format(response.status_code))

# Get a random lyric index
def get_random_index(limit):
   i = random.randrange(limit)

   with open('stats.json', "r") as file:
      stats = json.load(file)

   latest = list(stats['latest'])
   print(latest)

   while i in latest or stats['lyricOccurence'][i] > 10 + stats['averageOccurence']:
      i = random.randrange(limit)

   latest.append(i)
   latest.pop(0)
   stats['latest'] = latest
   stats['lyricOccurence'][i] += 1
   stats['totalOccurence'] += 1
   stats['averageOccurence'] = stats['totalOccurence'] / len(stats['lyricOccurence'])
   if stats['lyricOccurence'][i] > stats['max']:
      stats['max'] = stats['lyricOccurence'][i]

   with open('stats.json', "w") as file:
      json.dump(stats, file, indent=3, separators=(',', ': '))
      
   return i
      
# Get a random lyric and format it
def get_random_lyric():
   with open('lyrics.csv', 'r') as file:
      reader = csv.reader(file, delimiter=';')
      lyrics = list(reader)
   i = get_random_index(len(lyrics))

   lyric = ""
   for line in lyrics[i]:
      lyric += line + "\n"

   return lyric

def main():
   lyric = get_random_lyric()
   
   print(lyric)
   send_tweet(lyric)
   
if __name__ == "__main__":
   main()