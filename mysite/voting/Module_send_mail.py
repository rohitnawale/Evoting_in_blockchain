
import smtplib
from numpy.random import randint
import hashlib
from . import Module_aes_encryption
import traceback
import pymysql


def check_email(email):
    # create a mysql connection
    db = pymysql.connect("localhost","root","mysql","voting")
    cursor = db.cursor()
    try:
        select_query = "select voter_name from tbl_voters where email = '{}'".format(email)
        cursor.execute(select_query)
        result = cursor.fetchall()
    except:
        print("Error while updating status in database after voting")
        traceback.print_exc()
        
    if len(result)>0:
        return True
    else:
        return False

def Mail_Sender(receipent,gmail_user, gmail_password):
    sent_from = gmail_user
    to = [receipent]
    subject = 'Message From Election Commission of India'
    otp = randint(100000,999999)
    email_text ='''Welcome from Election Commission Of India
    Your OTP is: %d\n\n\n
    This is a system generated mail. Do not Reply.
                '''%(otp)

    message = 'Subject: {}\n\n{}'.format(subject,email_text)
                 

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com',465)
        server.ehlo()
        server.login(gmail_user,gmail_password)
        server.sendmail(sent_from,to,message)
        server.close()

        print("EMAIL SENT")

    except Exception as E:
        print("Unable to send mail.", E)

    return otp

    
def changePassword(email,new_Pass):

    new_password = str(hashlib.sha256(str(new_Pass).encode()).hexdigest())
    print('Hashed Password: ',new_password)

     # create a mysql connection
    db = pymysql.connect("localhost","root","mysql","voting")
    cursor = db.cursor()
    try:
        select_query = "select password, homomorphic_sets from tbl_voters where email = '{}'".format(email)
        cursor.execute(select_query)
        result = cursor.fetchall()
        db.commit()
    except:
        print("Error while fetching password for encryption")
        traceback.print_exc()
        
    # Let us decrypt using our original password

    encrypted_sets = result[0][1][2:]
    decrypted_sets = str(Module_aes_encryption.decrypt(encrypted_sets, result[0][0]))
    
    # Encrypting using new password
    encrypted_sets = Module_aes_encryption.encrypt(decrypted_sets, new_password)
    

    try:
        update_query = "update tbl_voters set password = '{}', homomorphic_sets = '{}' where email = '{}'".format(new_password,encrypted_sets,email)
        cursor.execute(select_query)
        result = cursor.fetchall()
        db.commit()
        return True
    except:
        print("Error while fetching password for encryption")
        traceback.print_exc()
        return False
