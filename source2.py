def network_matrix(nsize): 
    matrix = []
    node_id = 0
    for row_index in range (0, nsize):
        matrix_row = []
        for col_index in range (0, nsize):
            matrix_row.append(node_id)
            node_id = node_id + 1
        matrix.append(tuple(matrix_row))
    return tuple(matrix)


def available_ports(topology, nsize): 
    
    network = network_matrix(nsize)
    
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



def obtain_paths(nsize, sn, dn, visited_nodes, path_dict, src): 
    
    network_dict = available_ports('mesh', nsize)
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
                tentative_node = sn + nsize
            elif allowed_directions[i] == 'N':
                tentative_node = sn - nsize
            elif allowed_directions[i] == 'W':
                tentative_node = sn - 1
            else:
                tentative_node = sn + 1
                
            if tentative_node in visited_nodes:
                continue
            else:
                sn_updated = tentative_node
                visited_nodes.append(sn_updated)
                obtain_paths(nsize, sn_updated, dn, visited_nodes, path_dict, src)
                del(visited_nodes[-1])
                
    return path_dict


def hops_and_route_pairs_nooverlap_s2(nsize, s1, s2, d):
    pair_dict = {} 
    
    #make_source(s1)
    path_dict_1 = obtain_paths(nsize, s1, d, [], {}, s1)
    
    #make_source(s2)
    path_dict_2 = obtain_paths(nsize, s2, d, [], {}, s2)
    
    hops_list_1 = list(path_dict_1.keys())
    hops_list_1.sort()
    hops_list_2 = list(path_dict_2.keys())
    hops_list_2.sort()
    
    # iterate through all hops in the first dictionary
    for i in range(0, len(hops_list_1)):
        # iterate through all hops in the second dictionary
        for j in range(0, len(hops_list_2)):
            # if the hops (i.e., dictionary keys) match
            if hops_list_2[j]==hops_list_1[i]:
                # we get two different lists of paths
                list_of_paths_1 = path_dict_1[hops_list_1[i]]
                list_of_paths_2 = path_dict_2[hops_list_2[j]]
                # we need to iterate through the first list
                # and then through the second list
                # to get all valid COMBINATIONS !!!!! WITHOUT OVERLAPS !!!!! DO THISSSSSS
                # each combination (a pair) is to be associated with the corresponding hop key
                for p1 in range(0, len(list_of_paths_1)):
                    path1 = list_of_paths_1[p1]
                    for p2 in range(0, len(list_of_paths_2)):
                        # create pair only if there is no overlap
                        path2 = list_of_paths_2[p2]
                        
                        flag = 0
                        for k in range(0, len(path1)-1):
                            if path1[k] in path2[1:]:
                                flag = flag + 1
                                break
                            elif path2[k] in path1[1:]:
                                flag = flag + 1
                                break
                            else:
                                continue 
                        
                        if flag==0:
                            pair = [path1, path2]
                
                            if hops_list_2[j] in pair_dict:
                                pair_dict[hops_list_2[j]].append(tuple(pair))
                            else:
                                pair_dict[hops_list_2[j]] = [tuple(pair)]
                                
                        pair = []
                    
    return pair_dict



def number_of_path_pairs(hops_pairs):
    numberofpairs_perhop = {}
    key_list = list(hops_pairs.keys())
    for i in range(0, len(hops_pairs)):
        key = key_list[i]
        value = hops_pairs[key]
        numberofpairs_perhop[key] = len(value)
        
    return numberofpairs_perhop



def generate_routepairs_count_s2(nsize):
    
    network = network_matrix(nsize)
    
    file_extension = ".ct"
    
    #r_var = 5 --> count mode
    
    file_name = "NoC_" + str(nsize) + "x" + str(nsize) + "_2S_m1_nooverlap" + file_extension
    filename = os.path.join('count', file_name) 
        
    with open(filename, "w") as f0:
        f0.write("#HOPS-->#PATH_PAIRS\n")
    
    # list out all router ids first, i.e., flatten the network
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
                s1 = routers[y]
                for k in range(0, len(routers)):
                    if routers[k] != d and routers[k] > s1: 
                        s2 = routers[k]
                
                        hops_pairs_dict = hops_and_route_pairs_nooverlap_s2(nsize, s1, s2, d)
                            
                        if len(hops_pairs_dict) != 0:
                            number_of_pairs_perhop = number_of_path_pairs(hops_pairs_dict)
                            hops_list = list(number_of_pairs_perhop.keys()) 
                            
                            with open(filename, "a") as f1:
                                
                                for index1 in range(0, len(number_of_pairs_perhop)):
                                    key = hops_list[index1]
                                    value = number_of_pairs_perhop[key] 
                                    f1.write(str(key) + "-->" + str(value) + " \n") 
