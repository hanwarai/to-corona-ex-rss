import csv
import datetime
import json
from pathlib import Path

import feedgenerator
import requests
from jinja2 import Environment, FileSystemLoader

FEEDS_DIR = Path("feeds")

with Path("feed.csv").open(encoding="utf-8") as feed_file:
    feed_rows = list(csv.reader(feed_file))

headers = {
    "x-api-environment-key": "K4FWy7Iqott9mrw37hDKfZ2gcLOwO-kiLHTwXT8ad1E=",
}

rendered_feeds = []
for feed in feed_rows:
    print(feed)

    comic_url = "https://api.to-corona-ex.com/comics/" + feed[0]
    comic = json.loads(requests.get(comic_url, headers=headers).text)

    comic_title = comic.get("title")
    rendered_feeds.append({"id": feed[0], "title": comic_title})

    rss = feedgenerator.Atom1Feed(
        title=comic_title,
        link="https://to-corona-ex.com/comics/" + feed[0],
        description=comic.get("description"),
        language="ja",
        image=comic.get("cover_image_url"),
    )

    episodes_url = (
        "https://api.to-corona-ex.com/episodes"
        f"?comic_id={feed[0]}"
        "&episode_status=free_viewing&limit=5&order=desc&sort=episode_order"
    )
    episodes = json.loads(requests.get(episodes_url, headers=headers).text)

    for ep in episodes.get("resources"):
        rss.add_item(
            unique_id=ep.get("id"),
            title=ep.get("title"),
            link="https://to-corona-ex.com/episodes/" + ep.get("id"),
            description="",
            pubdate=datetime.datetime.fromisoformat(ep.get("published_at")),
            content="",
        )

    with (FEEDS_DIR / f"{feed[0]}.xml").open("w", encoding="utf-8") as fp:
        rss.write(fp, "utf-8")

# Generate index.html
jinja_env = Environment(loader=FileSystemLoader("templates"), autoescape=True)
jinja_template = jinja_env.get_template("index.html")
(FEEDS_DIR / "index.html").write_text(jinja_template.render(feeds=rendered_feeds), encoding="utf-8")
