''''
This module accepts details from front end to add new voter along with its attributes on blockchain.
Smart contracts are deployed on remix.ethereum.com/Election.sol
'''
from web3 import Web3
import json
import pymysql
import traceback
import hashlib

def add_new_voter_to_database(voter_id, voter_name, password, age, region, email):
	# create a mysql connection
	db = pymysql.connect("localhost","root","mysql","voting")
	cursor = db.cursor()
	#hash the password
	password = str(hashlib.sha256(str(password).encode()).hexdigest())
	#print(password)
	# insert the details fetched from blockchain to local database in mysql table
	insert_query = "replace into tbl_voters(voter_id, voter_name, password, age, region, email) values( {},'{}','{}',{},'{}','{}' )".format(voter_id, voter_name, password, age, region, email)
	#print(insert_query)
	try:
		cursor.execute(insert_query)
		db.commit()
	except:
		print("Error while inserting new voter data to local DB")
		traceback.print_exc()
		
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

def add_new_voter_to_blockchain(voter_id, voter_name, password, age, region, email):

	hashed_string = "0x" + str(add_new_voter_to_database(voter_id, voter_name, password, age, region, email))
	print(hashed_string)
	ganache_url = "http://127.0.0.1:7545"
	#connect to local private blockchain on ganache
	web3 = Web3(Web3.HTTPProvider(ganache_url))

	#print(web3.isConnected())
	
	if web3.isConnected():
		# load the json data which can be obtained after deploying smart contracts
		abi = json.loads(' [{"constant":false,"inputs":[{"name":"_voterID","type":"uint256"},{"name":"_details","type":"string"}],"name":"addCastedDetailsHash","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getVoterCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_voterID","type":"uint256"},{"name":"_voterDetails","type":"string"}],"name":"addVoter","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"votersCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_voterID","type":"uint256"}],"name":"getVoter","outputs":[{"name":"","type":"uint256"},{"name":"","type":"string"},{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"voters","outputs":[{"name":"voterID","type":"uint256"},{"name":"voterDetailsHashed","type":"string"},{"name":"voteCastedDetailsHash","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}]')

		# load the address where smart contracts are deployed
		address = web3.toChecksumAddress('0x11f7bA2ed968E14aa2228e746c56e9D2851A0bCE')

		# establish the connection with blockchain using address and ABI
		contract = web3.eth.contract(address=address, abi = abi)
		
		# create a transaction on blockchain to add the new voter details using the private key
		tx_hash = contract.functions.addVoter(voter_id, hashed_string).transact({'from':'0x2c08A59BB7989dFea6d9366552bC7E233a2dbD21', 'gas': 3400000})
		#tx_hash = contract.functions.addVoter(voter_name, age, region).transact({'from':'0x2c08A59BB7989dFea6d9366552bC7E233a2dbD21', 'gas': 3400000})
		
		# wait for the block to be  mined on blockchain
		web3.eth.waitForTransactionReceipt(tx_hash)

		# get the total number of voters on blockchain
		total_voters = contract.functions.getVoterCount().call()
		print(total_voters)
		#for i in range(total_voters):
		current_voter = contract.functions.getVoter(int(voter_id)).call()
		#print(current_voter)
		#for i in current_voter:
		print(current_voter[0])
		print(current_voter[1])
		#voterDetailsHashed = current_voter[1].hex().rstrip("0x")
		#print(bytes.fromhex(str(voterDetailsHashed)).decode('utf-8'))
		# print(str(current_voter[2][2:], "utf-8"))
		
			
				
#print(add_new_voter_to_database(13, "thirteen", "13", 25, "nigdi", "demo@gmail.com"))
add_new_voter_to_blockchain(13, "thirteen", "13", 25, "nigdi", "demo@gmail.com")