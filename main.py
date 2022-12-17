import datetime
import json
import urllib

import requests
import feedgenerator
import csv

feed_file = open('feed.csv')

index = open('feeds/index.html', 'w')
index.write('<!DOCTYPE html><html><body><ul>')

for feed in csv.reader(feed_file):
    print(feed)
    comic_url = "https://api.to-corona-ex.com/comics/" + feed[0]
    comic = json.loads(requests.get(comic_url).text)

    rss = feedgenerator.Atom1Feed(
        title=comic.get('title'),
        link="https://to-corona-ex.com/comics/" + feed[0],
        description=comic.get('description'),
        language="ja",
        image=comic.get('cover_image_url')
    )

    episodes_url = "https://api.to-corona-ex.com/episodes?comic_id=" + feed[0] + "&episode_status=free_viewing&limit=5&order=desc&sort=episode_order"
    episodes = json.loads(requests.get(episodes_url).text)

    for ep in episodes.get('resources'):
        rss.add_item(
            unique_id=ep.get('id'),
            title=ep.get('title'),
            link="https://to-corona-ex.com/episodes/" + ep.get('id'),
            description="",
            pubdate=datetime.datetime.fromisoformat(ep.get('published_at'))
        )

    with open('feeds/' + feed[0] + '.xml', 'w') as fp:
        rss.write(fp, 'utf-8')

    index.write('<li><a href="{href}">{title}</a></li>'.format(href=feed[0] + '.xml', title=comic.get('title')))

index.write('</ul></body></html>')
