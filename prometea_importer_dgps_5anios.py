#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 13:21:17 2019

@author: Miguel Salinas Gancedo
"""

import datetime
import argparse

import pandas_access as mdb
from tqdm import tqdm
from pymongo import MongoClient

# Datasets with episodios 
# - PROMETEA_Cardiopatia.mdb [dgp, dgpTxt, valor, fecha]
# - PROMETEA_Diabetes.mdb    [dgp, dgpTxt, valor, fecha]
# - PROMETEA_Prostata.mdb    [dgp, dgpTxt, valor, fecha]
        
if __name__ == '__main__':
    init = datetime.datetime.now()
    
    # load command argument configurations
    parser = argparse.ArgumentParser(description='Prometa DGP 5 Años Importer', epilog='Example of use: python3 prometea_importer_dgps_5anios.py -d <DATASET_MDB_FILE>')    
    parser.add_argument('-d', '--dataset', type=str, help='Prometea Dataset file')

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
    print('Loading Prometea DGP 5 Años Dataset from ' + args.dataset)    
    dataset = mdb.read_table(args.dataset, 'DGP_5Anios')
    print()
          
    # Iterate over parent datasets
    print('STEP 03: Start Merge DGP 5 Años Dataset')    
    print('--------------------------------------')
    
    # insert child pacientes dataset
    pbar = tqdm(total=dataset.shape[0], desc='DGP 5 Años Dataset')
    num = 0
    
    for index, rows in dataset.iterrows(): 
        db.Paciente.update_one({'centro': rows.centro, 'nhc': rows.nhc}, 
                                {'$push': {'dgps': {'enfermedad': 'prostata', 
                                                    'dgp': rows.dgp, 
                                                    'dgpTxt': rows.dgpTxt, 
                                                    'valor': rows.valor, 
                                                    'fecha': rows.fecha}}})
        
        # update progress bar and num instances inserted
        num = num + 1
        
        # update instance checked
        pbar.update(1)
              
    # close progress bar
    pbar.close()              
    
    duration = datetime.datetime.now() - init
    print('Import ' + str(num) + ' DGP 5 Años' + ' en ' + str(duration))