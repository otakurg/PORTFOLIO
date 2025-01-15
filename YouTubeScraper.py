import requests
from yt_dlp import YoutubeDL
from bs4 import BeautifulSoup
  
## Downloading a YouTube Video
def download_video(video_url):
    opts = {}
    with YoutubeDL(opts) as yt:
        yt.download([video_url])
    print(f"Downloaded video: {video_url}")
  
## Extracting YouTube Comments    
def extract_comments(video_url):
    opts = {"getcomments": True}
    with YoutubeDL(opts) as yt:
        info = yt.extract_info(video_url, download=False)
        comments = info["comments"]
        thread_count = info["comment_count"]
        print("Number of threads: {}".format(thread_count))
        for comment in comments:
            print(comment['text'])
  
## Extracting Metadata
def extract_metadata(video_url):
    opts = {}
    with YoutubeDL(opts) as yt:
        info = yt.extract_info(video_url, download=False)
        data = {
            "URL": video_url,
            "Title": info.get("title"),
            "Width": info.get("width"),
            "Height": info.get("height"),
            "Language": info.get("language"),
            "Channel": info.get("channel"),
            "Likes": info.get("like_count")
        }
        print("Metadata:", data)
        return data
  
## Scraping Channel Information
# def scrape_channel_info(channel_url, api_key):
#     params = {
#         'api_key': api_key,
#         'url': channel_url,
#         'render': 'true'
#     }
#     response = requests.get('https://api.scraperapi.com', params=params)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         channel_name = soup.find('yt-formatted-string', {'id': 'text', "class":"style-scope ytd-channel-name"})
#         channel_desc = soup.find('div', {'id': 'wrapper', "class":"style-scope ytd-channel-tagline-renderer"})
#         if channel_name and channel_desc:
#             channel_info = {
#                 "channel_name": channel_name.text.strip(),
#                 "channel_desc": channel_desc.text.strip(),
#             }
#             print("Channel Info:", channel_info)
#             return channel_info
#         else:
#             print("Failed to retrieve channel info")
#     else:
#         print("Failed to retrieve the page:", response.status_code)
  
## Example Usage
if __name__ == "__main__":
    # Download a video
    video_url =  "https://www.youtube.com/watch?v=_SQcugGeZIw&t=6s"
    download_video(video_url)
  
    # Extract comments
    video_url_for_comments = "https://www.youtube.com/watch?v=_SQcugGeZIw&t=6s"
    extract_comments(video_url_for_comments)
  
    # Extract metadata
    video_url_for_metadata = "https://www.youtube.com/watch?v=_SQcugGeZIw&t=6s"
    extract_metadata(video_url_for_metadata)

    # # Scrape channel information
    # api_key = 'YOUR_API_KEY'
    # channel_url = 'https://www.youtube.com/@scraperapi/about'
    # scrape_channel_info(channel_url, api_key)