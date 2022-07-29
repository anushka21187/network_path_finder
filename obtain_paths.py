"""
Given a source node (sn) and a destination node (dn), find all possible paths between sn and dn.
Each path is a tuple of nodes traversed from sn to dn.
Return a dictionary with key as the number of hops and value as the corresponding list of paths. 
For example, a dictionary entry 2:[(4,1,2), (4,5,2)] has 
    - sn = 4, dn = 2
    - "2" as the number of hops, and 
    - the list as the collection of paths (tuples) that take two hops to go from 4 to 2
"""

def obtain_paths(network_dict, number_of_rows, number_of_columns, sn, dn, visited_nodes, allowed_directions, path_dict): 
    global source
    if sn==dn:
        hop_count = len(visited_nodes) - 1
        if hop_count in path_dict:
            path_dict[hop_count].append(tuple(visited_nodes))
        else:
            path_dict[hop_count] = [tuple(visited_nodes)]

    else:
        if sn==source:
            del(visited_nodes[:])
            visited_nodes.append(sn)
 
        for i in range (0, len(allowed_directions)):
            if allowed_directions[i] == 'S':
                tentative_node = sn + number_of_columns
            elif allowed_directions[i] == 'N':
                tentative_node = sn - number_of_columns
            elif allowed_directions[i] == 'W':
                tentative_node = sn - 1
            else:
                tentative_node = sn + 1
                
            if tentative_node in visited_nodes:
                continue
            else:
                sn_updated = tentative_node
                visited_nodes.append(sn_updated)
                dir_list = network_dict[sn_updated]
                obtain_paths(network_dict, number_of_rows, number_of_columns, sn_updated, dn, visited_nodes, dir_list, path_dict)
                del(visited_nodes[-1])
                
    return path_dict
