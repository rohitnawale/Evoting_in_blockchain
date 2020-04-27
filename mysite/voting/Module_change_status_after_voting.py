from web3 import Web3
import json
import pymysql
import traceback
import hashlib

def change_status_to_yes_sql(voter_name):
    # create a mysql connection
    print("Changing status to yes after voting")
    db = pymysql.connect("localhost","root","mysql","voting")
    cursor = db.cursor()
    try:
        update_query = "update tbl_voters set status = 'yes' where voter_name = '{}'".format(voter_name)
        cursor.execute(update_query)
        db.commit()
        cursor.close()
        return True
        
    except:
        print("Error while change_status_to_yes after voting")
        traceback.print_exc()
        
    return False
    
def change_status_to_yes_blockchain(voter_name, encrypted_sets):
    # create a mysql connection
    db = pymysql.connect("localhost","root","mysql","voting")
    cursor = db.cursor()
    try:
        select_query = "select voter_id from tbl_voters where voter_name = '{}'".format(voter_name)
        cursor.execute(select_query)
        result = cursor.fetchall()
    except:
        print("Error while updating status in database after voting")
        traceback.print_exc()
        
    voter_id = int(result[0][0])
    
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
        
        #unlock the geth account to create transaction
        try:
            web3.geth.personal.unlockAccount(web3.toChecksumAddress("0x74a625b67a5acd0d1b44e3185e65b9d9835925a3"), "s492")
            web3.geth.personal.unlockAccount(web3.toChecksumAddress("0x63ce142723bf1cd4205708cfb329b44bd4783452"), "s492")
        except:
            print("Error while unlocking geth account")
            traceback.print_exc()
            return False
        # create a transaction on blockchain to add the new voter details using the private key
        try:
            tx_hash = contract.functions.addCastedDetailsHash(int(voter_id), encrypted_sets).transact({'from':web3.toChecksumAddress('0x74a625b67a5acd0d1b44e3185e65b9d9835925a3'), 'gas': 3400000})
            
        except:
            print("Error while creating transaction")
            traceback.print_exc()
            return False
        #tx_hash = contract.functions.addVoter(voter_name, age, region).transact({'from':'0x2c08A59BB7989dFea6d9366552bC7E233a2dbD21', 'gas': 3400000})
        
        # wait for the block to be  mined on blockchain
        #web3.eth.waitForTransactionReceipt(tx_hash)
        
        # Change the status to yes in mysql database too
        change_status_to_yes_sql(voter_name)
        
        return True
    
    else:
        return False
    
    return False
