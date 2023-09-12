#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 09:56:02 2023

@author: useradmin
"""


import os
from path import Path
import datetime
import sys




def main(dirPath, dirName, algos):
   

    from brats_toolkit.fusionator import Fusionator
    
    # log
    starttime = str(datetime.datetime.now().time())
    print("*** starting at", starttime, "***")
    
    # instantiate
    fus = Fusionator(verbose=True)
    
    # input
    SOURCEDIR = dirPath+"/outputSegmentator/"
    print(SOURCEDIR)
    # output
    OUTPUTDIR = dirPath+"/outputFusionator/"
    
    # cids of the algorithms we want to fuse
    cids = algos#['isen-20','hnfnetv1-20','sanet0-20','scan-20']
    
    # segmentation file paths
   
            
    segs = [SOURCEDIR + s + ".nii.gz" for s in cids]
    
    # execution
    # mav
    mavPath = OUTPUTDIR + "mav.nii.gz"
    fus.fuse(segmentations=segs, outputPath=mavPath, method='mav', weights=None)
    
    # simple
    simplePath = OUTPUTDIR + "simple.nii.gz"
    fus.fuse(segmentations=segs, outputPath=simplePath,
             method='simple', weights=None)
    
    # log
    endtime = str(datetime.datetime.now().time())
    print("*** finished at:", endtime, "***")
    
    
if __name__ == "__main__":
    import sys
    f = open(sys.argv[1]+"/bratFusionatorOutput.txt", 'w')#correct path
    print("I am here ............................................",sys.argv[0],"...",sys.argv[1],"...", sys.argv[2],"......", sys.argv[3])
    import ast

    listAlgo = ast.literal_eval(sys.argv[3])
    listAlgo2 = []
    for a in listAlgo:
        print(a)
        listAlgo2.append(a)
        
    sys.stdout = f
    
    main(sys.argv[1], sys.argv[2],listAlgo2)
    #f.close()
    