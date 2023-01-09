#!/usr/bin/python

import os 

class config :
	def config():
		a = os.getcwd()
		# https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html
		os.system('export ORACLE_HOME='+a.replace(' ','\ ')+'/instantclient_21_8/')
		os.system('export LD_LIBRARY_PATH=$ORACLE_HOME:$LD_LIBRARY_PATH')
		os.system('export PATH=$ORACLE_HOME:$PATH')
		os.system('export ORACLE_CLIENT_LIB=$ORACLE_HOME')
		#os.system('source $HOME/.bashrc')
    
