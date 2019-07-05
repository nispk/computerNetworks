##Example-2: Send an integer or float data to another block and perform an arithemtic operation on it in the second block.

In this task, we build a simple network with a single node, two blocks and one pipe connecting the blocks.We send data between the blocks via pipe. Once the data is received by the second block it performs an arithematic operation on it and prints the output to the MARVELO output window.The network processing in MARVELO takes place in the following steps-

1. We write an xml file that describes the distribution of nodes and their respective blocks in the network.

```xml
<network>
    <node pi_id="127.0.0.1">
       <algorithm path="/home/asn/asn_server/Demos/system/shk" executable="./task2a.py">   
	   <output target_pi_id = "127.0.0.1" pipe_id="1"></output>                            	
       </algorithm>
       <algorithm path="/home/asn/asn_server/Demos/system/shk" executable="./task2b.py">
	   <input source_pi_id = "127.0.0.1" pipe_id="1"></input>                                	
       </algorithm>
    </node>
</network>
```

In this xml file, the network described has one node that performs 2 tasks- **task2a.py** and **task2b.py**.Since the tasks are connected by one single pipe and the first task send's data to the second task, we define the output element in the first block with the target_pi_id of the block of the node which receives data. we define the input element in the second block with the source_pi_id of the block of the node which transfers the data to the second block.

2. task2a.py and task2b.py are the block codes in the node. We declare the network ports- input port and output port in the parse arguments() function, which were defined in the xml file as input element and output element.The argparse module parses the arguments of the command line out of sys.argv into Python datatype as follows-
   1. In our example, the first block task2a.py reads the 'output' argument from the command line, this output argument is provided by the MARVELO to the Daemon process running on client.
```python
def parse_arguments():
    parser = argparse.ArgumentParser(description='arguments')

    parser.add_argument("--outputs", "-o",
                            action="append")

    return parser.parse_args()

args = parse_arguments()
```
   2. The add_argument method in ArgumentParser function creates a list of pipe objects of int data type and appends each output argument from the command line to the --outputs list . Since there is only one output element defined in the xml file, there will be only one pipe object appended to the outputs[] list. 

```python
outputs = [os.fdopen(int(args.outputs[0]), 'wb')]
outputs[0].write(y)
```
   3. This outputs list can be queried as args.outputs[0]. Here args.output[0] refers to the first pipe object which is an output port named "1" on the node with ip address "127.0.0.1" in the outputs[] list. The data to be sent to the second block is written to this pipe object. We open a write enabled file object of args.outputs[0] using os.fdopen function and later the int data is written to the pipe through the write method.

3. task2b.py creates a list of pipe objects called inputs[] of int data type using argparse library.





