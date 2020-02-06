import mysql.connector
from . import homomorphic


#extracts the ref,set and beta strings of all voters in that region and returns the vote count
def tally_votes(regions):
    region_results = {}
    connection = mysql.connector.connect(host='localhost',
                                         database='voting',
                                         user='root',
                                         password='mysql', auth_plugin='mysql_native_password')
    for region in regions:
        mySql_select_query = """select homomorphic_sets from voter where region=%s"""
        cursor = connection.cursor()
        cursor.execute(mySql_select_query, (region,))
        record = cursor.fetchall()
        ref_list = []
        set_list = []
        beta_list = []
        for row in record:
            strings = row[0].split(";")
            ref_list.append(list(map(int,strings[0].split(","))))
            set_list.append(list(strings[1].split(",")))
            beta_list.append(list(map(int,strings[2].split(","))))
            print("ref = ", strings[0])
            print("set = ", strings[1])
            print("beta = ", strings[2], "\n")
        cursor.close()

        vote_count = homomorphic.decrypt(ref_list, set_list, beta_list)
        region_results.update({region:vote_count})
    connection.close
    print(region_results)
    return region_results


def get_regions():
    regions = []
    connection = mysql.connector.connect(host='localhost',
                                         database='voting',
                                         user='root',
                                         password='mysql', auth_plugin='mysql_native_password')
    mySql_select_query = """select distinct region from voter"""
    cursor = connection.cursor()
    cursor.execute(mySql_select_query)
    record = cursor.fetchall()
    for row in record:
        regions.append(row[0])
    print(regions)
    return regions



#r = get_regions()
#tally_votes(r)