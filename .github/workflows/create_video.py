import os
import requests
from PIL import Image
import subprocess

def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
    else:
        raise Exception(f"Failed to download image from {url}")

def create_video(image_files, output_file, duration=20):
    # Create a temporary txt file for FFmpeg input
    with open('inputs.txt', 'w') as f:
        for img in image_files:
            f.write(f"file '{img}'\n")
            f.write(f"duration {duration}\n")
    
    # Use FFmpeg to create the video
    cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', 'inputs.txt',
        '-vsync', 'vfr',
        '-pix_fmt', 'yuv420p',
        output_file
    ]
    subprocess.run(cmd, check=True)

    # Clean up temporary files
    os.remove('inputs.txt')
    for img in image_files:
        os.remove(img)

def main():
    # Get image URLs from environment variables
    image_urls = [
        os.environ.get('IMAGE_URL_1'),
        os.environ.get('IMAGE_URL_2'),
        os.environ.get('IMAGE_URL_3')
    ]

    # Download images
    image_files = []
    for i, url in enumerate(image_urls, 1):
        filename = f'image_{i}.jpg'
        download_image(url, filename)
        image_files.append(filename)

    # Create video
    create_video(image_files, 'output.mp4')

    print("Video created successfully!")

if __name__ == "__main__":
    main()
