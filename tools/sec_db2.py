#!/usr/bin/python3

## Db2 Security-System
## Version 1.0
## Manfred Wagner
## info@manfred-wagner.at


from tkinter import messagebox
import sys
# import the db2-driver
import ibm_db

# --------------------------------------------------------------------------------
# DB2 DB2 DB2 DB2 DB2 DB2 DB2 DB2 DB2 DB2 DB2 DB2 DB2 DB2 DB2 DB2 DB2 DB2 DB2 DB2 
# --------------------------------------------------------------------------------
class Db2():
    """
    class Db2
    This class allows the acces to the IBM Db2 Database
    Properties:
        server = The server containing the Db2 database
        port   = The port for the communication to the database
        dbname = The name of the database
        user   = The user which wants to connect to the database
        pwd    = The password for the user
    Methods:
        open   = Establish the connection to the database at the 
                 specific server over the given port, user and password
        exec   = Executes the sql-statement
        fetch  = Returns row by row from the executed sql-statement
        close  = Destroys the connection to the database
    """

    # initialize the connection parameters
    def __init__(self):
        self.server: str = ""
        self.port:   int = 0
        self.dbname: str = ""
        self.user:   str = ""
        self.ssl:    str = ""
        self.pwd:    str = ""
        self.conn        = None
        self.stmt        = None
        self.con_user:str = ""
        self.adm_user:str = ""
        self.sec_user:str = ""
        # -- db metadata --
        self.tbl_col_list:list = []
    
    # open the connection to the database
    def open(self,server="",port="",dbname="",ssl="",user="",pwd=""):
        self.server  = server
        self.port    = port
        self.dbname  = dbname
        self.ssl     = ssl
        self.user    = user
        self.pwd     = pwd
        self.conn    = None
        self.stmt    = None
        conn_str = 'DATABASE='+str(self.dbname)+';HOSTNAME='+str(self.server)+\
            ';PORT='+str(self.port)+';'+'PROTOCOL=TCPIP;UID='+str(self.user)+\
            ';PWD='+str(self.pwd)+ssl
        try:
            self.conn = ibm_db.connect(conn_str,"","")
            # messagebox.showinfo("The DB-Connection was successfull",self.dbname+" : "+self.user)
            # print(f"The DB-Connection was successfull")
            return True
        except Exception as e:
            messagebox.showerror("The DB-Connection went wrong",e)
            #print(f"The DB-Connection went wrong:\n{e}")
            return False
            #sys.exit()
        
    # executes the sql-statement
    def exec(self,sql):
        typ = sql.split()
        try:
            #messagebox.showinfo("This SQL will be executed:",sql)
            self.stmt = ibm_db.exec_immediate(self.conn,sql)
        #except Exception as e:
        except Exception as e:
            print(f"The execution of <{sql}> went wrong")
            print(f">> {e}")
            exit
        if typ[0].upper() in ['DELETE','MERGE']:
            try:
                self.stmt = ibm_db.exec_immediate(self.conn,'COMMIT')
            except:
                print("The COMMIT was not successfull")

    # get the column-information for an table
    def get_col_info(self,schema,table):
        schema = schema.upper()
        table = table.upper()
        self.tbl_col_list = []
        no_data:bool = False
        sql = f"SELECT colname,colno,typename,keyseq \
            FROM syscat.columns WHERE (tabschema,tabname) = ('{schema}','{table}') ORDER by colno"
        self.stmt = ibm_db.exec_immediate(self.conn,sql)
        while no_data is False:
            record = ibm_db.fetch_assoc(self.stmt)
            if record is False:
                no_data = True
            else:
                self.tbl_col_list.append(record)
        return self.tbl_col_list


    # fetch row by row from the sql-statement
    def fetch(self,exec_mode='N'):
        try:
            if exec_mode == 'N':
                # access only by name
                row = ibm_db.fetch_assoc(self.stmt)
            else:
                # access by name and by number
                row = ibm_db.fetch_both(self.stmt)
            return row
        except Exception as e:
            print(f"The connection was interrupted")
            print(f">> {e}")
            exit

    # destroys the database connection
    def close(self):
        self.conn = None
        self.stmt = None

