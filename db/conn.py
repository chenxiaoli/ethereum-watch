from urllib.parse import quote_plus
from pymongo import MongoClient
from config.configs import configs
from mongoengine import connect

uri = "mongodb://%s:%s@%s" % (
    quote_plus(configs.db.username), quote_plus(configs.db.password),
    "%s:%s" % (configs.db.host, configs.db.port))
client = MongoClient(uri)
db=client[configs.db.db_name]
# db.account_detail.create_index("transaction_hash", unique=True)
# db.exception_trade.create_index("transaction_hash", unique=True)

connect(
    db=configs.db.db_name,
    username=configs.db.username,
    password=configs.db.password,
    host=configs.db.host, port=configs.db.port, authentication_source='admin'
)
