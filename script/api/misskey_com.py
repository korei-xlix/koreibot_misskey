#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Misskey
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_misskey/
# ::Class    : misskey com
#####################################################

#####################################################
class CLS_Misskey_Com() :
#####################################################

										### misskeyストリームURL
	DEF_MISSKEY_STREAM_URL = "wss://misskey.io/streaming?i="



#####################################################
	OBJ_Misskey = ""		#misskeyオブジェクト(トークン)

	STR_Status = {				# misskey状態
		"FLG_Con"	: False,	# 接続  True=接続確認済

		"FLG_Rec"	: False,	# 受信処理  True=受信中
		"FLG_RecEnd": True,		# 受信停止  True=停止ON
	}



