# Pacotes
import pymysql
import pymysql.cursors
import datetime
import requests
import random
from bs4 import BeautifulSoup
from time import sleep
from urllib.parse import urlencode

API = 'e60fe216c81498464f99a39613243083'

# Função Proxies

def get_url(http):
    payload = {'api_key':API,'url':http}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


## Conectando ao Banco de Dados

# Parametros para o acesso do banco de dados

db='instagram'
host = 'localhost'
port = 3300
user = 'root'
passwd = '34340012'

# Conectando ao banco de dados
db_conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset='utf8')
db_cur = db_conn.cursor()

## Explorando perfis do instagram
# Empresa Analisada -> Topper
# Empresas Concorrentes -> Nike, Adidas, Puma, Mizuno, Penalty

Empresas = ['topperbrasil','nike','adidas','puma','mizunobr','penaltybr']

for i in Empresas:
    # Obtendo a pagina html
    url = requests.get(get_url("https://www.picuki.com/profile/"+str(i)))
    # Organizando os elementos web
    html = BeautifulSoup(url.content,'html.parser')
    htm1 = html.find('div', {'class': "content box-photos-wrapper"})
    htm2 = htm1.find_all('ul')
    htm3 = htm2[0].find_all('div', {'class': "box-photo"})
    url=[]
    id=[]
    img=[]
    for num in range(len(htm3)):
        link = htm3[num].find('a')
        if link is not None:
            url = link['href']
            id = link['href'].replace('https://www.picuki.com/media/', "")
            img = link.find('img')['src']
        else:
            continue

        post=requests.get(get_url(link['href']))
        bs=BeautifulSoup(post.content,'html.parser')

        likes = bs.find('span', {'class': "icon-thumbs-up-alt"}).text.replace(" likes","")
        comments = bs.find('span',{'class':"icon-chat"}).text.replace(" comments","")
        period = bs.find('div',{'class':"single-photo-time"}).text
        empresa = i
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sql = 'INSERT INTO Instagram_Picuki (Empresa,Id,Post_Url,img,Likes,Comments,Periods,update_time) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'
        # Execute the SQL statement and submit it to the database for execution
        db_cur.execute(sql, (empresa, id, url, img, likes, comments, period, time))
        db_conn.commit()
        print("Insert finished")

