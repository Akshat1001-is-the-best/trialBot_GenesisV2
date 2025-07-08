import re
import urllib.request
from urllib.parse import unquote

def search_youtube(query):
    # Prepare the search URL
    search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    
    # Fetch and decode the HTML
    html = urllib.request.urlopen(search_url).read().decode()
    
    # Extract video IDs and titles using regex
    pattern = r'"videoRenderer":{"videoId":"(.{11})".*?"title":{"runs":\[{"text":"(.+?)"'
    matches = re.findall(pattern, html)
    
    # Format results
    videos = []
    for video_id, title in matches:
        videos.append({
            "title": unquote(title),
            "url": f"https://www.youtube.com/watch?v={video_id}"
        })
    
    return videos
