'''
This module fetches the details of all the voters on blockchain



'''
from web3 import Web3
import json
import traceback
import pymysql
import hashlib


def get_data_from_blockchain():
    ganache_url = "http://127.0.0.1:8545"
    #connect to local private blockchain on ganache 
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    #print(web3.isConnected())
    if web3.isConnected():
        # load the json data which can be obtained after deploying smart contracts
        abi = json.loads(' [{"constant":false,"inputs":[{"name":"_voterID","type":"uint256"},{"name":"_details","type":"string"}],"name":"addCastedDetailsHash","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getVoterCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_voterID","type":"uint256"},{"name":"_voterDetails","type":"string"}],"name":"addVoter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"votersCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_voterID","type":"uint256"}],"name":"getVoter","outputs":[{"name":"","type":"uint256"},{"name":"","type":"string"},{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"voters","outputs":[{"name":"voterID","type":"uint256"},{"name":"voterDetailsHashed","type":"string"},{"name":"voteCastedDetailsHash","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}]')

        # load the address where smart contracts are deployed
        address = web3.toChecksumAddress('0x8A707F18f249CfE5D15bEb10e0c34CcEC2785C86')


        # establish the connection with blockchain using address and ABI
        contract = web3.eth.contract(address=address, abi = abi)
        #print(contract)
        # get the total number of voters on blockchain
        total_voters = contract.functions.getVoterCount().call()
        print(total_voters)
        # for i in range(total_voters):
        current_voter = contract.functions.getVoter(15).call()
        print(current_voter)
        #for i in current_voter:
        # print(current_voter[0])
        # print(current_voter[1])
        #print(voter_details)
        
    
    
get_data_from_blockchain()