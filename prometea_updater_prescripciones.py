#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 13:21:17 2019

@author: Miguel Salinas Gancedo
"""

import datetime
import pandas as pd

from tqdm import tqdm
from pymongo import MongoClient
        
# Datasets with interconsultas
# - PROMETEA_Prostata.mdb [prueba, fecha]

if __name__ == '__main__':
    init = datetime.datetime.now()
           
    # connect to MongoDB prometea database
    print('STEP 01: Get all Prometea MongoDB Pacientes')
    print('---------------------------------------------')
    client = MongoClient(port=27017)
    db=client.prometeadb
    collection = db['Paciente']
    pacientes = collection.find({})
    #pacientes = collection.find({'centro': '05010110', 'nhc': '1003'})    
    print()
       
    # Iterate over parent datasets
    print('STEP 03: Start Merge Prescripciones Dataset')    
    print('--------------------------------------')
    # updtae child interconsultas dataset
    pbar = tqdm(total=pacientes.count(), desc='Prescripciones Dataset')
    num = 0
    
    for paciente in pacientes:
        try:
            key = 0
            for prescripcion in paciente['prescripciones']:
                if pd.isnull(prescripcion['fecha']) == True:
                    fecha = None
                else:    
                    fecha = prescripcion['fecha'][:6] + '20' + prescripcion['fecha'][6:]
                    fecha = datetime.datetime.strptime(fecha, '%m/%d/%Y %H:%M:%S')
                
                if pd.isnull(prescripcion['fechaCierre']) == True:
                    fechaCierre = None
                else:    
                    fechaCierre = prescripcion['fechaCierre'][:6] + '20' + prescripcion['fechaCierre'][6:]
                    fechaCierre = datetime.datetime.strptime(fechaCierre, '%m/%d/%Y %H:%M:%S')
                
                db.Paciente.find_and_modify({'_id': paciente['_id']},
                                             {'$set': {'prescripciones.' + str(key) + '.fecha': fecha,
                                                       'prescripciones.' + str(key) + '.fechaCierre': fechaCierre}})
                        
                key = key + 1
        except:
            print(paciente)        
            
        # update progress bar and num instances inserted
        num = num + 1
                
        # update instance checked
        pbar.update(1)
              
    # close progress bar
    pbar.close()              
    print()
    
    print('Update ' + str(num) + ' Prescripciones' + ' en ' + str(datetime.datetime.now() - init)) 