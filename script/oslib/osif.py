#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : OS I/F (OS向け共通処理)
#####################################################
from datetime import datetime
from datetime import timedelta
import unicodedata
import time
import os
import socket
import sys
import re
import subprocess as sp
from getpass import getpass
import random
import math

#####################################################
class CLS_OSIF() :
#####################################################

	__DEF_LAG_TIMEZONE  = 9			#デフォルト時間差 タイムゾーン: 9=東京
	__DEF_LAG_THRESHOLD = 300		#デフォルト時間差 時間差(秒)
									# 300(s) = 60 * 5(min)
	
	__DEF_PING_COUNT = "2"			#Ping回数 (文字型)

	#############################
	# ping除外
	__DEF_ARR_NOTPING = [
		"friends.nico",
		"flower.afn.social",
		"(dummy)"
	]

#####################################################
# 共通レスポンス取得
#####################################################

##		#############################
##		# 応答形式の取得
##		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
##		wRes = CLS_OSIF.sGet_Resp()
##		wRes['Class'] = "Class"
##		wRes['Func']  = "Function"

	@classmethod
	def sGet_Resp(cls):
		wRes = {
			"Result"   : False,
			"Class"    : None,
			"Func"     : None,
			"Reason"   : None,
			"Responce" : None,
			"StatusCode" : None }
		
		return wRes



#####################################################
# 引数取得
#####################################################
	@classmethod
	def sGetArg(cls):
		wArg = sys.argv
		return wArg



#####################################################
# 時間を取得する
#####################################################
	@classmethod
	def sGetTime(cls):
		wRes = {
			"Result"	: False,
			"Object"	: "",
			"TimeDate"	: "",
			"Hour"		: 0,
			"Week"		: 0,
			"(dummy)"	: 0
		}
		
		try:
			wNow_TD = datetime.now()
			wRes['Object']   = wNow_TD
			wRes['TimeDate'] = wNow_TD.strftime("%Y-%m-%d %H:%M:%S")
			wRes['Hour']     = wNow_TD.strftime("%H")		#時間だけ
			wRes['Week']     = str( wNow_TD.weekday() )		#曜日 0=月,1=火,2=水,3=木,4=金,5=土,6=日
		except ValueError as err :
			return wRes
		
		wRes['Result'] = True
		return wRes



#####################################################
# 日時の文字列を時間型にして比較する
#####################################################
	@classmethod
	def sCmpTime( cls, inSrcTD, inDstTD=None, inTest=False ):
		wRes = {
			"Result"	: False,
			"Object"	: "",
			"Future"	: False		# True= SrcTDが未来時間
		}
		
		try:
			#############################
			# 文字列を日時型に変換する
			wSrcTD = datetime.strptime( inSrcTD, "%Y-%m-%d %H:%M:%S")
			wRes['Object'] = wSrcTD
			
			#############################
			# 比較先がなければ現在時刻を取得する
			if inDstTD==None :
				wNowTD = datetime.now()
			else:
				wNowTD = inDstTD
				if isinstance( inDstTD, datetime )==False :
					wNowTD = datetime.strptime( inDstTD, "%Y-%m-%d %H:%M:%S")
		
		except ValueError as err :
			return wRes
		
		#############################
		# SrcTDが未来時間
		if wSrcTD>wNowTD :
			wRes['Future'] = True
		if inTest==True :
			print( "inStcTD= " + str(inSrcTD) )
			print( "inDstTD= " + str(inDstTD) )
			print( "Future= " + str(wRes['Future']) )
		
		wRes['Result'] = True
		return wRes



#####################################################
# 計算しやすいように時間フォーマットを変更する
# (mastodon時間)
#####################################################
	@classmethod
	def sGetTimeformat( cls, inTimedate, inTimezone=__DEF_LAG_TIMEZONE ):
		wRes = {
			"Result"	: False,
			"TimeDate"	: ""
		}
		
		#############################
		# 入力時間の整形
		wTD = str( inTimedate )
			##形式合わせ +、.を省く（鯖によって違う？
		wIfind = wTD.find('+')
		wTD = wTD[0:wIfind]
		wIfind = wTD.find('.')
		if wIfind>=0 :
			wTD = wTD[0:wIfind]
		
		#############################
		# タイムゾーンで時間補正
		try:
			wRes['TimeDate'] = datetime.strptime( wTD, "%Y-%m-%d %H:%M:%S") + timedelta( hours=inTimezone )
		except:
			return wRes	#失敗
		
		wRes['Result'] = True
		return wRes



#####################################################
# 計算しやすいように時間フォーマットを変更する
# (twitter時間)
#####################################################
	@classmethod

	def sGetTimeformat_Twitter( cls, inTimedate, inTimezone=__DEF_LAG_TIMEZONE ):
		wRes = {
			"Result"	: False,
			"Format"	: "",
			"TimeDate"	: ""
		}
		
		wTD = inTimedate
		#############################
		# タイムゾーンで時間補正
		try:
			###整形
			wIfind = wTD.find('Z')
			if wIfind>=0 :
				### Trend形式
				wTD = str( wTD )
				wTD = wTD[0:wIfind]
				wTD = wTD.split('T')
				
				wIfind = wTD[1].find('.')
				if wIfind>=0 :
					wTD[1] = wTD[1][0:wIfind]
				wTD = wTD[0] + " " + wTD[1]
				
				wTD = datetime.strptime( wTD, "%Y-%m-%d %H:%M:%S") + timedelta( hours=inTimezone )
				wTD = str( wTD )
				
				wRes['Format'] = "TrendType"
			else :
				### Twitter形式
				wIfind = wTD.find('+')
				if wIfind<0 :
					###変換対象ではない
					wRes['Format'] = "TwitterType(Not Change)"
				
				else:
					wTD = datetime.strptime( wTD, "%a %b %d %H:%M:%S %z %Y" ) + timedelta( hours=inTimezone )
					wTD = str( wTD )
					wIfind = wTD.find('+')
					if wIfind>=0 :
						wTD = wTD[0:wIfind]
					
					wRes['Format'] = "TwitterType"
			
			wRes['TimeDate'] = wTD
		except:
			return wRes	#失敗
		
		wRes['Result'] = True
		return wRes



#####################################################
# 入力の日付から、次の指定の週末日付を取得する
#####################################################
	@classmethod
	def sGetNextWeekday( cls, inDate, inNowDate, inHour, inWeek ):
		### Week..曜日 0=月,1=火,2=水,3=木,4=金,5=土,6=日
		
		wRes = {
			"Result"	: False,
			"RateTD"	: "",
			"NextTD"	: "",
			"Weekday"	: False,
			"Weekend"	: False
		}
		wRes['RateTD'] = inDate
		wRes['NextTD'] = inNowDate
		
		wNextWeek = int( inWeek ) + 1
		
		#############################
		# 入力日付の曜日を求める
		wARR_TD = inDate.split(" ")
		wARR_NowTD = inNowDate.split(" ")
		### 同一日・同一時刻は計算しない
		if wARR_TD[0]==wARR_NowTD[0] :
			wARR_TD_Time = wARR_TD[1].split(":")
			wARR_NowTD_Time = wARR_NowTD[1].split(":")
			if wARR_TD_Time[0]==wARR_NowTD_Time[0] :
				wRes['Result'] = True
				return wRes
		
		wARR_TD = wARR_TD[0].split("-")
		wOBJ_TD = datetime( int(wARR_TD[0]), int(wARR_TD[1]), int(wARR_TD[2]) )
		wNowWeek = wOBJ_TD.weekday() + 1
		
		#############################
		# 日付の曜日から、次の入力曜日までの日付差を求める
		if wNowWeek<=wNextWeek :
			wSaDay = wNextWeek - wNowWeek
		else :
			wSaDay = 7 - (wNowWeek - wNextWeek )
		
		wOBJ_NextTD = wOBJ_TD + timedelta( days=wSaDay )
		wNextDate = str( wOBJ_NextTD ).split(" ")
		
		#############################
		# 入力日付が週末か、週末を超えてるかを求める
		wOBJ_NowTD = datetime.now()	#現時刻
		wSa = wOBJ_NextTD - wOBJ_NowTD
		wSa = wSa.days + 1
		if wSa==0 :
			###当日の時刻か、超えているか
			wNowHour = wOBJ_NowTD.strftime("%H")
			if int(wNowHour)>=inHour :
				wRes['Weekday'] = True
				wRes['Weekend'] = True
		elif wSa<0 :
			wRes['Weekend'] = True
		
		wRes['Result'] = True
		return wRes



#####################################################
# 2つの時間差の秒数を返す
#
#####################################################
	@classmethod
	def sTimeLagSec( cls, inTimedate1=None, inTimedate2=None ):
		#############################
		# 応答形式
		wRes = {
			"Result"	: False,	# 結果
			"Reason"	: None,
			
			"TD1"		: None,		#
			"TD2"		: None,		#
			"RateSec"	: 0			# 時間差(秒)
		}
		
		#############################
		# 時間形式に変換する
		try:
			wTD1 = str( inTimedate1 )
			wTD1 = datetime.strptime( wTD1, "%Y-%m-%d %H:%M:%S")
		except:
			wRes['Reason'] = "inTimedate1 exception error: " + str(inTimedate1)
			return wRes	#失敗
		wRes['TD1'] = wTD1
		
		try:
			wTD2 = str( inTimedate2 )
			wTD2 = datetime.strptime( wTD2, "%Y-%m-%d %H:%M:%S")
		except:
			wRes['Reason'] = "inTimedate2 exception error: " + str(inTimedate2)
			return wRes	#失敗
		wRes['TD2'] = wTD2
		
		#############################
		# 差分を求めて秒数に変換する
		wRunTime = wTD1 - wTD2
		wRunTime = wRunTime.seconds
		wSec = cls.sGetRound( inValue=wRunTime, inFLen=2 )
		
		wRes['RateSec'] = wSec
		#############################
		# 正常
		wRes['Result']    = True
		return wRes



#####################################################
# 時間分加算して返す
#####################################################
	@classmethod
	def sTimeAddHour( cls, inTimedate=None, inSec=None ):
		#############################
		# 応答形式
		wRes = {
			"Result"	: False,	# 結果
			"Reason"	: None,
			
			"TimeDate"	: None,
			"NextTD"	: None		#
		}
		
		#############################
		# 時間形式に変換する
		try:
			wTD = str( inTimedate )
			wTD = datetime.strptime( wTD, "%Y-%m-%d %H:%M:%S")
		except:
			wRes['Reason'] = "inTimedate1 exception error: " + str(inTimedate1)
			return wRes	#失敗
		wRes['TimeDate'] = wTD
		
		#############################
		# 加算
		wTD = wTD + timedelta( seconds=inSec )
		
		wRes['NextTD'] = wTD
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# 時間差
#   inTimedate   比べる日時
#   inThreshold  比べる時間差(秒)
#   inTimezone   タイムゾーン補正値: デフォルト 9=東京
#                                    補正なし   -1
# 使い方１：
#   比べる日時と時間差を出す
#     inTimedate を設定("%Y-%m-%d %H:%M:%S")、
#     inThreshold を設定
#
# 使い方２：
#   現在日時から指定時間差の過去日時を出す
#     inTimedate は未設定 (None or null)
#     inThreshold を設定
#
#####################################################
	@classmethod
	def sTimeLag( cls, inTimedate=None, inThreshold=__DEF_LAG_THRESHOLD, inTimezone=-1 ):
		#############################
		# 応答形式
		wRes = {
			"Result"	: False,	# 結果
			
			"Beyond"	: False,	# True= 比べる時間差を超えている
			"Future"	: False,	# True= 比べる時間が未来時間
			"InputTime"	: "",		# 比べる日時 str(入力時)
			"NowTime"	: "",		# 現在日時 str
			"RateTime"	: "",		# 現在日時から指定時間差の過去日時 str
			"RateDay"	: 0,		# 時間差(日数)
			"RateSec"	: 0			# 時間差(秒)
		}
		
		#############################
		# 現時間の取得
		wNowTime = cls().sGetTime()
		if wNowTime['Result']!=True :
			return wRes	#失敗
		
		#############################
		# 入力時間の整形
		if inTimedate!=None and inTimedate!="" :
		### 使い方１の場合= 比べる日時と時間差を出す
			wTD = str( inTimedate )
				##形式合わせ +、.を省く（鯖によって違う？
			wIfind = wTD.find('+')
			wTD = wTD[0:wIfind]
			wIfind = wTD.find('.')
			if wIfind>=0 :
				wTD = wTD[0:wIfind]
			
			### 加工しやすいようにフォーマットする
			try:
				wTD = datetime.strptime( wTD, "%Y-%m-%d %H:%M:%S")
			except:
				return wRes	#失敗
		
		### 現在日時から指定時間差の過去日時を出す
		else :
			wTD = wNowTime['Object'] - timedelta( seconds=inThreshold )
			wTD = str( wTD )
				##形式合わせ +、.を省く（鯖によって違う？
			wIfind = wTD.find('+')
			wTD = wTD[0:wIfind]
			wIfind = wTD.find('.')
			if wIfind>=0 :
				wTD = wTD[0:wIfind]
			
			### 加工しやすいようにフォーマットする
			try:
				wTD = datetime.strptime( wTD, "%Y-%m-%d %H:%M:%S")
			except:
				return wRes	#失敗
		
		#############################
		# タイムゾーンの指定があれば補正する
		if inTimezone!=-1 :
			wTD = wTD + timedelta( hours=inTimezone )
		
		#############################
		# 使い方１の場合
		#  =差を求める(秒差)
		if inTimedate!=None and inTimedate!="" :
			if wNowTime['Object']>=wTD :
				wRateTime = wNowTime['Object'] - wTD
			else :
				wRateTime = wTD - wNowTime['Object']
				wRes['Future'] = True	#未来時間
			
			wRes['RateDay'] = wRateTime.days
			wRes['RateSec'] = wRateTime.total_seconds()
			
			### 現在から差までの日時
			wRes['RateTime'] = wTD + timedelta( seconds=inThreshold )
			
			if wRes['RateSec'] > inThreshold :
				wRes['Beyond'] = True	#差あり
			
			wRes['InputTime'] = wTD
			wRes['NowTime']   = wNowTime['TimeDate']
		
		#############################
		# 使い方２の場合
		#  =結果を載せる
		else :
			wRes['NowTime']   = wNowTime['TimeDate']
			wRes['RateTime']  = wTD
		
		#############################
		# 正常
		wRes['Result']    = True
		return wRes



#####################################################
# 日数加算
#####################################################
	@classmethod
	def sAddTimedate_day( cls, inTimedate, inDay ):
		wRes = {
			"Result"	: False,
			"TimeDate"	: ""
		}
		
		#############################
		# 入力時間の整形
		wTimedate = str(inTimedate)
		
		#############################
		# タイムゾーンで時間補正
		try:
			wRes['TimeDate'] = datetime.strptime( wTimedate, "%Y-%m-%d %H:%M:%S") + timedelta( days=inDay )
		except:
			return wRes	#失敗
		
		wRes['Result'] = True
		return wRes



#####################################################
# 日付が切り替わったか
#####################################################
	@classmethod
	def sCheckNextDay( cls, inSrcTD, inDstTD=None ):
		wRes = {
			"Result"	: False,
			"Reason"	: None,
			"Next"		: False		# True= SrcTDが翌日
		}
		
		try:
			#############################
			# 文字列を日時型に変換する
			wSrcTD = datetime.strptime( inSrcTD, "%Y-%m-%d %H:%M:%S")
			wSrcTD = str( wSrcTD )
			wSrcTD = wSrcTD.split(" ")
			wSrcTD = wSrcTD[0].split("-")
			
			#############################
			# 比較先がなければ現在時刻を取得する
			if inDstTD==None :
				wNowTD = datetime.now()
			else:
				wNowTD = inDstTD
				if isinstance( inDstTD, datetime )==False :
					wNowTD = datetime.strptime( inDstTD, "%Y-%m-%d %H:%M:%S")
					wNowTD = str( wNowTD )
					wNowTD = wNowTD.split(" ")
					wNowTD = wNowTD[0].split("-")
		
		except ValueError as err :
			wRes['Reason'] = "Exception error: " + str(err)
			return wRes
		
		#############################
		# SrcとDstが違う=翌日
		if wSrcTD[0]!=wNowTD[0] or \
		   wSrcTD[1]!=wNowTD[1] or \
		   wSrcTD[2]!=wNowTD[2] :
			wRes['Next'] = True
		
		wRes['Result'] = True
		return wRes



#####################################################
# スリープ
#####################################################
	@classmethod
	def sSleep( cls, inSec ):
		if isinstance( inSec, int )!=True :
			inSec = 5
		
		try:
			time.sleep( inSec )
		except ValueError as err :
			return False
		
		return True



#####################################################
# ping疎通確認
#####################################################
	@classmethod
	def sPing( cls, inSend_Ping="127.0.0.1" ):
		#############################
		# ping除外ホスト
		if inSend_Ping in cls.__DEF_ARR_NOTPING :
			return True	#ping除外なら疎通チェックせずOKとする
		
		#############################
		# hostがローカルっぽい？
		wHostname = cls().Get_HostName()
		wI = inSend_Ping.find( wHostname )
		if wI>=0 :
			wHostLen = len( wHostname )
			wPingLen = len( inSend_Ping )
			if (wHostLen + wI )==wPingLen :
				return True	#自hostなら疎通チェックせずOKとする
		
		#############################
		# Ping実行
		wPingComm = "ping -c " + cls.__DEF_PING_COUNT + " " + str(inSend_Ping)
		
		#############################
		# 結果判定
		wStatus, wResult = sp.getstatusoutput( wPingComm )
		if wStatus==0 :
			return True	# Link UP
		
		return False	# Link Down



#####################################################
# Python version取得
#   参考：
#   sys.version_info(major=2, minor=7, micro=5, releaselevel='final', serial=0)
#####################################################
	def Get_PythonVer(self):
		wCHR_version = str(sys.version_info.major) + "."
		wCHR_version = wCHR_version + str(sys.version_info.minor) + "."
		wCHR_version = wCHR_version + str(sys.version_info.micro) + "."
		wCHR_version = wCHR_version + str(sys.version_info.serial) + " "
		wCHR_version = wCHR_version + sys.version_info.releaselevel
		return wCHR_version



#####################################################
# Host名取得
#####################################################
	def Get_HostName(self):
		if os.name == 'nt':
			###windowsの場合
			wCHR_hostname = socket.gethostname()
		else:
			###それ以外：Linux系の場合
			wCHR_hostname = str(os.uname()[1]).strip()
		
		return wCHR_hostname



#####################################################
# 画面クリア
#####################################################
	@classmethod
	def sDispClr( cls ):
		if os.name == 'nt':
			###windowsの場合
			os.system('cls')
		else:
			###それ以外：Linux系の場合
			os.system('clear')
		
		return



#####################################################
# カレントパスの取得
#####################################################
	@classmethod
	def sGetCwd( cls ):
		wStr = os.getcwd()
		return wStr



#####################################################
# コンソールへのprint表示
#####################################################
	@classmethod
	def sPrn( cls, inMsg ):
		print( inMsg )
		return



#####################################################
# コンソールへのエラー表示
#####################################################
	@classmethod
	def sErr( cls, inRes ):
		wMsg = cls.sCatErr( inRes )
		print( wMsg )
		return



#####################################################
# エラークラス+関数+理由をくっつけて返す
#####################################################
	@classmethod
	def sCatErr( cls, inRes ):
		try:
			wMsg = str(inRes['Class']) + ": " + str(inRes['Func']) + ": " + str(inRes['Reason'])
		except ValueError as err :
			wMsg = str(inRes['Class']) + ": " + str(inRes['Func']) + ": " + "Detect Exception"
		
		return wMsg



#####################################################
# コンソールへのprint表示(1行消去して表示)
#####################################################
	@classmethod
	def sPrnER( cls, inMsg ):
		sys.stdout.write( "\r%s" % inMsg )
		sys.stdout.flush()
		return



#####################################################
# コンソールへのinput表示
#####################################################
	@classmethod
	def sInp( cls, inMsg ):
		wInput = input( inMsg ).strip()
		return wInput



#####################################################
# コンソールへのinput表示(入力が見えない)
#####################################################
	@classmethod
	def sGpp( cls, inMsg ):
		wInput = getpass( inMsg ).strip()
		return wInput



#####################################################
# コンソール待機
#####################################################
	@classmethod
	def sPrnWAIT( cls, inCount ):
		wCount = inCount
		try:
			while True:
				if wCount==0 :
					break
				
				#############################
				# 1行にカウントを表示
				# ctrl+cでウェイト中止
				wStr = "残り待機時間 " + str( wCount ) + " 秒"
				cls.sPrnER( wStr )
				cls.sSleep(1)
				wCount -= 1
		
		except KeyboardInterrupt:
			return False 	#ウェイト中止
		
		return True			#ウェイト完了



#####################################################
# row['content']からHTMLタグを除去
#####################################################
	@classmethod
	def sDel_HTML( cls, inCont ):
		wPatt = re.compile(r"<[^>]*?>")
		wD_Cont = wPatt.sub( "", inCont )
		return wD_Cont



#####################################################
# row['content']からハッシュタグを除去
#####################################################
	@classmethod
	def sDel_HashTag( cls, inCont ):
		wPatt = re.compile(r"(#[^\s]+)")
		wD_Cont = wPatt.sub( "", inCont )
		return wD_Cont



#####################################################
# row['content']からハッシュタグの個数を返す
#####################################################
	@classmethod
	def sGetCount_HashTag( cls, inCont ):
		wPatt = re.findall(r'(#[^\s]+)', inCont )
		wCount = len(wPatt)
		return wCount



#####################################################
# row['content']からHTMLタグを除去
#####################################################
	@classmethod
	def sChkREMString( cls, inStr, inSpace=True ):
		wPatt = r'[\\|/|:|?|.|"|<|>|\|]'
		wRes = cls().sRe_Search( wPatt, inStr )
		if wRes==False :
			return False
		
		if inSpace==True :
			if inStr.find(" ")<0 :
				return False
		
		return True



#####################################################
# row['content']からURLを除去
#####################################################
	@classmethod
	def sDel_URL( cls, inCont ):
		wPatt = re.compile(r"https?:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+")
		wD_Cont = wPatt.sub( "", inCont )
		return wD_Cont



#####################################################
# 文字列からパターン検索
#   wRes.group()  正規表現にマッチした文字列を返す。
#   wRes.start()  マッチの開始位置を返す。
#   wRes.end()    マッチの終了位置を返す。
#   wRes.span()   マッチの位置 (start, end) を含むタプルを返す。
#####################################################
	@classmethod
	def sRe_Search( cls, inPatt, inCont ):
		try:
			wRes = re.search( inPatt, inCont )
		except:
			return False
		
		return wRes



#####################################################
# 文字列からパターン置換
#####################################################
	@classmethod
	def sRe_Replace( cls, inPatt, inCont, inReplace ):
		wRes = {
			"Result"	: False,
			"Match"		: False,
			"After"		: None
		}
		
		if inCont=="" :
			return wRes
		
		wRes['Match'] = cls.sRe_Search( inPatt, inCont )
		
		try:
			wRes['After'] = inCont.replace( inPatt, inReplace )
		except:
			return wRes
		
		wRes['Result'] = True
		return wRes



#####################################################
# 文字列型から数値型に変換する
#####################################################
	@classmethod
	def sChgInt( cls, inCont ):
		wRes = {
			"Result"	: False,
			"Value"		: 0
		}
		
		try:
			wValue = int( inCont )
		except:
			return wRes
		
		wRes['Value']  = wValue
		wRes['Result'] = True
		return wRes



#####################################################
# 全角文字をLen=2としてカウントする
#####################################################
	@classmethod
	def sDCharaCount( cls, inText ):
		wCount = 0
		for wChar in inText:
			if unicodedata.east_asian_width(wChar) in 'FWA':
				wCount += 2
			else:
				wCount += 1
		return wCount



#####################################################
# ランダム値を取得
#####################################################
	@classmethod
	def sGetRand( cls, inValue ):
		if not isinstance( inValue, int ):
			return -1
		
		try:
			wVal = random.randrange( inValue )
		except:
			return -1
		
		return wVal



#####################################################
# 小数点以下切り捨て
#####################################################
	@classmethod
	def sGetFloor( cls, inValue ):
		wVal = math.floor( inValue )
		return wVal



#####################################################
# 小数点以下指定
#####################################################
	@classmethod
	def sGetRound( cls, inValue, inFLen=2 ):
		wVal = round( inValue, inFLen )
		return wVal



