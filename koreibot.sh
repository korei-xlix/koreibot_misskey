#! /bin/sh
#####################################################
# ::Project  : koreibot
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : 
#####################################################

#############################
# Load Function
###source galaxyfleet/server_ctrl/server_ctrl_function.sh



#####################################################
# main
#####################################################
if [ $1 == "start" ]; then
	#############################
	# Console
	cd
	cd koreibot/koreibot_win/
	python3 run.py run localhost koreibot koreibot GpIXgvUnzoxbgw07 korei_xlix

elif [ $1 == "init" ]; then
	#############################
	# Init
	cd
	cd koreibot/koreibot_win/
	python3 run.py init localhost koreibot koreibot GpIXgvUnzoxbgw07 ../koreibot_data

elif [ $1 == "add" ]; then
	#############################
	# Init
	cd
	cd koreibot/koreibot_win/
	python3 run.py add localhost koreibot koreibot GpIXgvUnzoxbgw07 korei_xlix ../koreibot_data

elif [ $1 == "ping" ]; then
	#############################
	# Ping
	cd
	cd koreibot/koreibot_win/
	python3 run.py ping none

fi

exit 0

