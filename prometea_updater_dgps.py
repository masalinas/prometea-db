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
    #pacientes = collection.find({'centro': '05080510', 'nhc': '5840'})    
    print()
       
    # Iterate over parent datasets
    print('STEP 03: Start Merge DGPs Dataset')    
    print('--------------------------------------')
    # updtae child interconsultas dataset
    pbar = tqdm(total=pacientes.count(), desc='DGPs Dataset')
    num = 0
    
    for paciente in pacientes:
        try:
            key = 0
            for dgp in paciente['dgps']:
                if pd.isnull(dgp['fecha']) == True:
                    fecha = None
                else:    
                    dia = dgp['fecha'][0:2]
                    mes = dgp['fecha'][3:5]
                    if int(dgp['fecha'][0:2]) == 12 and int(dgp['fecha'][3:5]) == 28:
                        fecha = dgp['fecha'][:6] + '18' + dgp['fecha'][6:]
                        fecha = datetime.datetime.strptime(fecha, '%m/%d/%Y %H:%M:%S')
                    else:
                        if int(dgp['fecha'][6:8]) > 19 :
                            fecha = dgp['fecha'][:6] + '19' + dgp['fecha'][6:]
                            fecha = datetime.datetime.strptime(fecha, '%m/%d/%Y %H:%M:%S')                    
                        else:
                            fecha = dgp['fecha'][:6] + '20' + dgp['fecha'][6:]
                            fecha = datetime.datetime.strptime(fecha, '%m/%d/%Y %H:%M:%S')                            
                            
                    db.Paciente.find_and_modify({'_id': paciente['_id']},
                                                {'$set': {'dgps.' + str(key) + '.fecha': fecha}})
                        
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
    
    print('Update ' + str(num) + ' DGPs' + ' en ' + str(datetime.datetime.now() - init))