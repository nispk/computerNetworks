#!/usr/bin/env python
import argparse
import numpy as np
import sys,os,select
import socket,subprocess


os.system("rm -f -r Practise/task3b_output")
os.system("rm -f -r Practise/task3b_error")

def parse_arguments():
    parser = argparse.ArgumentParser(description='arguments')

    parser.add_argument("--inputs", "-i",
                            action="append")

    return parser.parse_args()

args = parse_arguments()

out_file = "Practise/task3b_output"
err_file =  "Practise/task3b_error"

os.system("touch"+out_file)
inputs = [os.fdopen(int(args.inputs[0]), 'rb')]
x = np.fromfile(inputs[0],dtype=np.float16,count=5)

print ("from3b",x)

x = x/0
w = np.mean(x)
print (w)
#sys.stderr =  os.mkfifo(err_file) 
#sys.stdout = os.mkfifo(out_file)
#sys.stdout = open(out_file,'w') 
#sys.stderr = open(err_file,'w')

sys.stdout.flush()










	
