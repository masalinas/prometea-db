#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 13:21:17 2019

@author: Miguel Salinas Gancedo
"""

from datetime import datetime
import argparse

import pandas as pd
import pandas_access as mdb
from tqdm import tqdm
from pymongo import MongoClient
        
if __name__ == '__main__':
    init = datetime.now()
    
    # load command argument configurations
    parser = argparse.ArgumentParser(description='Prometa Pacientes Updater', epilog='Example of use: python3 prometea_updater_pacientes.py -d <DATASET_MDB_FILE>')    
    parser.add_argument('-d', '--dataset', type=str, help='Prometea Dataset filer')

    args = parser.parse_args()
            
    # connect to MongoDB prometea database
    print('STEP 01: Connect to Prometea MongoDB database')
    print('---------------------------------------------')
    client = MongoClient(port=27017)
    db=client.prometeadb
    print()

    # load to MS Access prometea database        
    print('STEP 02: Load Prometea MS Access dataset')
    print('----------------------------------------')
    print('Loading Prometea Pacientes Dataset from ' + args.dataset)    
    datasetPaciente = mdb.read_table(args.dataset, 'Pacientes')        
    print()
          
    # Iterate over parent datasets
    print('STEP 03: Start Update Pacientes Dataset')    
    print('--------------------------------------')
    # insert child pacientes dataset
    pbar = tqdm(total=datasetPaciente.shape[0], desc='Pacientes Dataset')
    num = 0
    
    for index, rows in datasetPaciente.iterrows(): 
        # get first paciente from centro and nhc
        paciente = db.Pacientes.find_one({'centro': rows.centro, 'nhc': rows.nhc})
        
        # if not exist the paciente insert the new one
        if paciente is None:
            try:
                # convert string to date
                if (int(rows.F_nacimiento[6:8]) < 19):
                    nacimiento = datetime.strptime(rows.F_nacimiento[:6] + '20' + rows.F_nacimiento[6:], '%m/%d/%Y %H:%M:%S')                
                else:
                    nacimiento = datetime.strptime(rows.F_nacimiento[:6] + '19' + rows.F_nacimiento[6:], '%m/%d/%Y %H:%M:%S')
                    
                # update paciente dates
                if pd.isnull(rows.F_exitus) == True:                                
                    db.Paciente.update_one({'centro': rows.centro, 'nhc': rows.nhc}, 
                                           {'$set': {'nacimiento': nacimiento}})
                else:                 
                    #exitus = datetime.strptime(rows.F_exitus, '%d/%m/%Y')
                    if (int(rows.F_exitus[6:8]) < 19):
                        exitus = datetime.strptime(rows.F_exitus[:6] + '20' + rows.F_exitus[6:], '%m/%d/%Y %H:%M:%S')
                    else:
                        exitus = datetime.strptime(rows.F_exitus[:6] + '19' + rows.F_exitus[6:], '%m/%d/%Y %H:%M:%S')
                    
                    db.Paciente.update_one({'centro': rows.centro, 'nhc': rows.nhc}, 
                                           {'$set': {'nacimiento': nacimiento, 'exitus': exitus}})
                                    
                # update progress bar and num instances updated
                num = num + 1
            except:
                    print(rows)
        
        # update instance checked
        pbar.update(1)
              
    # close progress bar
    pbar.close()              
    
    duration = datetime.now() - init
    print('Update ' + str(num) + ' pacientes' + ' en ' + str(duration))   