import pymysql
import traceback

def change_status_to_yes(voter_name):
	# create a mysql connection
    db = pymysql.connect("localhost","root","mysql","voting")
    cursor = db.cursor()
	try:
		update_query = "update tbl_voters set status = 'yes' where voter_name = '{}'".format(voter_name)
		cursor.execute(update_query)
		return True
		
	except:
		print("Error while change_status_to_yes after voting")
		traceback.print_exc()
		
	return False