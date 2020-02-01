from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
import random
import pymysql
from django.views.decorators.csrf import csrf_exempt
import traceback
import hashlib
from . import Module_get_voterdata_from_blockchain
from . import Module_get_candidate
from . import homomorphic
from . import Module_add_homomorphic_sets_to_database

# Create your views here.
@csrf_exempt
def index (request):
	
	# extract the username, client_random_number_hash and combined hash from the request
	username = request.POST.get('username')
	password = request.POST.get('hash_all')
	client_random_number_hash = str(request.POST.get('client_random_number_hash'))
	# if it is the first time visitng the page i.e. not a login request then generate a random number and write it in a temporary file
	if username == None:
		key = int(random.uniform(0,100000))
		fh = open('serverkey.txt', 'w')
		fh.write(str(key))
	# if it is a login request
	if username != None:
		# create a mysql connection
		print(username, password, client_random_number_hash)
		db = pymysql.connect("localhost","root","mysql","voting")
		cursor = db.cursor()
		# fetch the password from mysql
		query = 'select password, voter_id from voting.tbl_voters where voter_name = "{}"'.format(username)
		try:
			cursor.execute(query)
			result = cursor.fetchall()
		except:
			traceback.print_exc()
			
		# get the hashed password from db
		hash_from_db = str(result[0][0])
		voter_id = result[0][1]
		
		#hash of the server_key
		fh = open('serverkey.txt', 'r')
		key = fh.read()
		server_key_hash = str(hashlib.sha256(str(key).encode()).hexdigest())
		
		#generate the combined hash of hashed server_key, hashed client_key and hashed password
		h = str(hash_from_db+server_key_hash+client_random_number_hash).encode('utf8')
		hash_all = (hashlib.sha256(h)).hexdigest()
		# if the combined hash generated here and extracted from request is matched, then details are correct and redirect user to next page
		# or else send an error message
		if hash_all == password:
			print('correct password')
			if Module_get_voterdata_from_blockchain.is_voter_on_blockchain(voter_id):
				print('redirecting to next page')
				#return HttpResponse(json.dumps(response_data), content_type="application/json")
				return render(request,'voting/instructions.html', {'username':username})
			else:
				return render(request, 'voting/index.html', {'message':'Voter is not registered on blockchain'})
		else:
			print('wrong password')
			return render(request, 'voting/index.html', {'message':'Password is wrong'})
	return render(request, 'voting/index.html', {'key':key})

def instructions(request):
	# username = request.POST.get('username')
	# password = request.POST.get('hash_all')
	# client_random_number_hash = request.POST.get('client_random_number_hash')
	# print(username, password, client_random_number_hash)
	username = request.GET.get('username')
	if username != None:
		return render(request, 'voting/instructions.html')
	else:
		return index(request)
	
def cast_vote(request):
	username = request.GET.get('username')
	
	if request.method == "POST":
		ref_string = request.POST.get('ref_string')
		set_selected = request.POST.get('set_selected')
		candidate_id = request.POST.get('candidate_id')
		candidate_index = request.POST.get('candidate_index')
		username = request.POST.get('username')
		print(list(map(int, ref_string.split(","))), set_selected, int(candidate_id), "fjkdfvhkjfd",int(candidate_index))
		beta_string = homomorphic.encrypt(list(map(int, ref_string.split(","))), set_selected, int(candidate_index))
		homomorphic_sets = str(ref_string) + ";" + str(set_selected) + ";"+ str(beta_string)
		Module_add_homomorphic_sets_to_database.add_sets_to_database(str(homomorphic_sets).replace("[", "").replace("]",""), username)
		#if Module_add_homomorphic_sets_to_database.add_sets_to_blockchain(str(homomorphic_sets).replace("[", "").replace("]",""), username):
		return render(request, 'voting/done.html', {'ref_string': ref_string, 'set':set_selected, 'beta_string':beta_string, 'username':username})
	else:
		if str(username) != "None":
			result = Module_get_candidate.get_candidates('nigdi')
			total_candidate_count = len(result)
			ref_string = homomorphic.create_ref(total_candidate_count)
			set_selected = homomorphic.select_set()
			combined_set = zip(ref_string, result)
			print(combined_set)
			return render(request, 'voting/castVote.html', {'result': result, 'combined_set': combined_set, 'set_selected': set_selected, 'ref_string': ref_string, 'username':username})
		else:
			key = int(random.uniform(0,100000))
			fh = open('serverkey.txt', 'w')
			fh.write(str(key))
			return render(request, 'voting/index.html', {'key':key})

		
def done(request):
	username = request.GET.get('username')
	if str(username) != "None":
		return render(request, 'voting/done.html', {'username':username})
	else:
		key = int(random.uniform(0,100000))
		fh = open('serverkey.txt', 'w')
		fh.write(str(key))
		return render(request, 'voting/index.html', {'key':key})