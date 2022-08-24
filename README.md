# network_path_finder

Two Sources, One Destination

Mesh topology can be represented as a 2D matrix, where each element is a node/router

P1 = S1-->D and P2 = S2-->D should have equal number of hops 

S1 and S2 should at least be one hop apart 

1. Find all the possible pairs (P1, P2) 
2. Sort these pairs according to the number of hops 


To do:

CONSTRAINTS
1. Limit the minimum number of hops allowed for path pairs
2. Limit the maximum number of hops allowed for path pairs
3. Do not include those path pairs that cross the same node simultaneously

MISCELLANEOUS
1. Create a separate python script file and a python functions file
2. Create a shell script where the following parameters can be set for the python script before calling it
  * Generate results upto "n" rows and columns? (y/n)
    - If "y": n = ___
    - If "n": 
      * Number of rows = ___
      * Number of columns = ___
  * Limit the mimimum number of hops? (y/n)
    - Minimum number of hops
  * Limit the maximum number of hops (y/n)
    - Maximum number of hops
  * Exclude overlapping paths? (y/n)
  
  Results and Summary are dumped in the NoC directory.
3. Include the following in the report:
  * A summary of user inputs:
    - Number of rows
    - Number of columns
    - Minimum number of hops (can be NA)
    - Maximum number of hops (can be NA)
    - Overlapping paths excluded? (YES or NO)
  * A summary of statisics:
    Use the generated report for calculating these stats and then dump them to another summary file. For an mXn mesh network, find the: 
      - Longest path in hops
      - Shortest path in hops
      - Maximum path pairs of the same length 
        - The number of hops
        - The triplet and the number of pairs
        - The triplet and the number of pairs ...
      - Minimum path pairs of the same length
        - The number of hops
        - The triplet and the number of pairs
        - The triplet and the number of pairs ...
