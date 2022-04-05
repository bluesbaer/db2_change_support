
from tools import sec_db2 as driver
import tkinter as tk
from tkinter import ttk, simpledialog

class Screen(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = self
        self.root.title('Database Attribute Finder by M. Wagner')
        self.db2 = driver.Db2()
        pass

    def build(self):
        self.message = tk.StringVar()
        main_frame = ttk.LabelFrame(self.root,text='Input Area For Search-Pattern')
        main_frame.grid(row=0, column=0, padx=3, pady=3, sticky=('N','E','S','W'))
        ttk.Label(main_frame, text='Server:').grid(row=0, column=0, padx=3, pady=3, sticky=('E','W'))
        ttk.Label(main_frame, text='Port:').grid(row=1, column=0, padx=3, pady=3, sticky=('E','W'))
        ttk.Label(main_frame, text='Database:').grid(row=2, column=0, padx=3, pady=3, sticky=('E','W'))
        ttk.Label(main_frame, text='User:').grid(row=3, column=0, padx=3, pady=3, sticky=('E','W'))
        ttk.Label(main_frame, text='Schema:').grid(row=4, column=0, padx=3, pady=3, sticky=('E','W'))
        ttk.Label(main_frame, text='Field:').grid(row=5, column=0, padx=3, pady=3, sticky=('E','W'))
        self.server = ttk.Entry(main_frame)
        self.server.grid(row=0, column=1, padx=3, pady=3, sticky=('E','W'))
        self.port = ttk.Entry(main_frame)
        self.port.grid(row=1, column=1, padx=3, pady=3, sticky=('E','W'))
        self.database = ttk.Entry(main_frame)
        self.database.grid(row=2, column=1, padx=3, pady=3, sticky=('E','W'))
        self.user = ttk.Entry(main_frame)
        self.user.grid(row=3, column=1, padx=3, pady=3, sticky=('E','W'))
        self.schema = ttk.Entry(main_frame)
        self.schema.grid(row=4, column=1, padx=3, pady=3, sticky=('E','W'))
        self.field = ttk.Entry(main_frame)
        self.field.grid(row=5, column=1, padx=3, pady=3, sticky=('E','W'))
        tk.Button(main_frame, text='Search', command=self.search).grid(row=10, column=1, padx=3, pady=3, sticky=('E','W'))
        tk.Button(main_frame, text='Connect', command=self.connect).grid(row=10, column=0, padx=3, pady=3, sticky=('E','W'))
        ttk.Label(main_frame, text="", textvariable=self.message).grid(row=15, column=0, columnspan=2, padx=3, pady=3, sticky=('E','W'))
        self.server.focus()

    def search(self):
        self.text_liste:list = []
        search_schema = self.schema.get()
        search_field = self.field.get()
        col_sql = f"SELECT tabschema, tabname, colname, colno, typename, length, scale FROM syscat.columns WHERE tabschema = '{search_schema}' AND colname = '{search_field}' ORDER BY colno"
        rou_sql = f"SELECT routineschema,routinename,specificname,CASE WHEN routinetype='F' THEN 'Function' WHEN routinetype='P' THEN 'Procedure' ELSE routinetype END"
        rou_sql += f" FROM syscat.routines  WHERE routineschema = '{search_schema}' AND cast(text as varchar(20000)) LIKE '%{search_field}%';"
        self.db2.exec(col_sql)
        row = self.db2.fetch()
        while row != False:
            self.text_liste.append(row)
            row = self.db2.fetch()
        self.db2.exec(rou_sql)
        row = self.db2.fetch()
        while row != False:
            self.text_liste.append(row)
            row = self.db2.fetch()
        for _ in self.text_liste:
            print(_)

    def connect(self):
        con_server = self.server.get().upper()
        con_port = self.port.get()
        con_database = self.database.get().upper()
        con_user = self.user.get().upper()
        tmp_pwd = simpledialog.askstring(title='----- PASSWORD -----', prompt=f'   PASSWORD for {con_user}   ', show="?")
        con_flag = self.db2.open(con_server, con_port, con_database, '', con_user, tmp_pwd)
        if con_flag:
            tmp_pwd = ""
            self.message.set(f'User:{con_user} on Database:{con_database} Connected')
        pass

class Finder():

    def __init__(self):
        pass




if __name__ == '__main__':
    scr = Screen()
    scr.build()
    scr.mainloop()
