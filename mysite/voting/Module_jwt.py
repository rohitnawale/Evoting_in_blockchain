import jwt
import pymysql
import traceback

def add_token_to_db(username, token):
    # create a mysql connection
    db = pymysql.connect("localhost","root","mysql","voting")
    cursor = db.cursor()
    try:
        update_query = 'update tbl_voters set token = "{}" where voter_name = "{}"'.format(token, username)
        print(update_query)
        cursor.execute(update_query)
        db.commit()
        return True
    except:
        print("Error while updating status in database after login")
        traceback.print_exc()
        return False
        

def remove_token_from_db(username): 
    db = pymysql.connect("localhost","root","mysql","voting")
    cursor = db.cursor()
    try:
        update_query = 'update tbl_voters set token = "None" where voter_name = "{}"'.format(username)
        print(update_query)
        cursor.execute(update_query)
        db.commit()
        return True
    except:
        print("Error while updating status in database after logout")
        traceback.print_exc()
        return False       
        
def validate_token(username, token):
    # print(username, token)
    # create a mysql connection
    db = pymysql.connect("localhost","root","mysql","voting")
    cursor = db.cursor()
    try:
        select_query = 'select token from tbl_voters where voter_name = "{}"'.format(username)
        # print(update_query)
        cursor.execute(select_query)
        result = cursor.fetchall()
        # print("result", result[0][0])
        if(token == result[0][0]):
            print("valid token")
            return True
    except:
        print("Error while updating status in database after login")
        traceback.print_exc()
        return False
#jwt_token = {'token': jwt.encode({'id':'thirteen'}, "SECRET_KEY")}
#add_token_to_db('thirteen', jwt_token.get('token'))
#remove_token_from_db('thirteen')