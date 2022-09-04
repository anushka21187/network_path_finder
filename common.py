# ---------- 1 ---------- #
""" COMMON FUNCTIONS """

"""
1. network_matrix: Create a network matrix of router IDs
2. available_ports: Obtain ports available to any node in the network
3. obtain_paths: Obtain all possible paths (tuples of router IDs) between a given pair of source and destination nodes
"""

from helpers import *

def network_matrix(r, c): 
    
    matrix = []
    node_id = 0
    
    for row_index in range (0, r):
        matrix_row = []
        for col_index in range (0, c):
            matrix_row.append(node_id)
            node_id = node_id + 1
        matrix.append(tuple(matrix_row))
    return tuple(matrix)





def available_ports(topology, r, c): 
    
    network = network_matrix(r, c)
    
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
            if row_index==0:
                list_of_directions.append('S')
                        
            elif row_index==len(network)-1:
                list_of_directions.append('N')
                    
            else:
                list_of_directions.extend(['N', 'S'])
                
            for col_index in range (0, len(network[row_index])):
                
                if col_index==0: 
                    list_of_directions.append('E')
                    available_directions[network[row_index][col_index]] = tuple(list_of_directions)
                    del(list_of_directions[-1])   
                    
                elif col_index==len(network[row_index])-1: 
                    list_of_directions.append('W')
                    available_directions[network[row_index][col_index]] = tuple(list_of_directions)
                    del(list_of_directions[-1]) 
                else: 
                    list_of_directions.extend(['W', 'E'])
                    available_directions[network[row_index][col_index]] = tuple(list_of_directions)
                    del(list_of_directions[-2:])
        
    return available_directions





def obtain_paths(r, c, sn, dn, visited_nodes, path_dict, src): 
    
    network_dict = available_ports('mesh', r, c)
    #global source
    allowed_directions = network_dict[sn]
    
    if sn==dn:
        hop_count = len(visited_nodes) - 1
        if hop_count in path_dict:
            path_dict[hop_count].append(tuple(visited_nodes))
        else:
            path_dict[hop_count] = [tuple(visited_nodes)]

    else:
        if sn==src:
            visited_nodes.append(sn)
 
        for i in range (0, len(allowed_directions)):
            if allowed_directions[i] == 'S':
                tentative_node = sn + c
            elif allowed_directions[i] == 'N':
                tentative_node = sn - c
            elif allowed_directions[i] == 'W':
                tentative_node = sn - 1
            else:
                tentative_node = sn + 1
                
            if tentative_node in visited_nodes:
                continue
            else:
                sn_updated = tentative_node
                visited_nodes.append(sn_updated)
                obtain_paths(r, c, sn_updated, dn, visited_nodes, path_dict, src)
                del(visited_nodes[-1])
                
    return path_dict
