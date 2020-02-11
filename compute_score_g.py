#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 20:00:30 2019

@author: shariba
"""


import json

def computeDeviation(pDetect, pGener, tol_limit):
    """ per class deviation measurer"""
    expectedToleranceplus = pDetect+tol_limit*0.01*pDetect
    expectedToleranceminus = pDetect-tol_limit*0.01*pDetect
    
    if (pGener <= expectedToleranceplus and pGener >= expectedToleranceminus):
        deviation = 0
        print('within tolerance range, not penalized')
    else:
        deviation = abs(expectedToleranceminus-pGener)
    return deviation
        
    
def get_args():
    import argparse
    parser = argparse.ArgumentParser(description="For EAD2019 challenge: generalization scoring", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--detectionMetric", type=str, default="../Result_test/metrics_det_EAD2020.json", help="json file for detection")
    parser.add_argument("--generalizationMetric", type=str, default="../Result_test/metrics_gen_EAD2020.json", help="json file for generalization")
    parser.add_argument("--Result_dir", type=str, default="../Result_test_final", help="all evaluation scores used for grading")
    parser.add_argument("--jsonFileName", type=str, default="metric_gen_score.json", help="all evaluation scores used for grading")
    
    args = parser.parse_args()
    
    return args

def read_json(jsonFile):
    with open(jsonFile) as json_data:
        data = json.load(json_data)
        return data
    
if __name__ == '__main__':
    import os
    import numpy as np

#    deviation = computeDeviation(0.35, 0.35, 5)
    
    valArgs = get_args()
    exists_detect = os.path.isfile(valArgs.detectionMetric)
    exists_generalization = os.path.isfile(valArgs.generalizationMetric)
    perClassDeviation = []
    arrayNames = ["instrument", "artifact", "blur", "bubbles", "contrast", "saturation", "specularity"]
    if exists_detect and exists_generalization:
        data_det = read_json(valArgs.detectionMetric) 
        data_gen = read_json(valArgs.generalizationMetric) 
        valAppend_det = []
        valAppend_gen = []
        for p in data_det["EndoCV2020"].values():
            valAppend_det.append(p)
        for p in data_gen["EndoCV2020"].values():
            valAppend_gen.append(p)
        
        mAP_d=valAppend_det[0]['value']*0.01
        mAP_g=valAppend_gen[0]['value']*0.01
        
        # tolerance limit of 10% is provided
        tol_limit = 10
        for i in range (0, len(arrayNames)):
            deviation = computeDeviation(valAppend_det[8]['value'][arrayNames[i]], valAppend_gen[8]['value'][arrayNames[i]], tol_limit)
            perClassDeviation.append(deviation)
            
        # per class deviation
        meanDeviation = np.mean(perClassDeviation)
        
    else:
        print('generalization or detection file missing, both files are needed to compute this score')
    
    '''
    creating json file
    '''
    if exists_detect and exists_generalization:
        my_dictionary = {
            "EndoCV2020":{
                    "mAP_g":{
                     "value":(mAP_g) 
                    },
                    "score_g":{
                      "value": (meanDeviation),  
                    } 
                }
        }           
        # append json file             
        os.makedirs(valArgs.Result_dir, exist_ok=True)
        jsonFileName=os.path.join(valArgs.Result_dir, valArgs.jsonFileName)
        fileObj= open(jsonFileName, "a")
        fileObj.write("\n")
        json.dump(my_dictionary, fileObj)
        fileObj.close()