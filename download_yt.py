import yt_dlp
import os
import sys
from datetime import datetime
import subprocess


def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True)
        return True
    except FileNotFoundError:
        return False


def format_size(bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024
    return f"{bytes:.2f} GB"


def progress_hook(d):
    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
        
        if total:
            percentage = (downloaded / total) * 100
            speed = d.get('speed', 0)
            speed_str = format_size(speed) + '/s' if speed else 'N/A'
            
            eta = d.get('eta', None)
            eta_str = str(datetime.fromtimestamp(eta).strftime('%M:%S')) if eta else 'N/A'
            
            progress = f"\rProgress: {percentage:.1f}% | Speed: {speed_str} | ETA: {eta_str}"
            sys.stdout.write(progress)
            sys.stdout.flush()


def get_best_format(formats, target_height, ffmpeg_available):
    if ffmpeg_available:
        # FFmpeg is available, we can use separate video and audio streams
        return f'bestvideo[height<={target_height}][ext=mp4]+bestaudio[ext=m4a]/best[height<={target_height}][ext=mp4]/best'
    else:
        # FFmpeg isn't available, we need a merged format
        return f'best[height<={target_height}][ext=mp4]/best[ext=mp4]/best'


def download_video(url, preferred_quality=None, output_path='/Users/jyoti/Downloads'):
    try:
        # Check if FFmpeg is available
        ffmpeg_available = check_ffmpeg()
        if not ffmpeg_available:
            print("FFmpeg is not installed.")

        # Create output directory if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Configure yt-dlp options
        ydl_opts = {
            'progress_hooks': [progress_hook],
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'verbose': False
        }

        print("Fetching video information...")
        
        # Create a yt-dlp object and get video info
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video information
            info = ydl.extract_info(url, download=False)
            
            # Display video information
            print(f"\nVideo Title: {info.get('title', 'Unknown')}")
            duration = int(info.get('duration', 0))
            print(f"Duration: {duration // 60}:{duration % 60:02d}")
            
            # Get available formats and filter based on FFmpeg availability
            formats = info.get('formats', [])
            quality_set = set()
            
            # Collect available qualities, considering FFmpeg availability
            for f in formats:
                height = f.get('height')
                # If FFmpeg isn't available, only include formats that have both video and audio
                if height and (ffmpeg_available or f.get('acodec') != 'none'):
                    quality_set.add(f"{height}p")
            
            # Sort qualities from lowest to highest
            quality_list = sorted(quality_set, key=lambda x: int(x.replace('p', '')))
            
            print("\nAvailable qualities:")
            for i, quality in enumerate(quality_list, 1):
                print(f"{i}. {quality}")

            # Handle quality selection
            if not preferred_quality or preferred_quality not in quality_set:
                print("\nPlease select a quality from the available options:")
                while True:
                    try:
                        choice = int(input("Enter the number of your choice: "))
                        if 1 <= choice <= len(quality_list):
                            preferred_quality = quality_list[choice-1]
                            break
                        else:
                            print("Invalid choice. Please try again.")
                    except ValueError:
                        print("Please enter a valid number.")

            # Set format based on selected quality and FFmpeg availability
            height = int(preferred_quality.replace('p', ''))
            ydl_opts['format'] = get_best_format(formats, height, ffmpeg_available)
            
            print(f"\nDownloading video in {preferred_quality}...")
            
            # Download the video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            print("\nDownload completed successfully!")
            
    except Exception as e:
        print("there was an error")

#test: https://www.youtube.com/watch?v=x7X9w_GIm1s"""