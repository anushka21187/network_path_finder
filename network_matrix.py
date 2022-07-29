"""
Create a router network 
Input: number of rows, number of columns
Output: 2D matrix of node IDs 
Relevant topologies: mesh, torus
"""

def network_matrix(number_of_rows, number_of_columns): 
    #matrix = [[0]*number_of_columns]*number_of_rows
    matrix = []
    
    node_id = 0
    for row_index in range (0, number_of_rows):
        matrix_row = []
        for col_index in range (0, number_of_columns):
            matrix_row.append(node_id)
            node_id = node_id + 1
        matrix.append(tuple(matrix_row))
    return tuple(matrix)
