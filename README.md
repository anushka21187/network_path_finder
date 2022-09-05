# network_path_finder

## INSTALLATION:

*any*> `git clone https://github.com/anushka21187/network_path_finder/edit/main/README.md`


## UPDATE:
'''
*any/network_path_finder*> `git pull origin main`
'''

## COMMAND DESCRIPTION:

(Might need to run `chmod -R 777 ./` in *any/network_path_finder* directory once after installation.)

*any/network_path_finder*> `./cmd <square_mesh_dimension>=2> <num_sources=1or2> <mode=0or1or2> <report_format=0or1or2>` 

* *square_mesh_dimension*: number of rows/columns in the mesh; cannot be less than 2
* *num_sources*: 1 for route pairs between one source and a fixed destination, 2 for the same between two different sources and a fixed destination
* *mode*: 0 to remove all route pairs with common bidirectional nodes, 1 to remove route pairs with any common node, 2 to include all possible route pairs
* *report_format*: 0 for direction bits, 1 for direction chars, 2 for node/router IDs


## MISCELLANEOUS INFO:

To modify the bits corresponding to directions, open cmd, and look for the string *SET DIRECTION BITS HERE*.

The following reports are generated and then dumped in 'reports' directory inside the current working directory:
1. A detailed report (file name starts with *NoC_*) that consists of all possible S-D pairs or S1-S2-D triplets, hops, route pairs, etc.
2. A summary (file name starts with *summary_*) of stats like the total number of route pairs obtained, maximum/minimum possible hops, etc.


The following strings are appended to the file name depending on the four cmd variables:
* *<N>x<N>*: N is the first argument, i.e., the number of rows/columns in the mesh
* nothing is appended if num_sources = 1
* _S2_: the number of sources is 2
* nothing is appended if mode = 0, i.e., only those route pairs which contain common bidirectiona; nodes are removed
* _nooverlap_: mode = 1, i.e., all route pairs that contain at least one common node are removed
* _withoverlap_: mode = 0, i.e., all possible route pairs are included regardless of overlap
* nothing is appended if report_format = 0, i.e., when route information is required in bits
* _directions_: report_format = 1, i.e., routes are reported as a sequence of direction characters like 'N', 'S', 'W', 'E'
* _routers_: report_format = 2, i.e., routes are reported as a sequence of node/router IDs

For example, `./cmd 2 2 2 1` generates report *NoC_2x2_S2_withoverlap_directions.rpt*, while `./cmd 3 1 0 0` generates *NoC_3x3.rpt*.
