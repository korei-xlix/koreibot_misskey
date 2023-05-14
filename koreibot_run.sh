#! /bin/sh
#####################################################
# ::Project  : Korei Bot Misskey
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_misskey/
# ::Class    : バッチ実行 処理
#####################################################

#############################
# pass change
cd
cd $SCRIPT_PATH



#####################################################
# main
#####################################################

if [[ $1 == "dbstart" ]]; then
	#############################
	# dbstart
	mysqld_safe --datadir='/var/lib/mysql' &

elif [[ $1 == "start" ]]; then
	#############################
	# Console
	$PROGRAM run $MISSKEY_ID $DB_LOGIN

elif [[ $1 == "init" ]]; then
	#############################
	# init
	$PROGRAM init $DB_LOGIN

elif [[ $1 == "regist" ]]; then
	#############################
	# regist
	$PROGRAM regist $DB_LOGIN

elif [[ $1 == "add" ]]; then
	#############################
	# Init
	python3 run.py add localhost koreibot koreibot GpIXgvUnzoxbgw07 korei_xlix ../koreibot_data

elif [[ $1 == "ping" ]]; then
	#############################
	# Ping
	python3 run.py ping none

fi

