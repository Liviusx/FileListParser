import time
import Components.siteParser as siteParser
import pickle

baseObject = {
    "urls":{
        "base": "http://filelist.ro",
        "login": "/login.php",
        "formLoginAction": "takelogin.php",
        "default": "/browse.php",
    },
    "htmlElements": {
        "listElementsSelector": ".torrentrow",
    },
    "credentials":{
        "username": "",
        "password": ""
    }
}

_trackList = []

site = siteParser.siteParser(baseObject)

def onLoginSuccessfull(e):
    print("\n\n ----- Login successfull ------- \n\n")

site.on("site_login_successfull", onLoginSuccessfull)

site.login();

while True:
    tName = input("Enter the torrent name that you want to track: ")

    if len(tName) == 0:
        continue
        

    itemQuery = "?search=" + str(tName).replace(" ", "+") + "&cat=0&searchin=1&sort=2"
    items = site.lookItemByStringQuery(tName, itemQuery)

    print(items)

    with open("d:/"+ items[0]["Name"] + ".torrent", "wb") as output:
        output.write(site.downloadFile(items[0]))

    time.sleep(0.5)
