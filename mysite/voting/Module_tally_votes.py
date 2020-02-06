import mysql.connector
from . import homomorphic
from . import Module_get_candidate
from . import Module_aes_encryption


#extracts the ref,set and beta strings of all voters in that region and returns the vote count
def tally_votes(regions):
    region_results = {}
    connection = mysql.connector.connect(host='localhost',
                                         database='voting',
                                         user='root',
                                         password='mysql', auth_plugin='mysql_native_password')
    for region in regions:
        mySql_select_query = """select password, homomorphic_sets from tbl_voters where region=%s"""
        cursor = connection.cursor()
        cursor.execute(mySql_select_query, (region,))
        record = cursor.fetchall()
        ref_list = []
        set_list = []
        beta_list = []
        # print(record)
        for row in record:
            # print(row)
            encrypted_sets = str(row[1][2:])
            row = str(Module_aes_encryption.decrypt(encrypted_sets, row[0])).replace("'","").replace("b","")
            strings = row.split(";")
            # print("strings", strings)
            ref_list.append(list(map(int,strings[0].split(","))))
            set_list.append(list(strings[1].split(",")))
            beta_list.append(list(map(int,strings[2].split(", "))))
            # print("ref = ", strings[0])
            # print("set = ", strings[1])
            # print("beta = ", strings[2], "\n")
        cursor.close()

        vote_count = homomorphic.decrypt(ref_list, set_list, beta_list)
        region_results.update({region:vote_count})
    connection.close
    # print(region_results)
    return region_results


def get_regions():
    regions = []
    connection = mysql.connector.connect(host='localhost',
                                         database='voting',
                                         user='root',
                                         password='mysql', auth_plugin='mysql_native_password')
    mySql_select_query = """select distinct region from tbl_voters"""
    cursor = connection.cursor()
    cursor.execute(mySql_select_query)
    record = cursor.fetchall()
    for row in record:
        regions.append(row[0])
    print(regions)
    return regions


def get_results(region_results):
    winner_record = {}
    # print("region_results")
    # print(region_results)
    for region, votes in region_results.items():
        record = Module_get_candidate.get_candidates(region)
        # print("record")
        # print(record)
        candidate_list = []
        for row in record:
            ls = []
            ls.append(row[0])
            ls.append(row[1])
            ls.append(row[2])
            candidate_list.append(ls)
        winner_index = votes.index(max(votes))
        # print("***")
        # print(winner_index)
        # print(candidate_list)
        winner_record.update({region:candidate_list[winner_index]})
    # print("winner_record")
    # print(winner_record)
    return winner_record


# r = get_regions()
# c = tally_votes(r)
# get_results(c)

