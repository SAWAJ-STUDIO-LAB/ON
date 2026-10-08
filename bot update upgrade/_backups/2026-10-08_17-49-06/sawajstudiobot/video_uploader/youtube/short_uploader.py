# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      short_uploader.py                         ║
# ║  📁 PATH:      .../video_uploader/youtube/               ║
# ║                short_uploader.py                         ║
# ║  🎯 PURPOSE:   Upload Short to YouTube Shorts            ║
# ║  📖 FOLDER:    youtube                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📺 YOUTUBE SHORTS UPLOADER                             ║
║   ═══════════════════════════                            ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Short video ko YouTube Shorts pe upload karna       ║
║                                                          ║
║   📖 API:                                                ║
║      youtube.videos().insert()                           ║
║      youtube.playlistItems().insert()                    ║
║                                                          ║
║   🔑 Credentials:                                         ║
║      • YOUTUBE_CLIENT_ID                                 ║
║      • YOUTUBE_CLIENT_SECRET                             ║
║      • YOUTUBE_REFRESH_TOKEN                             ║
║      • DAILY_HADEES_YT_PLAYLIST_ID                       ║
║                                                          ║
║   📝 Note:                                                ║
║      YouTube auto-detects Shorts via #Shorts tag         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os


# ═══════════════════════════════════════════════════════════
# 📺 YOUTUBE SHORTS UPLOADER CLASS
# ═══════════════════════════════════════════════════════════

class YouTubeShortUploader:
    """Upload Short to YouTube Shorts."""

    def __init__(self, base=None):
        """Initialize uploader."""
        self.base = base

    # ─────────────────────────────────────────────────────
    # UPLOAD — main upload method
    # ─────────────────────────────────────────────────────
    def upload(self, video_path, title="", description="", tags=None):
        """
        Upload Short to YouTube.

        Args:
            video_path:  path to video file
            title:       video title (max 100 chars)
            description: video description
            tags:        list of tags

        Returns:
            True if successful, False otherwise
        """
        try:
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload

            # ═══════════ Authenticate ═══════════
            creds = Credentials(
                None,
                refresh_token=os.environ.get("YOUTUBE_REFRESH_TOKEN"),
                client_id=os.environ.get("YOUTUBE_CLIENT_ID"),
                client_secret=os.environ.get("YOUTUBE_CLIENT_SECRET"),
                token_uri="https://oauth2.googleapis.com/token")
            yt = build("youtube", "v3", credentials=creds, cache_discovery=False)

            # ═══════════ Prepare metadata ═══════════
            body = {
                "snippet": {
                    "title": title[:100],
                    "description": description,
                    "tags": tags or ["Shorts", "Hadith", "Islamic"],
                    "categoryId": "22",
                },
                "status": {
                    "privacyStatus": "public",
                    "selfDeclaredMadeForKids": False,
                },
            }

            # ═══════════ Upload ═══════════
            print(f"→ YT Short: Uploading {video_path}")
            req = yt.videos().insert(
                part="snippet,status",
                body=body,
                media_body=MediaFileUpload(video_path, chunksize=-1,
                                           resumable=True,
                                           mimetype="video/mp4"))

            response = None
            while response is None:
                _, response = req.next_chunk()

            vid = response.get("id")
            print(f"✅ YT Short: Upload successful! ID: {vid}")

            # ═══════════ Add to playlist ═══════════
            playlist_id = os.environ.get("DAILY_HADEES_YT_PLAYLIST_ID")
            if vid and playlist_id:
                try:
                    yt.playlistItems().insert(
                        part="snippet",
                        body={
                            "snippet": {
                                "playlistId": playlist_id.strip(),
                                "resourceId": {
                                    "kind": "youtube#video",
                                    "videoId": vid,
                                },
                            }
                        }).execute()
                    print("✅ YT Short: Added to playlist")
                except Exception as e:
                    print(f"⚠️ YT Short playlist: {str(e)[:60]}")

            return True

        except Exception as e:
            print(f"❌ YT Short error: {str(e)[:100]}")
            return False


# ═══════════════════════════════════════════════════════════
# 🧪 TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    uploader = YouTubeShortUploader()
    uploader.upload("test_video.mp4", "Test Title", "Test Description")
