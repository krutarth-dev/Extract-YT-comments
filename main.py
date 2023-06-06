import csv
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up YouTube Data API
api_key = 'AIzaSyAM4ft4C0C4Cn-AIovgkOE_PoSUw2ZWHkI'
youtube = build('youtube', 'v3', developerKey=api_key)

# Video IDs of the channels in scope
video_ids = [
    'p7V4Aa7qEpw',
    # Add more video IDs as needed
]

# Get comments from YouTube videos
def get_video_comments(service, video_id):
    comments = []
    try:
        request = service.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=10
        )
        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textOriginal']
            comments.append(comment)

        return comments

    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")

# Call YouTube Data API to get comments from each video
all_comments = []
for video_id in video_ids:
    comments = get_video_comments(youtube, video_id)
    if comments:
        all_comments.extend(comments)

# Store comments in a CSV file
csv_file = 'video_comments.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Comment"])
    writer.writerows([[comment] for comment in all_comments])

print("Comments extracted and stored in 'video_comments.csv'.")
