from web3 import Web3
import json
import pymysql
import traceback
import hashlib

def update_user_on_blockchain(voter_id):
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
        # get voter details from blockchain based on voter_id
        try:
            voter_details = contract.functions.getVoter(voter_id).call()
        except:
            traceback.print_exc()
        
        #print(voter_details)
        # if voter exists on blockchain and details are correct then return True otherwise False
        print("voter_details", voter_details[1][2:])
        print("from database", get_hash_from_database_query(voter_id))
        if str(voter_details[1])[2:] == get_hash_from_database_query(voter_id):
            return True
        else:
            return False
    return False
    
    
#print(is_voter_on_blockchain(14))