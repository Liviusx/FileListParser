from robobrowser import RoboBrowser
import datetime
import time
import pickle
import os
import eventFactory

class siteFilelistParser(object):
		eventHandler = None
		browser = RoboBrowser(history=True)
    baseObject = None
		events = eventFactory.eventFactory()
    _foundItems = []
    _dataDir = os.path.join(os.path.curdir, "data")
    _pathSearchHistory = os.path.join(_dataDir, "lookup.txt")

    def __init__(self, baseObject):
        self.baseObject = baseObject;
        eventHandler = eventFactory.eventFactory()
        
        os.makedirs(self._dataDir, exist_ok=True)

        if not os.path.exists(self._pathSearchHistory): 
            with open(self._pathSearchHistory, "wb") as writeHistory:
                writeHistory.write([])

        try:
            searchHistory = open(self._pathSearchHistory, 'rb')
            self._foundItems = pickle.load(searchHistory)
            searchHistory.close()
        except EOFError:
            self._foundItems = []
        
    def login(self):
        baseLoginUrl = str(self.baseObject["urls"]["base"]) + str(self.baseObject["urls"]["login"])
        
        self.browseTo(baseLoginUrl)
        
        form = self.browser.get_form(action=str(self.baseObject["urls"]["formLoginAction"]))

        form["username"].value = self.baseObject["credentials"]["username"]
        form["password"].value = self.baseObject["credentials"]["password"]

        self.browser.submit_form(form)
        
        self.trigger("site_login_successfull")

        if self.baseObject["urls"]["base"] is not None:
            defaultPage = str(self.baseObject["urls"]["base"]) + str(self.baseObject["urls"]["default"])
            self.browseTo(defaultPage)
        
    def browseTo(self, page):
        self.browser.open(page)

    def lookItemByStringQuery(self, searchInput, urlQuery):
        defaultPage = str(self.baseObject["urls"]["base"]) + str(self.baseObject["urls"]["default"])
        self.browser.open(defaultPage + urlQuery)
        
        if len(self._foundItems) > 0:
            for item in self._foundItems:
                if str(item["SearchKey"]) == str(searchInput):
                    return item["ItemList"]

        items = list(self.browser.select(str(self.baseObject["htmlElements"]["listElementsSelector"])))

        if len(items) == 0:
            return None

        downloadList = []
    
        for torrent in items:
            item = {}
            item["Name"] = str(torrent.select(".torrenttable b")[0].getText());
            item["Size"] = torrent.select("div.torrenttable span font")[0].getText();
            item["Link"] = torrent.select("a[href*=download]")[0]["href"];

            downloadList.append(item)

        foundItem = { "SearchKey": searchInput, "ItemList": downloadList, "TimeStamp": datetime.datetime.fromtimestamp(time.time())}
        self._foundItems.append(foundItem)

        with open(self._pathSearchHistory, "wb") as output:
            pickle.dump(self._foundItems, output)
        
        return downloadList

    def downloadFile(self, item):
        self.browser.open(str(self.baseObject["urls"]["base"]) + "/" + item["Link"])
        return self.browser.response.content
