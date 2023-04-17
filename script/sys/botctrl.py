#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : bot制御(共通)
#####################################################
from mylog import CLS_Mylog
from db_if import CLS_DB_IF
from twitter_if import CLS_Twitter_IF

from traffic import CLS_Traffic
from ktime import CLS_TIME
from osif import CLS_OSIF
from filectrl import CLS_File
from gval import gVal
#####################################################
class CLS_BotCtrl():
#####################################################

#####################################################
# Botテスト
#####################################################
	@classmethod
	def sBotTest(cls):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_BotCtrl"
		wRes['Func']  = "sBotTest"
		
		wRes['Responce'] = {
			"hostname"		: None,
			"database"		: None,
			"username"		: None,
			"password"		: None
		}
		#############################
		# 引数取得
		wArg = CLS_OSIF.sGetArg()
		
###		if len(wArg)<6 :	#引数が足りない
		if wArg[1]!="ping" and len(wArg)<6 :	#引数が足りない
			wRes['Reason'] = "CLS_BotCtrl: sBotTest: 引数が足りません(1)= " + str( wArg )
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# モード、DB情報の取得
###		wRes['Responce']['hostname'] = wArg[2]
###		wRes['Responce']['database'] = wArg[3]
###		wRes['Responce']['username'] = wArg[4]
###		wRes['Responce']['password'] = wArg[5]
		if wArg[1]!="ping" :
			wRes['Responce']['hostname'] = wArg[2]
			wRes['Responce']['database'] = wArg[3]
			wRes['Responce']['username'] = wArg[4]
			wRes['Responce']['password'] = wArg[5]
		
		#############################
		# add  : データ追加モード
		# word : 文字追加モード
		if wArg[1]=="add" or  \
		   wArg[1]=="word" :
			if len(wArg)!=8 :
				wRes['Reason'] = "CLS_BotCtrl: sBotTest: 引数が足りません(2)= " + str( wArg )
				CLS_OSIF.sErr( wRes )
				return wRes
			
			gVal.STR_SystemInfo['RunMode']      = wArg[1]
			gVal.STR_SystemInfo['EXT_FilePath'] = wArg[7]
			gVal.STR_UserInfo['Account']        = wArg[6]
			wRes['Result'] = True	#正常
			return wRes
		
		#############################
		# setup : セットアップモード
		elif wArg[1]=="setup" :
			if len(wArg)!=6 and len(wArg)!=7 :
				wRes['Reason'] = "CLS_BotCtrl: sBotTest: 引数が足りません(3)= " + str( wArg )
				CLS_OSIF.sErr( wRes )
				return wRes
			
			gVal.STR_SystemInfo['RunMode'] = wArg[1]
			
			if len(wArg)==7 :
				gVal.STR_SystemInfo['EXT_FilePath'] = wArg[6]
			
			wRes['Result'] = True	#正常
			return wRes
		
		#############################
		# init  : 初期化モード
		elif wArg[1]=="init" :
			if len(wArg)!=6 and len(wArg)!=7 :
				wRes['Reason'] = "CLS_BotCtrl: sBotTest: 引数が足りません(4)= " + str( wArg )
				CLS_OSIF.sErr( wRes )
				return wRes
			
			gVal.STR_SystemInfo['RunMode'] = wArg[1]
			
			if len(wArg)==7 :
				gVal.STR_SystemInfo['EXT_FilePath'] = wArg[6]
			
			wRes['Result'] = True	#正常
			return wRes
		
		#############################
		# testclear  : テストクリア
		elif wArg[1]=="testclear" :
			if len(wArg)!=6 :
				wRes['Reason'] = "CLS_BotCtrl: sBotTest: 引数が足りません(5)= " + str( wArg )
				CLS_OSIF.sErr( wRes )
				return wRes
			
			gVal.STR_SystemInfo['RunMode'] = wArg[1]
			
			wRes['Result'] = True	#正常
			return wRes
		
		#############################
		# ping  : Ping
		elif wArg[1]=="ping" :
			if len(wArg)!=3 and len(wArg)!=4 :
				wRes['Reason'] = "CLS_BotCtrl: sBotTest: 引数が足りません(6)= " + str( wArg )
				CLS_OSIF.sErr( wRes )
				return wRes
			
			gVal.STR_SystemInfo['RunMode'] = wArg[1]
			wRes['Responce']['hostname']   = wArg[2]
			
			wRes['Result'] = True	#正常
			return wRes
		
		#############################
		# test : テストモード
		elif wArg[1]==gVal.DEF_TEST_MODE :
			if len(wArg)!=7 :
				wRes['Reason'] = "CLS_BotCtrl: sBotTest: 引数が足りません(7)= " + str( wArg )
				CLS_OSIF.sErr( wRes )
				return wRes
			
			gVal.FLG_Test_Mode = True
		
		#############################
		# run : 通常モード
		elif wArg[1]=="run" :
			if len(wArg)!=7 :
				wRes['Reason'] = "CLS_BotCtrl: sBotTest: 引数が足りません(8)= " + str( wArg )
				CLS_OSIF.sErr( wRes )
				return wRes
			
			gVal.FLG_Test_Mode = False
		
		else:
			wRes['Reason'] = "CLS_BotCtrl: sBotTest: コマンドがありません= " + str( wArg )
			CLS_OSIF.sErr( wRes )
			return wRes
		
		gVal.STR_SystemInfo['RunMode'] = "Normal"
		gVal.STR_UserInfo['Account']   = wArg[6]
		
		#############################
		# DBに接続
		gVal.OBJ_DB_IF = CLS_DB_IF()
		wSubRes = gVal.OBJ_DB_IF.Connect( wRes['Responce'] )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "CLS_BotCtrl: sBotTest: DB接続失敗: reason=" + wResDB['Reason']
			CLS_OSIF.sErr( wRes )
			return wRes
		if wSubRes['Responce']!=True :
			##テーブルがない= 初期化してない
			wRes['Reason'] = "CLS_BotCtrl: sBotTest: DB未構築"
			CLS_OSIF.sErr( wRes )
			gVal.OBJ_DB_IF.Close()
			return wRes
		
		#############################
		# ログオブジェクトの生成
		gVal.OBJ_L = CLS_Mylog()
		
		#############################
		# Twitterデータ取得
		wTwitterDataRes = gVal.OBJ_DB_IF.GetTwitterData( gVal.STR_UserInfo['Account'] )
		if wTwitterDataRes['Result']!=True :
			wRes['Reason'] = "GetTwitterData is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 排他開始
		wLock = cls.sLock()
		if wLock['Result']!=True :
			wRes['Reason'] = "排他取得失敗: " + wLock['Reason']
			gVal.OBJ_L.Log( "A", wRes )
			gVal.OBJ_DB_IF.Close()
			return wRes
		elif wLock['Responce']!=None :
			gVal.OBJ_L.Log( "S", wRes, "排他中" )
			
			CLS_OSIF.sPrn( "処理待機中です。CTRL+Cで中止することもできます。" )
			CLS_OSIF.sPrn( wLock['Reason'] + '\n' )
			
			wResStop = CLS_OSIF.sPrnWAIT( wLock['Responce'] )
			if wResStop==False :
				###ウェイト中止
				CLS_OSIF.sPrn( '\n' + "待機を中止しました。プログラムを停止しました。" )
				gVal.OBJ_DB_IF.Close()
				return wRes
		
		#############################
		# Twitterに接続
		gVal.OBJ_Tw_IF = CLS_Twitter_IF()
		wTwitterRes = gVal.OBJ_Tw_IF.Connect( wTwitterDataRes['Responce'] )
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitterの接続失敗: reason=" + wResTwitter['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			cls.sBotEnd()	#bot終了
			return wRes
		
		#############################
		# 時間を取得
		wTD = CLS_TIME.sGet( wRes, "(1)" )
		if wTD['Result']!=True :
			cls.sBotEnd()	#bot終了
			return wRes
		### wTD['TimeDate']
		#############################
		# コマンド実行時間を設定
		wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "run", wTD['TimeDate'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "SetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# Version情報
		wReadme = []
		if CLS_File.sReadFile( gVal.DEF_STR_FILE['Readme'], outLine=wReadme )!=True :
			wRes['Reason'] = "Readme.mdファイルが見つかりません: path=" + gVal.DEF_STR_FILE['Readme']
			gVal.OBJ_L.Log( "D", wRes )
			cls.sBotEnd()	#bot終了
			return wRes
		
		if len(wReadme)<=1 :
			wRes['Reason'] = "Readme.mdファイルが空です: path=" + gVal.DEF_STR_FILE['Readme']
			gVal.OBJ_L.Log( "D", wRes )
			cls.sBotEnd()	#bot終了
			return wRes
		
		for wLine in wReadme :
			#############################
			# 分解+要素数の確認
			wLine = wLine.strip()
			wGetLine = wLine.split("= ")
			if len(wGetLine) != 2 :
				continue
			
			wGetLine[0] = wGetLine[0].replace("::", "")
			#############################
			# キーがあるか確認
			if wGetLine[0] not in gVal.STR_SystemInfo :
				continue
			
			#############################
			# キーを設定
			gVal.STR_SystemInfo[wGetLine[0]] = wGetLine[1]
		
		#############################
		# 時間情報の取得
		wListRes = gVal.OBJ_DB_IF.GetTimeInfo( gVal.STR_UserInfo['Account'] )
		if wListRes['Result']!=True :
			wRes['Reason'] = "GetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# トレンドタグ、リスト通知の取得
		wListRes = gVal.OBJ_DB_IF.GetListName( gVal.STR_UserInfo['Account'] )
		if wListRes['Result']!=True :
			wRes['Reason'] = "GetListName is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# システム情報の取得
		wCLS_work = CLS_OSIF()
		gVal.STR_SystemInfo['PythonVer'] = wCLS_work.Get_PythonVer()
		gVal.STR_SystemInfo['HostName']  = wCLS_work.Get_HostName()
		
		#############################
		# ログに記録する
		if gVal.FLG_Test_Mode==False :
			gVal.OBJ_L.Log( "S", wRes, "bot実行" )
		else:
			# テストモード
			gVal.OBJ_L.Log( "S", wRes, "bot実行(テストモード)" )
		
		#############################
		# テスト終了
		wRes['Result'] = True	#正常
		return wRes



#####################################################
# Bot終了
#####################################################
	@classmethod
	def sBotEnd(cls):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_BotCtrl"
		wRes['Func']  = "sBotEnd"
		
		#############################
		# 排他解除
		wRes = cls.sUnlock()
		if wRes['Result']!=True :
			wRes['Reason'] = "排他取得失敗: " + wRes['Reason']
			gVal.OBJ_L.Log( "C", wRes )
		
		#############################
		# 時間を取得
		wSubRes = CLS_TIME.sTimeUpdate()
		if wSubRes['Result']!=True :
			###時間取得失敗  時計壊れた？
			wRes['Reason'] = "TimeUpdate is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# トラヒック情報の記録と報告
		wResTraffic = CLS_Traffic.sSet()
		if wResTraffic['Result']!=True :
			wRes['Reason'] = "Set Traffic failed: reason=" + CLS_OSIF.sCatErr( wResTraffic )
			return wRes
		
		#############################
		# DB終了
		gVal.OBJ_DB_IF.Close()
		return True



#####################################################
# 排他制御
#####################################################
	@classmethod
	def sLock(cls):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_BotCtrl"
		wRes['Func']  = "sLock"
		
		#############################
		# ロックの取得
		wLockRes = gVal.OBJ_DB_IF.GetLock( gVal.STR_UserInfo['Account'] )
		if wLockRes['Result']!=True :
			wRes['Reason'] = "GetLock is failed"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		if wLockRes['Responce']['locked']==True :
			### 排他済み
			
			# ロック保持時間外かを求める (変換＆差)
			wGetLag = CLS_OSIF.sTimeLag( str(wLockRes['Responce']['get_date']), inThreshold=gVal.DEF_STR_TLNUM['forLockLimSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed"
				return wRes
			if wGetLag['Beyond']==True :
				#反応時間外
				cls.sUnlock()	#一度解除する
				
				#ログに記録する
				gVal.OBJ_L.Log( "S", wRes, "排他解除" )
				wRes['Reason'] = None
			
			else :
				wAtSec = gVal.DEF_STR_TLNUM['forLockLimSec'] - wGetLag['RateSec']
				wAtSec = CLS_OSIF.sGetFloor( wAtSec )	#小数点切り捨て
				wRes['Reason'] = "処理終了まであと " + str(wAtSec) + " 秒です"
				wRes['Responce'] = wAtSec
				wRes['Result']   = True
				return wRes
		
		#※排他がかかってない
		#############################
		# 時間を取得
		wTD = CLS_TIME.sGet( wRes, "(2)" )
		if wTD['Result']!=True :
			return wRes
		
		#############################
		# 排他する
		wLockRes = gVal.OBJ_DB_IF.SetLock( gVal.STR_UserInfo['Account'], True, wTD['TimeDate'] )
		if wLockRes['Result']!=True :
			wRes['Reason'] = "GetLock is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wRes['Result']   = True
		return wRes	#排他あり



#####################################################
# 排他延長
#####################################################
	@classmethod
	def sExtLock(cls):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_BotCtrl"
		wRes['Func']  = "sExtLock"
		
		#############################
		# ロックの取得
		wLockRes = gVal.OBJ_DB_IF.GetLock( gVal.STR_UserInfo['Account'] )
		if wLockRes['Result']!=True :
			wRes['Reason'] = "GetLock is failed"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# ロックの取得
		if wRes['Responce']['locked']==True :
			### 排他がかかってない
			wRes['Reason'] = "Do not lock"
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# 排他の延長 = 今の操作時間に更新する
		
		# 時間を取得
		wTD = CLS_TIME.sGet( wRes, "(3)" )
		if wTD['Result']!=True :
			return wRes
		
		#############################
		# 排他する
		wLockRes = gVal.OBJ_DB_IF.SetLock( gVal.STR_UserInfo['Account'], True, wTD['TimeDate'] )
		if wLockRes['Result']!=True :
			wRes['Reason'] = "GetLock is failed"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		wRes['Result']   = True
		return wRes



#####################################################
# 排他情報の取得
#####################################################
	@classmethod
	def sGetLock(cls):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_BotCtrl"
		wRes['Func']  = "sGetLock"
		
		wRes['Responce'] = {
			"Locked"    : False,
			"Beyond"    : False
		}
		
		#############################
		# ロックの取得
		wLockRes = gVal.OBJ_DB_IF.GetLock( gVal.STR_UserInfo['Account'] )
		if wLockRes['Result']!=True :
			wRes['Reason'] = "GetLock is failed"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# ロックの取得
		if wRes['Responce']['locked']==True :
			### 排他がかかってる
			
			# ロック保持時間外かを求める (変換＆差)
			wGetLag = CLS_OSIF.sTimeLag( str(wLockRes['Responce']['get_date']), inThreshold=gVal.DEF_STR_TLNUM['forLockLimSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==True :
				###解除可能
				wRes['Reason'] = "解除可能です"
			
			else :
				wAtSec = gVal.DEF_STR_TLNUM['forLockLimSec'] - wGetLag['RateSec']
				wAtSec = CLS_OSIF.sGetFloor( wAtSec )	#小数点切り捨て
				wRes['Reason'] = "処理終了まであと " + str(wAtSec) + " 秒です"
			
			#############################
			# ロック=ON, 排他解除 可or否
			wRes['Responce']['Beyond'] = wGetLag['Beyond']
		
		###else:
			#############################
			# ロック=OFF
		
		#############################
		# ロック状態 ON or OFF, 正常終了
		wRes['Responce']['Locked'] = wLocked
		wRes['Result'] = True
		return wRes



#####################################################
# 排他解除
#####################################################
	@classmethod
	def sUnlock(cls):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_BotCtrl"
		wRes['Func']  = "sUnlock"
		
		#############################
		# 排他解除
		wLockRes = gVal.OBJ_DB_IF.SetLock( gVal.STR_UserInfo['Account'], False, gVal.STR_Time['TimeDate'] )
		if wLockRes['Result']!=True :
			wRes['Reason'] = "GetLock is failed"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		wRes['Result']   = True
		return wRes	#排他なし



