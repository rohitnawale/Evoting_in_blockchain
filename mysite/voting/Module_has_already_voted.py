import pymysql
import traceback
import hashlib

def has_already_voted(username):
    # create a mysql connection
    db = pymysql.connect("localhost","root","mysql","voting")
    cursor = db.cursor()
    try:
        select_query = "select status from tbl_voters where voter_name = '{}'".format(username)
        cursor.execute(select_query)
        result = cursor.fetchall()
        print(result[0][0])
        if(result[0][0] == "yes"):
            return True
        else:
            return False
    except:
        print("Error while checking status")
        traceback.print_exc()
        return True
        
#print(has_already_voted("eleven"))