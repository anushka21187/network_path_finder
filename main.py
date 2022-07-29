import network_matrix
import available_ports
import obtain_paths

# 2x3 matrix
number_of_rows = 3
number_of_columns = 3

source = 0
destination = 2

mesh = network_matrix(number_of_rows, number_of_columns)
port_map_mesh = available_ports('mesh', mesh)
#port_map_torus = available_ports('torus', mesh)

source_directions = port_map_mesh[source]

dictionary_of_paths = obtain_paths(port_map_mesh, number_of_rows, number_of_columns, source, destination, [], source_directions, {})
