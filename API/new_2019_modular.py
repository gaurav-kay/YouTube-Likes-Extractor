# todo: okay so nextPageToken isn't returning all the videos.

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import os
import json

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def get_authorised_youtube():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "LOCATION OF CLIENT_SECRET_FILE.JSON"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                client_secrets_file,
                scopes
            )
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name,
        api_version,
        credentials=credentials
    )

    return youtube


def make_single_request(youtube, nextPageToken):
    if nextPageToken is None:
        request = youtube.videos().list(
            part="snippet",
            myRating="like",
            maxResults=50
        )
    else:
        request = youtube.videos().list(
            part="snippet",
            myRating="like",
            pageToken=nextPageToken,
            maxResults=50
        )
    response = request.execute()

    return response


def main():
    youtube = get_authorised_youtube()

    first_response = make_single_request(youtube, None)
    nextPageToken = first_response["nextPageToken"]

    try:
        count = 0
        while True:
            count += 1
            print(count, end=" ")
            response = make_single_request(youtube, nextPageToken)
            nextPageToken = response["nextPageToken"]
            print(nextPageToken)
    except KeyError as e:
        response.pop("items")
        print(response)


if __name__ == '__main__':
    main()
