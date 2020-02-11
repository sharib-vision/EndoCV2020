#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 16:06:39 2019

@author: shariba
FileName: semanticEval_dice_Jaccard_Overall.py
"""

import numpy as np
import sklearn

print('The scikit-learn version is {}.'.format(sklearn.__version__))

def _assert_valid_lists(groundtruth_list, predicted_list):
    assert len(groundtruth_list) == len(predicted_list)
    for unique_element in np.unique(groundtruth_list).tolist():
        assert unique_element in [0, 1]

def _all_class_1_predicted_as_class_1(groundtruth_list, predicted_list):
    _assert_valid_lists(groundtruth_list, predicted_list)
    return np.unique(groundtruth_list).tolist() == np.unique(predicted_list).tolist() == [1]

def _all_class_0_predicted_as_class_0(groundtruth_list, predicted_list):
    _assert_valid_lists(groundtruth_list, predicted_list)
    return np.unique(groundtruth_list).tolist() == np.unique(predicted_list).tolist() == [0]

def get_confusion_matrix_elements(groundtruth_list, predicted_list):
    """returns confusion matrix elements i.e TN, FP, FN, TP as floats
	See example code for helper function definitions
    """
    _assert_valid_lists(groundtruth_list, predicted_list)
    if _all_class_1_predicted_as_class_1(groundtruth_list, predicted_list) is True:
        tn, fp, fn, tp = 0, 0, 0, np.float64(len(groundtruth_list))
    elif _all_class_0_predicted_as_class_0(groundtruth_list, predicted_list) is True:
        tn, fp, fn, tp = np.float64(len(groundtruth_list)), 0, 0, 0
    else:
        tn, fp, fn, tp = sklearn.metrics.confusion_matrix(groundtruth_list, predicted_list).ravel()
        tn, fp, fn, tp = np.float64(tn), np.float64(fp), np.float64(fn), np.float64(tp)
    return tn, fp, fn, tp

def cv2_HDistance(gt, pred):
    import cv2
    _, ca, _ = cv2.findContours(gt, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS) 
    _, ca, _ = cv2.findContours(pred, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS) 
    hd = cv2.createHausdorffDistanceExtractor()
    return hd

def print_debug(dice_valPerImage, jaccard_valPerImage,f2_valPerImage, PPV_perImage, recall_perImage, distance_perImage, debug):
    if debug:
        print('mean dice score', np.mean(dice_valPerImage))
        print('mean iou score', np.mean(jaccard_valPerImage))
        print('mean f2 score', np.mean(f2_valPerImage)) 
        print('mean precision/ppv score', np.mean(PPV_perImage))
        print('mean recall score', np.mean(recall_perImage)) 
        print('mean distance based metric', np.mean(distance_perImage)) 
        # compute standard deviations observed/image in each cases
        print('mean std dice score', np.std(dice_valPerImage))
        print('mean std iou score', np.std(jaccard_valPerImage))
        print('mean std f2 score', np.std(f2_valPerImage)) 
        print('mean std precision/ppv score', np.std(PPV_perImage))
        print('mean std recall score', np.std(recall_perImage)) 
        print('mean std distance based metric', np.std(distance_perImage)) 

def get_args():
    
    import argparse
    parser = argparse.ArgumentParser(description="For EAD2019 challenge: semantic segmentation", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--GT_maskDIR", type=str, default="../groundTruths_EAD2019/semantic_masks/", help="ground truth mask image (5 channel tif image only)")
    parser.add_argument("--Eval_maskDIR", type=str, default="../detection_bbox/semantic_masks/", help="predicted mask image (5 channel tif image only)")
    parser.add_argument("--Result_dir", type=str, default="results", help="predicted mask image (5 channel tif image only)")
    parser.add_argument("--jsonFileName", type=str, default='metrics_semantic.json', help="predicted mask image (5 channel tif image only)")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    import tifffile as tiff
    import glob
    import os
#    https://scikit-learn.org/stable/modules/model_evaluation.html
    from sklearn.metrics import precision_recall_fscore_support 
    from sklearn.metrics import fbeta_score
    from sklearn.metrics import jaccard_score
    
    result_dice = []
    result_jaccard = []
    classTypes=['Instrument', 'Specularity', 'Artefact' , 'Bubbles', 'Saturation'] 
    args=get_args()
    ext=['*.tif']
    
    epsilon = 0.0000001
    dice_valPerImage =[]
    jaccard_valPerImage=[]
    f2_valPerImage = [] 
    PPV_perImage=[]
    recall_perImage=[]
    distance_perImage=[]
    distance_=[]
    for filename in sorted(glob.glob(args.GT_maskDIR +ext[0], recursive = True)):
        file_name_GT = args.GT_maskDIR+filename.split('/')[-1]
        file_name_eval_maskImage = args.Eval_maskDIR+filename.split('/')[-1] 
        
        y_true_Array = tiff.imread(file_name_GT)
        y_pred_Array = tiff.imread(file_name_eval_maskImage)

        Apred = ((y_pred_Array > 0).astype(np.uint8)).flatten()
        Btrue = ((y_true_Array > 0).astype(np.uint8)).flatten()
        #
        #val_hausD = directed_hausdorff(np.reshape(Btrue, [Btrue.shape[0], 1]), np.reshape(Apred, [Apred.shape[0], 1]))
        tn, fp, fn, tp = get_confusion_matrix_elements(Btrue.tolist(), Apred.tolist())
        p, r, fb_score, support = precision_recall_fscore_support( ((y_true_Array> 0).astype(np.uint8)).flatten(), ((y_pred_Array> 0).astype(np.uint8)).flatten(), average='binary')
        f2val = fbeta_score(Btrue, Apred, beta=2, average='binary')
        ## correct!
        jc = jaccard_score(Btrue, Apred)     
        # append all per images
        dice_valPerImage.append(fb_score)
        jaccard_valPerImage.append(jc)
        f2_valPerImage.append(f2val)
        # PPV/precision
        PPV_perImage.append(tp/(tp+fp+epsilon))
        # Recall/sensitivity
        recall_perImage.append(tp/(tp+fn+epsilon))
        # compute HD channelwise
        import cv2
        hd = cv2.createHausdorffDistanceExtractor()
        sd = cv2.createShapeContextDistanceExtractor()
        for i in range (0, len(classTypes)):
            _, ca, _ = cv2.findContours(((y_true_Array[i,:,:] > 0).astype(np.uint8)), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS) 
            _, cb, _ = cv2.findContours(((y_pred_Array[i, :,:] > 0).astype(np.uint8)), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS) 
            if ca !=[] and cb!=[] :
                d1 = hd.computeDistance(ca[0], cb[0])
                # distance based on the shape contours
#                d2 = sd.computeDistance(ca[0], cb[0])
                #distance_perImage.append(d1)
                distance_.append(d1)
            else:
                # penalise distance with large number
                distance_.append(1000)
        distance_perImage.append(np.mean(distance_))  
    # write all metric to json/csv file
    '''
    creating csv file (create dataframe for all the outputs/image)
    '''
#    csvFileName = args.jsonFileName.split('.')[0]+'.csv'
#    csvSaveFileTo=os.path.join(args.Result_dir, csvFileName)
#    import pandas as pd
    dsc_val = np.mean(dice_valPerImage)
    dsc_val_std = np.std(dice_valPerImage)
    
#    dataset = pd.DataFrame({'dsc':dice_valPerImage, 'jsc': jaccard_valPerImage,
#                            'f2score':f2_valPerImage,
#                            'PPV':PPV_perImage, 
#                            'recall':recall_perImage,
#                            'dist':distance_perImage})
#    
#    dataset.to_csv(csvSaveFileTo, sep=',', encoding='utf-8')
    
    print_debug(dice_valPerImage, jaccard_valPerImage,f2_valPerImage, PPV_perImage, recall_perImage, distance_perImage, 0)

    # final scores are wrapped in json file
    import json
    my_dictionary = { "EndoCV2020":{
                "dice":{
                "value":  (np.mean(dice_valPerImage)) 
                },
                "jaccard":{
                "value": (np.mean(jaccard_valPerImage))
                },
                "typeIIerror":{
                "value": (np.mean(f2_valPerImage))
                },
                "PPV":{
                "value": (np.mean(PPV_perImage)),
                },
                "recall":{
                "value": (np.mean(recall_perImage)),
                }, 
                "dist":{
                "value": (np.mean(distance_perImage)),
                },
                "dice_std":{
                "value": (np.std(dice_valPerImage)),
                },
                "jc_std":{
                "value": (np.std(jaccard_valPerImage)),
                },
                "f2_std":{
                "value": (np.std(f2_valPerImage)),
                },
                "ppv_std":{
                "value": (np.std(PPV_perImage)),
                },
                "r_std":{
                "value": (np.std(recall_perImage)),
                },                   
                "d_std":{
                "value": (np.std(distance_perImage)),
                },             
            }
    }   
    os.makedirs(args.Result_dir, exist_ok=True)
    jsonFileName=os.path.join(args.Result_dir, args.jsonFileName)
    fileObj= open(jsonFileName, "a")
    fileObj.write("\n")
    json.dump(my_dictionary, fileObj)
    fileObj.close()
    print('Evaluation metric values written to---->', (jsonFileName))