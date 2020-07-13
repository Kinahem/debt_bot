import pymongo
import config 

MONGODB_URI = config.mongo_url
client = pymongo.MongoClient(MONGODB_URI, connectTimeoutMS=30000)
db = client.get_database("test_bot")
dolg_col = db.user_records
user_col = db.users
music_col = db.music
user_access = db.music_access

#postgres_url = "postgres://yrorprmbhfdotx:3a82fda7f91e8ae9b4b143953f14b5a943c3552ba21184cc25f6ba183c00c329@ec2-107-20-167-11.compute-1.amazonaws.com:5432/dd4iosmt4pslgs"
