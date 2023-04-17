#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : 時間取得(共通)
#####################################################

from osif import CLS_OSIF
from gval import gVal
#####################################################
class CLS_TIME():
#####################################################

#####################################################
# グローバル時間更新
#####################################################
	@classmethod
	def sTimeUpdate(cls):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TIME"
		wRes['Func']  = "TimeUpdate"
		
		#############################
		# 時間を取得
		wTD = cls.sGet( wRes, "(1)" )
		if wTD['Result']!=True :
			return wRes
		
		gVal.STR_Time['TimeDate'] = wTD['TimeDate']
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# 時間取得
#####################################################
	@classmethod
	def sGet( cls, inCallInfo, inReason ):
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
			wCall = inCallInfo
			wCall['Reason'] = inReason
			wRes['Reason'] = "PC time get is failer: " + CLS_OSIF.sCatErr( wCall )
			gVal.OBJ_L.Log( "C", wRes )
			
			### ダミー時間
			wRes['TimeDate'] = gVal.DEF_TIMEDATE
		else:
			### 正常取得
			wRes['TimeDate'] = wTD['TimeDate']
		
		### wTD['TimeDate']
		
		#############################
		# 正常
		wRes['Result'] = True	#正常
		return wRes



#####################################################
# 時間変換
#####################################################
	@classmethod
	def sTTchg( cls, inCallInfo, inReason, inTimeDate ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TIME"
		wRes['Func']  = "sTTchg"
		
		wRes.update({ "TimeDate" : None })
		#############################
		# TTwitter時間を変換
		wTime = CLS_OSIF.sGetTimeformat_Twitter( inTimeDate )
		if wTime['Result']!=True :
			wCall = inCallInfo
			wCall['Reason'] = inReason
			wRes['Reason'] = "Twitter time change is failer: " + CLS_OSIF.sCatErr( wCall ) + " timedate=" + str(inTimeDate)
			gVal.OBJ_L.Log( "C", wRes )
			
			### ダミー時間
			wRes['TimeDate'] = gVal.DEF_TIMEDATE
		else:
			### 正常取得
			wRes['TimeDate'] = wTime['TimeDate']
		
		###wTime['TimeDate']
		
		#############################
		# 正常
		wRes['Result'] = True	#正常
		return wRes



