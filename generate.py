# ---------- 5 ---------- #
""" GENERATE REPORTS """

from helpers import *
from common import *
from routepairs import *
from reportformat import *

import os


# num_sources = 1
def generate_routepairs(r, c, m_var, r_var, north_var, south_var, west_var, east_var):
    
    network = network_matrix(r, c)
    
    spaces = "          " # 10 spaces
    spaces_halved = "     " # 5 spaces
    spaces_halved_small = "    " # 4 spaces
    file_extension = ".rpt"
    
    
    if m_var == 2: 
        m_string = '_withoverlap'
    elif m_var == 1:
        m_string = '_nooverlap'
    else:
        m_string = ''
    
    if r_var == 2:
        rf_string = '_routers'
    elif r_var == 1:
        rf_string = '_directions'
    else:
        rf_string = ''
    
    file_name = "NoC_" + str(r) + "x" + str(c) + m_string + rf_string + file_extension
    filename = os.path.join('reports', file_name)
    
    
    with open(filename, "w") as f0:
        f0.write("----- START ----- \n\n")
        f0.write("Number of rows = " + str(r) + " \n")
        f0.write("Number of columns = " + str(c) + " \n")
        f0.write("Network: \n")
        
        f0.write(spaces)
        for i in range(0, len(network)):
            for j in range(0, len(network[i])):
                if network[i][j] < 10:
                    f0.write(str(network[i][j])+spaces_halved)
                else:
                    f0.write(str(network[i][j])+spaces_halved_small)
            f0.write("\n"+spaces)
        f0.write("\n")
        
        f0.write("Port reference: N = " + north_var + ", S = " + south_var + ", W = " + west_var + ", E = " + east_var + " \n\n\n")
    
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
                s = routers[y]
                
                if r_var == 2:
                    if m_var == 2:
                        hops_pairs_dict = hops_and_route_pairs(r, c, s, d)
                    elif m_var == 1:
                        hops_pairs_dict = remove_all_overlaps(r, c, s, d)
                    else:
                        hops_pairs_dict = remove_overlapping_paths(r, c, s, d)
                elif r_var == 1:
                    hops_pairs_dict = routes_in_directions(r, c, s, d, m_var)
                else:
                    hops_pairs_dict = routes_in_bits(r, c, s, d, m_var, north_var, south_var, west_var, east_var) 
                
                if len(hops_pairs_dict) != 0:
                    number_of_pairs_perhop = number_of_path_pairs(hops_pairs_dict)
                    hops_list = list(number_of_pairs_perhop.keys())
                    min_hops = min(hops_list)
                    max_hops = max(hops_list)
                    number_of_hops_perpair = exchange_key_value(number_of_pairs_perhop)
                    min_pairs = min(list(number_of_hops_perpair.keys()))
                    min_pairs_hop = number_of_hops_perpair[min_pairs]
                    max_pairs = max(list(number_of_hops_perpair.keys()))
                    max_pairs_hop = number_of_hops_perpair[max_pairs]   
                    
                    with open(filename, "a") as f1:
                        f1.write("s = "+str(s)+", d = "+str(d)+": \n")
                        f1.write(spaces+"Minimum hops = "+str(min_hops)+" \n")
                        f1.write(spaces+"Maximum hops = "+str(max_hops)+" \n")
                        f1.write(spaces+"Minimum path pairs = "+str(min_pairs)+" ")
                        f1.write("for hop count = "+str(min_pairs_hop)+" \n")
                        f1.write(spaces+"Maximum path pairs = "+str(max_pairs)+" ")
                        f1.write("for hop count = "+str(max_pairs_hop)+" \n")
                        f1.write("\n")
                        
                        for index1 in range(0, len(hops_pairs_dict)):
                            key = hops_list[index1]
                            f1.write(spaces+"HOPS = "+str(key)+" \n")
                            value = hops_pairs_dict[key]
                            for index2 in range(0, len(value)):
                                pair = value[index2]
                                f1.write(spaces+spaces+"PAIR_"+str(index2+1)+": "+str(pair[0])+", "+str(pair[1])+" \n")
                       
                        f1.write("\n\n")
                        
    with open(filename, "a") as f2:
        f2.write("----- END ----- \n")
        
        
        
        

# num_sources = 2
def generate_routepairs_s2(r, c, m_var, r_var, north_var, south_var, west_var, east_var):
    
    network = network_matrix(r, c)
    
    spaces = "          " # 10 spaces
    spaces_halved = "     " # 5 spaces
    spaces_halved_small = "    " # 4 spaces
    file_extension = ".rpt"
    
    
    if m_var == 2: 
        m_string = '_withoverlap'
    elif m_var == 1:
        m_string = '_nooverlap'
    else:
        m_string = ''
    
    if r_var == 2:
        rf_string = '_routers'
    elif r_var == 1:
        rf_string = '_directions'
    else:
        rf_string = ''
    
    file_name = "NoC_" + str(r) + "x" + str(c) + "_2S" + m_string + rf_string + file_extension
    filename = os.path.join('reports', file_name)
    
    with open(filename, "w") as f0:
        f0.write("----- START ----- \n\n")
        f0.write("Number of rows = " + str(r) + " \n")
        f0.write("Number of columns = " + str(c) + " \n")
        f0.write("Network: \n")
        
        f0.write(spaces)
        for i in range(0, len(network)):
            for j in range(0, len(network[i])):
                if network[i][j] < 10:
                    f0.write(str(network[i][j])+spaces_halved)
                else:
                    f0.write(str(network[i][j])+spaces_halved_small)
            f0.write("\n"+spaces)
        f0.write("\n")
        
        f0.write("Port reference: N = " + north_var + ", S = " + south_var + ", W = " + west_var + ", E = " + east_var + " \n\n\n")
    
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
                
                        if r_var == 2:
                            if m_var == 2:
                                hops_pairs_dict = hops_and_route_pairs_s2(r, c, s1, s2, d)
                            elif m_var == 1:
                                hops_pairs_dict = remove_all_overlaps_s2(r, c, s1, s2, d)
                            else:
                                hops_pairs_dict = remove_overlapping_paths_s2(r, c, s1, s2, d)
                        elif r_var == 1:
                            hops_pairs_dict = routes_in_directions_s2(r, c, s1, s2, d, m_var)
                        else:
                            hops_pairs_dict = routes_in_bits_s2(r, c, s1, s2, d, m_var, north_var, south_var, west_var, east_var) 
                        
                        if len(hops_pairs_dict) != 0:
                            number_of_pairs_perhop = number_of_path_pairs(hops_pairs_dict)
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
                                
                                for index1 in range(0, len(hops_pairs_dict)):
                                    key = hops_list[index1]
                                    f1.write(spaces+"HOPS = "+str(key)+" \n")
                                    value = hops_pairs_dict[key]
                                    for index2 in range(0, len(value)):
                                        pair = value[index2]
                                        f1.write(spaces+spaces+"PAIR_"+str(index2+1)+": "+str(pair[0])+", "+str(pair[1])+" \n")
                               
                                f1.write("\n\n")
                        
    with open(filename, "a") as f2:
        f2.write("----- END ----- \n")





# num_sources = 0
def generate_routepairs_s2all(r, c, m_var, r_var, north_var, south_var, west_var, east_var):
    
    network = network_matrix(r, c)
    
    spaces = "          " # 10 spaces
    spaces_halved = "     " # 5 spaces
    spaces_halved_small = "    " # 4 spaces
    file_extension = ".rpt"
    
    
    if m_var == 2: 
        m_string = '_withoverlap'
    elif m_var == 1:
        m_string = '_nooverlap'
    else:
        m_string = ''
    
    if r_var == 2:
        rf_string = '_routers'
    elif r_var == 1:
        rf_string = '_directions'
    else:
        rf_string = ''
    
    file_name = "NoC_" + str(r) + "x" + str(c) + "_2S-all" + m_string + rf_string + file_extension
    filename = os.path.join('reports', file_name)
    
    with open(filename, "w") as f0:
        f0.write("----- START ----- \n\n")
        f0.write("Number of rows = " + str(r) + " \n")
        f0.write("Number of columns = " + str(c) + " \n")
        f0.write("Network: \n")
        
        f0.write(spaces)
        for i in range(0, len(network)):
            for j in range(0, len(network[i])):
                if network[i][j] < 10:
                    f0.write(str(network[i][j])+spaces_halved)
                else:
                    f0.write(str(network[i][j])+spaces_halved_small)
            f0.write("\n"+spaces)
        f0.write("\n")
        
        f0.write("Port reference: N = " + north_var + ", S = " + south_var + ", W = " + west_var + ", E = " + east_var + " \n\n\n")
    
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
                    if routers[k] != d and routers[k] >= s1: 
                        s2 = routers[k]
                
                        if r_var == 2:
                            if m_var == 2:
                                hops_pairs_dict = hops_and_route_pairs_s2all(r, c, s1, s2, d)
                            elif m_var == 1:
                                hops_pairs_dict = remove_all_overlaps_s2all(r, c, s1, s2, d)
                            else:
                                hops_pairs_dict = remove_overlapping_paths_s2all(r, c, s1, s2, d)
                        elif r_var == 1:
                            hops_pairs_dict = routes_in_directions_s2all(r, c, s1, s2, d, m_var)
                        else:
                            hops_pairs_dict = routes_in_bits_s2all(r, c, s1, s2, d, m_var, north_var, south_var, west_var, east_var) 
                        
                        if len(hops_pairs_dict) != 0:
                            number_of_pairs_perhop = number_of_path_pairs(hops_pairs_dict)
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
                                
                                for index1 in range(0, len(hops_pairs_dict)):
                                    key = hops_list[index1]
                                    f1.write(spaces+"HOPS = "+str(key)+" \n")
                                    value = hops_pairs_dict[key]
                                    for index2 in range(0, len(value)):
                                        pair = value[index2]
                                        f1.write(spaces+spaces+"PAIR_"+str(index2+1)+": "+str(pair[0])+", "+str(pair[1])+" \n")
                               
                                f1.write("\n\n")
                        
    with open(filename, "a") as f2:
        f2.write("----- END ----- \n")






# report_format = 3
# num_sources = 1
def generate_routepairs_concise(r, c, m_var, north_var, south_var, west_var, east_var):
    
    network = network_matrix(r, c)

    file_extension = ".rpt"
    
    
    if m_var == 2: 
        m_string = '_withoverlap'
    elif m_var == 1:
        m_string = '_nooverlap'
    else:
        m_string = ''
    
    file_name = "NoC_" + str(r) + "x" + str(c) + m_string + "_concise" + file_extension
    filename = os.path.join('reports', file_name)
    
    
    with open(filename, "w") as f0:
        f0.write("----- START ----- \n") 
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
                s = routers[y]
                
                hops_pairs_dict = routes_in_bits(r, c, s, d, m_var, north_var, south_var, west_var, east_var)
                if m_var == 2:
                    reference_dict = hops_and_route_pairs(r, c, s, d)
                elif m_var == 1:
                    reference_dict = remove_all_overlaps(r, c, s, d)
                else:
                    reference_dict = remove_overlapping_paths(r, c, s, d)
                
                if len(hops_pairs_dict) != 0:
                    number_of_pairs_perhop = number_of_path_pairs(hops_pairs_dict)
                    hops_list = list(number_of_pairs_perhop.keys()) 
                    
                    with open(filename, "a") as f1: 
                        
                        for index1 in range(0, len(hops_pairs_dict)):
                            key = hops_list[index1]                         
                                                        
                            value = hops_pairs_dict[key]
                            ref_value = reference_dict[key]
                            
                            for index2 in range(0, len(value)): 
                                pair = value[index2]
                                ref_pair = ref_value[index2]
                               
                                f1.write(str(s)+"_"+str(d)+"_hop"+str(key)+" = ")
 
                                for path_index in range(0, 2):
                                    path_frompair = pair[path_index]
                                    ref_path_frompair = ref_pair[path_index]
                                    new_path = []

                                    for bit_index in range(0, len(path_frompair), 2):
                                        if bit_index == 0:
                                            f1.write("(")
                                        f1.write(str(ref_path_frompair[int(bit_index/2)])+":"+str(path_frompair[bit_index])+str(path_frompair[bit_index+1]))
                                        f1.write(", ")
                                    f1.write(str(d)+":00)")
                                    
                                    if path_index==0:
                                        f1.write(", ")
                                    else:
                                        f1.write(" \n")                                

    with open(filename, "a") as f2:
        f2.write("----- END ----- \n") 



# num_sources = 2
def generate_routepairs_concise_s2(r, c, m_var, north_var, south_var, west_var, east_var):
    
    network = network_matrix(r, c)

    file_extension = ".rpt"
    
    
    if m_var == 2: 
        m_string = '_withoverlap'
    elif m_var == 1:
        m_string = '_nooverlap'
    else:
        m_string = ''
    
    file_name = "NoC_" + str(r) + "x" + str(c) + "_2S" + m_string + "_concise" + file_extension
    filename = os.path.join('reports', file_name)
    
    
    with open(filename, "w") as f0:
        f0.write("----- START ----- \n") 
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
                
                        hops_pairs_dict = routes_in_bits_s2(r, c, s1, s2, d, m_var, north_var, south_var, west_var, east_var)
                        if m_var == 2:
                            reference_dict = hops_and_route_pairs_s2(r, c, s1, s2, d)
                        elif m_var == 1:
                            reference_dict = remove_all_overlaps_s2(r, c, s1, s2, d)
                        else:
                            reference_dict = remove_overlapping_paths_s2(r, c, s1, s2, d)
                        
                        if len(hops_pairs_dict) != 0:
                            number_of_pairs_perhop = number_of_path_pairs(hops_pairs_dict)
                            hops_list = list(number_of_pairs_perhop.keys()) 
                            
                            with open(filename, "a") as f1: 
                                
                                for index1 in range(0, len(hops_pairs_dict)):
                                    key = hops_list[index1]
                                    
                                    value = hops_pairs_dict[key]
                                    ref_value = reference_dict[key]
                                    
                                    for index2 in range(0, len(value)): 
                                        pair = value[index2]
                                        ref_pair = ref_value[index2]

                                        f1.write(str(s1)+"_"+str(s2)+"_"+str(d)+"_hop"+str(key)+" = ")

                                        for path_index in range(0, 2):
                                            path_frompair = pair[path_index]
                                            ref_path_frompair = ref_pair[path_index]
                                            new_path = []
                                            for bit_index in range(0, len(path_frompair), 2):
                                                if bit_index == 0:
                                                    f1.write("(")
                                                f1.write(str(ref_path_frompair[int(bit_index/2)])+":"+str(path_frompair[bit_index])+str(path_frompair[bit_index+1]))
                                                f1.write(", ")
                                            f1.write(str(d)+":00)")
                                    
                                            if path_index==0:
                                                f1.write(", ")
                                            else:
                                                f1.write(" \n")                               

    with open(filename, "a") as f2:
        f2.write("----- END ----- \n")
        


        
# num_sources = 0
def generate_routepairs_concise_s2all(r, c, m_var, north_var, south_var, west_var, east_var):
    
    network = network_matrix(r, c)

    file_extension = ".rpt"
    
    
    if m_var == 2: 
        m_string = '_withoverlap'
    elif m_var == 1:
        m_string = '_nooverlap'
    else:
        m_string = ''
    
    file_name = "NoC_" + str(r) + "x" + str(c) + "_2S-all" + m_string + "_concise" + file_extension
    filename = os.path.join('reports', file_name)
    
    
    with open(filename, "w") as f0:
        f0.write("----- START ----- \n") 
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
                    if routers[k] != d and routers[k] >= s1: 
                        s2 = routers[k]
                
                        hops_pairs_dict = routes_in_bits_s2all(r, c, s1, s2, d, m_var, north_var, south_var, west_var, east_var)
                        if m_var == 2:
                            reference_dict = hops_and_route_pairs_s2all(r, c, s1, s2, d)
                        elif m_var == 1:
                            reference_dict = remove_all_overlaps_s2all(r, c, s1, s2, d)
                        else:
                            reference_dict = remove_overlapping_paths_s2all(r, c, s1, s2, d)
                        
                        if len(hops_pairs_dict) != 0:
                            number_of_pairs_perhop = number_of_path_pairs(hops_pairs_dict)
                            hops_list = list(number_of_pairs_perhop.keys()) 
                            
                            with open(filename, "a") as f1: 
                                
                                for index1 in range(0, len(hops_pairs_dict)):
                                    key = hops_list[index1]
                                    
                                    value = hops_pairs_dict[key]
                                    ref_value = reference_dict[key]
                                    
                                    for index2 in range(0, len(value)): 
                                        pair = value[index2]
                                        ref_pair = ref_value[index2]

                                        f1.write(str(s1)+"_"+str(s2)+"_"+str(d)+"_hop"+str(key)+" = ")

                                        for path_index in range(0, 2):
                                            path_frompair = pair[path_index]
                                            ref_path_frompair = ref_pair[path_index]
                                            new_path = []
                                            for bit_index in range(0, len(path_frompair), 2):
                                                if bit_index == 0:
                                                    f1.write("(")
                                                f1.write(str(ref_path_frompair[int(bit_index/2)])+":"+str(path_frompair[bit_index])+str(path_frompair[bit_index+1]))
                                                f1.write(", ")
                                            f1.write(str(d)+":00)")
                                    
                                            if path_index==0:
                                                f1.write(", ")
                                            else:
                                                f1.write(" \n")                               

                                
    with open(filename, "a") as f2:
        f2.write("----- END ----- \n") 



# report_format = 4
# num_sources = 1
def generate_routepairs_stimuli(r, c, s_var, m_var, north_var, south_var, west_var, east_var):
    
    network = network_matrix(r, c)
    
    file_dir = 'stimuli_'+str(r)+'x'+str(c)+'_m'+str(m_var)
    file_extension = '.sp'
    
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
                s = routers[y]
                
                hops_pairs_dict = routes_in_bits(r, c, s, d, m_var, north_var, south_var, west_var, east_var)
                if m_var == 2:
                    reference_dict = hops_and_route_pairs_s2(r, c, s, d)
                elif m_var == 1:
                    reference_dict = remove_all_overlaps(r, c, s, d)
                else:
                    reference_dict = remove_overlapping_paths(r, c, s, d)
                
                if len(hops_pairs_dict) != 0:
                    number_of_pairs_perhop = number_of_path_pairs(hops_pairs_dict)
                    hops_list = list(number_of_pairs_perhop.keys())    
                    
                        
                    for index1 in range(0, len(hops_pairs_dict)):
                        key = hops_list[index1]
                        
                        value = hops_pairs_dict[key]
                        ref_value = reference_dict[key]
                        
                        for index2 in range(0, len(value)): 
                            pair = value[index2]
                            ref_pair = ref_value[index2]

                            file_name = 'stimuli.noc.' + str(s) + '.' + str(d)+ '.' + 'hop' + str(key) + 'pair' + str(index2+1) + file_extension
                            filename = os.path.join(file_dir, file_name)
                            with open(filename, "w") as f1:
                                
                                for path_index in range(0, 2):
                                    path_frompair_temp = pair[path_index]
                                    path_frompair = path_frompair_temp + '00'
                                    ref_path_frompair = ref_pair[path_index]
                                    new_path = []
                                    
                                    f1.write('* Data transfer from: R' + str(s) + ' to R' + str(d) + ' --> Circuit Switched Path: \n') 
                                    
                                    for bit_index in range(0, len(path_frompair), 2):
                                        
                                        
                                        # source - define MSB, input port
                                        if bit_index==0:
                                            MSB = '1' 
                                            supply = 'vh'
                                            inportbits = '00'
                                            in_dir_string = 'local'
                                            
                                            outportbits = str(path_frompair[bit_index])+str(path_frompair[bit_index+1])
                                            if outportbits == str(north_var):
                                                out_dir_string = 'north' 
                                            elif outportbits == str(south_var):
                                                out_dir_string = 'south'
                                            elif outportbits == str(west_var):
                                                out_dir_string = 'west'    
                                            else:
                                                out_dir_string = 'east'
                                            out_dir_string_sel = str(out_dir_string[0])
                                        
                                        # if any node other than the source - set MSB, input port
                                        else:
                                            MSB = '0'
                                            supply = '0'
                                            
                                            prevportbits = str(path_frompair[bit_index-2])+str(path_frompair[bit_index-1])
                                            if prevportbits=='00':
                                                inportbits = '11'
                                            elif prevportbits=='11':
                                                inportbits = '00'
                                            elif prevportbits=='01':
                                                inportbits = '10'
                                            else:
                                                inportbits = '01'

                                            if inportbits == str(north_var):
                                                in_dir_string = 'north'
                                            elif inportbits == str(south_var):
                                                in_dir_string = 'south'
                                            elif inportbits == str(west_var):
                                                in_dir_string = 'west'    
                                            else:
                                                in_dir_string = 'east'
                                            
                                            # destination - set output port
                                            outportbits = '00'
                                            if bit_index==len(path_frompair)-2:
                                                if path_index==0:
                                                    out_dir_string = 'local0'     
                                                else:
                                                    out_dir_string = 'local1'
                                                out_dir_string_sel = str(out_dir_string[0])+str(out_dir_string[-1])
                                            # any other node
                                            else:
                                                outportbits = str(path_frompair[bit_index])+str(path_frompair[bit_index+1])
                                                if outportbits == str(north_var):
                                                    out_dir_string = 'north' 
                                                elif outportbits == str(south_var):
                                                    out_dir_string = 'south'
                                                elif outportbits == str(west_var):
                                                    out_dir_string = 'west'    
                                                else:
                                                    out_dir_string = 'east' 
                                                out_dir_string_sel = str(out_dir_string[0])
                                            
                                        
                                        f1.write('* R'+str(ref_path_frompair[int(bit_index/2)])+': out'+out_dir_string+' mux select line s2s1s0 = '+MSB+str(inportbits)+' (selecting in'+in_dir_string+' port): \n') 
                                            
                                        for q in range (2, -1, -1):
                                            f1.write('vr'+str(ref_path_frompair[int(bit_index/2)])+'_s'+str(q)+out_dir_string_sel)
                                            f1.write(' r'+str(ref_path_frompair[int(bit_index/2)])+'_s'+str(q)+out_dir_string_sel)
                                            if q==2:
                                                f1.write(' 0 ' + supply + ' \n')
                                            else:
                                                if q==1:
                                                    q_new = 0
                                                else:
                                                    q_new = 1
                                                if inportbits[q_new] == '0':
                                                    f1.write(' 0 ' + '0' + ' \n')
                                                else:
                                                    f1.write(' 0 ' + 'vh' + ' \n')
                                        
                                     
                                        if bit_index==len(path_frompair)-2:
                                            if path_index==0:
                                                f1.write('\n*** Input starting at R' + str(ref_path_frompair[0]) + ': \n')
                                                f1.write('vr' + str(ref_path_frompair[0]) + '_inlocal')
                                                f1.write(' r' + str(ref_path_frompair[0]) + '_inlocal')
                                                f1.write(" 0 pulse(vh 0 0 slope slope th '2*th') \n")
                                                f1.write('*** To observe: out'+out_dir_string+' port \n\n')
                                            else:
                                                f1.write('\n*** Input starting at R' + str(ref_path_frompair[0]) + ': \n')
                                                f1.write('vr' + str(ref_path_frompair[0]) + '_inlocal')
                                                f1.write(' r' + str(ref_path_frompair[0]) + '_inlocal')
                                                f1.write(" 0 pulse(vh 0 clockDelay slope slope th '2*th') \n")
                                                f1.write('*** To observe: out'+out_dir_string+' port \n\n')




# num_sources = 2
def generate_routepairs_stimuli_s2(r, c, s_var, m_var, north_var, south_var, west_var, east_var):
    
    network = network_matrix(r, c)
    
    file_dir = 'stimuli_'+str(r)+'x'+str(c)+'_2S'+'_m'+str(m_var)
    file_extension = '.sp'
    
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
                
                        hops_pairs_dict = routes_in_bits_s2(r, c, s1, s2, d, m_var, north_var, south_var, west_var, east_var)
                        if m_var == 2:
                            reference_dict = hops_and_route_pairs_s2(r, c, s1, s2, d)
                        elif m_var == 1:
                            reference_dict = remove_all_overlaps_s2(r, c, s1, s2, d)
                        else:
                            reference_dict = remove_overlapping_paths_s2(r, c, s1, s2, d)
                        
                        if len(hops_pairs_dict) != 0:
                            number_of_pairs_perhop = number_of_path_pairs(hops_pairs_dict)
                            hops_list = list(number_of_pairs_perhop.keys())    
                            
                                
                            for index1 in range(0, len(hops_pairs_dict)):
                                key = hops_list[index1]
                                
                                value = hops_pairs_dict[key]
                                ref_value = reference_dict[key]
                                
                                for index2 in range(0, len(value)): 
                                    pair = value[index2]
                                    ref_pair = ref_value[index2]

                                    file_name = 'stimuli.noc.' + str(s1) + '.' + str(s2) + '.' + str(d)+ '.' + 'hop' + str(key) + 'pair' + str(index2+1) + file_extension
                                    filename = os.path.join(file_dir, file_name)
                                    with open(filename, "w") as f1:
                                        
                                        for path_index in range(0, 2):
                                            path_frompair_temp = pair[path_index]
                                            path_frompair = path_frompair_temp + '00'
                                            ref_path_frompair = ref_pair[path_index]
                                            new_path = []
                                            
                                            if path_index == 0:
                                                f1.write('* Data transfer from: R' + str(s1) + ' to R' + str(d) + ' --> Circuit Switched Path: \n')
                                            else:
                                                f1.write('* Data transfer from: R' + str(s2) + ' to R' + str(d) + ' --> Circuit Switched Path: \n')
                                            
                                            for bit_index in range(0, len(path_frompair), 2):
                                                
                                                
                                                # source - define MSB, input port
                                                if bit_index==0:
                                                    MSB = '1' 
                                                    supply = 'vh'
                                                    inportbits = '00'
                                                    in_dir_string = 'local'
                                                    
                                                    outportbits = str(path_frompair[bit_index])+str(path_frompair[bit_index+1])
                                                    if outportbits == str(north_var):
                                                        out_dir_string = 'north' 
                                                    elif outportbits == str(south_var):
                                                        out_dir_string = 'south'
                                                    elif outportbits == str(west_var):
                                                        out_dir_string = 'west'    
                                                    else:
                                                        out_dir_string = 'east'
                                                    out_dir_string_sel = str(out_dir_string[0])
                                                
                                                # if any node other than the source - set MSB, input port
                                                else:
                                                    MSB = '0'
                                                    supply = '0'
                                                    
                                                    prevportbits = str(path_frompair[bit_index-2])+str(path_frompair[bit_index-1])
                                                    if prevportbits=='00':
                                                    	inportbits = '11'
                                                    elif prevportbits=='11':
                                                        inportbits = '00'
                                                    elif prevportbits=='01':
                                                        inportbits = '10'
                                                    else:
                                                        inportbits = '01'

                                                    if inportbits == str(north_var):
                                                        in_dir_string = 'north'
                                                    elif inportbits == str(south_var):
                                                        in_dir_string = 'south'
                                                    elif inportbits == str(west_var):
                                                        in_dir_string = 'west'    
                                                    else:
                                                        in_dir_string = 'east'
                                                    
                                                    # destination - set output port
                                                    outportbits = '00'
                                                    if bit_index==len(path_frompair)-2:
                                                        if path_index==0:
                                                            out_dir_string = 'local0'     
                                                        else:
                                                            out_dir_string = 'local1'
                                                        out_dir_string_sel = str(out_dir_string[0])+str(out_dir_string[-1])
                                                    # any other node
                                                    else:
                                                        outportbits = str(path_frompair[bit_index])+str(path_frompair[bit_index+1])
                                                        if outportbits == str(north_var):
                                                            out_dir_string = 'north' 
                                                        elif outportbits == str(south_var):
                                                            out_dir_string = 'south'
                                                        elif outportbits == str(west_var):
                                                            out_dir_string = 'west'    
                                                        else:
                                                            out_dir_string = 'east' 
                                                        out_dir_string_sel = str(out_dir_string[0])
                                                    
                                                
                                                f1.write('* R'+str(ref_path_frompair[int(bit_index/2)])+': out'+out_dir_string+' mux select line s2s1s0 = '+MSB+str(inportbits)+' (selecting in'+in_dir_string+' port): \n') 
                                                    
                                                for q in range (2, -1, -1):
                                                    f1.write('vr'+str(ref_path_frompair[int(bit_index/2)])+'_s'+str(q)+out_dir_string_sel)
                                                    f1.write(' r'+str(ref_path_frompair[int(bit_index/2)])+'_s'+str(q)+out_dir_string_sel)
                                                    if q==2:
                                                        f1.write(' 0 ' + supply + ' \n')
                                                    else:
                                                        if q==1:
                                                            q_new = 0
                                                        else:
                                                            q_new = 1
                                                        if inportbits[q_new] == '0':
                                                            f1.write(' 0 ' + '0' + ' \n')
                                                        else:
                                                            f1.write(' 0 ' + 'vh' + ' \n')
                                                
                                             
                                                if bit_index==len(path_frompair)-2:
                                                    if path_index==0:
                                                        f1.write('\n*** Input starting at R' + str(ref_path_frompair[0]) + ': \n')
                                                        f1.write('vr' + str(ref_path_frompair[0]) + '_inlocal')
                                                        f1.write(' r' + str(ref_path_frompair[0]) + '_inlocal')
                                                        f1.write(" 0 pulse(vh 0 0 slope slope th '2*th') \n")
                                                        f1.write('*** To observe: out'+out_dir_string+' port \n\n')
                                                    else:
                                                        f1.write('\n*** Input starting at R' + str(ref_path_frompair[0]) + ': \n')
                                                        f1.write('vr' + str(ref_path_frompair[0]) + '_inlocal')
                                                        f1.write(' r' + str(ref_path_frompair[0]) + '_inlocal')
                                                        f1.write(" 0 pulse(vh 0 clockDelay slope slope th '2*th') \n")
                                                        f1.write('*** To observe: out'+out_dir_string+' port \n\n')
     

# num_sources = 0
def generate_routepairs_stimuli_s2all(r, c, s_var, m_var, north_var, south_var, west_var, east_var):
    
    network = network_matrix(r, c)
    
    file_dir = 'stimuli_'+str(r)+'x'+str(c)+'_2S-all_m'+str(m_var)
    file_extension = '.sp'
    
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
                    if routers[k] != d and routers[k] >= s1: 
                        s2 = routers[k]
                
                        hops_pairs_dict = routes_in_bits_s2all(r, c, s1, s2, d, m_var, north_var, south_var, west_var, east_var)
                        if m_var == 2:
                            reference_dict = hops_and_route_pairs_s2all(r, c, s1, s2, d)
                        elif m_var == 1:
                            reference_dict = remove_all_overlaps_s2all(r, c, s1, s2, d)
                        else:
                            reference_dict = remove_overlapping_paths_s2all(r, c, s1, s2, d)
                        
                        if len(hops_pairs_dict) != 0:
                            number_of_pairs_perhop = number_of_path_pairs(hops_pairs_dict)
                            hops_list = list(number_of_pairs_perhop.keys())    
                            
                                
                            for index1 in range(0, len(hops_pairs_dict)):
                                key = hops_list[index1]
                                
                                value = hops_pairs_dict[key]
                                ref_value = reference_dict[key]
                                
                                for index2 in range(0, len(value)): 
                                    pair = value[index2]
                                    ref_pair = ref_value[index2]

                                    file_name = 'stimuli.noc.' + str(s1) + '.' + str(s2) + '.' + str(d)+ '.' + 'hop' + str(key) + 'pair' + str(index2+1) + file_extension
                                    filename = os.path.join(file_dir, file_name)
                                    with open(filename, "w") as f1:
                                        
                                        for path_index in range(0, 2):
                                            path_frompair_temp = pair[path_index]
                                            path_frompair = path_frompair_temp + '00'
                                            ref_path_frompair = ref_pair[path_index]
                                            new_path = []
                                            
                                            if path_index == 0:
                                                f1.write('* Data transfer from: R' + str(s1) + ' to R' + str(d) + ' --> Circuit Switched Path: \n')
                                            else:
                                                f1.write('* Data transfer from: R' + str(s2) + ' to R' + str(d) + ' --> Circuit Switched Path: \n')
                                            
                                            for bit_index in range(0, len(path_frompair), 2):
                                                
                                                
                                                # source - define MSB, input port
                                                if bit_index==0:
                                                    MSB = '1' 
                                                    supply = 'vh'
                                                    inportbits = '00'
                                                    in_dir_string = 'local'
                                                    
                                                    outportbits = str(path_frompair[bit_index])+str(path_frompair[bit_index+1])
                                                    if outportbits == str(north_var):
                                                        out_dir_string = 'north' 
                                                    elif outportbits == str(south_var):
                                                        out_dir_string = 'south'
                                                    elif outportbits == str(west_var):
                                                        out_dir_string = 'west'    
                                                    else:
                                                        out_dir_string = 'east'
                                                    out_dir_string_sel = str(out_dir_string[0])
                                                
                                                # if any node other than the source - set MSB, input port
                                                else:
                                                    MSB = '0'
                                                    supply = '0'
                                                    
                                                    prevportbits = str(path_frompair[bit_index-2])+str(path_frompair[bit_index-1])
                                                    if prevportbits=='00':
                                                    	inportbits = '11'
                                                    elif prevportbits=='11':
                                                        inportbits = '00'
                                                    elif prevportbits=='01':
                                                        inportbits = '10'
                                                    else:
                                                        inportbits = '01'

                                                    if inportbits == str(north_var):
                                                        in_dir_string = 'north'
                                                    elif inportbits == str(south_var):
                                                        in_dir_string = 'south'
                                                    elif inportbits == str(west_var):
                                                        in_dir_string = 'west'    
                                                    else:
                                                        in_dir_string = 'east'
                                                    
                                                    # destination - set output port
                                                    outportbits = '00'
                                                    if bit_index==len(path_frompair)-2:
                                                        if path_index==0:
                                                            out_dir_string = 'local0'     
                                                        else:
                                                            out_dir_string = 'local1'
                                                        out_dir_string_sel = str(out_dir_string[0])+str(out_dir_string[-1])
                                                    # any other node
                                                    else:
                                                        outportbits = str(path_frompair[bit_index])+str(path_frompair[bit_index+1])
                                                        if outportbits == str(north_var):
                                                            out_dir_string = 'north' 
                                                        elif outportbits == str(south_var):
                                                            out_dir_string = 'south'
                                                        elif outportbits == str(west_var):
                                                            out_dir_string = 'west'    
                                                        else:
                                                            out_dir_string = 'east' 
                                                        out_dir_string_sel = str(out_dir_string[0])
                                                    
                                                
                                                f1.write('* R'+str(ref_path_frompair[int(bit_index/2)])+': out'+out_dir_string+' mux select line s2s1s0 = '+MSB+str(inportbits)+' (selecting in'+in_dir_string+' port): \n') 
                                                    
                                                for q in range (2, -1, -1):
                                                    f1.write('vr'+str(ref_path_frompair[int(bit_index/2)])+'_s'+str(q)+out_dir_string_sel)
                                                    f1.write(' r'+str(ref_path_frompair[int(bit_index/2)])+'_s'+str(q)+out_dir_string_sel)
                                                    if q==2:
                                                        f1.write(' 0 ' + supply + ' \n')
                                                    else:
                                                        if q==1:
                                                            q_new = 0
                                                        else:
                                                            q_new = 1
                                                        if inportbits[q_new] == '0':
                                                            f1.write(' 0 ' + '0' + ' \n')
                                                        else:
                                                            f1.write(' 0 ' + 'vh' + ' \n')
                                                
                                             
                                                if bit_index==len(path_frompair)-2:
                                                    if path_index==0:
                                                        f1.write('\n*** Input starting at R' + str(ref_path_frompair[0]) + ': \n')
                                                        f1.write('vr' + str(ref_path_frompair[0]) + '_inlocal')
                                                        f1.write(' r' + str(ref_path_frompair[0]) + '_inlocal')
                                                        f1.write(" 0 pulse(vh 0 0 slope slope th '2*th') \n")
                                                        f1.write('*** To observe: out'+out_dir_string+' port \n\n')
                                                    else:
                                                        f1.write('\n*** Input starting at R' + str(ref_path_frompair[0]) + ': \n')
                                                        f1.write('vr' + str(ref_path_frompair[0]) + '_inlocal')
                                                        f1.write(' r' + str(ref_path_frompair[0]) + '_inlocal')
                                                        f1.write(" 0 pulse(vh 0 clockDelay slope slope th '2*th') \n")
                                                        f1.write('*** To observe: out'+out_dir_string+' port \n\n')
 
