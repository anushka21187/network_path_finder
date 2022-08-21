"""
Two Sources, One Destination

Mesh topology can be represented as a 2D matrix, where each element is a node/router
P1 = S1-->D and P2 = S2-->D should have equal number of hops
S1 and S2 should at least be one hop apart
* Find all the possible pairs (P1, P2) 
* Sort these pairs according to the number of hops 
"""

"""
Create a router network 
Input: number of rows, number of columns
Output: 2D matrix of node IDs 
Relevant topologies: mesh, torus
"""

def network_matrix(number_of_rows, number_of_columns): 
    #matrix = [[0]*number_of_columns]*number_of_rows
    #return matrix 
    
    matrix = []
    
    node_id = 0
    for row_index in range (0, number_of_rows):
        matrix_row = []
        for col_index in range (0, number_of_columns):
            matrix_row.append(node_id)
            node_id = node_id + 1
        matrix.append(tuple(matrix_row))
    return tuple(matrix)



"""
Map the nodes in the router network to a list of available ports.
Input: topology (string), network (can be a 2D list obtained from network_matrix)
Output: A dictionary with key as a node id and value as the list of directions
allowed for packet movement from that node
The topology determines which directions are allowed.
In torus topology, all directions are allowed in each node, so 
direction-related information becomes irrelevant. This is not the case for 
mesh topology.
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
                    available_directions[network[row_index][col_index]] = tuple(list_of_directions)
                    del(list_of_directions[-1])   
                    
                # or if this is the last column ...
                elif col_index==len(network[row_index])-1:
                    # then packets can only travel west but not east
                    list_of_directions.append('W')
                    available_directions[network[row_index][col_index]] = tuple(list_of_directions)
                    del(list_of_directions[-1]) 
                # or if this node is in any other column ... 
                else:
                    # add west and east to the list
                    list_of_directions.extend(['W', 'E'])
                    available_directions[network[row_index][col_index]] = tuple(list_of_directions)
                    del(list_of_directions[-2:])
        
    return available_directions



"""
Given a source node (sn) and a destination node (dn), find all possible paths between sn and dn.
Each path is a tuple of nodes traversed from sn to dn.
Return a dictionary with key as the number of hops and value as the corresponding list of paths. 
For example, a dictionary entry 2:[(4,1,2), (4,5,2)] has 
    - sn = 4, dn = 2
    - "2" as the number of hops, and 
    - the list as the collection of paths (tuples) that take two hops to go from 4 to 2
"""


def obtain_paths(network_dict, sn, dn, visited_nodes, path_dict): 
    global source
    allowed_directions = network_dict[sn]
    
    if sn==dn:
        hop_count = len(visited_nodes) - 1
        if hop_count in path_dict:
            path_dict[hop_count].append(tuple(visited_nodes))
        else:
            path_dict[hop_count] = [tuple(visited_nodes)]

    else:
        if sn==source:
            visited_nodes.append(sn)
 
        for i in range (0, len(allowed_directions)):
            if allowed_directions[i] == 'S':
                tentative_node = sn + number_of_columns
                # MUST MODIFY number_of_rows, number_of_columns GLOBALLY 
                # TO MODIFY network_dict
                # AND TO CALCULATE allowed_directions AND tentative_node CORRECTLY
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
                #dir_list = network_dict[sn_updated]
                obtain_paths(network_dict, sn_updated, dn, visited_nodes, path_dict)
                del(visited_nodes[-1])
                
    return path_dict


# create another obtain_paths that lists out directions to take between s and d
def obtain_paths_directions(network_dict, sn, dn, visited_nodes, directions_to_take, path_dict): 
    global source
    allowed_directions = network_dict[sn]
    
    if sn==dn:
        hop_count = len(visited_nodes) - 1
        if hop_count in path_dict:
            path_dict[hop_count].append(tuple(directions_to_take))
        else:
            path_dict[hop_count] = [tuple(directions_to_take)]

    else:
        if sn==source:
            visited_nodes.append(sn)
 
        for i in range (0, len(allowed_directions)):
            if allowed_directions[i] == 'S':
                tentative_node = sn + number_of_columns
                next_direction = allowed_directions[i]
            elif allowed_directions[i] == 'N':
                tentative_node = sn - number_of_columns
                next_direction = allowed_directions[i]
            elif allowed_directions[i] == 'W':
                tentative_node = sn - 1
                next_direction = allowed_directions[i]
            else:
                tentative_node = sn + 1
                next_direction = allowed_directions[i]
                
            if tentative_node in visited_nodes:
                continue
            else:
                sn_updated = tentative_node
                visited_nodes.append(sn_updated)
                directions_to_take.append(next_direction)
                obtain_paths_directions(network_dict, sn_updated, dn, visited_nodes, directions_to_take, path_dict)
                del(visited_nodes[-1])
                del(directions_to_take[-1])
                
    return path_dict




"""
make a global source
"""
def make_source(router_id):
    global source
    source = router_id

"""
make a global destination
"""
def make_destination(router_id):
    global destination
    destination = router_id
    
"""
modify number_of_rows and number_of_columns
"""
def make_rows(r):
    global number_of_rows
    number_of_rows = r
    
def make_columns(c):
    global number_of_columns
    number_of_columns = c
    


"""
get maximum possible number of hops for an NxN matrix
- generate all dictionaries corresponding to a source-destination pair
- keep appending the dictionary keys to a list
- return maximum value obtained from this hops list
"""






"""
list or dictionary of path pairs
hops can be access using list(dictionary.keys())[index]
"""
def hops_and_path_pairs(s1, s2, d):
    pair_dict = {}
    
    make_destination(d)
    
    # list out the valid hops for a given source and destination pair
    make_source(s1)
    #path_dict_1 = obtain_paths(router_ids_ports, s1, d, [], {})
    path_dict_1 = obtain_paths_directions(router_ids_ports, s1, d, [], [], {})
    
    make_source(s2)
    #path_dict_2 = obtain_paths(router_ids_ports, s2, d, [], {})
    path_dict_2 = obtain_paths_directions(router_ids_ports, s2, d, [], [], {})
    
    
    hops_list_1 = list(path_dict_1.keys()) 
    hops_list_2 = list(path_dict_2.keys())
    
    # iterate through the first dictionary
    for i in range(0, len(path_dict_1)):
        # iterate through the second dictionary
        for j in range(0, len(path_dict_2)):
            # if the hops (i.e., dictionary keys) match
            if hops_list_2[j]==hops_list_1[i]:
                # now we have two different lists of items
                # we need to iterate through both lists to get all possible COMBINATIONS
                # each combination (a pair) is to be associated with the corresponding hop key
                list_of_paths_1 = path_dict_1[hops_list_1[i]]
                list_of_paths_2 = path_dict_2[hops_list_2[j]]
                for p1 in range(0, len(list_of_paths_1)):
                    for p2 in range(0, len(list_of_paths_2)):
                        pair = [list_of_paths_1[p1], list_of_paths_2[p2]]
                
                        if hops_list_2[j] in pair_dict:
                            pair_dict[hops_list_2[j]].append(tuple(pair))
                        else:
                            pair_dict[hops_list_2[j]] = [tuple(pair)]
                        pair = []
                    
    return pair_dict



"""
convert paths to string bit sequences
ref: N = 00, S = 01, W = 10, E = 11
"""
def hops_and_pathbits_pairs(s1, s2, d):
    hops_pairs = hops_and_path_pairs(s1, s2, d)
    
    pathbitspairs_perhop = {} 
    hops_list = list(hops_pairs.keys()) 
    pairslist_list = list(hops_pairs.values()) 
    
    for i in range(0, len(pairslist_list)): 
        hop = hops_list[i] 
        pairslist = pairslist_list[i] 
        newpairslist = []
        
        for p in range(0, len(pairslist)): 
            pair = pairslist[p]
            newpair = []
            
            for j in range(0, 2): 
                path = pair[j] 
                newpath = ""
                
                for k in range(0, len(path)): 
                    if path[k] == 'N': 
                        newpath = newpath + '00'
                    elif path[k] == 'S':
                        newpath = newpath + '01'
                    elif path[k] == 'W':
                        newpath = newpath + '10'
                    else:
                        newpath = newpath + '11'
                
                newpair.append(newpath) 
                
            newpairslist.append(tuple(newpair))
            
        if hop in list(pathbitspairs_perhop.keys()):
            pathbitspairs_perhop[hop].append(newpairslist)
        else:
            pathbitspairs_perhop[hop] = newpairslist
            
    return pathbitspairs_perhop




def number_of_path_pairs(hops_pairs):
    numberofpairs_perhop = {}
    key_list = list(hops_pairs.keys())
    for i in range(0, len(hops_pairs)):
        key = key_list[i]
        value = hops_pairs[key]
        numberofpairs_perhop[key] = len(value)
        
    return numberofpairs_perhop


def exchange_key_value(in_dict):
    out_dict = {}
    new_values = list(in_dict.keys())
    new_keys = list(in_dict.values())
    for i in range(0, len(in_dict)):
        out_dict[new_keys[i]] = new_values[i]
        
    return out_dict



"""
generate dictionaries of all possible source and destination pairs
when dictionary for one triplet is done, store the following in a file:
    s1, s2, d (the triplet, a size-3 tuple of int values)
        hops: path pairs (the dict)
then reuse the dictionary variable in the next iteration, i.e., for a new triplet
               
Iterations will go like this:
    COMBINATIONS --> s1 != d; s2 != d AND s2 > s1
    PERMUTATIONS --> s1 != d; s2 != d AND s2 != s1
    
"""
def generate_all_pairs(network):
    
    with open(filename, "w") as f0:
        f0.write("----- START ----- \n\n")
        f0.write("Number of rows = " + str(number_of_rows) + " \n")
        f0.write("Number of columns = " + str(number_of_columns) + " \n")
        f0.write("Network: \n")
        
        f0.write(spaces)
        for i in range(0, len(network)):
            for j in range(0, len(network[i])):
                f0.write(str(network[i][j])+spaces_halved)
            f0.write("\n"+spaces)
        f0.write("\n")
        
        f0.write("Port reference: N = 00, S = 01, W = 10, E = 11 \n\n\n")
    
    # list out all router ids first
    routers = []
    for i in range(0, len(network)):
        for j in range(0, len(network[i])):
            routers.append(network[i][j])
            
    # iterate through each destination
    for x in range(len(routers)-1, -1, -1):
        # get the destination router ID; d = 8
        d = routers[x]
        for y in range(0, len(routers)):
            if routers[y] != d:
                # s1 = 0
                s1 = routers[y]
                for k in range(0, len(routers)):
                    if routers[k] != d and routers[k] > s1:
                        #s2 = 1
                        s2 = routers[k]
                        
                        hops_pairs_bits = hops_and_pathbits_pairs(s1, s2, d)
                        if len(hops_pairs_bits) != 0:
                            number_of_pairs_perhop = number_of_path_pairs(hops_pairs_bits)
                            hops_list = list(number_of_pairs_perhop.keys())
                            min_hops = min(hops_list)
                            max_hops = max(hops_list)
                            number_of_hops_perpair = exchange_key_value(number_of_pairs_perhop)
                            min_pairs = min(list(number_of_hops_perpair.keys()))
                            min_pairs_hop = number_of_hops_perpair[min_pairs]
                            max_pairs = max(list(number_of_hops_perpair.keys()))
                            max_pairs_hop = number_of_hops_perpair[max_pairs]   
                            
                            with open(filename, "a") as f1:
                                f1.write("s1 = "+str(s1)+", s2 = "+str(s2)+", d = "+str(d)+": \n")
                                f1.write(spaces+"Minimum hops = "+str(min_hops)+" \n")
                                f1.write(spaces+"Maximum hops = "+str(max_hops)+" \n")
                                f1.write(spaces+"Minimum path pairs = "+str(min_pairs)+" ")
                                f1.write("for hop count = "+str(min_pairs_hop)+" \n")
                                f1.write(spaces+"Maximum path pairs = "+str(max_pairs)+" ")
                                f1.write("for hop count = "+str(max_pairs_hop)+" \n")
                                f1.write("\n")
                                
                                for index1 in range(0, len(hops_pairs_bits)):
                                    key = hops_list[index1]
                                    f1.write(spaces+"HOPS = "+str(key)+" \n")
                                    value = hops_pairs_bits[key]
                                    for index2 in range(0, len(value)):
                                        pair = value[index2]
                                        f1.write(spaces+spaces+"PAIR_"+str(index2)+": ("+pair[0]+", "+pair[1]+") \n")
                               
                                f1.write("\n\n")
                        
    with open(filename, "a") as f2:
        f2.write("----- END ----- \n")
                        


def generate_all_pairs_permutations(network):
    
    with open(filename_p, "w") as f0:
        f0.write("----- START ----- \n\n")
        f0.write("Number of rows = " + str(number_of_rows) + " \n")
        f0.write("Number of columns = " + str(number_of_columns) + " \n")
        f0.write("Network: \n")
        
        f0.write(spaces)
        for i in range(0, len(network)):
            for j in range(0, len(network[i])):
                f0.write(str(network[i][j])+spaces_halved)
            f0.write("\n"+spaces)
        f0.write("\n")
        
        f0.write("Port reference: N = 00, S = 01, W = 10, E = 11 \n\n\n")
    
    # list out all router ids first
    routers = []
    for i in range(0, len(network)):
        for j in range(0, len(network[i])):
            routers.append(network[i][j])
            
    # iterate through each destination
    for x in range(len(routers)-1, -1, -1):
        # get the destination router ID; d = 8
        d = routers[x]
        for y in range(0, len(routers)):
            if routers[y] != d:
                # s1 = 0
                s1 = routers[y]
                for k in range(0, len(routers)):
                    if routers[k] != d and routers[k] != s1:
                        #s2 = 1
                        s2 = routers[k]
                        
                        hops_pairs_bits = hops_and_pathbits_pairs(s1, s2, d)
                        if len(hops_pairs_bits) != 0:
                            number_of_pairs_perhop = number_of_path_pairs(hops_pairs_bits)
                            hops_list = list(number_of_pairs_perhop.keys())
                            min_hops = min(hops_list)
                            max_hops = max(hops_list)
                            number_of_hops_perpair = exchange_key_value(number_of_pairs_perhop)
                            min_pairs = min(list(number_of_hops_perpair.keys()))
                            min_pairs_hop = number_of_hops_perpair[min_pairs]
                            max_pairs = max(list(number_of_hops_perpair.keys()))
                            max_pairs_hop = number_of_hops_perpair[max_pairs]   
                            
                            with open(filename_p, "a") as f1:
                                f1.write("s1 = "+str(s1)+", s2 = "+str(s2)+", d = "+str(d)+": \n")
                                f1.write(spaces+"Minimum hops = "+str(min_hops)+" \n")
                                f1.write(spaces+"Maximum hops = "+str(max_hops)+" \n")
                                f1.write(spaces+"Minimum path pairs = "+str(min_pairs)+" ")
                                f1.write("for hop count = "+str(min_pairs_hop)+" \n")
                                f1.write(spaces+"Maximum path pairs = "+str(max_pairs)+" ")
                                f1.write("for hop count = "+str(max_pairs_hop)+" \n")
                                f1.write("\n")
                                
                                for index1 in range(0, len(hops_pairs_bits)):
                                    key = hops_list[index1]
                                    f1.write(spaces+"HOPS = "+str(key)+" \n")
                                    value = hops_pairs_bits[key]
                                    for index2 in range(0, len(value)):
                                        pair = value[index2]
                                        f1.write(spaces+spaces+"PAIR_"+str(index2)+": ("+pair[0]+", "+pair[1]+") \n")
                               
                                f1.write("\n\n")
                        
    with open(filename_p, "a") as f2:
        f2.write("----- END ----- \n")            
                
"""
def generate_over_range(limit):
    for i in range(2, limit):
        make_rows(i)
        make_columns(i)
        generate_all_pairs(network_matrix(number_of_rows, number_of_columns))
"""



# ----- user inputs ----- #
number_of_rows = int(input("Number of rows = "))
number_of_columns = int(input("Number of columns = "))
#number_of_rows = 2
#number_of_columns = 2
# ----- end of user inputs ----- #


# ----- modifiable global variables ----- #
source_1 = 1
source_2 = 3
destination = 2
# ----- end of modifiable global variables ----- #


# ----- file variables ----- #
spaces = "          " # 10 spaces
spaces_halved = "     " # 5 spaces
file_extension = ".txt"
filename = "NoC_" + str(number_of_rows) + "x" + str(number_of_columns) + file_extension
filename_p = "NoC_P_" + str(number_of_rows) + "x" + str(number_of_columns) + file_extension
# ----- end of file variables ----- #


mesh_network = network_matrix(number_of_rows, number_of_columns)
router_ids_ports = available_ports('mesh', mesh_network)
#port_map_torus = available_ports('torus', mesh_network 
source = 0
#source_directions = router_ids_ports[source] # default source for testing

#dictionary_of_paths = obtain_paths(router_ids_ports, source, destination, [], {})
#dictionary_of_paths_directions = obtain_paths_directions(router_ids_ports, source, destination, [], [], {})

#list_of_hops = list(dictionary_of_paths_directions.keys())
#max_hops = max(list_of_hops)

#make_source(source_1)
#source_directions = router_ids_ports[source_1]
#dict1 = obtain_paths(router_ids_ports, source_1, destination, [], {})
#dict1 = obtain_paths_directions(router_ids_ports, source_1, destination, [], [], {})
#make_source(source_2)
#source_directions = router_ids_ports[source_2]
#dict2 = obtain_paths(router_ids_ports, source_2, destination, [], {})
#dict2 = obtain_paths_directions(router_ids_ports, source_2, destination, [], [], {})
#s1_s2_pairs = hops_and_path_pairs(source_1, source_2, destination)
#pairs_in_bits = hops_and_pathbits_pairs(source_1, source_2, destination)
#hopsperpair = number_of_path_pairs(pairs_in_bits)
generate_all_pairs(mesh_network)
generate_all_pairs_permutations(mesh_network)
#generate_over_range(5)
