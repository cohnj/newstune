import feedparser
import newspaper
from pymongo import Connection
import logging
import time

conn = Connection().newstune.articles

logging.basicConfig(filename='logs/feed.log',level=logging.DEBUG)


feed_urls = ["news/artsculture","reuters/businessNews","reuters/companyNews",
			 "reuters/entertainment","reuters/environment","reuters/healthNews",
			 "reuters/lifestyle","news/wealth", "reuters/oddlyEnoughNews",
			 "reuters/peopleNews", "Reuters/PoliticsNews", "reuters/scienceNews",
			 "reuters/sportsNews", "reuters/technologyNews","Reuters/domesticNews",
			 "Reuters/worldNews"]

while True:

	n_inserted = 0
	n_downloaded = 0
	n_skipped = 0
	n_total = 0

	for feed_url in feed_urls:
		source = feed_url
		feed_url = 'http://feeds.reuters.com/' + feed_url + '.rss'
		feed = feedparser.parse(feed_url)
		for entry in feed['entries']:
			n_total += 1
			if conn.find_one({'url' : entry['link']}):
				logging.debug('Skip: %s' % entry['link'])
				n_skipped += 1
				continue

			n_downloaded += 1
			article = newspaper.Article(entry['link'])
			article.download()
			article.parse()
			conn.insert({'url' : entry['link'],
						 'link' : article.canonical_link,
						 'title' : article.title,
						 'text' : article.text,
						 'date' : str(article.publish_date),
						 'images' : article.images,
						 'source' : source})
			n_inserted += 1
			logging.debug('Insert: %s' % entry['link'])

	response = "%d total articles\n%d downloaded\n%d inserted\n%d skipped" % (n_total,n_downloaded,n_inserted,n_skipped)

	print response
	logging.info(response)

	time.sleep(3600)