import pymongo
from flask import Flask
from flask import render_template_string
from flask import render_template,request
from werkzeug.utils import secure_filename

import json
import plotly
import plotly.express as px
from  mongotest import MongoDbSupport
from datetime import datetime, timedelta
import os
app = Flask(__name__)

import requests
from bs4 import  BeautifulSoup
app.logger.error('testing error log')
app.logger.info('testing info log')
app.config['UPLOAD_FOLDER']="./upload"





def arxiv_pages(code):
    

    header={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}
    url=f"https://arxiv.org/search/?query={code}&searchtype=all&abstracts=hide&order=-announced_date_first&size=50"


    
    #print(url)
    res=requests.get(url,headers=header)
    
    soup=BeautifulSoup(res.text,"html.parser")
    pdfs=soup.find_all("p",class_="list-title is-inline-block")
    pdflist=[]
    for pdf in pdfs:
        st=pdf.a["href"]
        st=st.replace("abs","pdf")
        pdflist+=[st]
    #pages_txt=pages[0].text.strip()
    #print(pages_txt)
    titles=soup.find_all("p",class_="title is-5 mathjax")
    titlelist=[]
    
    for title in titles:
        st=title.text.strip()
        
        titlelist+=[st]

    dates=soup.find_all("p",class_="is-size-7")
    datelist=[]
    montslist=["January","February","March","April","May","June","July","August", "September","October","November","December"]
    for date in dates:
        st=date.text
        if "Submitted" in st:
            st=st.split(";")
            st=st[0][10:].strip()
            date=st.split(" ")
            monts=date[1][:-1]
            #print(monts)
            if monts in montslist and st[0] in "123456789":
               datelist+=[st]
    o=[]
    for i,title in enumerate(titlelist):
        o.append([datelist[i],title,pdflist[i]])
    return(o)








@app.route('/arxiv/<query>')

def getarxiv(query="python"):
   outstr=render_template("html_template_arxiv.html",
                                 query_in=query,
                                 arxiv_in=arxiv_pages(query)
                                 )
                                 
   #print(outstr)
   return outstr



@app.route('/')
def hello_world():
    outstr=render_template("html_template_root.html")
                                 
    return outstr

@app.route('/arxiv', methods=['POST'])
def arxiv():
    text = request.form['Field1']
    
    processed_text = text.upper()
    outstr=render_template("html_template_arxiv.html",
                                 query_in=processed_text,
                                 arxiv_in=arxiv_pages(processed_text.replace(" ","+"))
                                 )
    return outstr



# *** CHAT ***

def rg_topic():
    

   
   
    header={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}

    url="https://forum.portfolio.hu/topics/richter-topik/6389"
    res=requests.get(url,headers=header)
    #print (res.text)
    soup=BeautifulSoup(res.text,"html.parser")
    datelist=soup.find_all("span", class_="date" )
    textlist=soup.find_all("div", class_="text")
    out=[]
    for i in range(len(datelist)):
        out.append((datelist[i].text,textlist[i].text.replace("\n","").replace("\xa0"," ")))

    print("----------------  END  ------------------------")
    return(out)


@app.route('/chat')
def topic_chat():
    outstr=""
    
    outstr=render_template("html_template_chat.html",
                                 chat_in=rg_topic()
                                 )
    
      
    return outstr



@app.route('/login', methods = ['GET', 'POST'])
def login():
      outstr=render_template("html_google_login.html",)
      return outstr


@app.route('/uploader', methods=['GET'])
def bwcolorizer():
    
    outstr=render_template("html_template_uploader.html",
                                 
                                 )
    return outstr



@app.route('/uploader', methods = ['POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      fname2="./static/img/"+f.filename  

      f.save(fname2,)
      
      outstr=render_template("html_template_uploader_work.html",
                                 path2=fname2,
                                 )

      
      
      return outstr



@app.route("/mongo")


def mongodb():
   from os import getenv
   _mongo_conn_=f"mongodb+srv://{getenv('mongo_usr')}:{getenv('mongo_pwd')}@cluster0.fuant.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
   # _mongo_conn_=f"mongodb://127.0.0.1"
   _DB_="PDF_DB"
   _INCIDENT_COLLECTION_="incident"
   mc=MongoDbSupport(_mongo_conn_)
   mc.debug_mode()
   mc.connect(_DB_)
   out=f"length of {_INCIDENT_COLLECTION_} : {mc.count(_INCIDENT_COLLECTION_)}"  
    

   return out
id_num=2
_X_INTERVALL_=None
    



@app.route('/dash', methods = ['GET','POST'])

def notdash():
    
    global id_num, _X_INTERVALL_
    from os import getenv   
   
    if os.getenv("mongo_remote")==None:
        local=True # local vs cloud server
    else:
        local=False

    if local==True:
        _mongo_conn_=f"mongodb://127.0.0.1"
        _DB_="DBASE"
    else:  
        _mongo_conn_=f"mongodb+srv://{getenv('mongo_usr')}:{getenv('mongo_pwd')}@cluster0.fuant.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        _DB_="PDF_DB"    
    _INCIDENT_COLLECTION_="Incident"
    
    
    if request.method=="POST":
        
        

        content = request.get_json(silent=True)
        print(type(content))
        if content.get( "xrange") !=None:
            print("MEGVAGY")
            if content["xrange"]=="1year":
                _X_INTERVALL_=365
            if content["xrange"]=="3months":
                _X_INTERVALL_=6*31
            
            
            if content["xrange"]=="1month":
                _X_INTERVALL_=4*31
            if content["xrange"]=="all":
                _X_INTERVALL_=None

            
                
            return "<HTML><BODY>Hello<BODY></HTML>"


        id_num=id_num+1
        from os import getenv
       
        
        
        mc=MongoDbSupport(_mongo_conn_)
        mc.debug_mode()
        mc.connect(_DB_)
        
        len_of_db=f"length of {_INCIDENT_COLLECTION_} : {mc.count(_INCIDENT_COLLECTION_)}"  
        print("len_of_db:",len_of_db)
        mc.insert_record(_INCIDENT_COLLECTION_,content)
        mc.disconnect()
        
        return "<HTML><BODY>Hello<BODY></HTML>"
        return content     

   
    if request.method=="GET":
        import pandas as pd
        import math
        print("__id_num__:",id_num)
        mc=MongoDbSupport(_mongo_conn_)
        mc.debug_mode()
        mc.connect(_DB_)
        
        df=mc.to_df(_INCIDENT_COLLECTION_)
        

        df["letrejott"]=pd.to_datetime(df["letrejott"], format="%Y. %m. %d. %H:%M:%S")
        df["folyamatban"]=pd.to_datetime(df["folyamatban"], format="%Y. %m. %d. %H:%M:%S")
        df["felveve"]=pd.to_datetime(df["felveve"], format="%Y. %m. %d. %H:%M:%S")

        df["MASDOR"]=(df["felveve"]-df["folyamatban"])
        df["MASDOR"]=df["MASDOR"].values.astype("float64")
        df["MASDOR"]=df["MASDOR"] /1000.0/1000.0/1000.0/60.0  
      
        
        df["ServiceDesk"]=((df["folyamatban"]-df["letrejott"]))
        df["ServiceDesk"]=df["ServiceDesk"].values.astype("float64")
        df["ServiceDesk"]=df["ServiceDesk"]/1000.0/1000.0/1000.0/60.0  

        #Melyik napon történneek a dolgok?
        df["Day_letrejott"]=df["letrejott"].dt.dayofweek
        df["Day_folyamatban"]=df["folyamatban"].dt.dayofweek
        df["Day_felveve"]=df["felveve"].dt.dayofweek
        df["h_folyamatban"]=df["folyamatban"].dt.hour

        df.sort_values(by=["letrejott"], inplace=True)

        #csak az érdekel minket, ami hétköznap volt
        df.query("Day_letrejott<5", inplace=True )
        df.query("Day_folyamatban<5", inplace=True )
        df.query("Day_felveve<5", inplace=True )
        #csak az érdekel minket, ami hétköznap volt
        
        df.query("h_folyamatban>6", inplace=True )
        df.query("h_folyamatban<15", inplace=True )
        if _X_INTERVALL_!=None:
            most = datetime.now()
            time_delta = timedelta(days=int(_X_INTERVALL_))
            one_year_ago=most-time_delta
            df = df.loc[df['letrejott'] > one_year_ago]





        
        
        


        #df.query("Day==2", inplace=True )
        print(df.columns)
        print(df.dtypes)
        print(df.head(100))

        fig = px.line(df,x="letrejott", y=["MASDOR","ServiceDesk"],text="inc_id", markers=False,title="Masdor incidensek",log_y=True)
        fig.update_traces(mode="markers+lines", hovertemplate=None)
        fig.update_layout(hovermode="x unified")
        fig.update_xaxes(title_text='Incidens létrehozási időpont')
        fig.update_yaxes(title_text='Átfutási idő [perc]')
        fig.add_shape(
            legendrank=1,
            showlegend=True,
            type="line",
            xref="paper",
            line=dict(dash="5px"),
            x0=0.,
            x1=1,
            y0=15,
            y1=15,
        )
        fig.update_layout(
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
                )
                )


        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        #graphJSON=None
        return render_template('html_template_plotly.html', graphJSON=graphJSON)





if __name__ == '__main__':
   porto = int(os.environ.get("PORT", 5000))
   app.run(host="0.0.0.0", port=porto)
