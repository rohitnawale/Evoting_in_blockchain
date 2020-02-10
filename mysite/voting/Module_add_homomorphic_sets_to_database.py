import traceback
import pymysql
import hashlib
import web3
from . import Module_aes_encryption
def add_sets_to_database(homomorphic_sets, voter_name):
    # create a mysql connection
    db = pymysql.connect("localhost","root","mysql","voting")
    cursor = db.cursor()
    try:
        select_query = "select password from tbl_voters where voter_name = '{}'".format(voter_name)
        cursor.execute(select_query)
        password = cursor.fetchall()
        db.commit()
    except:
        print("Error while fetching password for encryption")
        traceback.print_exc()
    encrypted_sets = Module_aes_encryption.encrypt(homomorphic_sets, password[0][0])
    insert_query = 'update tbl_voters set homomorphic_sets = "{}" where voter_name = "{}"'.format(encrypted_sets, voter_name)
    try:
        cursor.execute(insert_query)
        db.commit()
        cursor.close()
        return True
    except:
        print("Error while inserting new voter data to local DB")
        traceback.print_exc()
        return False
        
def add_sets_to_blockchain(homomorphic_sets, voter_name):
    # create a mysql connection
    db = pymysql.connect("localhost","root","mysql","voting")
    cursor = db.cursor()
    query = "select voter_id from tbl_voters where voter_name = '{}'".format(voter_name)
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        db.commit()
        cursor.close()
    except:
        print("Error while inserting new voter data to local DB")
        traceback.print_exc()
    voter_id = result[0][0]
    hashed_string = str(hashlib.sha256(str(homomorphic_sets).encode()).hexdigest())
    
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
            # create a transaction on blockchain to add the new voter details using the private key
            tx_hash = contract.functions.addCastedDetailsHash(voter_id, hashed_string).transact({'from':'0x2c08A59BB7989dFea6d9366552bC7E233a2dbD21', 'gas': 3400000})
            #tx_hash = contract.functions.addVoter(voter_name, age, region).transact({'from':'0x2c08A59BB7989dFea6d9366552bC7E233a2dbD21', 'gas': 3400000})
            
            # wait for the block to be  mined on blockchain
            web3.eth.waitForTransactionReceipt(tx_hash)
            return True

        except:
            traceback.print_exc()