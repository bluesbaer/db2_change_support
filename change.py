
from tools import sec_db2 as driver
import tkinter as tk
from tkinter import ttk, simpledialog

class Screen(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = self
        self.root.title('Database Attribute Finder by M. Wagner')
        self.driver = driver.Db2()
        self.detail_window:list = []
        pass

    def build(self):
        self.db_screen = ttk.LabelFrame(self.root,text='Database Connection Parameter')
        self.db_screen.grid(row=0, column=0, padx=3, pady=3, sticky=('N','E','S','W'))
        ttk.Label(self.db_screen,text='Server').grid(row=1,column=0, padx=3, pady=3, sticky=('E','W'))
        ttk.Label(self.db_screen,text='Port').grid(row=1,column=1, padx=3, pady=3, sticky=('E','W'))
        ttk.Label(self.db_screen,text='Database').grid(row=1,column=2, padx=3, pady=3, sticky=('E','W'))
        ttk.Label(self.db_screen,text='User').grid(row=1,column=3, padx=3, pady=3, sticky=('E','W'))
        self.server_col = ttk.Entry(self.db_screen)
        self.server_col.grid(row=2, column=0, padx=3, pady=3, sticky=('E','W'))
        self.port_col = ttk.Entry(self.db_screen)
        self.port_col.grid(row=2, column=1, padx=3, pady=3, sticky=('E','W'))
        self.database_col = ttk.Entry(self.db_screen)
        self.database_col.grid(row=2, column=2, padx=3, pady=3, sticky=('E','W'))
        self.user_col = ttk.Entry(self.db_screen)
        self.user_col.grid(row=2, column=3, padx=3, pady=3, sticky=('E','W'))
        con_button = ttk.Button(self.db_screen, text='CONNECT', command=self.db_connect)
        con_button.grid(row=2, column=4, padx=3, pady=3, sticky=('N','E','S','W'))
        # con_button.bind('<Enter>',self.db_connect)
        self.server_col.focus_set()


    def extend_screen(self):
        self.search_screen = ttk.LabelFrame(self.root,text='Input Area For Search-Pattern')
        self.search_screen.grid(row=10, column=0, padx=3, pady=3, sticky=('N','E','S','W'))
        ttk.Label(self.search_screen, text='Column-Name:').grid(row=0, column=0, padx=3, pady=3, sticky=('E','W'))
        self.column = ttk.Entry(self.search_screen)
        self.column.grid(row=0, column=1, padx=3, pady=3, sticky=('E','W'))
        ttk.Label(self.search_screen, text='Schema-Name:').grid(row=1, column=0, padx=3, pady=3, sticky=('E','W'))
        self.schema = ttk.Entry(self.search_screen)
        self.schema.grid(row=1, column=1, padx=3, pady=3, sticky=('E','W'))

        ttk.Button(self.search_screen, text='SEARCH', command=self.start_search).grid(row=0, column=2, padx=3, pady=3, sticky=('N','E','S','W'), rowspan=2)

        ttk.Label(self.search_screen, text='Table:').grid(row=10, column=0, padx=3, pady=3, sticky=('E','W'))
        self.tbl_scroll = ttk.Scrollbar(self.search_screen)
        self.tbl_scroll.grid(row=10, column=13, rowspan=6, padx=3, pady=3, sticky=('N','S'))
        self.tbl_list = tk.Listbox(self.search_screen, height=6, width=80, yscrollcommand = self.tbl_scroll.set)
        self.tbl_list.grid(row=10, column=1, columnspan=12, padx=3, pady=3, sticky=('E','W'))
        self.tbl_scroll.config(command=self.tbl_list.yview)
        self.tbl_list['yscrollcommand'] = self.tbl_scroll.set
        self.tbl_list.bind('<Double-1>',self.tbl_show)

        ttk.Label(self.search_screen, text='View:').grid(row=20, column=0, padx=3, pady=3, sticky=('E','W'))
        self.vie_scroll = ttk.Scrollbar(self.search_screen)
        self.vie_scroll.grid(row=20, column=13, rowspan=6, padx=3, pady=3, sticky=('N','S'))
        self.vie_list = tk.Listbox(self.search_screen, height=6, width=80, yscrollcommand = self.vie_scroll.set)
        self.vie_list.grid(row=20, column=1, columnspan=12, padx=3, pady=3, sticky=('E','W'))
        self.vie_scroll.config(command=self.vie_list.yview)
        self.vie_list['yscrollcommand'] = self.vie_scroll.set
        self.vie_list.bind('<Double-1>',self.vie_show)

        ttk.Label(self.search_screen, text='Function:').grid(row=30, column=0, padx=3, pady=3, sticky=('E','W'))
        self.fun_scroll = ttk.Scrollbar(self.search_screen)
        self.fun_scroll.grid(row=30, column=13, rowspan=6, padx=3, pady=3, sticky=('N','S'))
        self.fun_list = tk.Listbox(self.search_screen, height=6, width=80, yscrollcommand = self.fun_scroll.set)
        self.fun_list.grid(row=30, column=1, columnspan=12, padx=3, pady=3, sticky=('E','W'))
        self.fun_scroll.config(command=self.fun_list.yview)
        self.fun_list['yscrollcommand'] = self.fun_scroll.set
        self.fun_list.bind('<Double-1>',self.fun_show)

        ttk.Label(self.search_screen, text='Procedure:').grid(row=40, column=0, padx=3, pady=3, sticky=('E','W'))
        self.prc_scroll = ttk.Scrollbar(self.search_screen)
        self.prc_scroll.grid(row=40, column=13, rowspan=6, padx=3, pady=3, sticky=('N','S'))
        self.prc_list = tk.Listbox(self.search_screen, height=6, width=80, yscrollcommand = self.prc_scroll.set)
        self.prc_list.grid(row=40, column=1, columnspan=12, padx=3, pady=3, sticky=('E','W'))
        self.prc_scroll.config(command=self.prc_list.yview)
        self.prc_list['yscrollcommand'] = self.prc_scroll.set
        self.prc_list.bind('<Double-1>',self.prc_show)
        self.column.focus_set()

    def show_detail(self, obj_data, det_data):
        dw = External_Window()
        dw.build(obj_data, det_data)
        pass

    def tbl_show(self,event):
        cs = self.tbl_list.curselection()
        row_num = cs[0]
        obj_data = f"{self.table_data[row_num]['TABSCHEMA'].strip()}.{self.table_data[row_num]['TABNAME'].strip()}"
        det_data = f"{self.table_data[row_num]['COLNAME'].strip()} = {self.table_data[row_num]['TYPENAME'].strip()}"
        det_data += f"({self.table_data[row_num]['LENGTH']},{self.table_data[row_num]['SCALE']})"
        self.show_detail(obj_data, det_data)

    def vie_show(self,event):
        cs = self.vie_list.curselection()
        row_num = cs[0]
        obj_data = f"{self.view_data[row_num]['TABSCHEMA'].strip()}.{self.view_data[row_num]['TABNAME'].strip()}"
        det_data = f"{self.view_data[row_num]['COLNAME'].strip()} = {self.view_data[row_num]['TYPENAME'].strip()}"
        det_data += f"({self.view_data[row_num]['LENGTH']},{self.view_data[row_num]['SCALE']})"
        self.show_detail(obj_data, det_data)
        pass

    def fun_show(self,event):
        cs = self.fun_list.curselection()
        row_num = cs[0]
        obj_data = f"{self.func_data[row_num]['FUNCSCHEMA'].strip()}.{self.func_data[row_num]['FUNCNAME'].strip()}"
        obj_data += f" ({self.func_data[row_num]['SPECIFICNAME'].strip()})"
        det_data = f"({self.func_data[row_num]['4']})"
        self.show_detail(obj_data, det_data)
        pass

    def prc_show(self,event):
        cs = self.prc_list.curselection()
        row_num = cs[0]
        obj_data = f"{self.proc_data[row_num]['PROCSCHEMA'].strip()}.{self.proc_data[row_num]['PROCNAME'].strip()}"
        obj_data += f" ({self.proc_data[row_num]['SPECIFICNAME'].strip()})"
        det_data = f"({self.proc_data[row_num]['4']})"
        self.show_detail(obj_data, det_data)
        pass

    def db_connect(self):
        server = self.server_col.get()
        port = self.port_col.get()
        dbname = self.database_col.get()
        user = self.user_col.get()
        pwd = simpledialog.askstring(title=f"{dbname}",\
            prompt=f"Input password for user >> {user} <<",show="*")
        try:
            con_status = self.driver.open(server,port,dbname,'',user,pwd)
            if con_status:
                self.extend_screen()
        except Exception as e:
            print(f"DB-ERROR:{e}")
        pass

    def start_search(self):
        self.table_data:list = []
        self.view_data:list = []
        self.func_data:list = []
        self.proc_data:list = []
        pattern:str = self.column.get().upper()
        sql = "SELECT COL.TABSCHEMA, COL.TABNAME, COL.COLNAME, COL.TYPENAME, COL.LENGTH, COL.SCALE "
        sql += "FROM SYSCAT.COLUMNS AS COL JOIN SYSCAT.TABLES AS TAB "
        sql += "ON (COL.TABSCHEMA,COL.TABNAME) = (TAB.TABSCHEMA,TAB.TABNAME) "
        sql += f"WHERE TAB.TYPE = 'T' AND COL.COLNAME = '{pattern}'"
        if self.schema.get() != '':
            sql += f" AND TAB.TABSCHEMA = '{self.schema.get().upper().strip()}'"
        self.table_data = self.search_content(sql)
        sql = "SELECT COL.TABSCHEMA, COL.TABNAME, COL.COLNAME, COL.TYPENAME, COL.LENGTH, COL.SCALE "
        sql += "FROM SYSCAT.COLUMNS AS COL JOIN SYSCAT.TABLES AS TAB "
        sql += "ON (COL.TABSCHEMA,COL.TABNAME) = (TAB.TABSCHEMA,TAB.TABNAME) "
        sql += f"WHERE TAB.TYPE = 'V' AND COL.COLNAME = '{pattern}'"
        if self.schema.get() != '':
            sql += f" AND TAB.TABSCHEMA = '{self.schema.get().upper().strip()}'"
        self.view_data = self.search_content(sql)
        sql = f'''SELECT FUNCSCHEMA, FUNCNAME, SPECIFICNAME, CAST(BODY AS VARCHAR(3000)) FROM SYSCAT.FUNCTIONS WHERE BODY LIKE '%{pattern}%' '''
        if self.schema.get() != '':
            sql += f" AND FUNCSCHEMA = '{self.schema.get().upper().strip()}'"
        self.func_data = self.search_content(sql)
        sql = f'''SELECT PROCSCHEMA, PROCNAME, SPECIFICNAME, CAST(TEXT AS VARCHAR(3000)) FROM SYSCAT.PROCEDURES WHERE TEXT LIKE '%{pattern}%' '''
        if self.schema.get() != '':
            sql += f" AND PROCSCHEMA = '{self.schema.get().upper().strip()}'"
        self.proc_data = self.search_content(sql)
        self.prepare_screen(self.table_data,self.view_data,self.func_data,self.proc_data)

    def search_content(self,sql):
        data:list = []
        self.driver.exec(sql)
        row = self.driver.fetch()
        while row != False:
            data.append(row)
            row = self.driver.fetch()
        return data

    def prepare_screen(self,table,view,function,procedure):
        row_num:int = 1
        self.tbl_list.delete(0,'end')
        for line in table:
            self.tbl_list.insert(row_num,f"{line['TABSCHEMA'].strip()}.{line['TABNAME'].strip()}")
            row_num += 1
        row_num:int = 1
        self.vie_list.delete(0,'end')
        for line in view:
            self.vie_list.insert(row_num,f"{line['TABSCHEMA'].strip()}.{line['TABNAME'].strip()}")
            row_num += 1
        row_num:int = 1
        self.fun_list.delete(0,'end')
        for line in function:
            self.fun_list.insert(row_num,f"{line['FUNCSCHEMA'].strip()}.{line['FUNCNAME'].strip()} ({line['SPECIFICNAME'].strip()})")
            row_num += 1
        row_num:int = 1
        self.prc_list.delete(0,'end')
        for line in procedure:
            self.prc_list.insert(row_num,f"{line['PROCSCHEMA'].strip()}.{line['PROCNAME'].strip()} ({line['SPECIFICNAME'].strip()})")
            row_num += 1


class External_Window(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = self
        self.root.title('Detail Datawindow')

    def build(self, obj_data, det_data):
        self.detail_frame = ttk.LabelFrame(self.root, text = 'Detail - Data')
        self.detail_frame.grid(row=20, column=0, padx=3, pady=3, sticky=('N','E','S','W'))
        ttk.Label(self.detail_frame, text='Object:').grid(row=0, column=0, padx=3, pady=3, sticky=('E','W'))
        obj_entry = tk.Entry(self.detail_frame)
        obj_entry.grid(row=0,column=1,padx=3,pady=3,sticky=('E','W'))
        obj_entry.delete(0,'end')
        obj_entry.insert(0,obj_data)
        ttk.Label(self.detail_frame, text='Data:').grid(row=1, column=0, padx=3, pady=3, sticky=('E','W'))
        det_entry = tk.Text(self.detail_frame)
        det_entry.grid(row=1,column=1,padx=3,pady=3,sticky=('E','W'))
        #det_entry.delete(0,END)
        det_entry.insert('end',det_data)
        pass


class Finder():

    def __init__(self):
        pass




if __name__ == '__main__':
    scr = Screen()
    scr.build()
    scr.mainloop()
