import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

def add_candidiate(name, party_name, region):
    connection = mysql.connector.connect(host='localhost',
                                         database='voting',
                                         user='root',
                                         password='mysql',auth_plugin='mysql_native_password')
    mySql_insert_query = """INSERT INTO candidate (name, party_name, region) 
                               VALUES 
                               (%s, %s, %s) """
    recordTuple = (name, party_name, region)
    cursor = connection.cursor()
    cursor.execute(mySql_insert_query,recordTuple)
    connection.commit()
    print(cursor.rowcount, "Record inserted successfully into Laptop table")
    cursor.close()
    connection.close


def get_candidates(region):
    connection = mysql.connector.connect(host='localhost',
                                         database='voting',
                                         user='root',
                                         password='mysql', auth_plugin='mysql_native_password')
    mySql_select_query = "select id,name,party from voting.tbl_candidates where region='{}' order by name asc".format(region)
    cursor = connection.cursor()
    cursor.execute(mySql_select_query)
    record = cursor.fetchall()
    '''
	candidate_list = []
    for row in record:
        ls = []
        ls.append(row[0])
        ls.append(row[1])
        ls.append(row[2])
        candidate_list.append(ls)
        print("Id = ", row[0], )
        #print("Name = ", row[1])
        #print("party_name = ", row[2], "\n")
	'''
    cursor.close()
    connection.close
    return record


#clist = get_candidates("nigdi")
#print(clist)
#print(get_candidates('nigdi'))