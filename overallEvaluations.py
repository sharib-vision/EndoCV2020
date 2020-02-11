#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 11:22:09 2019

@author: shariba

"""

import json
    
def get_args():
    import argparse
    parser = argparse.ArgumentParser(description="For EAD2019 challenge: semantic segmentation", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--detectionMetric", type=str, default="../Result_test/metrics_det_EAD2020.json", help="json file for detection")
    parser.add_argument("--generalizationMetric", type=str, default="../Result_test/metric_gen_score.json", help="json file for generalization")
#    parser.add_argument("--semantic_detection", type=str, default="mAP-IOU_EAD2019_results/metrics_detection.json", help="son file for segmentation")
    parser.add_argument("--semanticMetric", type=str, default="../Result_test/metrics_sem.json", help="son file for segmentation")
    parser.add_argument("--caseType", type=int, default=3, help="please set 0: only for dection both balanced, 1: only for instance segmentation only, 2: for generalization, 3: for all tasks")
    parser.add_argument("--Result_dir", type=str, default="finalEvaluationScores", help="all evaluation scores used for grading")
    parser.add_argument("--jsonFileName", type=str, default="metrics.json", help="all evaluation scores used for grading")
    args = parser.parse_args()
    return args

def read_json(jsonFile):
    with open(jsonFile) as json_data:
        data = json.load(json_data)
        return data
    
if __name__ == '__main__':
    import os
    
    valArgs = get_args()
    mAP_d = 0
    mAP_d_25=0
    mAP_d_50=0
    mAP_d_75=0
    IOU_d = 0
    overlap = 0
    semScore = 0
    mAP_g = 0
    score_d = 0
    F1score=0
    F2score=0
    PPV=0
    Recall = 0
    scoreSemantic=0
    mAP_d_std=0
    score_g = 0
    debug = 1
    semScore_mean_dev=0
    
    print("detected case type", )
    
    """ case: Detection """
    if valArgs.caseType == 0 or valArgs.caseType == 3 or valArgs.caseType == 2 or valArgs.caseType == 4 or valArgs.caseType == 5:
        exists = os.path.isfile(valArgs.detectionMetric)
        if exists:
            data = read_json(valArgs.detectionMetric)
            valAppend = []
            for p in data["EndoCV2020"].values():
                valAppend.append(p)
            scoreDetection = valAppend[2]['value']*0.01
            if debug:
                print('final score is computed for detection, (task-I, EndoCV2020 challenge)')
                print('your score is:', valAppend[2]['value']*0.01)
                
                print('~~~~~~~~~~~~~~~Complimentary informations~~~~~~~~~~~~~~~')
                print('mean mAP:', valAppend[0]['value']*0.01)
                print('mean IOU:', valAppend[1]['value']*0.01)
                print('~~~~~~~~~~~~~~~~~~~~~~~~E.O.F~~~~~~~~~~~~~~~~~~~~~~~~~~')
                print('All scores are saved in json files, see dir:', valArgs.Result_dir)
        
            mAP_d = valAppend[0]['value']*0.01
            IOU_d = valAppend[1]['value']*0.01
            
            # sub-scores for different IoU thresholds [25,50,75]
            mAP_d_25 = valAppend[2]['value']*0.01
            mAP_d_50 = valAppend[4]['value']*0.01
            mAP_d_75 = valAppend[6]['value']*0.01
            
            mAP_d_std = valAppend[9]['value']*0.01
        
    """ case: Semantic """
    if valArgs.caseType == 1 or valArgs.caseType == 3 or valArgs.caseType == 5:
        exists = os.path.isfile(valArgs.semanticMetric)
        if exists:
            data = read_json(valArgs.semanticMetric)
            valAppend_Semantic=[]
            for p in data["EndoCV2020"].values():
                valAppend_Semantic.append(p)
                    
            # compute scores
            F1score=valAppend_Semantic[0]['value']
            F2score=valAppend_Semantic[2]['value']
            PPV = valAppend_Semantic[3]['value']
            Recall = valAppend_Semantic[4]['value']
            scoreSemantic = (F1score+ F2score+ PPV + Recall)/4.0
            
            # compute mean deviation
            F1score_dev=valAppend_Semantic[6]['value']
            F2score_dev=valAppend_Semantic[8]['value']
            PPV_dev = valAppend_Semantic[9]['value']
            Recall_dev = valAppend_Semantic[10]['value']
            semScore_mean_dev = (F1score_dev+F2score_dev+PPV_dev + Recall_dev)/4
            
            if debug:
                print ('overall score for instance segmentation for EndoCV202 challenge is:', scoreSemantic)
                print('~~~~~~~~~~~~~~~Complimentary informations~~~~~~~~~~~~~~~')
                print('number of semantic samples:', len(data))
                print('mean F1: {}, F2: {}, PPV: {}, Recall: {}:'.format(F1score, F2score, PPV, Recall))
                print('~~~~~~~~~~~~~~~~~~~~~~E.O.F~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        
            F2_score = valAppend_Semantic[2]['value']
            
            if (valArgs.caseType == 1):
                ratioPass = 0
                
            """ case: Generalization """
    if  valArgs.caseType == 3 or valArgs.caseType == 4:
        exists = os.path.isfile(valArgs.generalizationMetric)
        if exists:
            data = read_json(valArgs.generalizationMetric)
            valGen = []
            for p in data["EndoCV2020"].values():
                valGen.append(p)
                
            if debug:
                print('~~~~~~~~~~~~~~~Complimentary informations~~~~~~~~~~~~~~~')
                print('mean mAP:', valGen[0]['value'])
                print('mean score_g:', valGen[1]['value'])
                print('~~~~~~~~~~~~~~~E.O.F~~~~~~~~~~~~~~~')
  
            mAP_g = valGen[0]['value']
            score_g = valGen[1]['value']
#    
#    else:
#        print('no multi-class artefact detection found, mAPs are required for scoring both segmentation and generalization tasks')
#        
    '''
    creating json file
    '''
    # TODO: Loop this for 
    my_dictionary = {
        "EndoCV2020":{
                "mAP_d":{
                 "value":  (mAP_d) 
                },
                "IOU_d":{
                  "value": (IOU_d)
                },
                "mAP_d25":{
                 "value":  (mAP_d_25) 
                },
                "mAP_d50":{
                 "value":  (mAP_d_50) 
                },
                "mAP_d75":{
                 "value":  (mAP_d_75) 
                },
                "dice":{
                 "value":  (F1score) 
                },
                "F2-score":{
                 "value":   (F2score) 
                },
                "PPV":{
                 "value":   (PPV) 
                },
                "Recall":{
                  "value": (Recall)
                },
                "Sem_score":{
                  "value": (scoreSemantic)
                },
                "Sem_score_dev":{
                  "value": (semScore_mean_dev)
                },
                "mAP_g":{
                  "value": (mAP_g)
                },
                "dev_g":{
                  "value": (score_g)
                },
                "mAP_d_std":{
                  "value": (mAP_d_std)
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
    
            
            
        
        
