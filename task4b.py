#!/usr/bin/env python
import argparse
import numpy as np
import sys,os,select,subprocess

#from IPython.utils.io import 

#os.system("rm -f -r Practise/task3b_output")
#os.system("rm -f -r Practise/task3b_error")

 

def parse_arguments():
    parser = argparse.ArgumentParser(description='arguments')

    parser.add_argument("--inputs", "-i", action="append")

    return parser.parse_args()


out_file = "Practise/task4b_output"
err_file =  "Practise/task4b_error"



args = parse_arguments()

def saveop(save_stdout,save_stderr):
    inputs = [os.fdopen(int(args.inputs[0]), 'rb')]
    x = np.fromfile(inputs[0],dtype=np.float16,count=5)
    print ("from4a",x)
    x = x/0
    w = np.mean(x)
    print (w)
    if save_stdout and save_stderr:
        save_stdout = sys.stdout
        save_stderr = sys.stderr
    else:
        return


#sys.stderr = open(err_file,'w')
#f = open('out_file','r')
#f = open('err_file','r')
#sys.stdout.flush()

y = saveop(1,1)
print("The stdout is displayed at terminal")

#fh = open(out_file,'w')
#fe = open(err_file,'w')


sys.stdout =  os.mkfifo(out_file)
sys.stderr =  os.mkfifo(err_file) 

#sys.stdout = fh 
#sys.stdout = fe

z = saveop(0,0)
print("The stdout is saved to out_file")

#fh.close()
#fe.close()

#print f.read()
#f.close()














	
