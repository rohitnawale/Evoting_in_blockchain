'''
This module checks if the queried voter is registered on blockchain or not.



'''
from web3 import Web3
import json
import traceback
import pymysql
import hashlib

def get_hash_from_database_query(voter_id):
    # create a mysql connection
    db = pymysql.connect("localhost","root","mysql","voting")
    cursor = db.cursor()
    try:
        query = "select voter_id, voter_name, password, age, region, email from tbl_voters where voter_id = {}".format(voter_id)
        cursor.execute(query)
        result = cursor.fetchall()
    except:
        traceback.print_exc()
    
    details_string = ''     
    for element in result:
        details_string += str(element) + ", "
    details_string = details_string.replace("(", "")
    details_string = details_string.replace(")", "")
    details_string = details_string[:-2]
    #print(details_string)
    #details_string = str(voter_id) + voter_name + password + str(age) + region + email
    hashed_string =  str(hashlib.sha256(str(details_string).encode('utf-8')).hexdigest())
    return hashed_string


def is_voter_on_blockchain(voter_id):
    ganache_url = "http://127.0.0.1:7545"
    #connect to local private blockchain on ganache 
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    #print(web3.isConnected())
    if web3.isConnected():
        abi = json.loads('[{"constant":false,"inputs":[{"name":"_voterID","type":"uint256"},{"name":"_details","type":"string"}],"name":"addCastedDetailsHash","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getVoterCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_voterID","type":"uint256"},{"name":"_voterDetails","type":"string"}],"name":"addVoter","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"votersCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_voterID","type":"uint256"}],"name":"getVoter","outputs":[{"name":"","type":"uint256"},{"name":"","type":"string"},{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"voters","outputs":[{"name":"voterID","type":"uint256"},{"name":"voterDetailsHashed","type":"string"},{"name":"voteCastedDetailsHash","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}]')

        # load the address where smart contracts are deployed
        address = web3.toChecksumAddress('0x8C0AAe119A1143b5244Aa67f8e74E214F6f10cd0')


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