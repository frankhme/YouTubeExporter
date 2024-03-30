#import necessary packages and modules
import csv
import os
import re

from googleapiclient.discovery import build

# Define API key
API_KEY = '#your API key'

#Function 1: define a function to retrieve the playlist ID from a public YouTube URL:
def get_playlist_id(playlist_url):
#common expression to extract playlist ID from URL
  pattern = r'(?<=list=)[\w-]+'
  match = re.search(pattern, playlist_url)
  if match: 
    return match.group(0)
  else:
      raise ValueError("Invalid playlist URL :(")

#Function 2: define a function to get playlist videos from the playlist ID and YouTube API key:
def get_playlist_videos(playlist_id, api_key):
  youtube = build("youtube", "v3", developerKey=api_key)
#The function will start with an empty list and pagination
  playlist_items = []
  next_page_token = None

#run a loop to retrieve playlist items. The loop runs       indefinitely until a break statement is encountered.
  while True:
#request the YouTube Data API to retrieve a list of playlist   items.
    request = youtube.playlistItems().list(
#We want to retrieve a snippet part of each playlist item,        which includes basic details about each video
      part="snippet",
      playlistId = playlist_id,
      maxResults = 50,
      pageToken = next_page_token
    )  
#Executes the constructed request, sending it to the YouTube data API, and retrieves the response.
    response = request.execute()
    playlist_items.extend(response["items"])
    next_page_token = response.get("nextPageToken")

    if not next_page_token: 
      break
  return playlist_items

#Function 3: Exporting the retrieved playlist items to a CSV file

#Opens a file in write mode, make sure no newline characters are modeified, and ensure writing is in utf-8 encoding
def export_to_csv(playlist_items, csv_filename):
  fieldnames = ["Video Title", "Video Link"]
  with open(csv_filename, "w", newline = "", encoding = "utf-8") as csvfile:
#DictWriter class from the csv module is used to write dictionaries into the CSV file. It requires 2 arguments: csv file, and field names for the CSV file.
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#Write the header row for the CSV file. 
    writer.writeheader()

#For each item identified in the playlist_items list, (an item represents a video in the playlist), extract the title of the video from the 'snippet' section of the title
    for item in playlist_items:
#In the context of the YouTube Data API, the resourceId and videoId are used to uniquely identify a video within a playlist or any other context where videos are referenced. Here's why we need them:
        print(item.keys())
        video_title = item["snippet"]["title"]
        video_id = item["snippet"]["resourceId"]["videoId"]
        video_link = f"https://www.youtube.com/watch?v={video_id}"
        writer.writerow({"Video Title": video_title, "Video Link": video_link})

#Checks if the script is being run as part of the main program
if __name__ == "__main__":
  playlist_url = input("Please provide the name of the YouTube playlist URL: ")

  try: 
  #Calls function 1
    playlist_id = get_playlist_id(playlist_url)
  except ValueError as e:
    print(e)
    exit()

#calls function 2: 
playlist_items = get_playlist_videos(playlist_id, API_KEY)

#file export and naming:
csv_filename = "Playlist_Videos.csv"
export_to_csv(playlist_items, csv_filename)

print(f"Success! Your playlist videos have been saved to {os.path.abspath(csv_filename)}")
