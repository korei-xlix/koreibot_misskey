#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : メイン処理(コンソール)
#####################################################

from ktime import CLS_TIME
from osif import CLS_OSIF
from traffic import CLS_Traffic
from filectrl import CLS_File
from setup import CLS_Setup
from botctrl import CLS_BotCtrl
from mydisp import CLS_MyDisp

from twitter_main import CLS_TwitterMain
from gval import gVal
#####################################################
class CLS_Main_Console() :
#####################################################
	#使用クラス実体化
	OBJ_TwitterMain = ""
	
	FLG_MainDispClear = True

#####################################################
# 実行
#####################################################
	@classmethod
	def sRun(cls):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Main_Console"
		wRes['Func']  = "sRun"
		
		#############################
		# 時間を取得
		wSubRes = CLS_TIME.sTimeUpdate()
		if wSubRes['Result']!=True :
			###時間取得失敗  時計壊れた？
			wRes['Reason'] = "TimeUpdate is failed"
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# 実行チェック
		wTestRes = cls.sCheckTest()
		if wTestRes!=True :
			###処理終了
			CLS_OSIF.sInp( '\n' + "リターンキーを押して再度コンソールアプリを起動してください。[RT]" )
			return wRes
		
		### ※通常処理継続
		
		#############################
		# 初期化
		cls.OBJ_TwitterMain  = CLS_TwitterMain()	#メインの実体化
		wResIni = cls.OBJ_TwitterMain.Init()		#初期化
		if wResIni['Result']!=True :
			CLS_BotCtrl.sBotEnd()	#bot停止
			return wRes
		
		#############################
		# コマンド実行前処理
		wSubRes = cls.sFirstProcess()
		if wSubRes['Result']!=True :
			wRes['Reason'] = wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			CLS_BotCtrl.sBotEnd()	#bot停止
			return wRes
		
		#############################
		# コンソールを表示
		while True :
			wCommand = cls().sViewMainConsole()
			
			if wCommand=="" :
				###未入力は再度入力
				continue
			
			if wCommand.find("\\q")>=0 or wCommand=="exit" :
				#############################
				# 終了
				gVal.OBJ_L.Log( "S", wRes, "コンソール停止" )
				CLS_BotCtrl.sBotEnd()	#bot停止
				break
				#############################
			
			#############################
			# システム設定
			if wCommand=="\\conf" :
				while True :
					wSysCommand = cls().sViewSystemConfigConsole()
					
					if wSysCommand=="" :
						###未入力は再度入力
						continue
					
					if wSysCommand=="\\q" :
						#############################
						# 終了
						break
					
					#############################
					# コマンド実行
					wResCmd = cls().sRunSystemConfig( wSysCommand )
					
					#############################
					# 待機(入力待ち)
					CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
				
				continue
			
			#############################
			# コマンド実行前処理
			wSubRes = cls.sFirstProcess()
			if wSubRes['Result']!=True :
				wRes['Reason'] = wSubRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				CLS_BotCtrl.sBotEnd()	#bot停止
				return wRes
			
			#############################
			# コマンド実行
			wResCmd = cls().sRunCommand( wCommand )
			
			#############################
			# 待機(入力待ち)
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			
		return




#####################################################
# メインコンソール画面の表示
#####################################################
	@classmethod
	def sViewMainConsole(cls):
		
		#############################
		# メインコンソール画面
		wResDisp = CLS_MyDisp.sViewDisp( "MainConsole", inClear=cls.FLG_MainDispClear )
		if wResDisp['Result']==False :
			gVal.OBJ_L.Log( "D", wResDisp )
			return "\\q"	#失敗=強制終了
		
		wCommand = CLS_OSIF.sInp( "コマンド？=> " )
		return wCommand



#####################################################
# 実行
#####################################################
	@classmethod
	def sRunCommand( cls, inCommand ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Main_Console"
		wRes['Func']  = "sRunCommand"
		
		#############################
		# Bot実行回数の記録
		CLS_Traffic.sP( "run" )
		
	#####################################################
		#############################
		# 自動監視
		if inCommand=="\\a" :
			cls.OBJ_TwitterMain.AllRun()
		
		#############################
		# タイムラインフォロー
		elif inCommand=="\\f" :
			cls.OBJ_TwitterMain.TimelineFollow()
		
		#############################
		# トレンドツイート
		elif inCommand=="\\tt" :
			cls.OBJ_TwitterMain.TrendTweet()
		
	#####################################################
		#############################
		# キーワードいいね
		elif inCommand=="\\kk" :
			cls.OBJ_TwitterMain.KeywordFavo()
		
		#############################
		# リストいいね設定
		elif inCommand=="\\fc" :
			cls.OBJ_TwitterMain.SetListFavo()
		
	#####################################################
		#############################
		# ユーザ管理
		elif inCommand=="\\u" :
			cls.OBJ_TwitterMain.UserAdmin()
		
		#############################
		# 警告ユーザ管理
		elif inCommand=="\\uc" :
			cls.OBJ_TwitterMain.AdminCautionUser()
		
###		#############################
###		# 非絡みユーザ一覧
###		elif inCommand=="\\ub" :
###			cls.OBJ_TwitterMain.UserBList()
###		
		#############################
		# VIPフォロー監視
		elif inCommand=="\\vc" :
			cls.OBJ_TwitterMain.ManualCheckVipFollow()
		
		#############################
		# 被ブロックユーザ一覧
		elif inCommand=="\\lb" :
			cls.OBJ_TwitterMain.BlockList()
		
	#####################################################
		#############################
		# ログの表示(異常ログ)
		elif inCommand=="\\l" :
			gVal.OBJ_L.View( inViewMode="E" )
		
		#############################
		# ログの表示(ユーザ記録ログ)
		elif inCommand=="\\lu" :
			gVal.OBJ_L.View( inViewMode="U" )
		
		#############################
		# ログの表示(運用ログ)
		elif inCommand=="\\lr" :
			gVal.OBJ_L.View( inViewMode="R" )
		
		#############################
		# ログの表示(全ログ)
		elif inCommand=="\\la" :
			gVal.OBJ_L.View()
		
		#############################
		# スケジュールの表示
		elif inCommand=="\\vt" :
			cls.OBJ_TwitterMain.View_Schedule()
		
		#############################
		# システム情報の表示
		elif inCommand=="\\v" :
			cls.OBJ_TwitterMain.View_Sysinfo()
		
		#############################
		# トラヒック情報の表示
		elif inCommand=="\\lt" :
			wResTraffic = CLS_Traffic.sReport()
			if wResTraffic['Result']!=True :
				gVal.OBJ_L.Log( "B", wResTraffic )
		
		#############################
		# テスト
		elif inCommand=="\\test" :
			cls.OBJ_TwitterMain.Test()
		
	#####################################################
		#############################
		# ないコマンド
		else :
			wRes['Reason'] = "存在しないコマンド :" + str(inCommand)
			gVal.OBJ_L.Log( "D", wRes )
			return False
		
		return True



#####################################################
# システム設定の表示
#####################################################
	@classmethod
	def sViewSystemConfigConsole(cls):
		
		#############################
		# システム設定画面
		wResDisp = CLS_MyDisp.sViewDisp( "SystemConfigConsole", inClear=cls.FLG_MainDispClear )
		if wResDisp['Result']==False :
			gVal.OBJ_L.Log( "D", wResDisp )
			return "\\q"	#失敗=強制終了
		
		wCommand = CLS_OSIF.sInp( "コマンド？=> " )
		return wCommand



#####################################################
# システム設定 実行
#####################################################
	@classmethod
	def sRunSystemConfig( cls, inCommand ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Main_Console"
		wRes['Func']  = "sRunSystemConfig"
		
	#####################################################
		#############################
		# いいね全解除
		if inCommand=="\\rm" :
			cls.OBJ_TwitterMain.AllFavoRemove()
		
		#############################
		# 強制自動リムーブ
		elif inCommand=="\\fr" :
			cls.OBJ_TwitterMain.ForceCheckAutoRemove()
		
		#############################
		# 強制いいね情報送信
		elif inCommand=="\\ff" :
			cls.OBJ_TwitterMain.ForceSendFavoDate()
		
	#####################################################
		#############################
		# 相互いいね停止
		elif inCommand=="\\fs" :
			cls.OBJ_TwitterMain.SetMfvStop()
		
		#############################
		# トレンドタグ設定
		elif inCommand=="\\tc" :
			cls.OBJ_TwitterMain.SetTrendTag()
		
		#############################
		# 質問タグ設定
		elif inCommand=="\\qc" :
			cls.OBJ_TwitterMain.SetQuestionTag()
		
		#############################
		# VIPタグ設定
		elif inCommand=="\\vc" :
			cls.OBJ_TwitterMain.SetVipTag()
		
		#############################
		# 削除タグ設定
		elif inCommand=="\\dc" :
			cls.OBJ_TwitterMain.SetDelTag()
		
		#############################
		# リスト通知設定
		elif inCommand=="\\ic" :
			cls.OBJ_TwitterMain.SetListName()
		
		#############################
		# 自動リムーブ
		elif inCommand=="\\ac" :
			cls.OBJ_TwitterMain.SetAutoRemove()
		
	#####################################################
		#############################
		# 禁止ユーザ
		elif inCommand=="\\uc" :
			cls.OBJ_TwitterMain.ExcuteUser()
		
	#####################################################
		#############################
		# 運用ログ（全部）
		elif inCommand=="\\lr" :
			gVal.OBJ_L.View( inViewMode="V" )
		
		#############################
		# ログの表示(トラヒック)
		elif inCommand=="\\lt" :
			gVal.OBJ_L.View( inViewMode="T" )
		
		#############################
		# ログの表示(全ログ)
		elif inCommand=="\\la" :
			gVal.OBJ_L.View( inViewMode="F" )
		
		#############################
		# ログクリア
		elif inCommand=="\\lcr" :
			gVal.OBJ_L.Clear()
		
		#############################
		# 全ログクリア
		elif inCommand=="\\lall" :
			gVal.OBJ_L.Clear( inAllClear=True )
		
	#####################################################
		#############################
		# Twitter APIの変更
		elif inCommand=="\\apiconf" :
			wResAPI = gVal.OBJ_Tw_IF.SetTwitter( gVal.STR_UserInfo['Account'] )
			if wResAPI['Result']!=True :
				wRes['Reason'] = "Set Twitter API failed: " + wResAPI['Reason']
				gVal.OBJ_L.Log( "D", wRes )
		
		#############################
		# 時間リセット
		elif inCommand=="\\tres" :
			cls.OBJ_TwitterMain.ResetTimeInfo()
		
	#####################################################
		#############################
		# ないコマンド
		else :
			wRes['Reason'] = "存在しないコマンド :" + str(inCommand)
			gVal.OBJ_L.Log( "D", wRes )
			return False
		
		return True



#####################################################
# 実行チェック処理
#####################################################
	@classmethod
	def sCheckTest(cls):
		#############################
		# botテスト、引数ロード
		#   テスト項目
		#     1.引数ロード
		#     2.データベースの取得
		#     3.ログの取得
		#     4.排他
		#     5.Twitterの取得
		#     6.Readme情報の取得
		#     7.Python情報の取得
		#     8.TESTログ記録
		wResTest = CLS_BotCtrl.sBotTest()
		if wResTest['Result']!=True :
			return False	###問題あり
		
		wCLS_Setup = CLS_Setup()
		#############################
		# セットアップモードで実行
		if gVal.STR_SystemInfo['RunMode']=="setup" :
			wCLS_Setup.Setup( wResTest['Responce'] )
			return False	###問題あり
		
		#############################
		# 初期化モードで実行
		elif gVal.STR_SystemInfo['RunMode']=="init" :
			wCLS_Setup.AllInit( wResTest['Responce'] )
			return False	###問題あり
		
		#############################
		# データ追加モードで実行
		elif gVal.STR_SystemInfo['RunMode']=="add" :
			wCLS_Setup.Add( wResTest['Responce'] )
			return False	###問題あり
		
		#############################
		# 禁止ワード追加モードで実行
		elif gVal.STR_SystemInfo['RunMode']=="word" :
			wCLS_Setup.Add( wResTest['Responce'], inWordOnly=True )
			return False	###問題あり
		
		#############################
		# データクリアモードで実行
		elif gVal.STR_SystemInfo['RunMode']=="testclear" :
			wCLS_Setup.testClear( wResTest['Responce'] )
			return False	###問題あり
		
		#############################
		# PINGテストで実行
		elif gVal.STR_SystemInfo['RunMode']=="ping" :
			wCLS_Setup.Ping( wResTest['Responce']['hostname'] )
			return False	###問題あり
		
		#############################
		# =正常
		return True



#####################################################
# コマンド実行前処理
#####################################################
	@classmethod
	def sFirstProcess(cls):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Main_Console"
		wRes['Func']  = "sFirstProcess"
		
		#############################
		# 開始or前回チェックから15分経ったか
		w15Res = cls.OBJ_TwitterMain.Circle15min()
		if w15Res['Result']!=True :
			wRes['Reason'] = "Circle15min is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常
		wRes['Result']   = True
		return wRes



