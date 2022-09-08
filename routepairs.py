# ---------- 3 ---------- #
""" FIND ROUTE PAIRS """

"""
defaults: num_sources = 1, mode = 0

1. hops_and_route_pairs: Find all possible pairs of routes from one source to one destination (num_sources = 1, mode = 2)
2. hops_and_route_pairs_s2: Find all possible pairs of routes from two different sources to one destination (num_sources = 2, mode = 2)

3. remove_all_overlaps: Remove pairs with any common node(s) from (1.) (num_sources = 1, mode = 1)
4. remove_all_overlaps_s2: Remove pairs with any common node(s) from (2.) (num_sources = 2, mode = 1)

5. remove_overlapping_paths: Remove pairs with any bidirectional common node(s) (partial overlap) from (1.) (num_sources = 1, mode = 0)
6. remove_overlapping_paths_s2: Remove pairs with any bidirectional common node(s) (partial overlap) from (2.) (num_sources = 2, mode = 0)

All these functions return a dictionary with key = hops, and value = a list of route pairs. 
Each route pair is a tuple of two routes.
Each route is a either a sequence of direction bits, a tuple of direction characters, or a tuple of router/node IDs.
The returned dictionary can look something like:
    { 3: [ ((1, 4, 7, 8), (1, 2, 5, 8)),   <-- one route pair
           ((1, 4, 7, 8), (1, 4, 5, 8)) 
          ],
      5: [ ((1, 0, 3, 6, 7, 8), (1, 2, 5, 4, 7, 8)),
            ...
          ],
      ...
    }
"""

from helpers import *
from common import *

# num_sources = 1, mode = 2
def hops_and_route_pairs(r, c, s, d):
    pair_dict = {} 
    
    #make_source(s)
    path_dict = obtain_paths(r, c, s, d, [], {}, s)
    
    hops_list = list(path_dict.keys())
    hops_list.sort()
    
    # iterate through the hops list
    for i in range(0, len(hops_list)):
        # get the paths list: it is the list of path tuples for this hop count
        list_of_paths = path_dict[hops_list[i]]
        # iterate through all paths 
        # all paths are unique; pair them
        # each combination (a pair) is to be associated with the corresponding hop key
        for p1 in range(0, len(list_of_paths)-1):
            for p2 in range(p1+1, len(list_of_paths)):
                
                pair = [list_of_paths[p1], list_of_paths[p2]]
        
                if hops_list[i] in pair_dict:
                    pair_dict[hops_list[i]].append(tuple(pair))
                else:
                    pair_dict[hops_list[i]] = [tuple(pair)]
                pair = []
                    
    return pair_dict
    
    
    

# num_sources = 2, mode = 2    
def hops_and_route_pairs_s2(r, c, s1, s2, d):
    pair_dict = {} 
    
    #make_source(s1)
    path_dict_1 = obtain_paths(r, c, s1, d, [], {}, s1)
    
    #make_source(s2)
    path_dict_2 = obtain_paths(r, c, s2, d, [], {}, s2)
    
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
                # to get all valid COMBINATIONS
                # each combination (a pair) is to be associated with the corresponding hop key
                for p1 in range(0, len(list_of_paths_1)):
                    for p2 in range(0, len(list_of_paths_2)):
                        pair = [list_of_paths_1[p1], list_of_paths_2[p2]]
                
                        if hops_list_2[j] in pair_dict:
                            pair_dict[hops_list_2[j]].append(tuple(pair))
                        else:
                            pair_dict[hops_list_2[j]] = [tuple(pair)]
                        pair = []
                    
    return pair_dict
    
    
    


# num_sources = 0, mode = 2
def hops_and_route_pairs_s2all(r, c, s1, s2, d):
    
    if s1 != s2:
        return hops_and_route_pairs(r, c, s1, s2, d)
    else:
        return hops_and_route_pairs(r, c, s1, d)





# num_sources = 1, mode = 1    
def remove_all_overlaps(r, c, s, d):
    pair_dict = hops_and_route_pairs(r, c, s, d)
    new_pair_dict = {}
    
    hops_list = list(pair_dict.keys())
    pairslist_list = list(pair_dict.values())
    
    # for a given number of hops
    for i in range(0, len(pairslist_list)): 
        hop = hops_list[i] 
        pairslist = pairslist_list[i] 
        newpairslist = []
        
        for p in range(0, len(pairslist)): 
            pair = pairslist[p]
            newpair = []
            
            path1 = pair[0]
            path2 = pair[1]
             
            # no overlap
            count = 0
            for k in range(1, len(path1)-1):
                if path1[k] in path2[1:]:
                    count = count + 1
                    break
                elif path2[k] in path1[1:]:
                    count = count + 1
                    break
                else:
                    continue 
                
            if count==0:
                newpair.append(path1)
                newpair.append(path2)
                newpairslist.append(tuple(newpair))
        
        if len(newpairslist)!=0:
            if hop in list(new_pair_dict.keys()):
                new_pair_dict[hop].append(newpairslist)
            else:
                new_pair_dict[hop] = newpairslist
            
    return new_pair_dict
    
    
    
    
    
# num_sources = 2, mode = 1    
def remove_all_overlaps_s2(r, c, s1, s2, d):
    pair_dict = hops_and_route_pairs_s2(r, c, s1, s2, d)
    new_pair_dict = {}
    
    hops_list = list(pair_dict.keys())
    pairslist_list = list(pair_dict.values())
    
    # for a given number of hops
    for i in range(0, len(pairslist_list)): 
        hop = hops_list[i] 
        pairslist = pairslist_list[i] 
        newpairslist = []
        
        for p in range(0, len(pairslist)): 
            pair = pairslist[p]
            newpair = []
            
            path1 = pair[0]
            path2 = pair[1]
             
            # no overlap
            count = 0
            for k in range(0, len(path1)-1):
                if path1[k] in path2[1:]:
                    count = count + 1
                    break
                elif path2[k] in path1[1:]:
                    count = count + 1
                    break
                else:
                    continue 
                
            if count==0:
                newpair.append(path1)
                newpair.append(path2)
                newpairslist.append(tuple(newpair))
        
        if len(newpairslist)!=0:
            if hop in list(new_pair_dict.keys()):
                new_pair_dict[hop].append(newpairslist)
            else:
                new_pair_dict[hop] = newpairslist
            
    return new_pair_dict





# num_sources = 0, mode = 1
def remove_all_overlaps_s2all(r, c, s1, s2, d):
    if s1 != s2:
        return remove_all_overlaps(r, c, s1, s2, d)
    else:
        return remove_all_overlaps(r, c, s1, d)





# num_sources = 1, mode = 0    
def remove_overlapping_paths(r, c, s, d):
    pair_dict = hops_and_route_pairs(r, c, s, d)
    new_pair_dict = {}
    
    hops_list = list(pair_dict.keys())
    pairslist_list = list(pair_dict.values())
    
    # for a given number of hops
    for i in range(0, len(pairslist_list)): 
        hop = hops_list[i] 
        pairslist = pairslist_list[i] 
        newpairslist = []
        
        for p in range(0, len(pairslist)): 
            pair = pairslist[p]
            newpair = []
            
            path1 = pair[0]
            path2 = pair[1]
            
            # default --> partial overlap
            count = 0
            for k in range(1, len(path1)-1): 
                if path1[0] in path2[1:]:
                    count = count+1
                    break
                elif path2[0] in path1[1:]:
                    count = count+1
                    break
                elif path1[k]!=path2[k]:
                    continue
                else:
                    if path1[k-1]==path2[k-1] or path1[k-1]==path2[k+1] or path1[k+1]==path2[k-1]:
                        count = count+1
                        break
                    elif k==len(path1)-1-1:
                        count = count+1
                        break
                    else:
                        continue
                
            if count==0:
                newpair.append(path1)
                newpair.append(path2)
                newpairslist.append(tuple(newpair))
        
        if len(newpairslist)!=0:
            if hop in list(new_pair_dict.keys()):
                new_pair_dict[hop].append(newpairslist)
            else:
                new_pair_dict[hop] = newpairslist
            
    return new_pair_dict





# num_sources = 2, mode = 0    
def remove_overlapping_paths_s2(r, c, s1, s2, d):
    pair_dict = hops_and_route_pairs_s2(r, c, s1, s2, d)
    new_pair_dict = {}
    
    hops_list = list(pair_dict.keys())
    pairslist_list = list(pair_dict.values())
    
    # for a given number of hops
    for i in range(0, len(pairslist_list)): 
        hop = hops_list[i] 
        pairslist = pairslist_list[i] 
        newpairslist = []
        
        for p in range(0, len(pairslist)): 
            pair = pairslist[p]
            newpair = []
            
            path1 = pair[0]
            path2 = pair[1]
            
            # default --> partial overlap
            count = 0
            for k in range(1, len(path1)-1): 
                if path1[0] in path2[1:]:
                    count = count+1
                    break
                elif path2[0] in path1[1:]:
                    count = count+1
                    break
                elif path1[k]!=path2[k]:
                    continue
                else:
                    if path1[k-1]==path2[k-1] or path1[k-1]==path2[k+1] or path1[k+1]==path2[k-1]:
                        count = count+1
                        break
                    elif k==len(path1)-1-1:
                        count = count+1
                        break
                    else:
                        continue
                
            if count==0:
                newpair.append(path1)
                newpair.append(path2)
                newpairslist.append(tuple(newpair))
        
        if len(newpairslist)!=0:
            if hop in list(new_pair_dict.keys()):
                new_pair_dict[hop].append(newpairslist)
            else:
                new_pair_dict[hop] = newpairslist
            
    return new_pair_dict





# num_sources = 0, mode = 0    
def remove_overlapping_paths_s2all(r, c, s1, s2, d):
    if s1 != s2:
        return remove_overlapping_paths_s2(r, c, s1, s2, d)
    else:
        return remove_overlapping_paths(r, c, s1, d) 

