import network_matrix
import available_ports

mesh = network_matrix(4, 4)
port_map_mesh = available_ports('mesh', mesh)
port_map_torus = available_ports('torus', mesh)
