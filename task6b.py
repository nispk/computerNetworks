#!/usr/bin/env python
import argparse
import numpy as np
import sys,os,select,subprocess
import shutil
from pathlib import Path

#from IPython.utils.io import 

#os.system("rm -f -r Practise/task3b_output")
#os.system("rm -f -r Practise/task3b_error")



def parse_arguments():
    parser = argparse.ArgumentParser(description='arguments')

    parser.add_argument("--inputs", "-i", action="append")

    return parser.parse_args()

args = parse_arguments()

inputs = [os.fdopen(int(args.inputs[0]), 'rb')]

x = np.fromfile(inputs[0],dtype=np.float16,count=5)
y = x


def saveop(x):
   print ("from4a",x)
   x = x/0
   w = np.mean(x)
   print ('x divide by 0 is',x)
    
    
def saveop_gn(x):
    print ("from4a",x)
    x = x/0
    w = np.mean(x)
    print ('x divide by 0 is',x)



z = saveop(x)
print("The stdout is displayed at terminal")

sys.stdout.flush()


#p = Path("task4b_output")


sys.stdout =  open('out_file','w')

sys.stderr =  open('err_file','w')


z_ = saveop_gn(x)
print("The stdout is saved to out_file")













	
