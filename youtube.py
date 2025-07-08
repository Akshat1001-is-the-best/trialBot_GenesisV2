from findURL import search_youtube
from download_yt import download_video

def vid_download(text):
    results = search_youtube(text)
    for idx, video in enumerate(results[:5], 1):  # shows top 5 results
        print(f"{idx}. {video['title']}")
        print(f"   {video['url']}\n")

    num = int(input("choose which video you would like: "))
    video_url = results[num]["url"]
    preferred_quality = input("press Enter to see available options: ").strip()
        
    download_video(video_url, preferred_quality)