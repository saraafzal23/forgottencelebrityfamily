import streamlit as st
import requests
from datetime import datetime, timedelta

# YouTube API Key
API_KEY = "AIzaSyCPSSzbWaiQfIKNABhutCaV3X1WRbeiUVI"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

# Streamlit App Title
st.title("YouTube Viral Topics Tool")

# Input Fields
days = st.number_input("Enter Days to Search (1–30):", min_value=1, max_value=30, value=5)

# Keywords: original + all new keyword batches merged here
keywords = [
    # Original macabre + horror family history keywords
    "Macabre History of the Blackridge Family", "Blackridge Family Mystery", "Blackridge Family Mayors",
    "Creepy Family History", "Dark Town Secrets", "Macabre Family Lineage", "True Horror Story",
    "Family Legacy Horror", "Eerie Historical Families", "Henderson Family", "Las Vegas 1909",
    "Land Deal Mystery", "89 Bodies Buried",

    # Celebrity family & legacy keywords
    "Celebrity Children", "Where Are They Now", "Forgotten Celebrity Families", "Hollywood Legacy Kids",
    "Famous People's Children", "Untold Family Stories", "Celebrity Family History", "What Happened After Fame",
    "Children of Legends", "Hollywood Generational Secrets",

    # Royal family drama & updates
    "Royal Family Secrets", "Meghan Markle Controversy", "Prince William Emotional Speech", "King Charles Latest News",
    "Queen Camilla Crying", "Princess Diana Mystery", "Royal Family Drama 2025", "Archie and Lilibet Truth",
    "Royal Titles Revoked", "Shocking Royal Revelations",

    # Then and Now transformations (Filipino + Hollywood)
    "Then and Now Celebrities", "Teleserye Stars Then and Now", "80s Actors Transformation", "90s Hollywood Icons",
    "Classic Filipino TV Stars", "Pinoy Child Actors Grown Up", "Old Hollywood Legends Today",
    "Teen Idols 70s and 90s", "Filipino Celebrities Transformation", "Famous Child Stars Then and Now",
    "Filipino Teleserye Legends Through the Years", "Hollywood 70s Stars Where Are They Now",
    "Child Stars Before and After Fame", "Pinoy Big Brother Celebrities Transformation",
    "Then and Now Stars We Grew Up Watching", "Beloved Teleserye Actors Aging Gracefully",
    "1970s–1990s Heartthrobs Revisited", "TV Stars Who Defined a Generation",
    "Most Beautiful Actresses Then and Now", "Icons of Classic Philippine Television",

    # Celebrity kids & families legacy
    "Whatever Happened To", "Children of Celebrities", "Celebrity Kids Now", "Hollywood Legends Families",
    "Celebrity Children Updates", "Famous Kids Then and Now", "Celebrity Legacy", "Old Hollywood Families",
    "Hollywood Children Today", "What Happened to Their Children", "Celebrity Kids Stories", "Old Stars' Kids",
    "Classic Hollywood Kids", "Hollywood Children Secrets", "Untold Stories of Celebrity Families",
    "Biography of Celebrity Children", "Vintage Hollywood Families",

    # Classic scandals, secrets, rivalries
    "Old Hollywood Secrets", "Then and Now Hollywood", "Classic Hollywood Drama", "Celebrity Scandals Revealed",
    "Hollywood Forbidden Love Affairs", "Shocking Celebrity Confessions", "Classic Movie Stars Secrets",
    "Hollywood Hidden Relationships", "Gay Hollywood History", "Hollywood Rivalries Exposed",
    "Famous Feuds of Old Hollywood", "Dark Hollywood Stories", "Old Hollywood Stars Today",
    "Unsolved Hollywood Mysteries", "Tragic Celebrity Deaths", "Untold Stories of Hollywood Legends",
    "Hollywood Gossip Then and Now", "Secret Hollywood Affairs", "Vintage Hollywood Secrets",
    "Old Hollywood Love Triangles",

    # Mixed recent topics: drama, lgbtq+, surgery fails, plastic surgery
    "Celebrity Kids Now", "Hollywood Children Today", "Then and Now", "Where Are They Now",
    "Celebrity Transformations", "Old Hollywood Scandals", "Royal Family Secrets", "Hollywood Legacy Families",
    "Child Stars Then and Now", "Hollywood Then and Now", "Shocking Celebrity Secrets", "Hollywood's Forgotten Stars",
    "Celebrity Family Drama", "Vintage Hollywood", "Classic Hollywood Kids", "Royal Drama Today",
    "Meghan and Harry Exposed", "Plastic Surgery Fails", "LGBTQ+ Hollywood Icons",

    # Final group: shocking headlines, pop culture, predictions
    "Transgender Celebrities", "Shocking Transformations", "Hollywood Updates 2025", "Child Stars",
    "Plastic Surgery Disasters", "Celebrity Scandals", "Courtroom Drama", "Celebrity Confessions",
    "Aging Celebrities", "Before and After", "Gone Too Soon", "Final Verdict", "Family Secrets",
    "Cast Updates", "Famous Couples", "LGBTQ+ Celebrities", "Tragic Endings", "Old Hollywood",
    "Surprise Revelations", "Shocking Truth", "Famous Divorces", "Inspirational Stories", "Celebrity Deaths",
    "Nostalgic Stars", "Famous Siblings", "Celebrity Relationships", "Celebrity Surgeries", "Legendary Actors",
    "Surprise Families", "Famous Secrets", "Prison Sentences", "Shocking Interviews",
    "Golden Age Hollywood", "Lesbian Rumors", "Oscar Winners", "Celebrity Lovers", "Hollywood Marriages",
    "Simpsons Predictions", "2025 Predictions", "Vatican Conspiracies", "Cryptocurrency Predictions",
    "Simpsons Future Events", "Hollywood Drama", "Shocking Endings", "Classic Stars"
]

# Fetch Button
if st.button("Fetch Data"):
    try:
        start_date = (datetime.utcnow() - timedelta(days=int(days))).isoformat("T") + "Z"
        all_results = []

        for keyword in keywords:
            st.write(f"🔍 Searching for keyword: **{keyword}**")

            search_params = {
                "part": "snippet",
                "q": keyword,
                "type": "video",
                "order": "viewCount",
                "publishedAfter": start_date,
                "maxResults": 5,
                "key": API_KEY,
            }

            response = requests.get(YOUTUBE_SEARCH_URL, params=search_params)
            data = response.json()

            if "items" not in data or not data["items"]:
                st.warning(f"No videos found for: {keyword}")
                continue

            videos = data["items"]
            video_ids = [v["id"]["videoId"] for v in videos if "id" in v and "videoId" in v["id"]]
            channel_ids = [v["snippet"]["channelId"] for v in videos if "snippet" in v and "channelId" in v["snippet"]]

            if not video_ids or not channel_ids:
                st.warning(f"Missing video/channel data for: {keyword}")
                continue

            # Fetch Video Stats
            stats_response = requests.get(YOUTUBE_VIDEO_URL, params={
                "part": "statistics",
                "id": ",".join(video_ids),
                "key": API_KEY
            })
            stats_data = stats_response.json()

            # Fetch Channel Stats
            channel_response = requests.get(YOUTUBE_CHANNEL_URL, params={
                "part": "statistics",
                "id": ",".join(channel_ids),
                "key": API_KEY
            })
            channel_data = channel_response.json()

            if "items" not in stats_data or "items" not in channel_data:
                continue

            for video, stat, channel in zip(videos, stats_data["items"], channel_data["items"]):
                title = video["snippet"].get("title", "N/A")
                description = video["snippet"].get("description", "")[:200]
                video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
                views = int(stat["statistics"].get("viewCount", 0))
                subs = int(channel["statistics"].get("subscriberCount", 0))

                if subs < 3000:
                    all_results.append({
                        "Title": title,
                        "Description": description,
                        "URL": video_url,
                        "Views": views,
                        "Subscribers": subs
                    })

        if all_results:
            st.success(f"✅ Found {len(all_results)} small-channel videos!")
            for result in all_results:
                st.markdown(f"""
                **📺 Title:** {result['Title']}  
                **📝 Description:** {result['Description']}  
                **🔗 URL:** [Watch Here]({result['URL']})  
                **👁️ Views:** {result['Views']}  
                **👤 Subscribers:** {result['Subscribers']}
                """)
                st.write("---")
        else:
            st.warning("No videos found from small channels under 3,000 subs.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
