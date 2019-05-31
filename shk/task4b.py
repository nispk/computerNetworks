#!/usr/bin/env python
import argparse
import numpy as np
import sys,os,select
from IPython.utils.io import 

#os.system("rm -f -r Practise/task3b_output")
#os.system("rm -f -r Practise/task3b_error")

def parse_arguments():
    parser = argparse.ArgumentParser(description='arguments')

    parser.add_argument("--inputs", "-i",
                            action="append")

    return parser.parse_args()

args = parse_arguments()


#inputs = [os.fdopen(int(args.inputs[0]), 'rb')]
#x = np.fromfile(inputs[0],dtype=np.float16,count=5)
x = 5
print ("from3b",x)
x = x/0
w = np.mean(x)
print (w)
#sys.stdout.flush()











	
