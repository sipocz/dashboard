class MongoDbSupport:
    
    def __init__(self,connection_str:str):
        
        self._connection_str_=connection_str
        self.dms=False
        self.connected=False  

# -----------------------------------

    def count(self,coll:str) -> int:
        mydb = self.mydb    #DB 
        col=mydb[coll]      #Collection
        return col.count_documents({})

# -----------------------------------

    def connect(self,db) -> None:
        from pymongo import MongoClient
        
        '''
        Adatbázis kapcsolódás
        '''
        if not self.connected:
            self.client = MongoClient(self._connection_str_)
            
            self.mydb = self.client[db]   #DB 
            self.connected=True
            return
        else:
             print("Connected!!")

# -----------------------------------

    def disconnect(self) -> None:
        from pymongo import MongoClient
        '''
        zárja a kapcsolatokat
        '''
        if self.connected:            
            self.client.close()
            self.mydb=None
            self.connected=False
        else:
            print("Disconnected")
        
# -----------------------------------

    def to_csv(self,coll:str,fname:str):
        
        '''
        MONGODB adatbázisból id alapján data visszaadása
        '''
        # print("Mongo_start")
        if self.dms:
            print("to_csv")
        import pymongo
        import pandas as pd
    
        mydb = self.mydb    #DB 
        col=mydb[coll]      #Collection

        cursor=col.find()
            
        cursor_list=list(cursor)

        df  = pd.DataFrame(cursor_list)
        #print(df.head())
        df.to_csv(fname,index=False)
        df=None
        if self.dms:
            print("to_csv exit")
        return(col)

# -----------------------------------

    def kill_collection(self,coll:str):
        
        '''
        MONGODB adatbázis collection törlése
        '''
        if self.dms:
            print("Mongo_kill_collection ")
        import pymongo
        import pandas as pd
    
        client = pymongo.MongoClient(self._connection_str_)
        mydb = self.mydb    #DB 
        col=mydb[coll]      #Collection
        col.drop()

        return(col)

# -----------------------------------

    def upload_from_csv(self,coll:str,fname:str):
        
        '''
        MONGODB adatbázisba collection feltöltése fname csv-ből
       
        '''
        if self.dms:
            print("Upload_start")
        import pymongo
        import pandas as pd
    
        client = pymongo.MongoClient(self._connection_str_)
        mydb = self.mydb   #DB 
        col=mydb[coll]      #Collection
        #print(df.head())
        df=pd.read_csv(fname)
        if self.dms:
            print(df.head())
        list_of_dict=df.to_dict('records')
        col.insert_many(list_of_dict)
        if self.dms:
            print("exit upload")
        return(col)

# -----------------------------------

    def debug_mode(self,value:bool=True):
        '''
        Az osztályt debug üzemmódba teszi.(default=True) Több kiírás jelenik neg a kimeneten 
            ha bemeneti értéke False: a debug móde kikapcsolásra kerül
            az osztály létrehozásakor a debug mód ki van kapcsolva 
        '''
        self.dms=value #Debug_mode_state

# -----------------------------------
    
    def regenerate_from_csv(self,coll:str,fname:str):
        
        '''
        MONGODB adatbázisba collection feltöltése fname csv-ből
        '''
        if self.dms:
            print("Upload_start")
        import pymongo
        import pandas as pd
    
        client = pymongo.MongoClient(self._connection_str_)
        mydb = self.mydb   #DB 
        col=mydb[coll]      #Collection
        #print(df.head())
        df=pd.read_csv(fname)
        

# -----------------------------------


    def get_selection(self,collection_name,id):
        '''
        MONGODB adatbázisból id alapján data visszaadása
        '''
        from bson import ObjectId
        
        if self.dms:
            print(f"Mongo get selection coolection: {collection_name} id: {id} ")

        mydb = self.mydb          
        col=mydb[collection_name]         #  DB[collection]
        
        cursor=col.find_one({"_id":ObjectId(id)})
        
        if self.dms:
            print("** get_mongo_selection_data Cursor:",cursor) #DEBUG
            
        return(cursor)
    




    def create_collection(self,collection_name,record_def:dict):

        import pymongo
        import pandas as pd

        mydb = self.mydb   #DB 
        collections=mydb.list_collection_names()
        if collection_name not in collections:
            
            if self.dms:
                print(f"Collection {collection_name} created!!") 

        col=mydb[collection_name]      #Collection
        #print(df.head())
        
        col.insert_one(record_def)
        return(col)

    def list_collections(self):

        import pymongo
        import pandas as pd

        mydb = self.mydb   #DB 
        collections=mydb.list_collection_names()
        return(collections)        


if __name__=="__main__":
    from os import getenv
    '''
    _mongo_conn_=f"mongodb+srv://{getenv('mongo_usr')}:{getenv('mongo_pwd')}@cluster0.fuant.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

    _PDF_DB_="PDF_DB"
    _FILE_LOCATION_COLLECTION_="ABB_file_location"
    _META_INFO_="ABB_pdf"
    '''

    from os import getenv

    _mongo_conn_=f"mongodb://127.0.0.1"
    _mongo_conn_=f"mongodb+srv://{getenv('mongo_usr')}:{getenv('mongo_pwd')}@cluster0.fuant.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    _PDF_DB_="PDF_DB"
    _FILE_LOCATION_COLLECTION_="Collection_2"
   


    mc=MongoDbSupport(_mongo_conn_)
    mc.debug_mode()
    mc.connect(_DB_)

    print(f"length of {_FILE_LOCATION_COLLECTION_} : {mc.count(_FILE_LOCATION_COLLECTION_)}")
    
    # mc.to_csv(_META_INFO_,"E:/Backup/20220508/Mongodb_pdf_file_location.csv")
    mc.get_selection(_FILE_LOCATION_COLLECTION_,"65621ecf8d50a659342dcf59")
    print(mc.connected)
    
    _collection_def_={"_name":"","pwd":""}
    mc.create_collection("Collection_3",_collection_def_)    

    print(mc.list_collections())
    mc.upload_from_csv("coll1","d:/csv/organizations-100000.txt")
    mc.disconnect()

    print(mc.connected)
    
    



