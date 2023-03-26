import json
import sys
import ssl, socket
import sqlite3

from dateutil import parser

import pika

def ssl_connection(hostname):
    print(hostname, "in the function ")
    soc = ssl.create_default_context()
    with soc.wrap_socket(socket.socket(), server_hostname=hostname) as R:
        R.connect((hostname,443))
        certt = R.getpeercert()
        
        cipher_suit=R.cipher()
        
        db_rec['cipher_suit_name']=hostname

        db_rec['version']=hostname
        db_rec['secret_bits']=hostname
        return certt


connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-server'))
channel = connection.channel()

db_rec={}
hostname="www.google.com"   
print(hostname)
certt= ssl_connection(hostname) # This function get the details of SSL Certificate given by the user
subject = dict(x[0] for x in certt['subject'])

db_rec['subject_common_name']=subject['commonName']

r=parser.parse(certt['notAfter']).strftime("%A ,%d %B %Y")

db_rec['cert_expiry_date']=r
print(db_rec,"printing the value of db_rec")

json_data= json.dumps(db_rec)

channel.queue_declare(json_data, durable=True)
channel.basic_publish(exchange='', routing_key='hello', body=json_data)
print(" [x] Sent !!! this message to receiver",json_data)

connection.close()