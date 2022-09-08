# ---------- 6 ---------- #
""" MAIN SCRIPT """
import os

from helpers import *
from common import *
from routepairs import *
from reportformat import *
from generate import *

source = 0

north = 'northbits'
south = 'southbits'
west = 'westbits'
east = 'eastbits'

mesh_size_var = anushka_1
num_sources_var = anushka_s
mode_var = anushka_m
report_format_var = anushka_rf


if 'reports' not in os.listdir():
    os.mkdir('reports')


if num_sources_var == 2:
    generate_routepairs_s2(anushka_1, anushka_1, mode_var, report_format_var, north, south, west, east)
elif num_sources_var == 1:
    generate_routepairs(anushka_1, anushka_1, mode_var, report_format_var, north, south, west, east)
else:
    generate_routepairs_s2all(anushka_1, anushka_1, mode_var, report_format_var, north, south, west, east)

    
