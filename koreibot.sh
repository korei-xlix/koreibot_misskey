#! /bin/sh
#####################################################
# ::Project  : Korei Bot Misskey
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_misskey/
# ::Class    : バッチ実行
#####################################################

#############################
# User Config

PROGRAM='python3 run.py'
SCRIPT_PATH='koreibot/koreibot_misskey/script/'

MISSKEY_ID=''

DB_HOST='localhost'
DB_NAME=''
DB_USER=''
DB_PASS=''



#############################
###COMMAND=$MISSKEY_ID' '$DB_LOGIN
DB_LOGIN=$DB_HOST' '$DB_NAME' '$DB_USER' '$DB_PASS



#############################
# Load Function
source koreibot/koreibot_misskey/koreibot_run.sh

exit 0

