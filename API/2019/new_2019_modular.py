# todo: ~okay so nextPageToken isn't returning all the videos.~
# todo: verify that more than 5000 videos are recorded
# requires a paid GCP account to work properly (CLIENT_SECRET)

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import os
import json
from time import sleep

scopes = ["https://www.googleapis.com/auth/youtube"]
parts = "snippet"
items = []
total = 0


def get_authorised_youtube():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "CLIENT_SECRET_FILE.JSON"

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
            part=parts,
            myRating="like",
            maxResults=50
        )
    else:
        request = youtube.videos().list(
            part=parts,
            myRating="like",
            pageToken=nextPageToken,
            maxResults=50
        )
    response = request.execute()

    return response


def write(response):
    for item in response["items"]:
        with open('test1.json', 'a', encoding='utf-8') as fp:
            print(json.dumps(item, sort_keys=True, indent=4, ensure_ascii=False), file=fp)  # god. prints utf-8 prettified json
    global total
    total += len(response["items"])
    print(total)


def main():
    youtube = get_authorised_youtube()

    first_response = make_single_request(youtube, None)
    nextPageToken = first_response["nextPageToken"]

    write(first_response)

    try:
        count = 0
        while True:
            count += 1
            print(count, end=" ")
            response = make_single_request(youtube, nextPageToken)
            write(response)
            nextPageToken = response["nextPageToken"]
            print(nextPageToken)

            # items.append(item for item in response["items"])
            # with open("final.txt", 'a') as f:
            #     lines = '\n'.join(items)
            #     f.write(lines)

            sleep(1)

    except KeyError:
        write(response)
        response.pop("items", None)

        print(response)


if __name__ == '__main__':
    main()

