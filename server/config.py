from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Environment variables
load_dotenv()
dbUsername = os.environ.get("DB_USERNAME")
dbPassword = os.environ.get("DB_PASSWORD")
dbName = os.environ.get("DB_NAME")

# Database
load_dotenv()

cluster = MongoClient(
    "mongodb+srv://%s:%s@cluster0.xyttr.mongodb.net/%s" % (dbUsername, dbPassword, dbName),
	tls=True,
    tlsAllowInvalidCertificates=True
)
db = cluster[dbName]