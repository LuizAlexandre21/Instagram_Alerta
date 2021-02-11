import requests
from bs4 import BeautifulSoup
import pymysql
import pymysql.cursors
import datetime
from time import sleep
import random

## Conectando no Banco de Dados

db = 'instagram'
host = 'localhost'
port = 3300
user = 'root'
passwd = '34340012'

db_conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset='utf8')

db_cur = db_conn.cursor()

# Explorando o perfil da CRC
# Importando o html da pagina
sleep(random.randint(0,30))
url=requests.get("https://www.picuki.com/profile/centralcrc_")
# Organizando o html
html = BeautifulSoup(url.content,'html.parser')

#### Dissecando os posts
htm1=html.find('div',{'class':"content box-photos-wrapper"})
htm2=htm1.find_all('ul')
htm3=htm2[0].find_all('div',{'class':"box-photo"})
htm4=[]
htm4_1=[]
htm5=[]
htm6=[]
for i in range(len(htm3)):
    link=htm3[i].find('a')
    if link is not None:
        url=link['href']
        id=link['href'].replace('https://www.picuki.com/media/',"")
    else:
        continue
    like=htm3[i].find('div',{'class':"likes_photo"})
    if like is not None:
        curtida=like.text.replace("\n","").replace(" ","")
    else:
        continue
    comment = htm3[i].find('div',{'class':"comments_photo"})
    if comment is not None:
        comentarios=comment.text.replace("\n","").replace(" ","")
    else:
        continue

    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# Salvando as informações no Banco de Dados
    sql = 'INSERT INTO Instagram_Picuki (Id,Post_Url,Likes,Comments,update_time) VALUES(%s,%s,%s,%s,%s)'
    # Execute the SQL statement and submit it to the database for execution
    db_cur.execute(sql, (id,url,curtida,comentarios,time))
    db_conn.commit()
    print("Insert finished")

