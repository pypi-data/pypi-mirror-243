import os

import requests
from requests.auth import HTTPBasicAuth


def read_cookie(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    user, password = content.split(':')
    return user, password


class BitcoinRPC:
    
    def __init__(self, network='main', cookie_path=None, url=None, port=None):
        # print(f"BitcoinRPC.__init__({network=}, {cookie_path=}, {url=}, {port=}")
        if port:
            self.network = 'custom'
        else:
            self.network = network
        
        match network:
            case 'main':
                self.port = '8332'
            case 'testnet':
                self.port = '18332'
            case 'regtest':
                self.port = '18443'
            case 'signet':
                self.port = '38332'
            case 'custom':
                self.port = port
            case _:
                raise ValueError('Wrong port value')
        
        if url:
            if url.startswith('http://'):
                self.url = url
            else:
                self.url = 'http://' + url
        else:
            self.url = 'http://localhost'
        
        if cookie_path:
            self.cookie_path = cookie_path
        else:
            root = os.path.expanduser('~')
            if self.network == 'main':
                self.cookie_path = os.path.join(root, '.bitcoin', '.cookie')
            elif self.network in ['testnet', 'regtest', 'signet']:
                self.cookie_path = os.path.join(root, '.bitcoin', self.network, '.cookie')
            else:
                raise (ValueError('cookie_path might be specified for custom network'))
        
        self.user, self.password = read_cookie(self.cookie_path)
    
    def request(self, method: str, params: [] = [], wallet: str = None):
        url = f"{self.url}:{self.port}"
        if wallet:
            url += f"/wallet/{wallet}"
        
        payload = {
            "jsonrpc": "1.0",
            "id": "rpcclient",
            "method": method,
            "params": params,
        }
        
        ret = requests.post(url, json=payload, auth=HTTPBasicAuth(self.user, self.password))
        # print(ret.text)
        try:
            if 'result' in ret.json().keys():
                return ret.json()['result']
            else:
                return ret.text
        except:
            return ret
        

# rpc = BitcoinRPC('signet')
#
# print(rpc.request('createwallet', ['liana', True]))
# param = [{"desc": "wsh(or_d(pk([a5c6b76e/48'/1'/0'/2']tpubDF5861hj6vR3iJr3aPjGJz4rNbqDCRujQ21mczzKT5SiedaQqNVgHC8HT9ceyxvMFRoPMx4P6HAcL3NZrUPhRUbwCyj3TKSa64bAfnE3sLh/1/*),and_v(v:pkh([c477fd13/48'/1'/0'/2']tpubDFn7iPbFqGrTQ2aRACNsUK1MXQR4Z6dYfU2nD1WA9ifSaia642j3Wah4n5pBUEpERNWGJsyv3Dv5qwBabC9TLQrwSboKzukw9wmurGu7XVH/1/*),older(3))))#vpa5k5p6",
#           "range": [0, 10000],
#           "timestamp": 1682920310,
#           "active": True,
#           "internal":False}]
# print(rpc.request('importdescriptors', [param], wallet='liana'))
# print(rpc.request('listdescriptors', wallet='liana'))
#
# print(rpc.request('listunspent', wallet='joinstr'))
