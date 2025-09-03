# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id="UCPsR-AeGMiL3ZPt1KYTbcig"
        # mine=True
    )
    
    response = request.execute()
    channel = response["items"][0]
    snippet = channel["snippet"]
    statistics = channel["statistics"]
        
    print("Title: " + snippet["title"])
    print("Description: " + snippet["description"])
    print("customUrl: " + snippet["customUrl"])
    print("thumbnails: " + str(snippet["thumbnails"]["default"]["url"]))
    print("viewCount: " + statistics["viewCount"])
    print("subscriberCount: " + statistics["subscriberCount"])
    print("videoCount: " + statistics["videoCount"])

if __name__ == "__main__":
    main()