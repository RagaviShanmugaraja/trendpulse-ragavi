import requests
import json
import os
import time
from datetime import datetime


# Hacker News API URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# User-Agent required by the assignment
headers = {
    "User-Agent": "TrendPulse/1.0"
}


# Keywords used to classify stories
categories = {
    "technology": [
        "AI", "software", "tech", "code", "computer",
        "data", "cloud", "API", "GPU", "LLM"
    ],
    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],
    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game",
        "team", "player", "league", "championship"
    ],
    "science": [
        "research", "study", "space", "physics", "biology",
        "discovery", "NASA", "genome"
    ],
    "entertainment": [
        "movie", "film", "music", "Netflix", "game",
        "book", "show", "award", "streaming"
    ]
}


# This list will store all the stories we collect
stories = []


# ---------------------------------------------------------
# STEP 1: Fetch the top 500 story IDs
# ---------------------------------------------------------

try:
    response = requests.get(
        TOP_STORIES_URL,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    # Get the first 1000 story IDs
    story_ids = response.json()[:1000]

    print(f"Fetched {len(story_ids)} story IDs.")

except requests.RequestException as e:
    print("Failed to fetch story IDs:", e)
    story_ids = []


# ---------------------------------------------------------
# STEP 2: Fetch the details of each story
# ---------------------------------------------------------

story_details = []

for story_id in story_ids:

    try:
        response = requests.get(
            ITEM_URL.format(story_id),
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        story = response.json()

        # Only keep valid Hacker News stories
        if story and story.get("type") == "story":
            story_details.append(story)

    except requests.RequestException as e:
        # If one request fails, print the error and continue
        print(f"Failed to fetch story {story_id}: {e}")
        continue


print(f"Successfully fetched {len(story_details)} stories.")


# ---------------------------------------------------------
# STEP 3: Process each category
# ---------------------------------------------------------

for category, keywords in categories.items():

    category_count = 0

    # Check the fetched stories for this category
    for story in story_details:

        # Stop after collecting 25 stories for this category
        if category_count >= 25:
            break

        title = story.get("title", "")
        title_lower = title.lower()

        # Check whether any keyword appears in the title
        matched = False

        for keyword in keywords:

            if keyword.lower() in title_lower:
                matched = True
                break

        # If the title doesn't contain a category keyword,
        # move to the next story.
        if not matched:
            continue

       

        # Create the required record
        story_data = {
            "post_id": story.get("id"),
            "title": title,
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by", "unknown"),
            "collected_at": datetime.now().isoformat()
        }

        stories.append(story_data)
        category_count += 1

    print(f"{category}: {category_count} stories collected.")

    # Wait 2 seconds before processing the next category
    time.sleep(2)


# ---------------------------------------------------------
# STEP 4: Create the data folder
# ---------------------------------------------------------

os.makedirs("data", exist_ok=True)


# ---------------------------------------------------------
# STEP 5: Create the output filename
# ---------------------------------------------------------

date_string = datetime.now().strftime("%Y%m%d")

file_path = f"data/trends_{date_string}.json"


# ---------------------------------------------------------
# STEP 6: Save the stories as JSON
# ---------------------------------------------------------

with open(file_path, "w", encoding="utf-8") as file:

    json.dump(
        stories,
        file,
        indent=4,
        ensure_ascii=False
    )


# ---------------------------------------------------------
# STEP 7: Print the final result
# ---------------------------------------------------------

print(f"\nCollected {len(stories)} stories.")
print(f"Saved to {file_path}")