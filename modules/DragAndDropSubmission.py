#|/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 11:41:36 2023

@author: khadim and Ahmad 
"""

import getpass
import os
from modules.SQLrequest import dbconnection
import pandas as pd 
from datetime import datetime

class DDSubmission:
    def submission():
        print('\n\n')
        user = ''
        while user == '':
            user = input('$ Your OPS$USER > ')
        
        opspasswd = ''
        while opspasswd == '':
            opspasswd = getpass.getpass(prompt='$ Enter you OPS password > ')
            
        suppasswd = ''
        while suppasswd == '':
            suppasswd = getpass.getpass(prompt='$ enter the super user password > ')
        
        webin_accout = ''
        while webin_accout =='':
            webin_accout = input ('$ Webin_account > ')
            
        test_sub = ''
        while test_sub =='':
            test_sub = input ('$ Do you use ENA test server for submission? [yes/no] > ')
            if test_sub.upper() == 'YES':
                t = '-t'
            elif test_sub.upper()=='NO': 
                t = ' '
            else :
                test_sub = ''
                
        file = ''
        while file == '':
            file = input ('$ path for the metadata spreadsheet (On excel file format) > ')
            
        action = ''
        while action=='':
            action = input ('$ Specify the type of action needed ( ADD ) > ')
            if action.upper() == 'ADD':
                action = 'ADD'
            # elif action.upper()=='MODIFY': 
            #     action = 'MODIFY'
            else :
                action = ''
        print('\n\n')
        # submission of Study and Samples
        start = datetime.now()
        print ('\033[92m'+'\t\t\t+---------------------------------------------------------------+')
        print ('\033[92m'+'\t\t\t|                                                               |')
        print ('\033[92m'+'\t\t\t|========>  Hello '+user.split('$')[0].upper()+' !!!   <========|')
        print ('\033[92m'+'\t\t\t|                                                               |')
        print ('\033[92m'+'\t\t\t+---------------------------------------------------------------+')
        
        print('\033[0m')
        
        print ('\n\n')
        print ('\033[93m'+'\t\t+--------------------------------------------------------------------------------------------------------------+')
        print ('\033[93m'+'\t\t|***********************************     SUBMISSION OF STUDY AND SAMPLES    ***********************************|')
        print ('\033[93m'+'\t\t+--------------------------------------------------------------------------------------------------------------+')
        print ('\n\n')
        print('\033[0m')
        os.system ('python3 modules/ena-content-dataflow/scripts/ena-metadata-xml-generator.py -u '+webin_accout+' -p '+suppasswd+' -f '+file+' -a '+action+' '+t)

        # connection to the Database
        if t == '-t':
            a = dbconnection('ERATEST',user,opspasswd)
        else :
            a = dbconnection('ERAPRO',user,opspasswd)
        a.connection()

        
        xls = pd.ExcelFile(file)
        l  = xls.sheet_names
        metadata = pd.read_excel(xls, l[0],header = None)
        metadata = metadata.fillna(-1)
        header_2 = list(metadata.iloc[1])
        
        print('\033[92m'+'DONE...\n') 
        print('\033[0m')

        
        # submission of run et experiment 
        print ('\n\n')
        print ('\033[93m'+'\t\t+--------------------------------------------------------------------------------------------------------------+')
        print ('\033[93m'+'\t\t|***********************************     SUBMISSION OF RUN / EXERIMENT    *************************************|')
        print ('\033[93m'+'\t\t+--------------------------------------------------------------------------------------------------------------+')
        print ('\n\n')
        print('\033[0m')
        res_study = a.select_1('STUDY_ID, STUDY_ALIAS','study',"submission_account_id in ('"+webin_accout+"')")
        res_sample = a.select_1('sample_id , sample_alias','sample',"submission_account_id in ('"+webin_accout+"')")
        study_alias = list(metadata[header_2.index('study_alias')])
        sample_alias = list(metadata[header_2.index('sample_alias')])
        study_id = ''

        for i in range(5,len(sample_alias)):
            print('\n\n')
            if sample_alias[i] == -1 :
                break
            directory = '/'.join(file.split('/')[0:len(file.split('/'))-1])
            manifest = open(directory+'/manifest_run'+str(i-4)+'.txt','w')
            study_id = ''
            sample_id = ''
            for j in res_study : 
                if study_alias[i] == j[1]:
                    study_id = j[0]
                    break
            for j in res_sample :
                if sample_alias[i] ==j[1]:
                    sample_id = j[0]
            manifest.write('STUDY\t'+study_id+'\n') 
            manifest.write('SAMPLE\t'+sample_id+'\n')
            sup_metadata = list(metadata.iloc[i])
            for j in range(header_2.index('experiment_name'),header_2.index('uploaded file 2')+1):
                if header_2[j]== 'experiment_name' :
                    manifest.write('NAME\t'+str(sup_metadata[j])+'\n')
                elif header_2[j]== 'uploaded file 1':
                    fq1 = 1
                    if sup_metadata[j] != -1 :
                        manifest.write('FASTQ\t'+str(sup_metadata[j])+'\n')
                    else:
                        fq1 = 0
                elif header_2[j]== 'uploaded file 2': 
                    fq2 = 1
                    if sup_metadata[j] != -1 :
                        manifest.write('FASTQ\t'+str(sup_metadata[j])+'\n')
                    else :
                        fq2 = 0 
                elif header_2[j].upper()== 'SEQUENCING_PLATFORM' and sup_metadata[j] != -1  :
                    manifest.write('PLATFORM\t'+str(sup_metadata[j])+'\n')
                elif header_2[j].upper()== 'SEQUENCING_INSTRUMENT' and sup_metadata[j] != -1  :
                    manifest.write('INSTRUMENT\t'+str(sup_metadata[j])+'\n')
                elif header_2[j].upper()== 'LIBRARY_DESCRIPTION' and sup_metadata[j] != -1  :
                    manifest.write('DESCRIPTION\t'+str(sup_metadata[j])+'\n')
                elif sup_metadata[j] != -1 :
                    manifest.write(header_2[j].upper()+'\t'+str(sup_metadata[j])+'\n')
            manifest.close()
            
            if fq1 != 0 and fq2 != 0 :
                if t == '-t':
                    os.system("java -jar modules/webin-cli-5.2.0.jar -context reads -manifest "+directory+"/manifest_run"+str(i-4)+".txt -inputDir "+directory+" -userName "+webin_accout+" -password '"+suppasswd+"' -test -validate")
                    print('\n')
                    os.system("java -jar modules/webin-cli-5.2.0.jar -context reads -manifest "+directory+"/manifest_run"+str(i-4)+".txt -inputDir "+directory+" -userName "+webin_accout+" -password '"+suppasswd+"' -test -submit")
                else :
                    os.system("java -jar modules/webin-cli-5.2.0.jar -context reads -manifest "+directory+"/manifest_run"+str(i-4)+".txt -inputDir "+directory+" -userName "+webin_accout+" -password '"+suppasswd+"'  -validate")
                    print('\n')
                    os.system("java -jar modules/webin-cli-5.2.0.jar -context reads -manifest "+directory+"/manifest_run"+str(i-4)+".txt -inputDir "+directory+" -userName "+webin_accout+" -password '"+suppasswd+"'  -submit")
                print('\n\n')
            else :
                print('\033[91m'+str(i-4)+' _No Fastq File')
                print('\033[0m')
            # os.system('rm '+directory+'/manifest_run.txt')    
    
        print('\033[92m'+'DONE...\n') 
        print('\033[0m')
        
        # submission of analysis 
        
        if str(' '.join([str(e) for e in header_2])).find('assemblyname') != -1 :
            print ('\n\n')
            print ('\033[93m'+'\t\t+--------------------------------------------------------------------------------------------------------------+')
            print ('\033[93m'+'\t\t|****************************************     SUBMISSION OF ANALYSIS    ***************************************|')
            print ('\033[93m'+'\t\t+--------------------------------------------------------------------------------------------------------------+')
            print ('\n\n')
            print('\033[0m')
            
            for i in range(5,len(sample_alias)):
                print('\n\n')
                if sample_alias[i] == -1 :
                    break
                directory = '/'.join(file.split('/')[0:len(file.split('/'))-1])
                manifest = open(directory+'/manifest_analysis'+str(i-4)+'.txt','w')
                study_id = ''
                sample_id = ''
                for j in res_study : 
                    if study_alias[i] == j[1]:
                        study_id = j[0]
                        break
                for j in res_sample :
                    if sample_alias[i] ==j[1]:
                        sample_id = j[0]
                res_run = a.select_1('run_id','run_sample',"sample_id in ('"+sample_id+"')")
                run_id = ''
                for j in res_run:
                    run_id = j[0] 
                manifest.write('STUDY\t'+study_id+'\n') 
                manifest.write('SAMPLE\t'+sample_id+'\n')
                if run_id != '':
                    manifest.write('RUN_REF\t'+run_id+'\n')
                sup_metadata = list(metadata.iloc[i])
                for j in range(header_2.index('assemblyname'),header_2.index('fasta/flatfile name')+1):
                    if header_2[j]== 'run_ref' :
                        pass
                    elif header_2[j]== 'fasta/flatfile name':
                        fa = 1
                        if sup_metadata[j] != -1 :
                            manifest.write('FASTA\t'+str(sup_metadata[j])+'\n')
                        else :
                            fa = 0
                    elif sup_metadata[j] != -1  :
                        manifest.write(header_2[j].upper()+'\t'+str(sup_metadata[j])+'\n')
                manifest.write('CHROMOSOME_LIST\t'+str(sup_metadata[header_2.index('fasta/flatfile name')]).split('.fasta')[0]+'_chrm_list.txt.gz\n')
                CHROMOSOME_LIST = open(directory+'/'+str(sup_metadata[header_2.index('fasta/flatfile name')]).split('.fasta')[0]+'_chrm_list.txt','w')
                CHROMOSOME_LIST.write(str(sup_metadata[header_2.index('assemblyname')])+'\t1\tMonopartite')
                CHROMOSOME_LIST.close()
                print('\033[92m'+'\nPress y then enter ...')
                print ('\033[93m')
                os.system('cd ' +directory+' ; gzip '+str(sup_metadata[header_2.index('fasta/flatfile name')]).split('.fasta')[0]+'_chrm_list.txt')
                print('\033[0m')
                manifest.close()
                if fa != 0:
                    if t == '-t':
                        os.system("java -jar modules/webin-cli-5.2.0.jar -context genome -manifest "+directory+"/manifest_analysis"+str(i-4)+".txt -inputDir "+directory+" -userName '"+webin_accout+"' -password '"+suppasswd+"' -test -validate")
                        print('\n')
                        os.system("java -jar modules/webin-cli-5.2.0.jar -context genome -manifest "+directory+"/manifest_analysis"+str(i-4)+".txt -inputDir "+directory+" -userName '"+webin_accout+"' -password '"+suppasswd+"' -test -submit")
                    else :
                        os.system("java -jar modules/webin-cli-5.2.0.jar -context genome -manifest "+directory+"/manifest_analysis"+str(i-4)+".txt -inputDir "+directory+" -userName '"+webin_accout+"' -password '"+suppasswd+"' -validate")
                        print('\n')
                        os.system("java -jar modules/webin-cli-5.2.0.jar -context genome -manifest "+directory+"/manifest_analysis"+str(i-4)+".txt -inputDir "+directory+" -userName '"+webin_accout+"' -password '"+suppasswd+"' -submit")
                    print('\n\n')
                else :
                    print('\033[91m'+str(i-4)+' _No Fasta File')
                    print('\033[0m')
                # os.system('rm '+directory+'/manifest_analysis.txt')
            
        print('\033[92m'+'DONE...\n') 
        end = datetime.now()
        print('\033[92m'+'[ '+str(start)+' ] Start time ...')
        print('\033[0m')
        print('\033[92m'+'[ '+str(end)+' ] End time ...')
        print('\033[0m')
        print('\033[0m')
        
        a.close()
        

