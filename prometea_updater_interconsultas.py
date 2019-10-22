#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 13:21:17 2019

@author: Miguel Salinas Gancedo
"""

import datetime

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
    #pacientes = collection.find({'centro': '05010110', 'nhc': '11792'})
    #pacientes = collection.find({'centro': '05010110', 'nhc': '1003'})    
    print()
       
    # Iterate over parent datasets
    print('STEP 03: Start Merge Interconsultas Dataset')    
    print('--------------------------------------')
    # updtae child interconsultas dataset
    pbar = tqdm(total=pacientes.count(), desc='Interconsultas Dataset')
    num = 0
    
    for paciente in pacientes:
        try:
            key = 0
            for interconsulta in paciente['interconsultas']:
                fecha = interconsulta['fecha'][:6] + '20' + interconsulta['fecha'][6:]
                fecha = datetime.datetime.strptime(fecha, '%m/%d/%Y %H:%M:%S')
                
                db.Paciente.find_and_modify({'_id': paciente['_id']},
                                             {'$set': {'interconsultas.' + str(key) + '.fecha': fecha,
                                                       'interconsultas.' + str(key) + '.enfermedad': 'prostata'}})
                        
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
    
    print('Import ' + str(num) + ' Interconsultas' + ' en ' + str(datetime.datetime.now() - init)) 