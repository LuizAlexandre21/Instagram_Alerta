import pymysql
import pymysql.cursors
import smtplib, ssl
import pandas as pd
import numpy as np
from email.mime.text import MIMEText
import datetime

## Conectando ao Banco de Dados

db = 'instagram'
host = 'localhost'
port = 3300
user = 'root'
passwd = '34340012'

db_conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset='utf8')

db_cur = db_conn.cursor()

Instagram = pd.read_sql_query('Select * From instagram_picuki',db_conn).sort_values(by=['Empresa', 'update_time'])

## Ajustando o painel - Topper - 1 , Demais  - 0

Instagram['Concorrente']=pd.get_dummies(Instagram['Empresa'])['topperbrasil']

likes=[]
comments=[]
for firm in np.unique(Instagram['Empresa']):
    Insta = Instagram[Instagram['Empresa']==firm]
    id=np.unique(Insta['ID'])
    for i in id:
        ID = Insta[Insta['ID']==i]
        if len(ID) > 1:
            for j in ID['Likes'].pct_change():
                likes.append(j)
            for k in ID['Comments'].pct_change():
                comments.append(k)
        else:
            likes.append(0)
            comments.append(0)

Instagram['Likes_var'] = likes
Instagram['Comments_var'] = comments
Instagram = Instagram.replace(np.nan,0)

#           Alertas

# Configurando o cliente de email
smtp_ssl_host = 'smtp.gmail.com'
smtp_ssl_port = 465
username = "email"
password='senha'

from_addr = 'email'
to_addrs = ['Luizalexandre21@outlook.com']


# 1- Alerta :Inicio do dia
# 2- Alerta :Fim do dia
# 3- Alerta :Variação de 15% - Comentarios e Likes




Cliente=Instagram[Instagram['Concorrente']==1].sort_values(by=['update_time'])[0:4]


curtidas=[]
comentarios=[]

for i in np.unique(Instagram['Empresa']):
    firma = Instagram[Instagram['Empresa']==i]
    id = np.unique(firma['ID'].head(4))
    for j in id:
        data=firma[firma['ID']==j].tail(1).reset_index()
        if float(data['Likes_var']) >=0.15:
            curtidas.append(data)
        elif float(data['Comments_var']) >=0.15:
            comentarios.append(data)


# Criando alertas




if datetime.datetime.now().strftime("%H:%M:%S") == "08:00:00":
    Mensagem = " Bom dia {} ! O comportamento da sua conta no instagram foi: \n\n\n\n" \
               "1 - {} → Likes:{} ↑Likes:{}  Comentarios :{} ↑Comentarios: {}   Postada há {}\n\n" \
               "2 - {} → Likes:{} ↑Likes:{}  Comentarios :{} ↑Comentarios: {}   Postada há {}\n\n" \
               "3 - {} → Likes:{} ↑Likes:{}  Comentarios :{} ↑Comentarios: {}   Postada há {}\n\n" \
               "4 - {} → Likes:{} ↑Likes:{}  Comentarios :{} ↑Comentarios: {}   Postada há {}\n\n" \
               "Espero que tenha um ótimo dia :)"

    mensagem = Mensagem.format(Cliente['Empresa'][0],
                               Cliente['img'][0],Cliente['Likes'][0],Cliente['Likes_var'][0],Cliente['Comments'][0],Cliente['Comments_var'][0], Cliente['Periods'][0],
                               Cliente['img'][1],Cliente['Likes'][1],Cliente['Likes_var'][1],Cliente['Comments'][1],Cliente['Comments_var'][1], Cliente['Periods'][1],
                               Cliente['img'][2],Cliente['Likes'][2],Cliente['Likes_var'][2],Cliente['Comments'][2],Cliente['Comments_var'][2], Cliente['Periods'][2],
                               Cliente['img'][3],Cliente['Likes'][3],Cliente['Likes_var'][3],Cliente['Comments'][3],Cliente['Comments_var'][3], Cliente['Periods'][3])

if datetime.datetime.now().strftime("%H:%M:%S") == "17:30:00":
    Mensagem = " Bom fim de tarde {} ! O comportamento da sua conta no instagram foi: \n\n\n\n" \
               "1 - {} → Likes:{} ↑Likes:{}  Comentarios :{} ↑Comentarios: {}   Postada há {}\n\n" \
               "2 - {} → Likes:{} ↑Likes:{}  Comentarios :{} ↑Comentarios: {}   Postada há {}\n\n" \
               "3 - {} → Likes:{} ↑Likes:{}  Comentarios :{} ↑Comentarios: {}   Postada há {}\n\n" \
               "4 - {} → Likes:{} ↑Likes:{}  Comentarios :{} ↑Comentarios: {}   Postada há {}\n\n" \
               "Espero que tenha um ótima noite :)"
    mensagem = Mensagem.format(Cliente['Empresa'][0],
                               Cliente['img'][0], Cliente['Likes'][0], Cliente['Likes_var'][0], Cliente['Comments'][0],Cliente['Comments_var'][0], Cliente['Periods'][0],
                               Cliente['img'][1], Cliente['Likes'][1], Cliente['Likes_var'][1], Cliente['Comments'][1],Cliente['Comments_var'][1], Cliente['Periods'][1],
                               Cliente['img'][2], Cliente['Likes'][2], Cliente['Likes_var'][2], Cliente['Comments'][2],Cliente['Comments_var'][2], Cliente['Periods'][2],
                               Cliente['img'][3], Cliente['Likes'][3], Cliente['Likes_var'][3], Cliente['Comments'][3],Cliente['Comments_var'][3], Cliente['Periods'][3])


mensagem=[" "]
if len(curtidas) !=0:
    for i in curtidas:
        msg=" Atenção!!! o perfil {} Apresentou uma variação consideravel no numero de curtidas na seguinte postagem do instagram:\n\n\n\n" \
               "    {} \n\n → teve uma variação de {} % curtidas desde a ultima atualização, agora totalizando um total de {} Curtidas \n\n\n\n\n\n"
        msg=msg.format(i['Empresa'][0],i['img'][0],i['Likes_var'][0]*100,i['Likes'][0])
        mensagem[0] = mensagem[0] + msg


if len(comentarios) !=0:
    for i in comentarios:
        msg=" Atenção!!! o perfil {} Apresentou uma variação consideravel no numero de comentarios na seguinte postagem do instagram:\n\n\n\n" \
               "    {} \n\n → teve uma variação de {} % curtidas desde a ultima atualização, agora totalizando um total de {} Curtidas \n\n\n\n\n\n"
        msg=msg.format(i['Empresa'][0],i['img'][0],i['Likes_var'][0]*100,i['Likes'][0])
        mensagem[0] = mensagem[0] + msg


message = MIMEText(mensagem[0])
message['subject'] = 'Alerta'
message['from'] = from_addr
message['to'] = ', '.join(to_addrs)


server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
server.login(username, password)
server.sendmail(from_addr, to_addrs, message.as_string())
server.quit()





