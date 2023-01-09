# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 11:41:36 2023

@author: khadim and Ahmad 
"""

import cx_Oracle
from modules.config import config
import sys

config.config()
class  dbconnection:
    # https://www.ebi.ac.uk/seqdb/confluence/pages/viewpage.action?spaceKey=EMBL&title=Content+Team+SQL+Connections
    # db = {'name':'','host':'','port':''}
    # user = ''
    # passwd = ''
    # request = ''
    def __init__(self,dbname,OPSusername,password):
        
        ENAPRO = {'name':'ENAPRO','host':'ora-ena-pro-hl.ebi.ac.uk','port':'1531'}
        ERAPRO = {'name':'ERAPRO','host':'ora-era-pro-hl.ebi.ac.uk','port':'1531'}
        ERATEST = {'name':'ERATEST','host':'ora-dlvm-124.ebi.ac.uk','port':'1521'}
        if dbname == 'ENAPRO':
           self.db = ENAPRO
        elif dbname == 'ERAPRO':
            self.db = ERAPRO
        elif dbname == 'ERATEST' :
            self.db = ERATEST
        self.user = OPSusername
        self.passwd = password
    

    
    def connection(self):
        try:
            dsn = cx_Oracle.makedsn(self.db['host'], self.db['port'], service_name=self.db['name'])
            connection = cx_Oracle.connect(self.user, self.passwd, dsn, encoding="UTF-8")
            self.request =  connection.cursor()
        except cx_Oracle.Error as error:
                print('\033[91m'+str(error))
                print('\033[0m')
                sys.exit()

    def select_1(self,attribute,table,condition):
        self.request.execute("SELECT "+attribute+" FROM  "+table+" where "+ condition)
        result = self.request.fetchall()
        return result 
    
    def select_2(self,attribute,table):
        self.request.execute("SELECT "+attribute+" FROM  "+table)
        result = self.request.fetchall()
        return result
        
    def update(self,table,attribute,condition):
        self.request.execute("UDDATE "+table+" SET  "+attribute+" where "+ condition)
        self.request.commit()

    def close (self):
        self.request.close()