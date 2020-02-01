import traceback
import pymysql
import hashlib
import base64
import Module_aes_encryption
def decrypt_sets(voter_name):
    # create a mysql connection
    db = pymysql.connect("localhost","root","mysql","voting")
    cursor = db.cursor()
    try:
        select_query = "select password, homomorphic_sets from tbl_voters where voter_name = '{}'".format(voter_name)
        cursor.execute(select_query)
        result = cursor.fetchall()
        db.commit()
    except:
        print("Error while fetching password for encryption")
        traceback.print_exc()
        
    # Let us decrypt using our original password
    #print(result)
    encrypted_sets = result[0][1][2:]
    decrypted_sets = str(Module_aes_encryption.decrypt(encrypted_sets, result[0][0]))
    return(decrypted_sets[2:len(decrypted_sets)-1])
    
print(decrypt_sets('thirteen'))