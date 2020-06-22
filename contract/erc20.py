import json
from web3_config.web3_instance import get_web3_instance
from contract.constants import ERC20_ABI_JSON_STRING


class Erc20(object):
    abi = None
    name = None
    symbol = None
    decimals = None

    def __init__(self, address):
        abi = json.loads(ERC20_ABI_JSON_STRING)
        w3 = get_web3_instance()
        self.contract = w3.eth.contract(address=address, abi=abi)

    @property
    def contract_info(self):
        _symbol = self.contract.functions.symbol().call()
        _name = self.contract.functions.name().call()
        _decimals = self.contract.functions.decimals().call()
        _total_supply = self.contract.functions.totalSupply().call()
        try:
            d = int(_decimals)
            return {
                "symbol": _symbol,
                "name": _name,
                "decimals": d,
                "totalSupply": str(_total_supply)
            }
        except ValueError:
            return {}

    def balance_of(self, address):
        raise NotImplemented
