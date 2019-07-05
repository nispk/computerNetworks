# Example-3: Send a single array to the second block and perform an arithematic operation on the received data in second block

In this task, we build a simple network with a single node, two blocks and one pipe connecting the blocks.We send data between the blocks via pipe. Once the data is received by the second block it performs an arithematic operation on it and prints the output to the MARVELO output window.The network processing in MARVELO takes place in the following steps-

## Step1: Define the network** 

We write an xml file that describes the distribution of nodes and their respective blocks in the network.

The same xml file described in Example1 can be used here.


## Step2: Define the block codes


**1. task3a.py**

  1. In this block code, we define the data that is sent to the second block code.
  *  argparse module is used to send the data through the output pipe

  5. The add_argument method in ArgumentParser function creates a list of pipe files of int data type and appends each `<output>` argument from the xml file to the `--outputs` list . Since there is only one output pipe defined in the xml file, there will be only one pipe file               appended to the `--outputs` list. 

       ```python
       outputs = [os.fdopen(int(args.outputs[0]), 'wb')]
       outputs[0].write(y)
       ```
  2. The `--outputs` list can be queried as `args.outputs[0]`. Here `args.output[0]` refers to the first pipe file which is defined as `pipe_id = "1"` in the xml file, appended in the 
      `--outputs` list. 
  3. The data to be sent to the second block is written to this pipe file. We open a write enabled file object of `args.outputs[0]` using `os.fdopen(int(args.outputs[0]),'wb')` function and           later the int data is written to the pipe through the `write` method.



**2. task3b.py** 

  1. In this block code, we define the arithmetic operation that is to be performed on the data received from `task3a.py`
  2. We declare the input port in the parse arguments() function, which was defined in the xml file        as `<input>`.
  * The argparse module parses the arguments of the command line out of sys.argv into Python datatype 
  * In our example, `task3b.py` reads the `input` argument from the command line(in xml file), this       input argument is provided by the MARVELO to the Daemon process running on client.
  * The add_argument method in ArgumentParser function creates a list of pipe files of int data type     and appends each `<input>` argument from the xml file to the `--inputs` list . Since there is         only one input pipe defined in the xml file, there will be only one pipe file appended to the 
    `--inputs` list. 

    ```python
     outputs = [os.fdopen(int(args.outputs[0]), 'wb')]
     outputs[0].write(y)
    ```
  2. The `--inputs` list can be queried as `args.inputs[0]`. Here `args.input[0]` refers to the first pipe file which is defined as `pipe_id = "1"` in the xml file, appended in the `--inputs` list. 
  3. The data to be from the first block is read from this pipe file. We open a read enabled file object of `args.inputs[0]` using `os.fdopen(int(args.inputs[0]),'rb')` function and later the int data is read from the pipe through the `readline()` method.


# Step3: 

We repeat the steps Step3 to Step5 as in Example1.
