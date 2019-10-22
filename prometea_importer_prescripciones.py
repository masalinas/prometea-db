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
# - PROMETEA_Cardiopatia.mdb [cap, capit, subcap, codter, codatc, codnac, tipoACD, tipoTE, fecha, fechaCierre]
# - PROMETEA_Diabetes.mdb    [cap, capit, subcap, codter, codatc, codnac, tipoACD, tipoTE, fecha, fechaCierre]
# - PROMETEA_Epoc.mdb        [cap, capit, subcap, codter, codatc, codnac, tipoACD, tipoTE, Fecha_creacion, Fecha_cierre]
# - PROMETEA_Prostata.mdb    [cap, capit, subcap, codter, codatc, codnac, tipoACD, tipoTE, fecha, fechaCierre]
        
if __name__ == '__main__':
    init = datetime.datetime.now()
    
    # load command argument configurations
    parser = argparse.ArgumentParser(description='Prometa Prescripciones Importer', epilog='Example of use: python3 prometea_importer_prescipciones.py -d <DATASET_MDB_FILE>')    
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
    print('Loading Prometea Prescripciones Dataset from ' + args.dataset)    
    dataset = mdb.read_table(args.dataset, 'prescripciones')        
    print()
          
    # Iterate over parent datasets
    print('STEP 03: Start Merge Prescripciones Dataset')    
    print('--------------------------------------')
    
    # insert child pacientes dataset
    pbar = tqdm(total=dataset.shape[0], desc='Prescripciones Dataset')
    num = 0
    
    for index, rows in dataset.iterrows(): 
        db.Pacientes.update_one({'centro': rows.centro, 'nhc': rows.nhc}, 
                                {'$push': {'prescripciones': {'enfermedad': 'prostata',
                                                              'cap': rows.cap, 
                                                              'capit': rows.capit, 
                                                              'subcap': rows.subcap, 
                                                              'codter': rows.codter, 
                                                              'codatc': rows.codatc, 
                                                              'codnac': rows.codnac, 
                                                              'tipoACD': rows.tipoACD, 
                                                              'tipoTE': rows.tipoTE, 
                                                              'fecha': rows.fecha,
                                                              'fechaCierre': rows.fechaCierre}}})
        
        # update progress bar and num instances inserted
        num = num + 1
        
        # update instance checked
        pbar.update(1)
              
    # close progress bar
    pbar.close()              
    
    duration = datetime.datetime.now() - init
    print('Import ' + str(num) + ' Prescripciones' + ' en ' + str(duration))