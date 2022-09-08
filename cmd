#!/bin/csh -f
#echo $0 $1 $2 $3 

# 1. square mesh dimensions; 2 or more
if ($1 < 2) then
	echo "Error_1: Mesh dimension must be greater than or equal to 2."
	echo "Usage: "
	echo "./script <square_mesh_dimension>=2>"
	exit()
endif

# 2. number of sources; 1 (default) or 2
if (($2 != 1) && ($2 != 2) && ($2 != 0)) then
	echo "Error_2: Number of sources must be either 1 or 2."
	echo "Usage: "
	echo "./script <square_mesh_dimension> <number_of_sources=1or2>"
	exit()
else if ($2 == 1) then
	set num_sources = $2
	set s_string = ""
else if ($2 == 2) then
	set num_sources = $2
	set s_string = "_2S"
else if ($2 == 0) then 
	set num_sources = $2
	set s_string = "_2S-all"
else
	set num_sources = 1
	set s_string = "" 
endif

# 3. mode; 0 (default) --> nodes common but not bidirectional, 1 --> no common node, 2 --> nodes can be common
if (($3 < 0) || ($3 > 2)) then
	echo "Error_3: valid modes are 0 (partial overlap: route pairs with bidirectional common nodes removed), 1 (no overlap: route pairs with any common node removed), 2 (no common node removed)."
	echo "Usage: "
	echo "./script <square_mesh_dimension> <number_of_sources> <mode=0or1or2>"
	exit()
else if ($3 == 0) then
	set mode = $3
	set m_string = ""
else if ($3 == 1) then
	set mode = $3
	set m_string = "_nooverlap"
else if ($3 == 2) then
	set mode = $3
	set m_string = "_withoverlap" 
else
	set mode = 0
	set m_string = ""
endif

# 4. report format; 0 (default) --> bitstring, 1 --> directions, 2 --> router/node IDs
if (($4 < 0) || ($4 > 2)) then
	echo "Error_4: valid report formats are 0 (bits), 1 (directions), 2 (router/node IDs)."
	echo "Usage: "
	echo "./script <square_mesh_dimension> <number_of_sources> <mode> <report_format=0or1or2>"
	exit()
else if ($4 == 0) then
	set report_format = $4
	set rf_string = ""
else if ($4 == 1) then
	set report_format = $4
	set rf_string = "_directions"
else if ($4 == 2) then
	set report_format = $4
	set rf_string = "_routers"
else
	set report_format = 0
	set rf_string = ""
endif


set py_script = main.py
set temp_py_script = .temp.$py_script
cp $py_script $temp_py_script



# ----- SET DIRECTION BITS HERE -----
perl -p -i -e 's/northbits/00/gi;' $temp_py_script
perl -p -i -e 's/southbits/01/gi;' $temp_py_script
perl -p -i -e 's/westbits/10/gi;' $temp_py_script
perl -p -i -e 's/eastbits/11/gi;' $temp_py_script
# ----



perl -p -i -e 's/anushka_1/'$1'/gi;' $temp_py_script
perl -p -i -e 's/anushka_s/'$num_sources'/gi;' $temp_py_script
perl -p -i -e 's/anushka_m/'$mode'/gi;' $temp_py_script
perl -p -i -e 's/anushka_rf/'$report_format'/gi;' $temp_py_script

echo "Finding routes for $1x$1 Mesh..."
if (($2 == 2) || ($2==0)) then
	echo "Pairing routes from 2 different sources to one destination..."
else
	echo "Pairing different routes from $2 source to one destination..."
endif
if ($3 == 1) then
	echo "Removing all route pairs with common nodes..."
else if ($3 == 2) then
	echo "Keeping all possible route pairs regardless of whether the routes overlap or not..."
else
	echo "Removing all route pairs with common bidirectional nodes..."
endif
if ($4 == 1) then
	echo "Reporting paths as sequences of directions..."
else if ($4 == 2) then
	echo "Reporting paths as sequences of router/node IDs..."
else
	echo "Reporting paths as sequences of direction bits..."
endif
#echo "" 


python $temp_py_script 


set report = reports/NoC_$1x$1$s_string$m_string$rf_string.rpt
set summary = reports/summary_$1x$1$s_string$m_string$rf_string.rpt


set report_location = `readlink -f $report`
echo "All the Routes and Associated Source-Destinations are in : $report_location"

echo "For $1x$1 mesh, total number of path pairs: " > $summary 
grep -iP "pair_" $report | wc -l >> $summary 
echo "" >> $summary 
echo "All possible unique hops: " >> $summary 
grep -iP "(minimum|maximum) hops" $report | sort -u -gk4 >> $summary 
echo "" >> $summary 
echo "Maximum and minimum possible hops in $1x$1 mesh: " >> $summary
grep -iP "maximum hops" $report | sort -u -gk4 | tail -1 >> $summary  
grep -iP "minimum hops" $report | sort -u -gk4 | head -1 >> $summary 

set summary_location = `readlink -f $summary`
echo "Summary of results is in : $summary_location"
