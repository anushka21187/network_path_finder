#!/bin/csh -f
#echo $1 $2 $3 $4 

if ($1 == "") then
	echo "### ERROR_0: No input arguments given. Four input arguments are necessary for correct functioning of this tool (script)."
	echo "## Usage description:"
	echo "$0 <square_mesh_dimension>=2> <num_sources=1or2> <mode=0or1or2> <report_format=0or1or2or3or4>"
	echo "## Argument(s) description:"
	echo "#1. *square_mesh_dimension*: number of rows/columns in the mesh; minimum = 2"
	echo "#2. *num_sources*: "
	echo "		* 1 for route pairs between one source and a fixed destination"
	echo "		* 2 for the same between two different sources and a fixed destination"
	echo "#3. *mode*: "
	echo "		* 0 to remove all route pairs with common bidirectional nodes (moderately small subset)"
	echo "		* 1 to remove route pairs with any common node (smallest subset)"
	echo "		* 2 to include all possible route pairs (largest subset)"
	echo "#4. *report_format*: "
	echo "		* 0 for detailed report having direction bits"
	echo "		* 1 for detailed report having direction chars"
	echo "		* 2 for detailed report having node/router IDs (numbers)"
	echo "		* 3 for concise report with format: source1_source2_destination_hop# = (source1:encoding, destination:encoding), (source2:encoding, destination:encoding)"
	echo "		* 4 for generating all the spice files for all (s1,s2,d) triplets reported in option #3 (previous line)"
	sleep 2s
	echo "			#Opening the README.md for detailed help ..."
	sleep 1s
	echo "				#Be patient human, it is still opening ..."
	sleep 0.5s
	echo "					#If the above information was sufficient, you may press Ctrl+C on keyboard to prevent openeing the README-HELP window."
	sleep 0.5s
	echo "						#Now, definitely it will open. Bear the consequences."
	sleep 1s
	gvim README.md
endif

# 1. square mesh dimensions; 2 or more
if ($1 < 2) then
	echo "### ERROR_1: Mesh dimension must be greater than or equal to 2."
	#echo "Usage: "
	#echo "./script <square_mesh_dimension>=2>"
	exit()
endif

# 2. number of sources; 1 (default) or 2
if (($2 != 1) && ($2 != 2) && ($2 != 0)) then
	echo "### ERROR_2: Number of sources must be either 1 or 2:"
	echo "				* 1 for route pairs between one source and a fixed destination"
	echo "				* 2 for the same between two different sources and a fixed destination"
	#echo "Usage: "
	#echo "./script <square_mesh_dimension> <number_of_sources=1or2>"
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
	echo "### ERROR_3: valid modes are 0 (partial overlap: route pairs with bidirectional common nodes removed), 1 (no overlap: route pairs with any common node removed), 2 (no common node removed)."
	echo "				* 0 to remove all route pairs with common bidirectional nodes (moderately small subset)"
	echo "				* 1 to remove route pairs with any common node (smallest subset)"
	echo "				* 2 to include all possible route pairs (largest subset)"
	#echo "Usage: "
	#echo "./script <square_mesh_dimension> <number_of_sources> <mode=0or1or2>"
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

# 4. report format; 0 (default) --> bitstring, 3 --> CONCISE (bits), 1 --> directions, 2 --> router/node IDs
if (($4 < 0) || ($4 > 4)) then
	#echo "### ERROR_4: valid detailed report formats are 0 (bits), 1 (directions), 2 (router/node IDs); concise format is 3 (s1_s2_d_hop#:respective_encoding); SPICE file generation is 4."
	echo "### ERROR_4: valid arguments are: 0 or 1 or 2 or 3 or 4. Details:"
	echo "				* 0 for detailed report having direction bits"
	echo "				* 1 for detailed report having direction chars"
	echo "				* 2 for detailed report having node/router IDs (numbers)"
	echo "				* 3 for concise report with format: source1_source2_destination_hop# = (source1:encoding, destination:encoding), (source2:encoding, destination:encoding)"
	echo "				* 4 for generating all the spice files for all (s1,s2,d) triplets reported in option #3 (previous line)"
	#echo "Usage: "
	#echo "./script <square_mesh_dimension> <number_of_sources> <mode> <report_format=0or1or2>"
	exit()
else if ($4 == 3) then
	set report_format = $4
	set rf_string = "_concise"
else if ($4 == 4) then
	set report_format = $4
	set rf_string = "_stimuli"
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
perl -p -i -e 's/southbits/11/gi;' $temp_py_script
perl -p -i -e 's/westbits/10/gi;' $temp_py_script
perl -p -i -e 's/eastbits/01/gi;' $temp_py_script
# ----



perl -p -i -e 's/anushka_1/'$1'/gi;' $temp_py_script
perl -p -i -e 's/anushka_s/'$num_sources'/gi;' $temp_py_script
perl -p -i -e 's/anushka_m/'$mode'/gi;' $temp_py_script
perl -p -i -e 's/anushka_rf/'$report_format'/gi;' $temp_py_script

echo "Finding routes for $1x$1 Mesh..."
if ($2 == 2) then
	echo "Pairing routes from 2 different sources to one destination..."
else if ($2 == 0) then
	echo "Pairing routes from 2 sources (can be identical) to one destination..."
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
else if ($4 == 3) then
	echo "Making a concise report of paths as sequences of <current_nodeID>:<direction_to_take_inbits>..."
else if ($4 == 4) then
	echo "Generating spice files..."
else
	echo "Reporting paths as sequences of direction bits..."
endif
#echo "" 


python3 $temp_py_script 


if ($4 == 3) then
	set report = reports/NoC_$1x$1$s_string$m_string$rf_string.rpt
	set summary = reports/summary_$1x$1$s_string$m_string$rf_string.rpt
	set report_location = `readlink -f $report`
	echo "All the Routes and Associated Source-Destinations are in : $report_location"
	
	echo "For $1x$1 mesh, total number of path pairs: " > $summary 
	grep -iP " = " $report | wc -l >> $summary 
	echo "" >> $summary 
	
	set summary_location = `readlink -f $summary`
	echo "Summary of results is in : $summary_location"
else if ($4 == 4) then
	set spice_dir = stimuli_$1x$1_s$2_m$3
	set spice_location = `readlink -f $spice_dir`
	echo "Spice files are in : $spice_location"
else
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
endif

