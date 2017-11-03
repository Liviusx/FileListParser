#from sqlitedict import SqliteDict
#import  pickle
import enum

class itemType(Enum):
	TV = 1
	MOVIE = 2 
	GAME = 3
	MUSIC = 4

exampleObject = {
    "show":{
        "title": "The walking dead",
        "type": itemType,
        "formLoginAction": "takelogin.php",
        "default": "/browse.php",
    }
}

class entertainmentItem(object):
	callbacks = None
	baseObject = None
	
	
	
	def __init__(self, baseObject):
 		self.baseObject = baseObject
 	
 	def retrieveData(self):
 		#Todo: functionality to retrieve persistent data
 		
 				
myDict = SqliteDict("./tvPreferences", autocommit=True)
#myDict["test"] = "Liviu"
print((myDict["test"]))
