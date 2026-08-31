from __future__ import annotations


def search_videos(youtube, query, max_results=5):

    response = (
        youtube.search()
        .list(
            part="snippet",
            q=query,
            type="video",
            maxResults=max_results,
            order="relevance"
        )
        .execute()
    )

    results = []

    for item in response.get("items", []):

        video_id = item.get("id", {}).get("videoId")

        snippet = item.get("snippet", {})

        if not video_id:
            continue

        results.append({
            "video_id": video_id,
            "title": snippet.get(
                "title",
                "Unknown title"
            ),
            "channel": snippet.get(
                "channelTitle",
                "Unknown channel"
            )
        })

    return results


def create_playlist(
    youtube,
    title: str,
    description: str = "",
    privacy_status: str = "private",
) -> str:
    """
    Create a YouTube playlist and return its playlist ID.
    """

    body = {
        "snippet": {
            "title": title,
            "description": description,
        },
        "status": {
            "privacyStatus": privacy_status,
        },
    }

    response = (
        youtube.playlists()
        .insert(
            part="snippet,status",
            body=body,
        )
        .execute()
    )

    return response["id"]


def add_video_to_playlist(
    youtube,
    playlist_id: str,
    video_id: str,
) -> str:
    """
    Add a video to a YouTube playlist.
    """

    body = {
        "snippet": {
            "playlistId": playlist_id,
            "resourceId": {
                "kind": "youtube#video",
                "videoId": video_id,
            },
        }
    }

    response = (
        youtube.playlistItems()
        .insert(
            part="snippet",
            body=body,
        )
        .execute()
    )

    return response["id"]
