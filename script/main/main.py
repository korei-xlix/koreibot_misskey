#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Misskey
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_misskey/
# ::Class    : メイン処理(コンソール)
#####################################################
import threading

###from traffic import CLS_Traffic
###from filectrl import CLS_File
###from setup import CLS_Setup
###
###from twitter_main import CLS_TwitterMain

from misskey_if import CLS_Misskey_IF
from mysql_if import CLS_MySQL_IF
from mylog import CLS_Mylog

from mydisp import CLS_MyDisp
from botctrl import CLS_BotCtrl

from ktime import CLS_TIME
from osif import CLS_OSIF
from gval import gVal
#####################################################
class CLS_Main() :
#####################################################

										## スレッド実行間隔(秒)
###	DEF_TIMELINE_ROOP = 5
	DEF_REACTION_ROOP = 60

###	VAL_Timeline_Roop = 0
	VAL_Reaction_Roop = 0

										## スレッド停止フラグ
###	FLG_Timeline_EndRoop = False
	FLG_Reaction_EndRoop = False		#

###	TRD_Timeline = None					## タイムラインスレッド用
	TRD_Reaction = None					## リアクションスレッド用
	TRD_Main     = None					## メインスレッド用

										## 非同期 受信処理
	FLG_Receive = False					#  True=受信中、False=未受信

	ARR_Reaction = {}					## 受信リアクション


#####################################################
# 実行
#####################################################
	def Run( self ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Main"
		wRes['Func']  = "Run"
		
		#############################
		# 処理開始表示
		CLS_OSIF.sPrn( "*** bot開始 ***" )
		
		#############################
		# 時間を取得
		wSubRes = CLS_TIME.sTimeUpdate( wRes )
		if wSubRes['Result']!=True :
			###時間取得失敗  時計壊れた？
			wRes['Reason'] = "Function is failed: CLS_TIME.sTimeUpdate"
			CLS_OSIF.sErr( wRes )
			return wRes
		
		wCLS_BotCtrl = CLS_BotCtrl( wRes, parentObj=self )
		if wRes['Result']!=True :
			###失敗  時計壊れた？
			wRes['Reason'] = "Create class is failed: CLS_BotCtrl"
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# 引数の取得
		wSubRes = wCLS_BotCtrl.GetParam()
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "Get param is failed"
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# 初期化
		



		#############################
		# 処理起動
		
		#############################
		# 通常モード
		if gVal.STR_SystemInfo['RunMode']=="run" :
			if gVal.FLG_Test==True :
				CLS_OSIF.sPrn( "mode: run" )
			
			#############################
			# スレッド起動
###			self.TRD_Timeline = threading.Thread(target=self.ThreadTimeline)
			self.TRD_Reaction = threading.Thread(target=self.ThreadReaction)
			self.TRD_Main     = threading.Thread(target=self.ThreadMain)
###			self.TRD_Timeline.start()
			self.TRD_Reaction.start()
			self.TRD_Main.start()
###			self.TRD_Timeline.join()
			self.TRD_Reaction.join()
			self.TRD_Main.join()
		
		#############################
		# 初期化モード
		elif gVal.STR_SystemInfo['RunMode']=="init" :
			if gVal.FLG_Test==True :
				CLS_OSIF.sPrn( "mode: init" )
			
			self.Init()
		


		
		#############################
		# 終了表示
		CLS_OSIF.sPrn( "*** bot停止 ***" )
		return



#####################################################
# 初期化
#####################################################
	def Init( self ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Main"
		wRes['Func']  = "Init"
		
		#############################
		# 処理開始表示
		if gVal.FLG_Test==True :
			CLS_OSIF.sPrn( "start: Init" )
		
		gVal.STR_UserInfo['Account'] = gVal.DEF_ROOT_USER_NAME
		
		#############################
		# 時間を取得
		wSubRes = CLS_TIME.sTimeUpdate( wRes )
		if wSubRes['Result']!=True :
			###時間取得失敗  時計壊れた？
			wRes['Reason'] = "Function is failed: CLS_TIME.sTimeUpdate"
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# DB接続
		gVal.OBJ_DB_IF = CLS_MySQL_IF( wRes, parentObj=self )
		wSubRes = gVal.OBJ_DB_IF.Connect()
		if wSubRes['Result']!=True :
			###失敗
			wStr = "Function is failed: Connect"
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# ログテーブル構築
		wSubRes = gVal.OBJ_DB_IF.CreateLOG()
		if wSubRes['Result']!=True :
			###失敗
			wStr = "Function is failed: CreateLOG"
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# テーブル再構築
		gVal.OBJ_DB_IF.CreateTable()
		
		gVal.OBJ_L = CLS_Mylog()
		#############################
		# 初回記録
		gVal.OBJ_L.Log( "S", wRes, "◎DB初期化" )
		
		#############################
		# DB切断
		gVal.OBJ_DB_IF.Close()
		
		#############################
		# 処理開始表示
		if gVal.FLG_Test==True :
			CLS_OSIF.sPrn( "end: Init" )
		
		#############################
		# 登録モード起動
		CLS_OSIF.sPrn( "登録モード起動中..." + '\n' )
		CLS_OSIF.sSleep( 5 )	# 5秒待機 (DB再接続用の待ち)
		
		self.Regist()
		return



#####################################################
# 登録
#####################################################
	def Regist( self ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Main"
		wRes['Func']  = "Regist"
		
		#############################
		# 処理開始表示
		if gVal.FLG_Test==True :
			CLS_OSIF.sPrn( "*** 登録モード起動 ***" )
		
		#############################
		# DB接続
		gVal.OBJ_DB_IF = CLS_MySQL_IF( wRes, parentObj=self )
		wSubRes = gVal.OBJ_DB_IF.Connect()
		if wSubRes['Result']!=True :
			###失敗
			wStr = "Function is failed: Connect"
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# misskeyオブジェクトの生成
		gVal.OBJ_Misskey_IF = CLS_Misskey_IF( wRes, parentObj=self )
		
		gVal.OBJ_L = CLS_Mylog()
		#############################
		# ユーザの登録
		wStr = '\n' + "ユーザ登録をおこないます。" + '\n'
		wStr = wStr + "**************************" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		wSTR_UserInfo = {
			"account"	: None,
			"host"		: None,
			"token"		: None
		}
		
		while True:
			#############################
			# ユーザ名入力
			wStr =        "登録するmisskeyアカウントを入力してください。" + '\n'
			wStr = wStr + "  形式：アカウント名@ホスト名(misskey.io)" + '\n'
			wStr = wStr + "misskeyアカウント ? > "
			wInput = CLS_OSIF.sInp( wStr )
			if wInput==None or wInput=="" :
				continue
			
			wSubRes = CLS_OSIF.sRe_Split( inPatt="@", inCont=wInput )
			if wSubRes['Result']!=True or len(wSubRes['After'])!=2 :
				CLS_OSIF.sPrn( "入力形式が違います" + '\n' )
				continue
			wSTR_UserInfo['account'] = wSubRes['After'][0]
			wSTR_UserInfo['host']    = wSubRes['After'][1]
			
			#############################
			# misskeyアクセストークン
			wStr = '\n' + "misskeyで取得したアクセストークンを入力してください。" + '\n'
			wStr = wStr + "misskeyアクセストークン ? > "
			wInput = CLS_OSIF.sInp( wStr )
			if wInput==None or wInput=="" :
				continue
			
			wSTR_UserInfo['token'] = wInput
			
			#############################
			# misskey接続
			wSubRes = gVal.OBJ_Misskey_IF.Connect(
					inAccount = wSTR_UserInfo['account'],
					inHost = wSTR_UserInfo['host'],
					inToken = wSTR_UserInfo['token']
			)
			if wSubRes['Result']!=True :
				###失敗
				wStr = "Function is failed: Connect"
				CLS_OSIF.sErr( wRes )
			
			break #登録ループ終了
		
		#############################
		# ユーザをデータベースに登録する
		wSubRes = gVal.OBJ_DB_IF.USER_Regist( inID=wSTR_UserInfo['account'], inHost=wSTR_UserInfo['host'], inToken=wSTR_UserInfo['token'] )
		if wSubRes['Result']!=True :
			###失敗
			wStr = "Function is failed: OBJ_DB_IF.USER_Regist"
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# 初回記録
		gVal.OBJ_L.Log( "S", wRes, "ユーザ登録完了: user=" + wSTR_UserInfo['account'] )
		
		#############################
		# DB切断
		gVal.OBJ_DB_IF.Close()
		
		#############################
		# 処理開始表示
		if gVal.FLG_Test==True :
			CLS_OSIF.sPrn( "*** 登録モード終了 ***" )
		return



#####################################################
# メインスレッド
#####################################################
	def ThreadMain( self ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Main"
		wRes['Func']  = "ThreadMain"
		
		#############################
		# スレッド開始表示
		if gVal.FLG_Test==True :
			CLS_OSIF.sPrn( "stsrt: ThreadMain" )
		
		gVal.OBJ_L = CLS_Mylog()
		#############################
		# DB接続
		gVal.OBJ_DB_IF = CLS_MySQL_IF( wRes, parentObj=self )
		wSubRes = gVal.OBJ_DB_IF.Connect()
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "Function is failed: Connect"
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# ユーザ情報ロード
		wSubRes = gVal.OBJ_DB_IF.USER_Get(
			inID = gVal.STR_UserInfo['Account'],
			inHost = gVal.STR_UserInfo['Host']
		)
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "Function is failed: OBJ_DB_IF.USER_Get"
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		wToken = str( wSubRes['Responce']['token'] )
		
		#############################
		# misskey接続
		gVal.OBJ_Misskey_IF = CLS_Misskey_IF( wRes, parentObj=self )
		
		wSubRes = gVal.OBJ_Misskey_IF.Connect(
				inAccount = gVal.STR_UserInfo['Account'],
				inHost = gVal.STR_UserInfo['Host'],
				inToken = wToken
		)
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "Function is failed: Connect"
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# スレッドループ
		while True :
			#############################
			# コンソール表示
			wInput = CLS_MyDisp.sViewConsole()
			
			#############################
			# スレッド停止コマンドか
			#   Input異常
			#   exit
			#   \\q
			wFLG_Stop = False
			# input異常か、exit
			if wInput['Result']==False or wInput['Responce']=="exit" :
				wFLG_Stop = True	#停止
			
			# \\q
			wSubRes = CLS_OSIF.sRe_Search( inPatt="\\\\q", inCont=wInput['Responce'] )
			if wSubRes['Match']==True :
				wFLG_Stop = True	#停止
			
			if wFLG_Stop==True :
				### 終了
				if gVal.FLG_Test==True :
					CLS_OSIF.sPrn( "stop: All Thread Stopping" )
###				self.FLG_Timeline_EndRoop = True
				self.FLG_Reaction_EndRoop = True
				break
			
			#############################
			# 受信開始
			#   \\r
			wSubRes = CLS_OSIF.sRe_Search( inPatt="^\\\\r", inCont=wInput['Responce'] )
			if wSubRes['Match']==True :
				wSubRes = gVal.OBJ_Misskey_IF.Async_StartReceive()
				continue
			
			#############################
			# ノート送信
			#   \\s
			wSubRes = CLS_OSIF.sRe_Search( inPatt="^\\\\s", inCont=wInput['Responce'] )
			if wSubRes['Match']==True :
				
				wStr = "ノート送信(\\q=キャンセル) ? > "
				wInput = CLS_OSIF.sInp( wStr )
				if wInput==None or wInput=="" :
					continue
				wSubRes = CLS_OSIF.sRe_Search( inPatt="^\\\\q", inCont=wInput )
				if wSubRes['Match']==True :
					continue
				
				wSubRes = gVal.OBJ_Misskey_IF.SendNote( inText=wInput )
				continue
			
##			#############################
##			# 受信停止
##			#   \\rs
##			wSubRes = CLS_OSIF.sRe_Search( inPatt="^\\\\s", inCont=wInput['Responce'] )
##			if wSubRes['Match']==True :
###				wSubRes = gVal.OBJ_Misskey_IF.Async_StopReceive()
###				if wSubRes['Result']==True :
###					CLS_OSIF.sPrn( "stop: Async misskey Receive" )
##				wSubRes = gVal.OBJ_Misskey_IF.Async_StopReceive( inFLG_Stop=True )
##				continue
##		
		#############################
		# スレッド終了表示
		if gVal.FLG_Test==True :
			CLS_OSIF.sPrn( "end: ThreadMain" )
		return



#####################################################
# タイムラインスレッド
#####################################################
###	def ThreadTimeline( self ):
###		#############################
###		# 応答形式の取得
###		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
###		wRes = CLS_OSIF.sGet_Resp()
###		wRes['Class'] = "CLS_Main"
###		wRes['Func']  = "ThreadTimeline"
###		
###		#############################
###		# スレッド開始表示
###		if gVal.FLG_Test==True :
###			CLS_OSIF.sPrn( "stsrt: ThreadTimeline" )
###		
###		self.FLG_Timeline_EndRoop = False
###		self.VAL_Timeline_Roop = 0
###		#############################
###		# スレッドループ
###		while True :
###			if self.FLG_Timeline_EndRoop==True :
###				break
###			
###			self.VAL_Timeline_Roop += 1
###			#############################
###			# 実行タイミングで、処理実行
###			if self.DEF_TIMELINE_ROOP<=self.VAL_Timeline_Roop :
###				wSubRes = gVal.OBJ_Misskey_IF.Async_StartReceive()
###				
###				self.VAL_Timeline_Roop = 0
###			
###			### 実行間隔(秒)
###			CLS_OSIF.sSleep(1)
###		
###		#############################
###		# スレッド終了表示
###		if gVal.FLG_Test==True :
###			CLS_OSIF.sPrn( "end: ThreadTimeline" )
###		return
###
###

#####################################################
# リアクションスレッド
#####################################################
	def ThreadReaction( self ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Main"
		wRes['Func']  = "ThreadReaction"
		
		#############################
		# スレッド開始表示
		if gVal.FLG_Test==True :
			CLS_OSIF.sPrn( "stsrt: ThreadReaction" )
		
		self.FLG_Reaction_EndRoop = False
		#############################
		# スレッドループ
		while True :
			if self.FLG_Reaction_EndRoop==True :
				break
			
			self.VAL_Reaction_Roop += 1
			#############################
			# 実行タイミングで、処理実行
			if self.DEF_REACTION_ROOP<=self.VAL_Reaction_Roop :
				CLS_OSIF.sPrn( "run: ThreadReaction: XXX1" )




				self.VAL_Reaction_Roop = 0
			
			### 実行間隔(秒)
			CLS_OSIF.sSleep(1)
		
		#############################
		# スレッド終了表示
		if gVal.FLG_Test==True :
			CLS_OSIF.sPrn( "end: ThreadReaction" )
		return



