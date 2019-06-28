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

In this xml file, the network described has one node that performs 2 tasks- **task2a.py** and **task2b.py**.Since the tasks are connected by one single pipe and the first task send's data to the second task, we define the output element in the first block with the target_pi_id of the block of the node which receives data. we define the input element in the second block with the source_pi_id of the block of the node which transfers the data to the second block.

2. The algorithm described in task2a.py 
