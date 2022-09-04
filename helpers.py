# ---------- 0 ---------- #
""" HELPERS """

"""
1. make_source: Sets the global source variable to the one used in obtain_paths 
2. number_of_path_pairs: Given a dictionary with key = hops, and value = a list of path pairs, returns a dictionary with key = hops, and value = number of path pairs
3. exchange_key_value: Given a dictionary with key = in_key, and value = in_value, returns a dictionary with key = in_value, and value = in_key
4. path_in_directions: Given a tuple of router IDs, returns a tuple of directions
""" 


def make_source(router_id):
    global source
    source = router_id





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





def path_in_directions(r, c, path):
    dir_path = []
    for i in range(0, len(path)-1):
        cur_node = path[i]
        next_node = path[i+1]
        
        if cur_node < c:
            if next_node == cur_node + c:
                dir_path.append('S') 
            elif cur_node%c==0:
                if next_node == cur_node + 1:
                    dir_path.append('E')
            elif cur_node-(c-1)%c==0:
                if next_node == cur_node - 1:
                    dir_path.append('W')
            else:
                if next_node == cur_node + 1:
                    dir_path.append('E')
                elif next_node == cur_node - 1:
                    dir_path.append('W')
        elif cur_node < ((r*c)-1) and cur_node > ((r*c)-1-c): 
            if next_node == cur_node - c:
                dir_path.append('N') 
            elif cur_node%c==0: 
                if next_node == cur_node + 1:
                    dir_path.append('E') 
            elif cur_node-(c-1)%c==0: 
                if next_node == cur_node - 1:
                    dir_path.append('W') 
            else: 
                if next_node == cur_node + 1:
                    dir_path.append('E')
                elif next_node == cur_node - 1:
                    dir_path.append('W') 
        else: 
            if next_node == cur_node + c:
                dir_path.append('S')
            elif next_node == cur_node - c:
                dir_path.append('N') 
            elif cur_node%c==0: 
                if next_node == cur_node + 1:
                    dir_path.append('E') 
            elif cur_node-(c-1)%c==0: 
                if next_node == cur_node - 1:
                    dir_path.append('W') 
            else: 
                if next_node == cur_node + 1:
                    dir_path.append('E')
                elif next_node == cur_node - 1:
                    dir_path.append('W')
        
                    
    return tuple(dir_path)
    
