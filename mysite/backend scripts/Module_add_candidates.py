''''
This module accepts details from front end to add new candidates along with its attributes on blockchain.
Smart contracts are deployed on remix.ethereum.com/Election.sol
'''
from web3 import Web3
import json
import pymysql
import traceback
import hashlib

def add_new_candidates_on_blockchain(candidate_name, party_name, region):
	ganache_url = "http://127.0.0.1:7545"
	#connect to local private blockchain on ganache
	web3 = Web3(Web3.HTTPProvider(ganache_url))

	print(web3.isConnected())
	
	if web3.isConnected():
		# load the json data which can be obtained after deploying smart contracts
		abi = json.loads()
	