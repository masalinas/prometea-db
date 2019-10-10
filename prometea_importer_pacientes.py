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
        
if __name__ == '__main__':
    init = datetime.datetime.now()
    
    # load command argument configurations
    parser = argparse.ArgumentParser(description='Prometa Pacientes Importer', epilog='Example of use: python3 prometea_importer_pacientes.py -d <DATASET_MDB_FILE>')    
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
    datasetPaciente = mdb.read_table(args.dataset, "Pacientes")        
    print()
          
    # Iterate over parent datasets
    print('STEP 03: Start Merge Pacientes Dataset')    
    print('--------------------------------------')
    # insert child pacientes dataset
    pbar = tqdm(total=datasetPaciente.shape[0], desc='Pacientes Dataset')
    num = 0
    
    for index, rows in datasetPaciente.iterrows(): 
        # get paciente if exist
        paciente = db.Pacientes.find_one({'centro': rows.centro, 'nhc': rows.nhc, 'cias': rows.CIAS})
        
        # if not exist the paciente insert the new one
        if paciente is None:
            # insert new paciente
            db.Pacientes.insert_one({'centro': rows.centro, 
                                     'nhc': rows.nhc, 
                                     'sexo': rows.sexo,
                                     'cias': rows.CIAS,
                                     'ubicacion': rows.ubicacion,
                                     'tipopac': rows.tipopac,                                 
                                     'nacimiento': rows.nacimiento,
                                     'exitus': rows.exitus,
                                     'episodios': [],
                                     'interconsultas': [],
                                     'prescripciones': [],
                                     'dgps': []})

            # update progress bar and num instances inserted
            num = num + 1
        
        # update instance checked
        pbar.update(1)
              
    # close progress bar
    pbar.close()              
    
    duration = datetime.datetime.now() - init
    print('Import ' + str(num) + ' pacientes' + ' en ' + str(duration))    