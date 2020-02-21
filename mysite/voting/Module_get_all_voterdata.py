''''
This module accepts details from front end to add new voter along with its attributes on blockchain.
Smart contracts are deployed on remix.ethereum.com/Election.sol
'''
from web3 import Web3
import json
import pymysql
import traceback
import hashlib

def get_voters_from_blockchain():
    ganache_url = "http://127.0.0.1:8545"
    #connect to local private blockchain on ganache
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    print(web3.isConnected())
    
    if web3.isConnected():
        # load the json data which can be obtained after deploying smart contracts
        abi = json.loads(' [{"constant":false,"inputs":[{"name":"_voterID","type":"uint256"},{"name":"_details","type":"string"}],"name":"addCastedDetailsHash","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getVoterCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_voterID","type":"uint256"},{"name":"_voterDetails","type":"string"}],"name":"addVoter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"votersCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_voterID","type":"uint256"}],"name":"getVoter","outputs":[{"name":"","type":"uint256"},{"name":"","type":"string"},{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"voters","outputs":[{"name":"voterID","type":"uint256"},{"name":"voterDetailsHashed","type":"string"},{"name":"voteCastedDetailsHash","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}]')

        # load the address where smart contracts are deployed
        address = web3.toChecksumAddress('0x8A707F18f249CfE5D15bEb10e0c34CcEC2785C86')

        # establish the connection with blockchain using address and ABI
        contract = web3.eth.contract(address=address, abi = abi)
        
        
        # get the total number of voters on blockchain
        total_voters = contract.functions.getVoterCount().call()

        for i in range(total_voters):
            current_voter = contract.functions.getVoter(i).call()
            print(current_voter)
            
            
                
#get_voters_from_blockchain()