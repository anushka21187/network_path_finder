# network_path_finder

## Installation

*any*> `git clone https://github.com/anushka21187/network_path_finder`

Required packages: python, csh


## Update

*any/network_path_finder*> `git pull origin main`


## Command description

*any/network_path_finder*> `./cmd <square_mesh_dimension>=2> <num_sources=1or2> <mode=0or1or2> <report_format=0or1or2or3or4>` 

* *square_mesh_dimension*: number of rows/columns in the mesh; minimum = 2
* *num_sources*: 
	* 1 for route pairs between one source and a fixed destination
	* 2 for the same between two different sources and a fixed destination
* *mode*: 
	* 0 to remove all route pairs with common bidirectional nodes (moderately small subset)
	* 1 to remove route pairs with any common node (smallest subset)
	* 2 to include all possible route pairs (largest subset)
* *report_format*: 
	* 0 for detailed report having direction bits
	* 1 for detailed report having direction chars
	* 2 for detailed report having node/router IDs (numbers)
	* 3 for concise report with format: source1_source2_destination_hop# = (source1:encoding, destination:encoding), (source2:encoding, destination:encoding)
	* 4 for generating all the spice files for all (s1,s2,d) triplets reported in option #3 (previous line)

## Possible errors

* `./cmd: Permission denied`: Run `chmod -R 777 ./` in *any/network_path_finder* directory once after installation.
* `Command 'python' not found`: Install the package *python-is-python3*.


## Miscellaneous info

### Modifying direction bits

Open cmd, look for the string *SET DIRECTION BITS HERE*, and make the required modifications.

### The output reports

The following reports are generated and then dumped in *any/network_path_finder/reports* directory:
1. A detailed report (file name starts with *NoC_*) that consists of all possible S-D pairs or S1-S2-D triplets, hops, route pairs, etc.
2. A summary (file name starts with *summary_*) of stats like the total number of route pairs obtained, maximum/minimum possible hops, etc.
3. Spice files (files in *stimuli_* directory and name start with *stimuli.noc*) has stimuli for receiving response using the apt (s1,s2,d) triplets mentioned in detailed-report.

The following strings are appended to the file name depending on the four cmd variables:
* *NxN*: *N* is replaced by the first argument, i.e., the number of rows/columns in the mesh
* _S2_: the number of sources is 2
* _nooverlap_: mode = 1, i.e., all route pairs that contain at least one common node are removed
* _withoverlap_: mode = 2, i.e., all possible route pairs are included regardless of overlap
* _directions_: report_format = 1, i.e., routes are reported as a sequence of comma-separated direction characters *N*, *S*, *W*, *E*
* _routers_: report_format = 2, i.e., routes are reported as a sequence of comma-separated node/router IDs
* Nothing is appended if:
  * num_sources = 1, i.e., the number of sources is 1
  * mode = 0, i.e., only those route pairs which contain common bidirectional nodes are removed
  * report_format = 0, i.e., when route information is reported in bits
  
* For example, `./cmd 2 2 2 1` generates report *NoC_2x2_S2_withoverlap_directions.rpt*, while `./cmd 3 1 0 0` generates *NoC_3x3.rpt*.
