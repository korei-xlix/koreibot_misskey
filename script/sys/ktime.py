#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Misskey
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_misskey/
# ::Class    : 時間取得(共通)
#####################################################

from osif import CLS_OSIF
from gval import gVal
#####################################################
class CLS_TIME():
#####################################################

#####################################################
# 時間取得
#####################################################
	@classmethod
	def sGetPCTime( cls, inRes ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TIME"
		wRes['Func']  = "sGet"
		
		wRes.update({ "TimeDate" : None })
		#############################
		# 時間を取得
		wTD = CLS_OSIF.sGetTime()
		if wTD['Result']!=True :
			###時間取得失敗  時計壊れた？
			wRes['Reason'] = "Function is failed: CLS_OSIF.sGetTime: " + CLS_OSIF.sCatErr( inRes )
			
			### ダミー時間
			wRes['TimeDate'] = gVal.DEF_TIMEDATE
			return wRes
		else:
			### 正常取得
			wRes['TimeDate'] = wTD['TimeDate']
		
		### wTD['TimeDate']
		
		#############################
		# 正常
		wRes['Result'] = True	#正常
		return wRes



#####################################################
# グローバル時間更新
#####################################################
	@classmethod
	def sTimeUpdate( cls, inRes ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TIME"
		wRes['Func']  = "TimeUpdate"
		
		#############################
		# 時間を取得
		wTD = cls.sGetPCTime( inRes )
		if wTD['Result']!=True :
			wRes['Reason'] = "Function is failed: sGetPCTime: " + CLS_OSIF.sCatErr( inRes )
			return wRes
		
		gVal.STR_Time['TimeDate'] = wTD['TimeDate']
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# グローバル時間取得
#####################################################
	@classmethod
	def sGet(cls):
		return gVal.STR_Time['TimeDate']



