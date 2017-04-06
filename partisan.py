import re

from pymongo import Connection

words = ["trump","lying","left","corrupt","liberal","islam","race","money","country","illegal",
		"hillary","bernie","republicans","nra","progressive","immigrant","wall","terrorist",
		"muslim","election","washington","debate","refugee","lyin","nasty","revolution","radical",
		"terrorism","rigged","alt-right","bigly","birther","breitbart","fake","divide","division",
		"wound","wing","brexit","isis","obama"]

conn = Connection().newstune
articles = conn.articles.find()

filtered = []

for article in articles:
	score = 0
	for word in words:
		if word in article['text'].lower():
			score += 1
	filtered.append((score,article['title']))
	filtered.sort()
	filtered = list(set(fitered))



