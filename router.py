"""
Create a router network
"""

def network_matrix(number_of_rows, number_of_columns):
    #rows, cols = (number_of_rows, number_of_columns)
    #matrix = [[0]*number_of_columns]*number_of_rows
    #return matrix 
    
    matrix = []
    
    router_id = 0
    for row_index in range (0, number_of_rows):
        matrix_row = []
        for col_index in range (0, number_of_columns):
            matrix_row.append(router_id)
            router_id = router_id + 1
        matrix.append(matrix_row)
        #router_id = router_id + 1
    return matrix
