import pymongo
import urllib 

class Database(object):
    #URI = "mongodb://127.0.0.1:27017"
    URI = "mongodb+srv://tawadev:" + urllib.parse.quote_plus("tawadev@2021")+"@cluster0.6geuj.mongodb.net/microblog?retryWrites=true&w=majority"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['fmc']

    @staticmethod
    def insert(collection,data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection,query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection,query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update_one(collection,query,new_value):
        return Database.DATABASE[collection].update_one(query,new_value)