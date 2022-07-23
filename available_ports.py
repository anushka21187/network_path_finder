import network_matrix

"""
Map the nodes in the router network to a list of available ports
Input: topology (string), network (can be a 2D list obtained from network_matrix)
Output: A dictionary with key as a node id and value as the list of directions allowed for packet movement from that node
The topology determines which directions are allowed.
In torus topology, all directions are allowed in each node, so direction-related information becomes irrelevant. This is not the case for mesh topology.
"""

def available_ports(topology, network): 
    
    available_directions = {} 
    
    if topology=='torus':
        list_of_directions = ['N', 'S', 'W', 'E']
        for row_index in range (0, len(network)):
            for col_index in range (0, len(network[row_index])):
                available_directions[network[row_index][col_index]] = \
                list_of_directions
                
    elif topology=='mesh':
        for row_index in range (0, len(network)):
            list_of_directions = []
            # if this is the first row of the network matrix ...
            if row_index==0:
                # then packets can definitely travel south
                list_of_directions.append('S')
                        
            # if this is the last row of the network matrix ...
            elif row_index==len(network)-1:
                # then packets can definitely travel north
                list_of_directions.append('N')
                
            # if this is any other row of the network matrix ...     
            else:
                # then packets can definitely travel north and south
                list_of_directions.extend(['N', 'S'])
                
            for col_index in range (0, len(network[row_index])):
                
                # and if this is the first column ...
                if col_index==0:
                    # then packets can travel east but not west
                    # so add east to the list
                    list_of_directions.append('E')
                    available_directions[network[row_index][col_index]] = []
                    for i in range (0, len(list_of_directions)):
                        available_directions[network[row_index][col_index]].append(list_of_directions[i])
                    del(list_of_directions[-1])   
                    
                # or if this is the last column ...
                elif col_index==len(network[row_index])-1:
                    # then packets can only travel west but not east
                    list_of_directions.append('W')
                    available_directions[network[row_index][col_index]] = []
                    for i in range (0, len(list_of_directions)):
                        available_directions[network[row_index][col_index]].append(list_of_directions[i])
                    del(list_of_directions[-1]) 
                # or if this node is in any other column ... 
                else:
                    # so add west and east to the list
                    list_of_directions.extend(['W', 'E'])
                    available_directions[network[row_index][col_index]] = []
                    for i in range (0, len(list_of_directions)):
                        available_directions[network[row_index][col_index]].append(list_of_directions[i])
                    del(list_of_directions[-2:])
        
    return available_directions
