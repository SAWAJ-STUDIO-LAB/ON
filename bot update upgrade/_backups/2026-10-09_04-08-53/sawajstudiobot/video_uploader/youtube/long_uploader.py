# ╔══════════════════════════════════════════════════════════╗
# ║  📄 FILE:      long_uploader.py                          ║
# ║  📁 PATH:      .../video_uploader/youtube/               ║
# ║                long_uploader.py                          ║
# ║  🎯 PURPOSE:   Upload Long video to YouTube              ║
# ║  📖 FOLDER:    youtube                                   ║
# ╚══════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════╗
║   📺 YOUTUBE LONG UPLOADER                               ║
║   ═══════════════════════════                            ║
║                                                          ║
║   🎯 Purpose:                                            ║
║      Long video ko YouTube pe upload karna               ║
║                                                          ║
║   📖 API:                                                ║
║      youtube.videos().insert()                           ║
║      youtube.playlistItems().insert()                    ║
║                                                          ║
║   📝 Difference:                                          ║
║      • Same API as Short                                 ║
║      • Chapters in description (timestamps)              ║
║      • Category: 22 (People & Blogs)                     ║
║                                                          ║
║   🔑 Credentials:                                         ║
║      • YOUTUBE_CLIENT_ID                                 ║
║      • YOUTUBE_CLIENT_SECRET                             ║
║      • YOUTUBE_REFRESH_TOKEN                             ║
║      • DAILY_HADEES_YT_PLAYLIST_ID                       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import os


# ═══════════════════════════════════════════════════════════
# 📺 YOUTUBE LONG UPLOADER CLASS
# ═══════════════════════════════════════════════════════════

class YouTubeLongUploader:
    """Upload Long video to YouTube."""

    def __init__(self, base=None):
        """Initialize uploader."""
        self.base = base

    # ─────────────────────────────────────────────────────
    # UPLOAD — main upload method
    # ─────────────────────────────────────────────────────
    def upload(self, video_path, title="", description="",
               tags=None, chapters=None):
        """
        Upload Long video to YouTube.

        Args:
            video_path:  path to video file
            title:       video title
            description: video description
            tags:        list of tags
            chapters:    list of timestamp strings

        Returns:
            True if successful, False otherwise
        """
        try:
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload

            # ═══════════ Add chapters to description ═══════════
            if chapters:
                description += "\n\n⏱️ Timestamps:\n" + "\n".join(chapters)

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
                    "tags": tags or ["Hadith", "Long Hadith", "Islamic"],
                    "categoryId": "22",
                },
                "status": {
                    "privacyStatus": "public",
                    "selfDeclaredMadeForKids": False,
                },
            }

            # ═══════════ Upload ═══════════
            print(f"→ YT Long: Uploading {video_path}")
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
            print(f"✅ YT Long: Upload successful! ID: {vid}")

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
                    print("✅ YT Long: Added to playlist")
                except Exception as e:
                    print(f"⚠️ YT Long playlist: {str(e)[:60]}")

            return True

        except Exception as e:
            print(f"❌ YT Long error: {str(e)[:100]}")
            return False


# ═══════════════════════════════════════════════════════════
# 🧪 TEST
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    uploader = YouTubeLongUploader()
    uploader.upload("test_video.mp4", "Test Title", "Test Description",
                    chapters=["00:00 Intro", "00:30 Hadith"])
