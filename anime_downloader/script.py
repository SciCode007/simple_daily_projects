"""
Created on Sat Jun 2 2024
Author: Mohamed Basher
Github: @SciCode007

This script can download an entire season of an anime show (or any range of episodes) from Animebelkom.net.
It is for experimental purposes only and should not be used for commercial purposes.
It uses concurrent.futures to download multiple episodes concurrently for faster download speeds.
"""

import requests
from bs4 import BeautifulSoup
import wget
import concurrent.futures


def download_video(link, series_name, current_episode):
    print(f"Downloading {series_name} Episode: {current_episode}", end="\n")
    wget.download(link, f"{series_name}-{current_episode}.mp4")
    print(
        f"{series_name} Episode {current_episode} has been downloaded successfully.",
        end="\n",
    )


def download_series(series_name, start_episode, end_episode):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for current_episode in range(start_episode, end_episode + 1):
            url = f"https://animeblkom.net/watch/{series_name}/{current_episode}"

            try:
                response = requests.get(url)
                response.raise_for_status()
            except requests.HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                continue
            except Exception as err:
                print(f"Other error occurred: {err}")
                continue

            soup = BeautifulSoup(response.content, "html.parser")
            download_links = soup.find("div", class_="panel-body")

            video_link = [
                link.get("href")
                for link in download_links.find_all("a")
                if "720p" in link.text
            ]

            executor.map(download_video, video_link, [series_name], [current_episode])

    print("The entire season has been downloaded.")


# Usage
download_series("psycho-pass", 17, 22)
