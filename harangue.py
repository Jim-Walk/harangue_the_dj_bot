#!/usr/bin/env python3
import random
import re
from bs4 import BeautifulSoup
from bs4.element import Tag
import requests

# This script grabs a random harangue the dj page from the Guardian Website,
# and then grabs a song from that page and prints it to the console.
GUARDIAN_URL = "https://www.theguardian.com"
DEBUG = False


def find_feature(tag: Tag):
    if "data-link-name" in tag.attrs:
        if tag["data-link-name"][:7] == "feature":
            return tag


def get_random_harangue():
    random_list_section = random.randint(1, 16)
    page_section = (
        f"{GUARDIAN_URL}/music/series/harangue-the-dj?page={random_list_section}"
    )
    response = requests.get(page_section)
    soup = BeautifulSoup(response.content, "html.parser")
    harangue_links = soup.find_all(find_feature)
    if DEBUG:
        print(f"Found {len(harangue_links)} harangues on page {random_list_section}.")
    if not harangue_links:
        print("No harangues found.")
        return
    random_harangue = random.choice(harangue_links)
    harangue_url = random_harangue["href"]
    harangue_response = requests.get(f"{GUARDIAN_URL}{harangue_url}")
    return harangue_response.text, harangue_url


def extract_songs(harangue_html):
    soup = BeautifulSoup(harangue_html, "html.parser")
    song_elements = soup.find_all("h2")
    song_elements = list(
        filter(
            lambda x: x.text not in ["Comments", "Comments (…)", "Most viewed", "More on this story"], song_elements
        )
    )
    return song_elements


def parse_song_info(songinfo: Tag):
    song_txt = songinfo.get_text()
    song_url = ""
    description = ""

    link = songinfo.find("a")
    if link:
        song_url = link["href"]
    else:
        iframe = songinfo.find_next("iframe")
        if iframe:
            url_frag = iframe["src"]
            if 'youtube' in url_frag:
                url_frag = url_frag.removeprefix(
                    "https://www.youtube-nocookie.com/embed/"
                )
                url_frag = url_frag.removesuffix("?wmode=opaque&feature=oembed")
                song_url = f"https://www.youtube.com/watch?v={url_frag}"
            else:
                song_url = url_frag

    next_ps = songinfo.find_next_siblings("p")
    for p_class in next_ps:
        if p_class.text not in ["", " ", "\n"]:
            description = p_class.text
            # print(f"Found description: {p_class}")
            break

    return song_txt, song_url, description


def extract_dj_info(harangue_html):
    dj_name = ""
    soup = BeautifulSoup(harangue_html, "html.parser")
    dj_element = soup.find("h1")
    dj_name = dj_element.get_text() if dj_element else ""
    if dj_name != "":
        dj_name = dj_name.split(":")[0]
        dj_name = dj_name.removesuffix("Q&A")
        dj_name = dj_name.removesuffix("' favourite tracks")
        dj_name = dj_name.removesuffix("'s favourite tracks")
        dj_name = dj_name.removesuffix("’s favourite tracks")

    print(f"DJ Name: {dj_name}")
    return dj_name


def post_to_bsky(dj_name, song_txt, song_url, desc, harangue_url):
    post_content = f"{dj_name}\n{song_txt}\n{song_url}\n{desc}\n{GUARDIAN_URL}{harangue_url}"
    print(f"Posting to Bluesky:\n{post_content}")
    exit(0)
    # Here you would add the code to post to Bluesky using their API.


def main():
    attempts = 0
    max_attempts = 8

    while attempts < max_attempts:
        harangue_html, harangue_url = get_random_harangue()
        if harangue_html:
            all_songs = extract_songs(harangue_html)
            dj_name = extract_dj_info(harangue_html)
            if dj_name:
                song_attempts = 0
                songinfo = random.choice(all_songs)
                while song_attempts < max_attempts:
                    song_txt, song_url, desc = parse_song_info(songinfo)
                    if song_txt and song_url:
                        if DEBUG:
                            print(f"Found song after {song_attempts} attempts")
                        post_to_bsky(dj_name, song_txt, song_url, desc, harangue_url)
                    songinfo = random.choice(all_songs)
                    song_attempts += 1
                print(f"Failed to find a valid song after {song_attempts} attempts.")
            else:
                print(f"DJ name not found, at {harangue_url}. Retrying...")
        attempts += 1
    print("Failed to find a valid song after multiple attempts.")
    exit(1)


if __name__ == "__main__":
    main()
