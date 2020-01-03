from mongoengine import *
import datetime



class Block(DynamicDocument):
    data = DictField()
    number = LongField(unique=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    transaction_count = LongField()
    read_done=StringField()


class ExceptionBlock(Document):
    data = DictField()
    number = IntField()
    created_at = DateTimeField(default=datetime.datetime.utcnow)


class Transaction(Document):
    data = DictField()
    block_number = IntField()
    transaction_hash = StringField(unique=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    transaction_receipt=DictField()




class ExceptionTransaction(Document):
    data = DictField()
    block_number = IntField()
    transaction_hash = StringField()
    created_at = DateTimeField(default=datetime.datetime.utcnow)


class Account(Document):
    """
    以太坊网络上已经发布了几万种token,把token 列表存放在这里?
    """
    address = StringField(unique=True)
    belong_to = StringField()
    eth_balance = DecimalField()
    block_number = IntField()
    token_balance_list = ListField()

    def update_token_balance(self, balance, token):
        if token:
            db_balance = TokenBalance.objects.get(account=self,token=token)
            db_balance.balance = balance
            db_balance.save()


class Token(Document):
    """
    以太坊 token
    """
    name = StringField("名称")
    symbol = StringField("代号")
    contract_address = StringField("合约地址")
    creator_address = StringField("创建者地址")
    contract_account_balance = DecimalField("合约账户余额")
    total_supply = DecimalField("总供应量")
    decimals = IntField("小数点位数")
    eip = StringField(default="erc20")
    abi = ListField()
    address_count = IntField("持币地址数")
    image_url = StringField()


class TokenBalance(Document):
    """token"""
    token = ReferenceField(Token)
    balance = DecimalField()
    symbol = StringField()
    symbol_contract_address = StringField()
    percent = FloatField("持币占比")
    trade_count = IntField("交易总数")
    block_number = IntField()
    account = ReferenceField(Account)


class AccountDetail(Document):
    from_address = StringField()
    to_address = StringField()
    value = DecimalField()
    symbol = StringField()
    contract_address = StringField()
    block_number = LongField()
    transaction_hash = StringField(unique=True)
    transaction_timestamp = LongField()
    created_at = DateTimeField(default=datetime.datetime.utcnow)

class ExceptionTrade(Document):
    from_address = StringField()
    to_address = StringField()
    value = StringField()
    symbol = StringField()
    symbol_contract_address = StringField()
    block_number = LongField()
    transaction_hash = StringField(unique=True)
    transaction_timestamp = LongField()
    created_at = DateTimeField(default=datetime.datetime.utcnow)
