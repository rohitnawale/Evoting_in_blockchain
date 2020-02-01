import mysql.connector
import homomorphic


#returns reference string and betabit for voter
def get_strings(voter_id):
    connection = mysql.connector.connect(host='localhost',
                                         database='voting',
                                         user='root',
                                         password='mysql', auth_plugin='mysql_native_password')
    mySql_select_query = """select homomorphic_sets from voter where voter_id=%s limit 1"""
    cursor = connection.cursor()
    cursor.execute(mySql_select_query, (voter_id,))
    record = cursor.fetchall()
    ref_string = ""
    betabit = ""
    ref_list = []
    set_list = []
    beta_list = []
    for row in record:
        strings = row[0].split(";")
        ref_list.append(list(map(int, strings[0].split(","))))
        beta_list.append(list(map(int, strings[2].split(","))))
        betabit = homomorphic.get_betabit(ref_list[0], strings[1], beta_list[0])
        ref_string = strings[0]
    return ref_string, betabit
