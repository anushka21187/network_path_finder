# ---------- 4 ---------- #
""" REPORT FORMAT """

"""
defaults: num_sources = 1, mode = 0, report_format = 0

For report_format = 2, i.e., to get routes in terms of router/node IDs, call any relevant funtion from routepairs.py.

routes_in_directions
routes_in_directions_s2
routes_in_bits
routes_in_bits_s2
"""

from helpers import *
from common import *
from routepairs import *

# report_format = 1 (directions) 
# num_sources = 1
def routes_in_directions(r, c, s, d, m_var1):
    if m_var1==2:
        hops_pairs = hops_and_route_pairs(r, c, s, d)
    elif m_var1==1:
        hops_pairs = remove_all_overlaps(r, c, s, d)
    else:
        hops_pairs = remove_overlapping_paths(r, c, s, d)
    
    pathdirspairs_perhop = {} 
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
                path_in = pair[j] 
                path = path_in_directions(r, c, path_in)
                
                newpair.append(path) 
                
            newpairslist.append(tuple(newpair))
            
        if hop in list(pathdirspairs_perhop.keys()):
            pathdirspairs_perhop[hop].append(newpairslist)
        else:
            pathdirspairs_perhop[hop] = newpairslist
            
    return pathdirspairs_perhop

# num_sources = 2
def routes_in_directions_s2(r, c, s1, s2, d, m_var1):
    if m_var1==2:
        hops_pairs = hops_and_route_pairs_s2(r, c, s1, s2, d)
    elif m_var1==1:
        hops_pairs = remove_all_overlaps_s2(r, c, s1, s2, d)
    else:
        hops_pairs = remove_overlapping_paths_s2(r, c, s1, s2, d)
    
    pathdirspairs_perhop = {} 
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
                path_in = pair[j] 
                path = path_in_directions(r, c, path_in)
                
                newpair.append(path) 
                
            newpairslist.append(tuple(newpair))
            
        if hop in list(pathdirspairs_perhop.keys()):
            pathdirspairs_perhop[hop].append(newpairslist)
        else:
            pathdirspairs_perhop[hop] = newpairslist
            
    return pathdirspairs_perhop





# report_format = 0 (default) (direction bits)
# num_sources = 1
def routes_in_bits(r, c, s, d, m_var1, north_var1, south_var1, west_var1, east_var1):
    if m_var1==2:
        hops_pairs = hops_and_route_pairs(r, c, s, d)
    elif m_var1==1:
        hops_pairs = remove_all_overlaps(r, c, s, d)
    else:
        hops_pairs = remove_overlapping_paths(r, c, s, d)
    
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
                path_in = pair[j] 
                path = path_in_directions(r, c, path_in)
                newpath = ""
                
                for k in range(0, len(path)): 
                    if path[k] == 'N': 
                        newpath = newpath + north_var1
                    elif path[k] == 'S':
                        newpath = newpath + south_var1
                    elif path[k] == 'W':
                        newpath = newpath + west_var1
                    else:
                        newpath = newpath + east_var1
                
                newpair.append(newpath) 
                
            newpairslist.append(tuple(newpair))
            
        if hop in list(pathbitspairs_perhop.keys()):
            pathbitspairs_perhop[hop].append(newpairslist)
        else:
            pathbitspairs_perhop[hop] = newpairslist
            
    return pathbitspairs_perhop

# num_sources = 2
def routes_in_bits_s2(r, c, s1, s2, d, m_var1, north_var1, south_var1, west_var1, east_var1):
    if m_var1==2:
        hops_pairs = hops_and_route_pairs_s2(r, c, s1, s2, d)
    elif m_var1==1:
        hops_pairs = remove_all_overlaps_s2(r, c, s1, s2, d)
    else:
        hops_pairs = remove_overlapping_paths_s2(r, c, s1, s2, d)
    
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
                path_in = pair[j] 
                path = path_in_directions(r, c, path_in)
                newpath = ""
                
                for k in range(0, len(path)): 
                    if path[k] == 'N': 
                        newpath = newpath + north_var1
                    elif path[k] == 'S':
                        newpath = newpath + south_var1
                    elif path[k] == 'W':
                        newpath = newpath + west_var1
                    else:
                        newpath = newpath + east_var1
                
                newpair.append(newpath) 
                
            newpairslist.append(tuple(newpair))
            
        if hop in list(pathbitspairs_perhop.keys()):
            pathbitspairs_perhop[hop].append(newpairslist)
        else:
            pathbitspairs_perhop[hop] = newpairslist
            
    return pathbitspairs_perhop
