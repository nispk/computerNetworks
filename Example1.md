#How to use MARVELO:
--------------------

We go through step by step tutorial on how to use MARVELO by giving examples for different tasks that can be performed using MARVELO-

##Example-1: Print 'Hello World!' on the MARVELO output window.

In this task, we build a simple network with a single node, single block and zero pipes.The MARVELO will read the block and print its output on the MARVELO output window.The network processing in MARVELO takes place in the following steps-

1. We write an xml file that describes the distribution of nodes and their respective blocks in the network.

```xml
<?xml version="1.0" ?>
	<network>
		<node pi_id="127.0.0.1">
			<algorithm path="/home/asn/MARVELO/asn_server/Practise" executable="./task1.py">                                	
			</algorithm>

</node>
</network>
```
In our task, there is only one node, a single block whose algorithm named **task1.py** is placed in the /home/asn/MARVELO/asn_server/Practise path.

2. The algorithm described in **task1.py** prints 'Hello World!' to the MARVELO's command window.

      MARVELO framework has 2 main roles in the network- controller(server) and client.In the above example the controller is fed with xml data. The client is the node present in the network. Each client hosts a single Daemon process.The Daemon process receives the orders from the controller through **CMD port** to process the algorithm **task1.py** and finally after execution it returns the output to the controller via **MSG port**. This output is printed on the MARVELO output window.





