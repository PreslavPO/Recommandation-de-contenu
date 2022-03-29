import pymongo
from pymongo import MongoClient
import log

cluster = MongoClient(
    "mongodb+srv://" + log.username + ":" + log.password + "@cluster0.xyttr.mongodb.net/" + log.namedb, tls=True,
    tlsAllowInvalidCertificates=True)
db = cluster["recommenderSystem"]
collection = db["movies"]

result = collection.find()

for movies in result:
    print(movies)
