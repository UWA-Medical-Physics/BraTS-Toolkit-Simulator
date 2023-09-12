#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 13:19:19 2023

@author: useradmin


"""

import os
import subprocess
def change_permissions_recursive(path, mode):
    for root, dirs, files in os.walk(path, topdown=True):
        for dir in [os.path.join(root,d) for d in dirs]:
            #import subprocess
            subprocess.Popen(["sudo", "chmod", "7777", dir], stdout=subprocess.PIPE, shell=True)
            
    
    

def checkFileFound(file):
    try:       
        f = open(file, 'r')
        f.close()
    except IOError:
        print('file not found')
    

def main(dirPath, dirName, algos):    
    import os
    import datetime
    
    from brats_toolkit.segmentor import Segmentor
    
    
    # log
    starttime = str(datetime.datetime.now().time())
    print("*** starting at", starttime, "***")
    
    # instantiate
    seg = Segmentor(verbose=True)
    
   

    change_permissions_recursive(dirPath+"/output", 0o777)
    #os.chmod("/media/useradmin/Disk2/Patient-w1/output", 0o777)
    #import subprocess
    #subprocess.Popen(["sudo", "chmod", "7777", "/media/useradmin/Disk2/Patient-w1/output"], stdout=subprocess.PIPE, shell=True)
    #subprocess.Popen(["sudo", "chmod", "666", "/media/useradmin/Disk2/Patient-w1/output"], stdout=subprocess.PIPE, shell=True)
    # input files
    #search the folder path hdbet_brats-space in the patients folder and join with the file like *t1.nii.gz
    t1File = dirPath+"/output/hdbet_brats-space/output_hdbet_brats_t1.nii.gz"
    checkFileFound(t1File)
    t1cFile = dirPath+"/output/hdbet_brats-space/output_hdbet_brats_t1c.nii.gz"
    checkFileFound(t1File)
    t2File = dirPath+"/output/hdbet_brats-space/output_hdbet_brats_t2.nii.gz"
    checkFileFound(t1File)
    flaFile =dirPath+"/output/hdbet_brats-space/output_hdbet_brats_fla.nii.gz"
    checkFileFound(t1File)
    # output
    outputFolder = dirPath+"/outputSegmentator/"
    
    # algorithms we want to select for segmentation
    cids = algos #['isen-20','hnfnetv1-20','sanet0-20','scan-20']
    print("cids", algos)
    # execute it

    for cid in cids:
        try:
            outputFile = outputFolder + cid + ".nii.gz"
            seg.segment(t1=t1File, t2=t2File, t1c=t1cFile,
                        fla=flaFile, cid=cid, outputPath=outputFile)
    
        except Exception as e:
            print("error:", str(e))
            print("error occured for:", cid)
    

    # log
    endtime = str(datetime.datetime.now().time())
    print("*** finished at:", endtime, "***")
    
    
       

if __name__ == "__main__":
    import sys
    f = open(sys.argv[1]+"/bratSegmentatorOutput.txt", 'w')
    print("file open")
    print("I am here ............................................",sys.argv[0],"...",sys.argv[1],"...", sys.argv[2], "......", sys.argv[3])
    import ast

    listAlgo = ast.literal_eval(sys.argv[3])
    listAlgo2 = []
    for a in listAlgo:
        print(a)
        listAlgo2.append(a)
        
    sys.stdout = f
    main(sys.argv[1], sys.argv[2], listAlgo2)
    #f.close()
