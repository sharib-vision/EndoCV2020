# =============================================================================
#   Evaluates mAP and IoU 
#
#   Requires bounding boxes to be given in the VOC format i.e:
#       ground-truth boxes: class_name, x1, y1, x2, y2
#       predicted boxes: class_name, confidence, x1, y1, x2, y2 
# EAD 2020 Challenge (https://ead2020.grand-challenge.org)
# If you encounter any error please contact us. Thank you for your participation.
# Contact: sharib[dot]ali[at]eng[dot]ox[dot]ac.uk
# =============================================================================

import os
import json
import sys
import numpy as np

MINOVERLAP = 0.25 # default value 

debug = 0
type = ''
# fetch the folders 
if debug:
    predictfolder ='../mAP-IoU_testdata/predicted'
    gtfolder ='../mAP-IoU_testdata/ground-truth'
    
    predictfolder ='../detection_bbox/detection_bbox'
    gtfolder ='../groundTruths_EAD2019/detection_bbox'
    resultsfolder ='../mAP-IoU_testdata/results'
    jsonFileName = 'detection_test_emptyPredictions.json'
else:    
    predictfolder = sys.argv[1]
    gtfolder = sys.argv[2]
    resultsfolder = sys.argv[3]
    jsonFileName = sys.argv[4]
#    MINOVERLAP = float(sys.argv[5])
    type = (sys.argv[5])

"""
Series of helper functions. 
"""

print("Finished computing mAP and IoU. Results are saved in {}/results.txt".format(resultsfolder))

'''
creating json file
'''
from endoCV2020_eval_detection import main_EndoCV2020 

# compute mAP at 0.25, 0.5 and 0.75 IoUs
MINOVERLAP = 0.25
mAP25, mIoU25, ap_dictionary_25 = main_EndoCV2020(MINOVERLAP, type, resultsfolder, gtfolder, predictfolder)
MINOVERLAP = 0.5
mAP50, mIoU50, ap_dictionary_50 = main_EndoCV2020(MINOVERLAP, type, resultsfolder, gtfolder, predictfolder)
MINOVERLAP = 0.75
mAP75, mIoU75, ap_dictionary_75 = main_EndoCV2020(MINOVERLAP, type, resultsfolder, gtfolder, predictfolder)

# compute mean of all over 0.25:0.05:0.75
Iou_thres_range = np.arange(0.25, 0.80, 0.05)
map_concat = []
mIou_concat = []
for i in range (0, 11):
    mAP, mIoU, _ = main_EndoCV2020(Iou_thres_range[i], type, resultsfolder, gtfolder, predictfolder)
    map_concat.append(mAP)
    mIou_concat.append(mIoU)
    
debug = 0
if debug:
    print('mean mAP_(0.25:0.05:0.75)',(np.mean(map_concat)))
    print('mean IoU_(0.25:0.05:0.75)',(np.mean(mIou_concat)))

my_dictionary = {
    "EndoCV2020":{
            "mAP":{
             "value":   (np.mean(map_concat)*100)
            },
            "IoU":{
              "value":       (np.mean(mIou_concat)*100)
            },
            "mAP25":{
             "value":   (np.mean(mAP25)*100)
            },
            "IoU25":{
              "value":       (np.mean(mIoU25)*100)
            },
            "mAP50":{
             "value":   (np.mean(mAP50)*100)
            },
            "IoU50":{
              "value":       (np.mean(mIoU50)*100)
            },
            "mAP75":{
             "value":   (np.mean(mAP75)*100)
            },
            "IoU75":{
              "value":       (np.mean(mIoU75)*100)
            },
            "ap_dict":{
              "value":       (ap_dictionary_25)
            },
            "mAP_std":{
             "value":   (np.std(map_concat)*100)
            }
        }
}

jsonFileName=os.path.join(resultsfolder, jsonFileName)

try:
    os.remove(jsonFileName)
except OSError:
    pass

fileObj= open(jsonFileName, "w+")
json.dump(my_dictionary, fileObj)
fileObj.close()




