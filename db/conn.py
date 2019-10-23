from urllib.parse import quote_plus
from pymongo import MongoClient
from config.configs import configs
from mongoengine import connect

uri = "mongodb://%s:%s@%s" % (
    quote_plus(configs["db"]["username"]), quote_plus(configs["db"]["password"]),
    "%s:%s" % (configs["db"]["host"], configs["db"]["port"]))
client = MongoClient(uri)
connect(
    db='ethereum-watch',
    username=configs.db.username,
    password=configs.db.password,
    host=configs.db.host, port=configs.db.port, authentication_source='admin'
)
