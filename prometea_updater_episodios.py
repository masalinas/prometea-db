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
    #pacientes = collection.find({})
    pacientes = collection.find({'centro': '05080510', 'nhc': '7434'})    
    print()
       
    # Iterate over parent datasets
    print('STEP 03: Start Merge Episodios Dataset')    
    print('--------------------------------------')
    # updtae child interconsultas dataset
    pbar = tqdm(total=pacientes.count(), desc='Episodios Dataset')
    num = 0
    
    for paciente in pacientes:
        key = 0
        for episodio in paciente['episodios']:
            try:
                if pd.isnull(episodio['fecha']) == True:
                    fecha = None
                else:    
                    if int(episodio['fecha'][6:8]) == 0 :
                        fecha = episodio['fecha'][:6] + '18' + episodio['fecha'][6:]
                        fecha = datetime.datetime.strptime(fecha, '%m/%d/%Y %H:%M:%S')
                    else:
                        if int(episodio['fecha'][6:8]) > 19 :
                            fecha = episodio['fecha'][:6] + '19' + episodio['fecha'][6:]
                            fecha = datetime.datetime.strptime(fecha, '%m/%d/%Y %H:%M:%S')                    
                        else:
                            fecha = episodio['fecha'][:6] + '20' + episodio['fecha'][6:]
                            fecha = datetime.datetime.strptime(fecha, '%m/%d/%Y %H:%M:%S')
                
                if pd.isnull(episodio['alta']) == True:
                    alta = None
                else:    
                    if int(episodio['alta'][6:8]) == 0 :
                        alta = episodio['alta'][:6] + '18' + episodio['alta'][6:]
                        alta = datetime.datetime.strptime(alta, '%m/%d/%Y %H:%M:%S')
                    else:
                        if int(episodio['alta'][6:8]) > 19 :
                            alta = episodio['alta'][:6] + '19' + episodio['alta'][6:]
                            alta = datetime.datetime.strptime(alta, '%m/%d/%Y %H:%M:%S')
                        else:
                            alta = episodio['alta'][:6] + '20' + episodio['alta'][6:]
                            alta = datetime.datetime.strptime(alta, '%m/%d/%Y %H:%M:%S')
                
                db.Paciente.find_and_modify({'_id': paciente['_id']},
                                             {'$set': {'episodios.' + str(key) + '.fecha': fecha,
                                                       'episodios.' + str(key) + '.alta': alta}})
                        
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
    
    print('Update ' + str(num) + ' Episodios' + ' en ' + str(datetime.datetime.now() - init)) 