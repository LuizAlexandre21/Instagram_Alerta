import pymysql
import pymysql.cursors
import smtplib, ssl
import pandas as pd
import numpy as np
from email.mime.text import MIMEText


# Conectando a base
db = 'instagram'
host = 'localhost'
port = 3300
user = 'root'
passwd = '34340012'

db_conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset='utf8')

db_cur = db_conn.cursor()

Instagram = pd.read_sql_query('Select * From instagram_picuki',db_conn)


### Criando Metricas - ID, Likes_T, Comments_T, Likes_var, Comments_var

id=np.unique(Instagram['ID'])[1:15]
text=[]
for i in id:
    a=Instagram[Instagram['ID']==i]
    b=a.tail(2).reset_index()
    Likes_var = int(b['Likes'].iloc[[1]]) - int(b['Likes'].iloc[[0]])
    Comments_var =  int(b['Comments'].iloc[[1]]) - int(b['Comments'].iloc[[0]])
    text.append(("ID:{} Likes_var:{} Comments_var:{} \n ").format(i,Likes_var,Comments_var))

mensagem=[""]
for i in range(len(text)):
    mensagem[0]=mensagem[0]+text[i]


# Criando alertas para email
smtp_ssl_host = 'smtp.gmail.com'
smtp_ssl_port = 465
username = "luizalexandremoreira21@gmail.com"
password='20031997l'

from_addr = 'luizalexandremoreira21@gmail.com'
to_addrs = ['Luizalexandre21@outlook.com']


message = MIMEText(mensagem[0])
message['subject'] = 'Alerta'
message['from'] = from_addr
message['to'] = ', '.join(to_addrs)


server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
server.login(username, password)
server.sendmail(from_addr, to_addrs, message.as_string())
server.quit()