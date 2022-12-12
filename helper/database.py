import pymongo 
import os
from helper.date import add_date
DB_NAME = os.environ.get("DB_NAME","amiami")
DB_URL = os.environ.get("DB_URL","mongodb+srv://amit:amit@cluster0.a9eqqkf.mongodb.net/?retryWrites=true&w=majority")
mongo = pymongo.MongoClient(DB_URL)
db = mongo[DB_NAME]
dbcol = db["user"]

def insert(chat_id):
            user_id = int(chat_id)
            user_det = {"_id":user_id,"file_id":None ,"caption":None ,"daily":0 ,"date":0 , "uploadlimit" :2147483648,"used_limit":0,"usertype":"Free","prexdate" : None}
            try:
            	dbcol.insert_one(user_det)
            except:
            	return True
            	pass

def addthumb(chat_id, file_id):
	dbcol.update_one({"_id":chat_id},{"$set":{"file_id":file_id}})
	
def delthumb(chat_id):
	dbcol.update_one({"_id":chat_id},{"$set":{"file_id":None}})

def addcaption(chat_id, caption):
       dbcol.update_one({"_id": chat_id},{"$set":{"caption": caption}})
	
def delcaption(chat_id): 
        dbcol.update_one({"_id": chat_id},{"$set":{"caption":None}})
	
def dateupdate(chat_id,date):
	dbcol.update_one({"_id":chat_id},{"$set":{"date":date}})

def used_limit(chat_id,used):
	dbcol.update_one({"_id":chat_id},{"$set":{"used_limit":used}})
	
def usertype(chat_id,type):
	dbcol.update_one({"_id":chat_id},{"$set":{"usertype":type}})
	
def uploadlimit(chat_id,limit):
	dbcol.update_one({"_id":chat_id},{"$set":{"uploadlimit":limit}})

def addpre(chat_id):
    date = add_date()
    dbcol.update_one({"_id":chat_id},{"$set":{"prexdate":date[0]}})

def addpredata(chat_id):
    dbcol.update_one({"_id":chat_id},{"$set":{"prexdate":None}})
    
  
def daily(chat_id,date):
	  dbcol.update_one({"_id":chat_id},{"$set":{"daily":date}})
	  
def find(chat_id):
	id =  {"_id":chat_id}
	x = dbcol.find(id)
	for i in x:
             file = i["file_id"]
             try:
                 caption = i["caption"]
             except:
                 caption = None
                 
             return [file, caption]

def getid():
    values = []
    for key  in dbcol.find():
         id = key["_id"]
         values.append((id)) 
    return values

def delete(id):
	dbcol.delete_one(id)
	
def find_one(id):
	return dbcol.find_one({"_id":id})
	
    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason="",
        )
        await self.col.update_one({"id": id}, {"$set": {"ban_status": ban_status}})

    async def ban_user(self, user_id, ban_duration, ban_reason):
        ban_status = dict(
            is_banned=True,
            ban_duration=ban_duration,
            banned_on=datetime.date.today().isoformat(),
            ban_reason=ban_reason,
        )
        await self.col.update_one({"id": user_id}, {"$set": {"ban_status": ban_status}})

    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason="",
        )
        user = await self.col.find_one({"id": int(id)})
        return user.get("ban_status", default)

    async def get_all_banned_users(self):
        banned_users = self.col.find({"ban_status.is_banned": True})
        return banned_users
