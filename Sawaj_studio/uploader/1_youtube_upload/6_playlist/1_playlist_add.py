"""
📋 YouTube Playlist Add
"""
import os


def add_to_playlist(video_id):
    try:
        from ..2_client.1_client_builder import build_client
        playlist_id = os.environ.get("DAILY_HADEES_YT_PLAYLIST_ID", "").strip()
        if not playlist_id:
            return False
        yt = build_client()
        if not yt:
            return False
        yt.playlistItems().insert(
            part="snippet",
            body={"snippet": {
                "playlistId": playlist_id,
                "resourceId": {"kind": "youtube#video", "videoId": video_id}}}).execute()
        return True
    except Exception:
        return False
