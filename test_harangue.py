import random
import pytest
from harangue import extract_songs, extract_dj_info, parse_song_info


class TestPinch:
    with open("dj_pinch.html", "r") as h_file:
        harangue_html = h_file.read()

    def test_only_songs(self):
        songinfos = extract_songs(self.harangue_html)
        for songinfo in songinfos:
            assert "Comments" not in songinfo.text
            assert "Most viewed" not in songinfo.text
            assert "More on this story" not in songinfo.text

    def test_no_empty_strs(self):
        all_songs = extract_songs(self.harangue_html)
        dj_name = extract_dj_info(self.harangue_html)
        songinfo = random.choice(all_songs)
        song_txt, song_url, desc = parse_song_info(songinfo)

        assert dj_name != ""
        assert song_txt != ""
        assert song_url != ""
        assert desc != ""


class TestKyle:
    with open("kyle_hall.html", "r") as h_file:
        harangue_html = h_file.read()

    def test_only_songs(self):
        songinfos = extract_songs(self.harangue_html)
        for songinfo in songinfos:
            assert "Comments" not in songinfo.text
            assert "Most viewed" not in songinfo.text
            assert "More on this story" not in songinfo.text

    def test_no_empty_strs(self):
        all_songs = extract_songs(self.harangue_html)
        dj_name = extract_dj_info(self.harangue_html)
        songinfo = random.choice(all_songs)
        song_txt, song_url, desc = parse_song_info(songinfo)

        assert dj_name != ""
        assert song_txt != ""
        assert song_url != ""
        assert desc != ""

class TestMorgen:
    with open("morgan_geist.html", "r") as h_file:
        harangue_html = h_file.read()

    def test_only_songs(self):
        songinfos = extract_songs(self.harangue_html)
        for songinfo in songinfos:
            assert "Comments" not in songinfo.text
            assert "Most viewed" not in songinfo.text
            assert "More on this story" not in songinfo.text

    def test_no_empty_strs(self):
        all_songs = extract_songs(self.harangue_html)
        dj_name = extract_dj_info(self.harangue_html)
        songinfo = random.choice(all_songs)
        song_txt, song_url, desc = parse_song_info(songinfo)

        assert dj_name != ""
        assert song_txt != ""
