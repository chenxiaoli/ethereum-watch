import sys
import os

path = os.path.dirname(os.path.abspath('.'))
print(path)
sys.path.append(path)
from contract.erc20 import Erc20

if __name__ == '__main__':
    contract_address = "0x08F174f81a5778Ece21C824E3c2eA22C2FBD7886"

    erc20 = Erc20(address=contract_address)
    print(erc20.contact_info)
