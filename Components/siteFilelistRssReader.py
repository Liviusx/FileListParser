import feedparser
import jsonpickle
import re

class rssFilelistParser(object):
	
	baseObject = None
	
	def __init__(self, baseObject):
 		self.baseObject = baseObject;
        
	feedLink = 	"http://filelist.ro/rss.php?&search=walking&feed=dl&cat=4,19,21&passkey=4f4431ffa674098126d5f86ee82d09f3"
	
	feed = feedparser.parse(feedLink)
	
	minIndex = 0
	maxIndex = len(feed.entries) - 1
	
	while minIndex < maxIndex:
		itemStart = feed.entries[minIndex].title.split(".")
		itemEnd = feed.entries[maxIndex].title.split(".")
		print(itemStart)
		print("======================")		
		print(itemEnd)
		minIndex = minIndex + 1
		maxIndex = maxIndex - 1

