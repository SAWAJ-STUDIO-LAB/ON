"""yt_long_playlist.py"""


def add(yt, video_id, playlist_id):
    try:
        yt.playlistItems().insert(
            part="snippet",
            body={"snippet": {"playlistId": playlist_id.strip(),
                              "resourceId": {"kind": "youtube#video",
                                             "videoId": video_id}}}).execute()
        return True
    except Exception:
        return False
