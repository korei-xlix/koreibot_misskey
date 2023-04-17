#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : Twitter監視 メインモジュール
#####################################################
from twitter_follower import CLS_TwitterFollower
from twitter_favo import CLS_TwitterFavo
from twitter_reaction import CLS_TwitterReaction
from twitter_keyword import CLS_TwitterKeyword
from twitter_admin import CLS_TwitterAdmin
from test_sample import CLS_Test

from ktime import CLS_TIME
from osif import CLS_OSIF
from traffic import CLS_Traffic
from mydisp import CLS_MyDisp
from gval import gVal
#####################################################
class CLS_TwitterMain():
#####################################################
	OBJ_TwitterFollower = None
	OBJ_TwitterFavo     = None
	OBJ_TwitterReaction = None
	OBJ_TwitterKeyword  = None
	OBJ_TwitterAdmin    = None
	OBJ_Test            = None

###	ARR_ReacrionUserID = []

###	CHR_AutoRemoveDate = None



#####################################################
# テスト用
#####################################################
	def Test(self):
		self.OBJ_Test.Test()
		return



#####################################################
# Init
#####################################################
	def __init__(self):
		self.OBJ_TwitterFollower = CLS_TwitterFollower( parentObj=self )
		self.OBJ_TwitterFavo     = CLS_TwitterFavo( parentObj=self )
		self.OBJ_TwitterReaction = CLS_TwitterReaction( parentObj=self )
		self.OBJ_TwitterKeyword  = CLS_TwitterKeyword( parentObj=self )
		self.OBJ_TwitterAdmin    = CLS_TwitterAdmin( parentObj=self )
		self.OBJ_Test            = CLS_Test( parentObj=self )
		return



#####################################################
# 初期化
#####################################################
	def Init(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "Init"
		
		#############################
		# Twitterから自ユーザ情報を取得する
		wUserinfoRes = gVal.OBJ_Tw_IF.GetMyUserinfo()
		if wUserinfoRes['Result']!=True :
			wRes['Reason'] = "Twitter Error"
			gVal.OBJ_L.Log( "A", wRes )
			return wRes
		gVal.STR_UserInfo['id'] = wUserinfoRes['Responce']['id']
		
		#############################
		# トラヒック情報読み込み
		wResSub = CLS_Traffic.sGet()
		if wResSub['Result']!=True :
			wRes['Reason'] = "Get Traffic failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 除外文字読み込み
		wResSub = gVal.OBJ_DB_IF.GetExeWord()
		if wResSub['Result']!=True :
			wRes['Reason'] = "GetExcWord failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 除外プロフ文字読み込み
		wResSub = gVal.OBJ_DB_IF.GetExeProf()
		if wResSub['Result']!=True :
			wRes['Reason'] = "GetExcProf failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 禁止ユーザ読み込み
		wResSub = gVal.OBJ_DB_IF.GetExeUser()
		if wResSub['Result']!=True :
			wRes['Reason'] = "GetExeUser failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 警告ツイート読み込み
		wResSub = gVal.OBJ_DB_IF.GetCautionTweet()
		if wResSub['Result']!=True :
			wRes['Reason'] = "GetCautionTweet failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 検索ワード読み込み
		wResSub = gVal.OBJ_DB_IF.GetSearchWord()
		if wResSub['Result']!=True :
			wRes['Reason'] = "GetSearchWord failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# リストいいね指定読み込み
		wResSub = gVal.OBJ_DB_IF.GetListFavo()
		if wResSub['Result']!=True :
			wRes['Reason'] = "GetListFavo failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 相互いいね停止設定 取得
		wSubRes = gVal.OBJ_DB_IF.GetMfvStop()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "GetMfvStop is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# 周期15分処理
#####################################################
	def Circle15min(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "Circle15min"
		
		#############################
		# 時間を取得
		wSubRes = CLS_TIME.sTimeUpdate()
		if wSubRes['Result']!=True :
			###時間取得失敗  時計壊れた？
			wRes['Reason'] = "TimeUpdate is failed"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# 前回チェックから15分経っているか
		wGetLag = CLS_OSIF.sTimeLag( gVal.STR_Time['run'], inThreshold=gVal.DEF_STR_TLNUM['resetAPISec'] )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		if wGetLag['Beyond']==False :
			###前回から15分経ってない
			wRes['Result'] = True
			return wRes
		
		### ※前回から15分経ったので処理実行
		#############################
		# Twitter再接続
		wTwitterRes = gVal.OBJ_Tw_IF.ReConnect()
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitterの再接続失敗"
			gVal.OBJ_L.Log( "A", wRes )
			return wRes
		
		#############################
		# コマンド実行時間を更新
		wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "run", wGetLag['NowTime'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "SetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# トラヒック情報の記録と報告
		wResTraffic = CLS_Traffic.sSet()
		if wResTraffic['Result']!=True :
			wRes['Reason'] = "Set Traffic failed: reason=" + CLS_OSIF.sCatErr( wResTraffic )
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# ウェイト処理
#####################################################
	def Wait_Init( self, inZanNum=0, inWaitSec=gVal.DEF_STR_TLNUM['defWaitSec'], inZanCount=gVal.DEF_STR_TLNUM['defWaitCount'] ):
		gVal.STR_WaitInfo['zanNum']   = inZanNum
		gVal.STR_WaitInfo['zanCount'] = inZanCount
		gVal.STR_WaitInfo['setZanCount'] = inZanCount
		gVal.STR_WaitInfo['waitSec']  = inWaitSec
		gVal.STR_WaitInfo['Skip']     = False
		return True

	#####################################################
	def Wait_Next( self, inZanCountSkip=False ):
		#############################
		# カウントダウン
		gVal.STR_WaitInfo['zanNum']   -= 1
		if inZanCountSkip==False :
			gVal.STR_WaitInfo['zanCount'] -= 1
		
		###処理全て終わり
		if gVal.STR_WaitInfo['zanNum']<0 :
			return False	###全処理完了
		
		#############################
		# カウントチェック
		if gVal.STR_WaitInfo['zanCount']<0 :
			###カウントリセット
			gVal.STR_WaitInfo['zanCount'] = gVal.STR_WaitInfo['setZanCount']
			gVal.STR_WaitInfo['Skip']     = False	#ノーマル待機するので無効化
			
			#############################
			# 処理ウェイト(ノーマル)
			CLS_OSIF.sPrn( "CTRL+Cで中止することもできます。残り処理数= " + str( gVal.STR_WaitInfo['zanNum'] ) + " 個" + '\n' )
			wResStop = CLS_OSIF.sPrnWAIT( gVal.STR_WaitInfo['waitSec'] )
			if wResStop==False :
				CLS_OSIF.sPrn( "処理を中止しました。" + '\n' )
				return False	#ウェイト中止
			
			#############################
			# ついでに、15分周期処理
			w15Res = self.Circle15min()
			if w15Res['Result']!=True :
				###関数側でエラーを吐くので
				return False
		
		else:
			#############################
			# スキップ待機が設定されているか
			if gVal.STR_WaitInfo['Skip']==True :
				gVal.STR_WaitInfo['Skip'] = False
				#############################
				# 処理ウェイト(スキップ)
				CLS_OSIF.sPrn( "CTRL+Cで中止することもできます。残り処理数= " + str( gVal.STR_WaitInfo['zanNum'] ) + " 個" + '\n' )
				wResStop = CLS_OSIF.sPrnWAIT( gVal.DEF_STR_TLNUM['defWaitSkip'] )
				if wResStop==False :
					CLS_OSIF.sPrn( "処理を中止しました。" + '\n' )
					return False	#ウェイト中止
			else:
				if inZanCountSkip==False :
					CLS_OSIF.sSleep( gVal.DEF_STR_TLNUM['defWaitSkip'] )	#スリープ
		
		return True

	#####################################################
	def Wait_Skip(self):
		gVal.STR_WaitInfo['Skip'] = True	#次のNext起動時、スキップ待機をおこなう
		return True



#####################################################
# Twittter情報取得
#####################################################
	def GetTwitterInfo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "GetTwitterInfo"
		
		wRes['Responce'] = False
		
		gVal.VAL_AutoReFollowCnt = 0
		#############################
		# リスト登録ユーザ取得
		wSubRes = gVal.OBJ_Tw_IF.GetFollowListUser()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "GetFollowListUser is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 自動リストユーザ取得
		wSubRes = gVal.OBJ_Tw_IF.GetAutoListUser()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "GetAutoListUser is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# ふぁぼ一覧 取得
		wFavoRes = gVal.OBJ_Tw_IF.GetFavo()
		if wFavoRes['Result']!=True :
			wRes['Reason'] = "GetFavo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# フォロー情報取得
		wFavoRes = gVal.OBJ_Tw_IF.GetFollow()
		if wFavoRes['Result']!=True :
			wRes['Reason'] = "GetFollow is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### フォロー情報 取得
		wFollowerData = gVal.OBJ_Tw_IF.GetFollowerData()
		
		#############################
		# フォロー状態をDBに反映する
		CLS_MyDisp.sViewHeaderDisp( "フォロー情報の記録中" )
		
		wKeylist = list( wFollowerData.keys() )
		for wID in wKeylist :
			wID = str(wID)
			
			#############################
			# DBからいいね情報を取得する(1個)
			wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( wFollowerData[wID] )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "GetFavoDataOne is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			### DB未登録
			if wSubRes['Responce']['Data']==None :
				wRes['Reason'] = "GetFavoDataOne(3) is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wSubRes['Responce']['FLG_New']==None :
				#############################
				# 新規情報の設定
				wSubRes = self.SetNewFavoData( inUser, wSubRes['Responce']['Data'] )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "SetNewFavoData is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			wARR_DBData = wSubRes['Responce']['Data']
			
			wMyFollow = None
			wFollower = None
			wUserLevel = None
			#############################
			# 相互フォロー、片フォロワー
			# リストチェック
			#   非フォロワーなら解除
			if gVal.OBJ_Tw_IF.CheckSubscribeListUser( wID )==False :
				if wARR_DBData['level_tag']=="A" or wARR_DBData['level_tag']=="A+" or wARR_DBData['level_tag']=="B" or wARR_DBData['level_tag']=="B+" or \
			       wARR_DBData['level_tag']=="C" or wARR_DBData['level_tag']=="C+" or wARR_DBData['level_tag']=="D" or wARR_DBData['level_tag']=="D+" or \
			       wARR_DBData['level_tag']=="E" :
					
					if gVal.OBJ_Tw_IF.CheckMutualListUser( wID )==True and \
					   wFollowerData[wID]['myfollow']==False :
						### 相互リストなのにフォロー者ではない
						###   リストリムーブか、
						###   フォロワーなら片フォローリストへ
						wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_Remove( wFollowerData[wID] )
						
						if wFollowerData[wID]['follower']==True :
							### 片フォローリスト
							wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, "E" )
						else:
							### リスト解除（元フォロー者or相互フォロー）
							wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, "C-" )
					
					if gVal.OBJ_Tw_IF.CheckFollowListUser( wID )==True and \
					   wFollowerData[wID]['follower']==False :
						### 片フォローリストなのにフォロワーではない
						###   リストリムーブか、
						###   フォロワーなら片フォローリストへ
						wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_Remove( wFollowerData[wID] )
						
						if wFollowerData[wID]['myfollow']==True :
							### 片フォロー者
							wTwitterRes = gVal.OBJ_Tw_IF.MutualList_AddUser( wFollowerData[wID] )
							
							### 片フォローリスト
							wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, "D" )
						else:
							### リスト解除（元フォロワー）
							wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, "E-" )
				
				elif wARR_DBData['level_tag']=="G" :
					if gVal.OBJ_Tw_IF.CheckFollowListUser( wID )==False and \
					   wFollowerData[wID]['myfollow']==False and \
					   wFollowerData[wID]['follower']==True :
						### レベルG（放置予備ユーザ）はレベルG-へ
						wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, "G-" )
				
				elif wARR_DBData['level_tag']=="G-" or wARR_DBData['level_tag']=="E-" :
					if gVal.OBJ_Tw_IF.CheckMutualListUser( wID )==True or \
					   gVal.OBJ_Tw_IF.CheckFollowListUser( wID )==True :
						### レベルG-（放置確定ユーザ）、レベルE（被リムーブ）時
						###   でリスト解除してなければリスト解除
						wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_Remove( wFollowerData[wID] )
			
			wFLG_Force = False
			#############################
			# 公式化  →レベルAへ
###			if ( wARR_DBData['level_tag']=="D" or wARR_DBData['level_tag']=="C+" ) and \
###			   wFollowerData[wID]['myfollow']==True and \
###			   gVal.OBJ_Tw_IF.CheckSubscribeListUser( wID )==True :
###			if wFollowerData[wID]['myfollow']==True and \
###			   gVal.OBJ_Tw_IF.CheckSubscribeListUser( wID )==True :
			if wARR_DBData['level_tag']!="F"  and \
			   wFollowerData[wID]['myfollow']==True and \
			   gVal.OBJ_Tw_IF.CheckSubscribeListUser( wID )==True :
				if gVal.OBJ_Tw_IF.CheckMutualListUser( wID )==False and \
				   gVal.OBJ_Tw_IF.CheckFollowListUser( wID )==False :
					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, "A" )
			
			#############################
			# 相互フォロワー（リスト追加済）
			elif wARR_DBData['level_tag']=="A" and \
			   wFollowerData[wID]['myfollow']==True and \
			   gVal.OBJ_Tw_IF.CheckSubscribeListUser( wID )==False and \
			   gVal.OBJ_Tw_IF.CheckMutualListUser( wID )==True and \
			   gVal.OBJ_Tw_IF.CheckFollowListUser( wID )==False :
				
				if wFollowerData[wID]['follower']==True :
					### 相互
					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, "C" )
				else:
					### 片フォロー者
					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, "D+" )
			
			#############################
			# 片フォロワー（リスト追加済）
			elif wARR_DBData['level_tag']=="A" and \
			   wFollowerData[wID]['follower']==True and \
			   gVal.OBJ_Tw_IF.CheckSubscribeListUser( wID )==False and \
			   gVal.OBJ_Tw_IF.CheckMutualListUser( wID )==False and \
			   gVal.OBJ_Tw_IF.CheckFollowListUser( wID )==True :
				
				if wFollowerData[wID]['myfollow']==True :
					### 相互（このルートありえる？）
					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, "C" )
				else:
					### 片フォロワー
					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, "E" )
			
			#############################
			# レベル未設定の場合、やり直す
			elif wARR_DBData['level_tag']==gVal.DEF_NOTEXT :
				wMyFollow  = False
				wFollower  = False
				wFLG_Force = True
				
				### ユーザレベル =F
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, "F" )
				
				### フォロー状態の再設定
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Follower( wID, wMyFollow, wFollower )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "UpdateFavoData_Follower is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				### DBの再取得
				wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( wFollowerData[wID], inFLG_New=False )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "GetFavoDataOne is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				### DB未登録
				if wSubRes['Responce']['Data']==None or \
				   wSubRes['Responce']['FLG_New']==None :
					wRes['Reason'] = "GetFavoDataOne(3) is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				wARR_DBData = wSubRes['Responce']['Data']
				
				wStr = "◆フォロー状態の再設定(1)"
				### ユーザ記録
				gVal.OBJ_L.Log( "R", wRes, wStr + ": " + wFollowerData[wID]['screen_name'], inID=wID )
			
			#############################
			# リスト追加しそこねチェック
			#   相互フォローリスト
			if ( wARR_DBData['level_tag']=="B+" or wARR_DBData['level_tag']=="B" or \
			     wARR_DBData['level_tag']=="C+" or wARR_DBData['level_tag']=="C" or \
			     wARR_DBData['level_tag']=="D+" or wARR_DBData['level_tag']=="D" ) and \
			   gVal.OBJ_Tw_IF.CheckSubscribeListUser( wID )==False and \
			   gVal.OBJ_Tw_IF.CheckMutualListUser( wID )==False and \
			   wFollowerData[wID]['myfollow']==True :
				
				### 相互フォローリストに追加
				wTwitterRes = gVal.OBJ_Tw_IF.MutualList_AddUser( wFollowerData[wID] )
			
			#############################
			# リスト追加しそこねチェック
			#   片フォロワーリスト
			elif wARR_DBData['level_tag']=="E" and \
			     gVal.OBJ_Tw_IF.CheckSubscribeListUser( wID )==False and \
			     gVal.OBJ_Tw_IF.CheckFollowListUser( wID )==False and \
			     wFollowerData[wID]['myfollow']==False and \
			     wFollowerData[wID]['follower']==True :
				
				### 片フォロワーリストに追加
				wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_AddUser( wFollowerData[wID] )
			
			#############################
			# フォロー者チェック
			if wARR_DBData['myfollow']!=wFollowerData[wID]['myfollow'] :
				#############################
				# 〇フォロー者検出
###				if wFollowerData[wID]['myfollow']==True :
				if wARR_DBData['myfollow']==False and wFollowerData[wID]['myfollow']==True :
					if str(wARR_DBData['myfollow_date'])==gVal.DEF_TIMEDATE :
						wStr = "〇新規フォロー者"
					else:
						wStr = "△再度フォロー者"
					
					if wARR_DBData['level_tag']!="A+" and \
					   self.CheckVIPUser( wFollowerData[wID] )==True :
						### VIPのフォロー
						wUserLevel = "A+"
					elif gVal.OBJ_Tw_IF.CheckSubscribeListUser( wID )==True :
						### 公式垢などのフォロー
						wUserLevel = "A"
					else:
						if wFollowerData[wID]['follower']==True :
							### フォローして相互フォローになった
							wUserLevel = "C+"
						else:
							### 自発的フォロー者（まだ相互じゃない）
							wUserLevel = "D"
						
						### 相互フォローリストに追加
						wTwitterRes = gVal.OBJ_Tw_IF.MutualList_AddUser( wFollowerData[wID] )
						
						### ミュートする
						wMuteRes = gVal.OBJ_Tw_IF.Mute( wID )
						if wMuteRes['Result']!=True :
							wRes['Reason'] = "Mute is failed"
							gVal.OBJ_L.Log( "B", wRes )
					
					###過去の記録
					if wARR_DBData['level_tag']=="D-" :
						wStr = wStr + "(▲過去にリムった)"
					
					elif wARR_DBData['level_tag']=="Z" :
						wStr = wStr + "(▲過去被ブロック)"
					
					elif wARR_DBData['level_tag']=="G-" :
						wStr = wStr + "(▲過去追い出し)"
						
					elif wARR_DBData['level_tag']=="L" :
						wStr = wStr + "(▲過去リスト乞食)"
					
					### ユーザレベル変更
					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, wUserLevel )
					
					### トラヒック記録（フォロー者獲得）
					CLS_Traffic.sP( "p_myfollow" )
					
					### ユーザ記録
					gVal.OBJ_L.Log( "R", wRes, wStr + ": " + wFollowerData[wID]['screen_name'], inID=wID )
				
###				else:
				elif wARR_DBData['myfollow']==True and wFollowerData[wID]['myfollow']==False :
				#############################
				# 〇リムーブ者検出
					wStr = "●リムーブ者"
					if wARR_DBData['level_tag']!="A" and wARR_DBData['level_tag']!="A+" :
						### 公式垢以外
						if wFollowerData[wID]['follower']==True :
							### フォロワー（フォロー者OFF・フォロワーになった）
###							if wARR_DBData['level_tag']=="G" or wARR_DBData['level_tag']=="G+" :
###								wUserLevel = "H+"
###							else:
###								wUserLevel = "E"
							wUserLevel = "E"
							
							### 片フォロワーリストに追加
							wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_AddUser( wFollowerData[wID] )
						
						else:
							### 自発的リムーブ扱い（フォロー者・フォロワーともにOFF）
###							if wARR_DBData['level_tag']=="G" or wARR_DBData['level_tag']=="G+" or \
###							   wARR_DBData['level_tag']=="H" or wARR_DBData['level_tag']=="H+" :
###								wUserLevel = "H-"
###							else:
###								wUserLevel = "D-"
							wUserLevel = "D-"
							
							### リストリムーブ
							wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_Remove( wFollowerData[wID] )
						
						### ユーザレベル変更
						wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, wUserLevel )
					
					### トラヒック記録（フォロー者減少）
					CLS_Traffic.sP( "d_myfollow" )
					
					### ユーザ記録
###					gVal.OBJ_L.Log( "R", wRes, wStr + ": " + wFollowerData[wID]['screen_name'], inID=wID )
					wStr = wStr + ": " + wFollowerData[wID]['screen_name']
					wStr = wStr + ": level=" + wUserLevel + ": send=" + str(wARR_DBData['pfavo_cnt']) + " recv=" + str(wARR_DBData['rfavo_cnt'])
					gVal.OBJ_L.Log( "R", wRes, wStr, inID=wID )
				
				wMyFollow = wFollowerData[wID]['myfollow']
			
			#############################
			# フォロワーチェック
			if wARR_DBData['follower']!=wFollowerData[wID]['follower'] :
				#############################
				# 〇フォロワー検出
###				if wFollowerData[wID]['follower']==True :
				if wARR_DBData['follower']==False and wFollowerData[wID]['follower']==True :
					#############################
					# ユーザ情報の確認
					# 次のユーザはブロック→リムーブする
					# ・ユーザレベル=A or A+以外
					# ・片フォロワー（フォロー者OFF）
					# ・ツイート数=0 もしくは 鍵アカウント
					# ・最終ツイートが一定期間過ぎてるか
					wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inScreenName=wFollowerData[wID]['screen_name'] )
					if wUserInfoRes['Result']!=True :
						wRes['Reason'] = "Twitter API Error(GetUserinfo): " + wUserInfoRes['Reason'] + " screen_name=" + wFollowerData[wID]['screen_name']
						gVal.OBJ_L.Log( "B", wRes )
						continue
					
					wFLG_RemDetect = False
					wStr = "●追い出し"
					if wARR_DBData['level_tag']=="A" or wARR_DBData['level_tag']=="A+" or wUserLevel=="A" or wUserLevel=="A+" :
						wStr = wStr + "（ユーザレベルA）"
						wFLG_RemDetect = False
					
					elif wARR_DBData['level_tag']=="G-" or wUserLevel=="G-" :
						if wARR_DBData['rfavo_cnt']<gVal.DEF_STR_TLNUM['forReFollowerPastRfavoCnt'] :
							wStr = wStr + "（ユーザレベルG-でリアクション少ない）"
							wFLG_RemDetect = True
					
###					elif wFollowerData[wID]['myfollow']==False and \
###					   wARR_DBData['level_tag']!="A" and wARR_DBData['level_tag']!="A+" and wUserLevel!="A" and \
###					   ( wUserInfoRes['Responce']['statuses_count']==0 or \
###					     wUserInfoRes['Responce']['protected']==True ) :
###							wFLG_RemDetect = True
					elif wFollowerData[wID]['myfollow']==False and \
					   wARR_DBData['level_tag']!="A" and wARR_DBData['level_tag']!="A+" and wUserLevel!="A" :
						
						if wUserInfoRes['Responce']['statuses_count']==0 :
							###対象
							wStr = wStr + "（ツイートなし）"
							wFLG_RemDetect = True
						
						elif wUserInfoRes['Responce']['protected']==True :
							###対象
							wStr = wStr + "（鍵垢アカウント）"
							wFLG_RemDetect = True
					
					else:
						###最終ツイート日時が規定日を超えているか
						wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="user", inFLG_Rep=False, inFLG_Rts=True,
							 inID=wID, inCount=1 )
						if wTweetRes['Result']!=True :
							wRes['Reason'] = "Twitter Error: GetTL"
							gVal.OBJ_L.Log( "B", wRes )
							continue
						
						###日時の変換をして、設定
						wTime = CLS_TIME.sTTchg( wRes, "(1)", wTweetRes['Responce'][0]['created_at'] )
						if wTime['Result']!=True :
							continue
						
						wGetLag = CLS_OSIF.sTimeLag( str( wTime['TimeDate'] ), inThreshold=gVal.DEF_STR_TLNUM['forAutoUserRemoveSec'] )
						if wGetLag['Result']!=True :
							wRes['Reason'] = "sTimeLag failed"
							gVal.OBJ_L.Log( "B", wRes )
							continue
						if wGetLag['Beyond']==True :
							### 規定外 =許容外の日数なので対象
							wStr = wStr + "（最終ツイートが古すぎる）"
							wFLG_RemDetect = True
					
					if wFLG_RemDetect==True :
						#############################
						# ブロック→リムーブする
						wBlockRes = gVal.OBJ_Tw_IF.BlockRemove( wID )
						if wBlockRes['Result']!=True :
							wRes['Reason'] = "Twitter API Error(BlockRemove): " + wBlockRes['Reason'] + " screen_name=" +wFollowerData[wID]['screen_name']
							gVal.OBJ_L.Log( "B", wRes )
							continue
						
						### ユーザレベル変更
###						wUserLevel = "Z-"
						wUserLevel = "G-"
						wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, wUserLevel )
						
						### トラヒック記録（フォロワー減少）
						CLS_Traffic.sP( "d_follower" )
						
						### ユーザ記録
###						wStr = "●追い出し"
						gVal.OBJ_L.Log( "R", wRes, wStr + ": " + wFollowerData[wID]['screen_name'], inID=wID )
					
					else:
						wFollower   = True
						wUserLevel2 = None
						if str(wARR_DBData['follower_date'])==gVal.DEF_TIMEDATE :
							wStr = "〇新規フォロワー"
						else:
###							wStr = "△再フォローされた"
							wStr = "△再度フォロワー"
						
						#############################
						# VIPのフォロワー
						if wARR_DBData['level_tag']!="A+" and wUserLevel!="A+" and \
						   self.CheckVIPUser( wFollowerData[wID] )==True :
###							### VIPのフォロワー
							wUserLevel = "A+"
							
							wStr = wStr + "(VIP)"
							### ユーザレベル変更
							wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, wUserLevel )
						
						#############################
						# 相互フォロー  フォロー者=ON・フォロワーOFF → ON
						elif ( wARR_DBData['level_tag']=="D"  or wUserLevel=="D"  or \
						       wARR_DBData['level_tag']=="D+" or wUserLevel=="D+" ) and \
						     wFollowerData[wID]['myfollow']==True :
							wUserLevel2 = "C+"
							
							wStr = wStr + "(相互化)"
							### 相互フォローリストに追加
							wTwitterRes = gVal.OBJ_Tw_IF.MutualList_AddUser( wFollowerData[wID] )
						
						#############################
						# 新規フォロワー  並びに自動フォロー
						#   フォロー者=OFF → ON・フォロワーOFF → ON
						elif wARR_DBData['level_tag']=="F" :
							### 自動フォロー
###							wSubRes = self.OBJ_TwitterFollower.AutoFollow( wFollowerData[wID], wFLG_Force )
							wSubRes = self.OBJ_TwitterFollower.AutoFollow( wFollowerData[wID]['id'], wFLG_Force )
							if wSubRes['Result']!=True :
								wRes['Reason'] = "AutoFollow is failed"
								gVal.OBJ_L.Log( "B", wRes )
								continue
							if wSubRes['Responce']==True :
								### 自動フォロー成功 フォロー者ON・フォローON
								wUserLevel2 = "C+"
								
								wStr = wStr + "(+自動フォロー)"
								### 相互フォローリストに追加
								wTwitterRes = gVal.OBJ_Tw_IF.MutualList_AddUser( wFollowerData[wID] )
							else:
								### 自動フォロー失敗 フォロー者OFF・フォローON
								wUserLevel2 = "E"
								### 片フォロワーリストに追加
								wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_AddUser( wFollowerData[wID] )
						
						#############################
						# 相互中にリムーブされて、またフォローされた
						#   フォロー者=ON・フォロワーOFF → ON
						elif wARR_DBData['level_tag']=="C-" :
							wUserLevel2 = "C+"
							wStr = wStr + "(再相互)"
						
						#############################
						# 過去にトラブルがあったため、放置する
						#   フォロー者=OFF・フォロワーOFF → ON
						elif wARR_DBData['level_tag']=="D-" :
							wStr = wStr + "(●過去にリムった)"
						
						elif wARR_DBData['level_tag']=="Z" :
							wStr = wStr + "(●過去被ブロック)"
						
						#############################
						# その他
						#   フォロー者=OFF・フォロワーOFF → ON
						else:
							wUserLevel2 = "E"
							
							if wARR_DBData['level_tag']=="G-" :
								wStr = wStr + "(過去追い出し)"
							elif wARR_DBData['level_tag']=="L" :
								wStr = wStr + "(過去リスト乞食)"
							
							### 片フォロワーリストに追加
							wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_AddUser( wFollowerData[wID] )
						
						#############################
						# レベル変更＋トラヒック記録
						### トラヒック記録（フォロワー獲得）
						CLS_Traffic.sP( "p_follower" )
						
						if wUserLevel2!=None :
							### ユーザレベル変更
							wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, wUserLevel2 )
							### ユーザ記録
							gVal.OBJ_L.Log( "R", wRes, wStr + ": " + wFollowerData[wID]['screen_name'], inID=wID )
						
				elif wARR_DBData['follower']==True and wFollowerData[wID]['follower']==False :
				#############################
				# 〇被リムーブ検出
					wFollower = False
					if wARR_DBData['level_tag']!="A" and wARR_DBData['level_tag']!="A+" and wUserLevel!="A" and wUserLevel!="A+" :
						if wFollowerData[wID]['myfollow']==True :
							### フォロー者（相互フォロー中、フォロー者ON・フォロワーOFFになった）
							#############################
							# 即自動リムーブする
							wSubRes = self.OBJ_TwitterFollower.AutoRemove( wFollowerData[wID], inFLG_Force=True )
							if wSubRes['Result']!=True :
								wRes['Reason'] = "AutoRemove is failed"
								gVal.OBJ_L.Log( "B", wRes )
								return wRes
							if wSubRes['Responce']==False :
								### 自動リムーブしてない（フォロー者ON・フォロワーOFF）
								
###								### ユーザレベル変更
###								wUserLevel2 = "C-"
###								
								wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, wUserLevel2 )
								
								### ユーザ記録
								wStr = "●リムーブされた(フォロー者ON)"
###								wStr = wStr + ": " + wFollowerData[wID]['screen_name']
###								wStr = wStr + ": level=" + wUserLevel2 + ": send=" + str(wARR_DBData['pfavo_cnt']) + " recv=" + str(wARR_DBData['rfavo_cnt'])
###								gVal.OBJ_L.Log( "R", wRes, wStr, inID=wID )
###							
							else:
								wStr = "●リムーブされた(相互リムーブ)"
							
							### ユーザレベル変更
							wUserLevel2 = "C-"
							
							wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, wUserLevel2 )
							
							### ユーザ記録
							wStr = wStr + ": " + wFollowerData[wID]['screen_name']
							wStr = wStr + ": level=" + wUserLevel2 + ": send=" + str(wARR_DBData['pfavo_cnt']) + " recv=" + str(wARR_DBData['rfavo_cnt'])
							gVal.OBJ_L.Log( "R", wRes, wStr, inID=wID )
						
						else:
							### リストリムーブ
							wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_Remove( wFollowerData[wID] )
							
							### ユーザレベル変更
							if wARR_DBData['level_tag']=="G" :
								### 完全スルーユーザからのリムーブは追い出し扱い
								wUserLevel2 = "G-"
								wStr = "●スルーユーザからのリムーブ"
							else:
								if wARR_DBData['level_tag']!="G-" :
									wUserLevel2 = "E-"
								wStr = "●リムーブされた"
							
							if wUserLevel2!=None :
								wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, wUserLevel2 )
								
								### ユーザ記録
								wStr = wStr + ": " + wFollowerData[wID]['screen_name']
								wStr = wStr + ": level=" + wUserLevel2 + ": send=" + str(wARR_DBData['pfavo_cnt']) + " recv=" + str(wARR_DBData['rfavo_cnt'])
								gVal.OBJ_L.Log( "R", wRes, wStr, inID=wID )
						
						#############################
						# 代わりにフォロー一覧から再フォロー
						wSubRes = self.OBJ_TwitterFollower.AutoReFollow( wID )
						if wSubRes['Result']!=True :
							wRes['Reason'] = "AutoReFollow is failed"
							gVal.OBJ_L.Log( "B", wRes )
					
					### トラヒック記録（フォロワー減少）
					CLS_Traffic.sP( "d_follower" )
			
			#############################
			# 変更ありの場合
			#   DBへ反映
			if wMyFollow!=None or wFollower!=None :
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Follower( wID, wMyFollow, wFollower )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "UpdateFavoData_Follower is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				wRes['Responce'] = True
		
		#############################
		# リムーブ もしくは ブロックでTwitterから完全リムーブされたか
		#   DB上フォロー者 もしくは フォロワーを抽出
		wARR_RateFavoDate = {}
		wSubRes = gVal.OBJ_DB_IF.GetFavoData()
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetFavoData is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		wARR_RateFavoDate = wSubRes['Responce']
		
		wKeylist = list( wARR_RateFavoDate.keys() )
		for wID in wKeylist :
			wUserID = str(wID)
			
			#############################
			# Twitterでフォロー者 もしくは フォロワーの場合
			# スキップ
			if wUserID in wFollowerData :
				continue
			
			# ※Twitterでリムーブした リムーブされた ブロックされた
			#   でTwitterからアンフォロー（=情報がなくなった）
			#   かつ DBではフォロー者 フォロワーの場合
			
			wMyFollow = None
			wFollower = None
			wBlockBy  = False
			if wARR_RateFavoDate[wUserID]['level_tag']!="Z" :
				### G以外はブロックチェック
				
				#############################
				# ブロックチェック
				wFollowInfoRes = gVal.OBJ_Tw_IF.GetFollowInfo( wUserID )
				if wFollowInfoRes['Result']!=True :
					if str(wFollowInfoRes['Responce'])=="404" :
						### Twitterに存在しないため削除する
						wQuery = "delete from tbl_favouser_data " + \
									"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
									" and id = '" + str(wUserID) + "' ;"
						
						wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
						if wResDB['Result']!=True :
							wRes['Reason'] = "Run Query is failed"
							gVal.OBJ_L.Log( "B", wRes )
						
						wStr = "●Twitterに存在しないユーザのため削除"
						continue
					else:
						wStr = "GetFollowInfo is failed: screen_name=" + wARR_RateFavoDate[wUserID]['screen_name']
						wStr = wStr + " status_code=" + str(wFollowInfoRes['Responce'])
						wRes['Reason'] = wStr
						gVal.OBJ_L.Log( "B", wRes )
						continue
				if wFollowInfoRes['Responce']['blocked_by']==True :
					### 被ブロック検知
					wBlockBy = True
					
					### 通信記録
					wStr = "●被ブロック検知"
					gVal.OBJ_L.Log( "R", wRes, wStr + ": " + wARR_RateFavoDate[wUserID]['screen_name'], inID=wUserID )
					
					### ユーザレベル変更
					wUserLevel = "Z"
					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wUserID, wUserLevel )
					
					### トラヒック記録
					if wARR_RateFavoDate[wUserID]['myfollow']==True :
						wMyFollow = True
						CLS_Traffic.sP( "d_myfollow" )
					
					if wARR_RateFavoDate[wUserID]['myfollow']==True :
						wFollower = True
						CLS_Traffic.sP( "follower" )
					
					### ブロック検知の送信
					self.SendBeenBlock( wARR_RateFavoDate[wUserID] )
			
			else:
				### Gは被ブロック済み
				wBlockBy  = True
			
			#############################
			# 〇リムーブ者検出
			if wARR_RateFavoDate[wUserID]['myfollow']==True and wBlockBy==False :
				wMyFollow = False
				
				#############################
				# 〇リムーブ者＆被リムーブ検出
				if wARR_RateFavoDate[wUserID]['follower']==True :
					wFollower = False
					
					### 通信記録（フォロー者ON・フォロワーONから、フォロー者・フォロワーOFFへ）
					wStr = "●リムーブ者・リムーブされた（同時検出）"
					
					### トラヒック記録
					CLS_Traffic.sP( "d_follower" )
				
				else:
					### 通信記録（片フォロー者・フォロワーOFFから、フォロー者・フォロワーOFFへ）
					wStr = "●リムーブ者"
				
				### リストリムーブ
				wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_Remove( wARR_RateFavoDate[wUserID] )
				
				### ユーザレベル変更
				wUserLevel = "E-"
				
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wUserID, wUserLevel )
				
				### 通信記録
				wStr = wStr + ": " + wARR_RateFavoDate[wUserID]['screen_name']
				wStr = wStr + ": level=" + wUserLevel + ": send=" + str(wARR_RateFavoDate[wUserID]['pfavo_cnt']) + " recv=" + str(wARR_RateFavoDate[wUserID]['rfavo_cnt'])
				gVal.OBJ_L.Log( "R", wRes, wStr, inID=wID )
				
				### トラヒック記録
				CLS_Traffic.sP( "d_myfollow" )
				
			
			#############################
			# 〇被リムーブ検出
			if wARR_RateFavoDate[wUserID]['follower']==True and wBlockBy==False and \
			   wARR_RateFavoDate[wUserID]['myfollow']==False :
				wFollower = False
				
				### リストリムーブ
				wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_Remove( wARR_RateFavoDate[wUserID] )
				
				wUserLevel = None
				### ユーザレベル変更
				if wARR_RateFavoDate[wUserID]['level_tag']=="G" :
					### 完全スルーユーザからのリムーブは追い出し扱い
					wUserLevel = "G-"
					wStr = "●スルーユーザからのリムーブ"
				else:
					if wARR_RateFavoDate[wUserID]['level_tag']!="G-" :
						wUserLevel = "E-"
					wStr = "●リムーブされた"
				
				if wUserLevel!=None :
					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wUserID, wUserLevel )
					
				### 通信記録（フォロー者OFF・フォロワーから、フォロー者・フォロワーOFFへ）
				wStr = wStr + ": " + wARR_RateFavoDate[wUserID]['screen_name']
###				wStr = wStr + ": level=" + wUserLevel + ": send=" + str(wARR_RateFavoDate[wUserID]['pfavo_cnt']) + " recv=" + str(wARR_RateFavoDate[wUserID]['rfavo_cnt'])
				if wUserLevel!=None :
					wStr = wStr + ": level=" + str(wUserLevel)
				wStr = wStr + " send=" + str(wARR_RateFavoDate[wUserID]['pfavo_cnt'])
				wStr = wStr + " recv=" + str(wARR_RateFavoDate[wUserID]['rfavo_cnt'])
				gVal.OBJ_L.Log( "R", wRes, wStr, inID=wID )
				
				### トラヒック記録
				CLS_Traffic.sP( "d_follower" )
				
				#############################
				# 代わりにフォロー一覧から再フォロー
				wSubRes = self.OBJ_TwitterFollower.AutoReFollow( wUserID )
				if wSubRes['Result']!=True :
					wRes['Reason'] = "AutoReFollow is failed"
					gVal.OBJ_L.Log( "B", wRes )
			
			#############################
			# 変更ありの場合
			#   DBへ反映する
			if wMyFollow!=None or wFollower!=None :
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Follower( wUserID, wMyFollow, wFollower )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "UpdateFavoData_Follower is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# 自動監視
#####################################################
	def AllRun(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "AllRun"
		
		wFLG_Short = False
		#############################
		# フル自動監視 期間内か
		wGetLag = CLS_OSIF.sTimeLag( str( gVal.STR_Time['autorun'] ), inThreshold=gVal.DEF_STR_TLNUM['forAutoAllRunSec'] )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wGetLag['Beyond']==False :
			### 規定以内= ショート処理
			wStr = "●ショート監視実行: 次回のフル監視日時= " + str(wGetLag['RateTime']) + '\n'
			CLS_OSIF.sPrn( wStr )
			wFLG_Short = True
		else:
			### 自動監視シーケンスリセットなら
			### リセットする
			wGetLag = CLS_OSIF.sTimeLag( str( gVal.STR_Time['autoseq'] ), inThreshold=gVal.DEF_STR_TLNUM['forAutoSeqSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed(autoseq)"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==True :
				### 規定外= リセット
				wSubRes = gVal.OBJ_DB_IF.SetAutoSeq( True )
				if wSubRes['Result']!=True :
					wRes['Reason'] = "SetAutoSeq is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				#############################
				# 自動監視シーケンスリセット時間に 現時間を設定
				wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "autoseq", gVal.STR_Time['TimeDate'] )
				if wTimeRes['Result']!=True :
					wRes['Reason'] = "SetTimeInfo is failed(autoseq)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			wStr = "〇フル監視実行" + '\n'
			CLS_OSIF.sPrn( wStr )
		
		#############################
		# Twitter情報取得
		wFavoRes = self.GetTwitterInfo()
		if wFavoRes['Result']!=True :
			wRes['Reason'] = "GetTwitterInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 自動監視シーケンス取得
		wSubRes = gVal.OBJ_DB_IF.GetAutoSeq()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "GetAutoSeq is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		while True :
			#############################
			# Twitter再接続
			wTwitterRes = gVal.OBJ_Tw_IF.ReConnect()
			if wTwitterRes['Result']!=True :
				wRes['Reason'] = "Twitterの再接続失敗"
				gVal.OBJ_L.Log( "A", wRes )
				return wRes
			
			#############################
			# 禁止ユーザ自動削除（●フル自動監視）
			if gVal.STR_UserInfo['AutoSeq']==0 :
				if wFLG_Short==False :
					wSubRes = self.OBJ_TwitterAdmin.ExcuteUser_AutoDelete()
					if wSubRes['Result']!=True :
						###失敗
						wRes['Reason'] = "ExcuteUser_AutoDelete is failed"
						gVal.OBJ_L.Log( "B", wRes )
						return wRes
			
			#############################
			# ユーザ自動削除（●フル自動監視）
			elif gVal.STR_UserInfo['AutoSeq']==1 :
				if wFLG_Short==False :
					wSubRes = self.OBJ_TwitterAdmin.RunAutoUserRemove()
					if wSubRes['Result']!=True :
						###失敗
						wRes['Reason'] = "RunAutoUserRemove is failed"
						gVal.OBJ_L.Log( "B", wRes )
						return wRes
			
			#############################
			# いいね解除（●フル自動監視）
			elif gVal.STR_UserInfo['AutoSeq']==2 :
				if wFLG_Short==False :
					wSubRes = self.OBJ_TwitterFavo.RemFavo()
					if wSubRes['Result']!=True :
						wRes['Reason'] = "RemFavo"
						gVal.OBJ_L.Log( "B", wRes )
						return wRes
			
			#############################
			# リスト通知 リストとユーザの更新
			elif gVal.STR_UserInfo['AutoSeq']==3 :
				wSubRes = self.UpdateListIndUser()
				if wSubRes['Result']!=True :
					wRes['Reason'] = "UpdateListIndUser error"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			#############################
			# リスト登録ユーザチェック
			elif gVal.STR_UserInfo['AutoSeq']==4 :
				wSubRes = self.CheckListUsers()
				if wSubRes['Result']!=True :
					wRes['Reason'] = "CheckListUsers error"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
###			#############################
###			# 自動リムーブチェック
###			elif gVal.STR_UserInfo['AutoSeq']==5 :
###				wSubRes = self.CheckAutoRemove()
###				if wSubRes['Result']!=True :
###					wRes['Reason'] = "CheckAutoRemove error"
###					gVal.OBJ_L.Log( "B", wRes )
###					return wRes
###			
###			#############################
###			# タイムラインフォロー
###			elif gVal.STR_UserInfo['AutoSeq']==6 :
###				wSubRes = self.OBJ_TwitterFollower.TimelineFollow()
###				if wSubRes['Result']!=True :
###					wRes['Reason'] = "TimelineFollow error"
###					gVal.OBJ_L.Log( "B", wRes )
###					return wRes
###			
			#############################
			# リアクションチェック
###			elif gVal.STR_UserInfo['AutoSeq']==7 :
			elif gVal.STR_UserInfo['AutoSeq']==5 :
###				wSubRes = self.OBJ_TwitterFollower.ReactionCheck( inFLG_Short=wFLG_Short )
###				wSubRes = self.OBJ_TwitterReaction.ReactionCheck( inFLG_Short=wFLG_Short )
				wSubRes = self.OBJ_TwitterReaction.ReactionCheck( inFLG_Short=False )
				if wSubRes['Result']!=True :
					wRes['Reason'] = "ReactionCheck"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			#############################
			# VIPリアクション監視チェック
###			elif gVal.STR_UserInfo['AutoSeq']==8 :
			elif gVal.STR_UserInfo['AutoSeq']==6 :
###				wSubRes = self.OBJ_TwitterFollower.VIP_ReactionCheck()
				wSubRes = self.OBJ_TwitterReaction.VIP_ReactionCheck()
				if wSubRes['Result']!=True :
					wRes['Reason'] = "VIP_ReactionCheck is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			#############################
			# 自動リムーブチェック
			elif gVal.STR_UserInfo['AutoSeq']==7 :
				wSubRes = self.CheckAutoRemove()
				if wSubRes['Result']!=True :
					wRes['Reason'] = "CheckAutoRemove error"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			#############################
			# タイムラインフォロー
			elif gVal.STR_UserInfo['AutoSeq']==8 :
				wSubRes = self.OBJ_TwitterFollower.TimelineFollow()
				if wSubRes['Result']!=True :
					wRes['Reason'] = "TimelineFollow error"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			#############################
			# フォロワー支援
			elif gVal.STR_UserInfo['AutoSeq']==9 :
				wSubRes = self.OBJ_TwitterFavo.FollowerFavo()
				if wSubRes['Result']!=True :
					wRes['Reason'] = "FollowerFavo"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			#############################
			# リストいいね（●フル自動監視）
			elif gVal.STR_UserInfo['AutoSeq']==10 :
				if wFLG_Short==False :
					wSubRes = self.OBJ_TwitterFavo.ListFavo()
					if wSubRes['Result']!=True :
						wRes['Reason'] = "ListFavo"
						gVal.OBJ_L.Log( "B", wRes )
						return wRes
			
			#############################
			# いいね情報送信
			elif gVal.STR_UserInfo['AutoSeq']==11 :
				wSubRes = self.OBJ_TwitterFollower.SendFavoDate()
				if wSubRes['Result']!=True :
					wRes['Reason'] = "SendFavoDate"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			#############################
			# 検索ワード実行（●フル自動監視）
			elif gVal.STR_UserInfo['AutoSeq']==12 :
				if wFLG_Short==False :
###					wSubRes = self.OBJ_TwitterKeyword.RunKeywordSearchFavo()
					wSubRes = self.OBJ_TwitterKeyword.Auto_RunKeywordSearchFavo()
					if wSubRes['Result']!=True :
###						wRes['Reason'] = "RunKeywordSearchFavo"
						wRes['Reason'] = "Auto_RunKeywordSearchFavo is failed"
						gVal.OBJ_L.Log( "B", wRes )
						return wRes
			
			#############################
			# 警告ツイートの削除（●フル自動監視）
			elif gVal.STR_UserInfo['AutoSeq']==13 :
				if wFLG_Short==False :
					wSubRes = self.OBJ_TwitterAdmin.RemoveCautionUser( inFLR_Recheck=True )
					if wSubRes['Result']!=True :
						###失敗
						wRes['Reason'] = "RemoveCautionUser is failed"
						gVal.OBJ_L.Log( "B", wRes )
						return wRes
			
#			#############################
#			# トレンドツイート
###			elif gVal.STR_UserInfo['AutoSeq']==5 :
#				wSubRes = self.OBJ_TwitterKeyword.TrendTweet()
#				if wSubRes['Result']!=True :
#					###失敗
#					wRes['Reason'] = "TrendTweet is failed"
#					gVal.OBJ_L.Log( "B", wRes )
#					return wRes
#			
			#############################
			# 古いいいね情報の削除（●フル自動監視）
			elif gVal.STR_UserInfo['AutoSeq']==14 :
				if wFLG_Short==False :
					wSubRes = gVal.OBJ_DB_IF.DeleteFavoData()
					if wSubRes['Result']!=True :
						###失敗
						wRes['Reason'] = "DeleteFavoData is failed"
						gVal.OBJ_L.Log( "B", wRes )
						return wRes
			
			#############################
			# 削除ツイート
			elif gVal.STR_UserInfo['AutoSeq']==15 :
				wSubRes = self.OBJ_TwitterKeyword.DelTweet()
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "DelTweet is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			#############################
			# ミュート解除(できるだけ)（●フル自動監視）
			elif gVal.STR_UserInfo['AutoSeq']==16 :
				if wFLG_Short==False :
					wSubRes = self.AllMuteRemove()
					if wSubRes['Result']!=True :
						###失敗
						wRes['Reason'] = "AllMuteRemove is failed"
						gVal.OBJ_L.Log( "B", wRes )
						return wRes
			
			#############################
			# VIPフォロー監視（●フル自動監視）
			elif gVal.STR_UserInfo['AutoSeq']==17 :
				if wFLG_Short==False :
					wSubRes = self.CheckVipFollow()
					if wSubRes['Result']!=True :
						###失敗
						wRes['Reason'] = "CheckVipFollow is failed"
						gVal.OBJ_L.Log( "B", wRes )
						return wRes
			
			#############################
			# 指定外のため、リセット
			# あるいは 終了
			else:
				wSeq = None
###				if gVal.STR_UserInfo['AutoSeq']!=17 :
				if gVal.STR_UserInfo['AutoSeq']!=18 :
					wSeq = gVal.STR_UserInfo['AutoSeq']		###異常検出
				
				wSubRes = gVal.OBJ_DB_IF.SetAutoSeq( True )
				if wSubRes['Result']!=True :
					wRes['Reason'] = "SetAutoSeq is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				elif wSeq==None :
					break	###正常終了
				
				else :
					### 指定外 ログ出して終わる
					wRes['Reason'] = "SetAutoSeq number is error seq=" + str( wSeq )
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			#############################
			# 自動監視シーケンス設定
			wSubRes = gVal.OBJ_DB_IF.SetAutoSeq()
			if wSubRes['Result']!=True :
				wRes['Reason'] = "SetAutoSeq is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			### スリープ時間
			CLS_OSIF.sSleep( gVal.DEF_STR_TLNUM['forAutoSeqSecSleep'] )
		
		#############################
		# 自動監視時間に 現時間を設定
		if wFLG_Short==False :
			wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "autorun", gVal.STR_Time['TimeDate'] )
			if wTimeRes['Result']!=True :
				wRes['Reason'] = "SetTimeInfo is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# 自動監視シーケンスリセット時間に 現時間を設定
		wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "autoseq", gVal.STR_Time['TimeDate'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "SetTimeInfo is failed(autoseq)"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
###		#############################
###		# メンション結果
###		self.OBJ_TwitterFollower.ReactionResult()
###		self.OBJ_TwitterReaction.ReactionResult()
###		
		#############################
		# 連ファボ測定
		self.OBJ_TwitterReaction.CheckRenFavo()
		
		#############################
		# スケジュール表示
		wSubRes = self.OBJ_TwitterAdmin.View_Schedule()
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "View_Schedule is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 被登録リストの表示
		wSubRes = self.View_SubsList()
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "View_SubsList is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# ユーザ管理
#####################################################
	def UserAdmin(self):
		
		#############################
		# Twitter情報取得
		wFavoRes = self.GetTwitterInfo()
		if wFavoRes['Result']!=True :
			gVal.OBJ_L.Log( "B", wFavoRes )
			return wFavoRes
		
		wRes = self.OBJ_TwitterAdmin.UserAdmin()
		return wRes



#####################################################
# 警告ユーザ管理
#####################################################
	def AdminCautionUser(self):
		wRes = self.OBJ_TwitterAdmin.AdminCautionUser()
		return wRes



#####################################################
# 非絡みユーザ一覧
#####################################################
###	def UserBList(self):
###		
###		#############################
###		# Twitter情報取得
###		wFavoRes = self.GetTwitterInfo()
###		if wFavoRes['Result']!=True :
###			gVal.OBJ_L.Log( "B", wFavoRes )
###			return wFavoRes
###		
###		wRes = self.OBJ_TwitterAdmin.UserBList()
###		return wRes
###
###



#####################################################
# VIPフォロー監視
#####################################################
	def ManualCheckVipFollow(self):
		wRes = self.CheckVipFollow()
		return wRes



#####################################################
# 被ブロックユーザ一覧
#####################################################
	def BlockList(self):
		
		wRes = self.OBJ_TwitterAdmin.BlockList()
		return wRes



#####################################################
# 相互いいね停止
#####################################################
	def SetMfvStop(self):
		wRes = self.OBJ_TwitterAdmin.SetMfvStop()
		return wRes



#####################################################
# トレンドタグ設定
#####################################################
	def SetTrendTag(self):
		wRes = self.OBJ_TwitterAdmin.SetTrendTag()
		return wRes



#####################################################
# 質問タグ設定
#####################################################
	def SetQuestionTag(self):
		wRes = self.OBJ_TwitterAdmin.SetQuestionTag()
		return wRes



#####################################################
# VIPタグ設定
#####################################################
	def SetVipTag(self):
		wRes = self.OBJ_TwitterAdmin.SetVipTag()
		return wRes



#####################################################
# 削除タグ設定
#####################################################
	def SetDelTag(self):
		wRes = self.OBJ_TwitterAdmin.SetDelTag()
		return wRes



#####################################################
# リスト通知設定
#####################################################
	def SetListName(self):
		wRes = self.OBJ_TwitterAdmin.SetListName()
		return wRes



#####################################################
# 自動リムーブ設定
#####################################################
	def SetAutoRemove(self):
		wRes = self.OBJ_TwitterAdmin.SetAutoRemove()
		return wRes



#####################################################
# 禁止ユーザ
#####################################################
	def ExcuteUser(self):
		wRes = self.OBJ_TwitterAdmin.ExcuteUser()
		return wRes



#####################################################
# 時間リセット
#####################################################
	def ResetTimeInfo(self):
		wRes = self.OBJ_TwitterAdmin.ResetTimeInfo()
		return wRes



#####################################################
# いいね全解除
#####################################################
	def AllFavoRemove(self):
		wRes = self.OBJ_TwitterFavo.RemFavo( inFLG_All=True )
		return wRes



#####################################################
# 強制自動リムーブ
#####################################################
	def ForceCheckAutoRemove(self):
		#############################
		# Twitter情報取得
		wFavoRes = self.GetTwitterInfo()
		if wFavoRes['Result']!=True :
###			wRes['Reason'] = "GetTwitterInfo is failed"
			gVal.OBJ_L.Log( "B", wFavoRes )
			return wFavoRes
		
		#############################
		# 自動リムーブ
		wSubRes = self.CheckAutoRemove( inFLG_Force=True )
		if wSubRes['Result']!=True :
###			wRes['Reason'] = "CheckAutoRemove"
			gVal.OBJ_L.Log( "B", wSubRes )
#			return wSubRes
		
		return wSubRes



#####################################################
# 強制いいね情報送信
#####################################################
	def ForceSendFavoDate(self):
		#############################
		# いいね情報送信
		wSubRes = self.OBJ_TwitterFollower.SendFavoDate( inFLG_Force=True )
		if wSubRes['Result']!=True :
###			wRes['Reason'] = "SendFavoDate"
			gVal.OBJ_L.Log( "B", wSubRes )
#			return wSubRes
		
		return wSubRes



#####################################################
# タイムラインフォロー
#####################################################
	def TimelineFollow(self):
###		wRes = self.OBJ_TwitterFollower.TimelineFollow()
		wRes = self.OBJ_TwitterFollower.TimelineFollow( inCheck=False )
		wRes['Result'] = True
		return wRes



#####################################################
# トレンドツイート
#####################################################
	def TrendTweet(self):
		wRes = self.OBJ_TwitterKeyword.TrendTweet()
		wRes['Result'] = True
		return wRes



#####################################################
# キーワードいいね
#####################################################
	def KeywordFavo(self):
		#############################
		# Twitter情報取得
		wFavoRes = self.GetTwitterInfo()
		if wFavoRes['Result']!=True :
			return wFavoRes
		
		wRes = self.OBJ_TwitterKeyword.KeywordFavo()
		return wRes



#####################################################
# リストいいね設定
#####################################################
	def SetListFavo(self):
		#############################
		# Twitter情報取得
		wFavoRes = self.GetTwitterInfo()
		if wFavoRes['Result']!=True :
			return wFavoRes
		
		wRes = self.OBJ_TwitterFavo.SetListFavo()
		return wRes



#####################################################
# リスト通知ユーザ更新
#####################################################
	def UpdateListIndUser(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "UpdateListIndUser"
		
		wGetLag = CLS_OSIF.sCheckNextDay( str( gVal.STR_Time['list_clear'] ), str( gVal.STR_Time['TimeDate'] ) )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sCheckNextDay failed: reason=" + wGetLag['Reason'] + " list_clear=" + str(gVal.STR_Time['list_clear'])
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wGetLag['Next']==False :
			### 翌日ではない= スキップ
			wRes['Result'] = True
			return wRes
		
		#############################
		# 翌日の場合
		#   リスト通知をクリアする
		wSubRes = gVal.OBJ_Tw_IF.ListInd_Clear()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "AllClearListInd error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wSubRes['Responce']==True :
			gVal.OBJ_L.Log( "SC", wRes, "リスト通知クリア" )
		
		#############################
		# 現時間を設定
		wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "list_clear", gVal.STR_Time['TimeDate'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "SetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		###	gVal.STR_Time['list_clear']
		
		wRes['Result'] = True
		return wRes



#####################################################
# リスト登録ユーザチェック
#####################################################
	def CheckListUsers(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "CheckListUsers"
		
		#############################
		# 取得開始の表示
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "リスト登録ユーザチェック" )
		
		#############################
		# 通知リストのチェック
		# 自動リムーブが有効なら、相互フォローリスト、片フォロワーリストのチェック
		wARR_IndListName = []
		if gVal.STR_UserInfo['ListID']!=gVal.DEF_NOTEXT :
			wARR_IndListName.append( gVal.STR_UserInfo['ListName'] )
		
		if gVal.STR_UserInfo['AutoRemove']==True and \
		   ( gVal.STR_UserInfo['mListID']!=gVal.DEF_NOTEXT or \
		     gVal.STR_UserInfo['fListID']!=gVal.DEF_NOTEXT ) :
			wARR_IndListName.append( gVal.STR_UserInfo['mListName'] )
			wARR_IndListName.append( gVal.STR_UserInfo['fListName'] )
		
		for wListName in wARR_IndListName :
			wStr = "〇チェック中リスト: " + wListName
			CLS_OSIF.sPrn( wStr )
			
			#############################
			# Twitterからリストの登録ユーザ一覧を取得
			wListRes = gVal.OBJ_Tw_IF.GetListSubscribers(
			   inListName=wListName,
			   inScreenName=gVal.STR_UserInfo['Account'] )
			
			if wListRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(GetListSubscribers:List): " + wListRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if len(wListRes['Responce'])>=1 :
				### 登録者あり
				wKeylistUser = list( wListRes['Responce'].keys() )
				for wID in wKeylistUser :
					wID = str(wID)
					
					### 警告済はスキップ
###					if wID in gVal.ARR_CautionTweet :
###						continue
###					wFLG_Caution = False
###					for wCautionIndex in gVal.ARR_CautionTweet :
###						if gVal.ARR_CautionTweet[wCautionIndex]['id']==wID :
###							wFLG_Caution = True
###					if wFLG_Caution==True :
###						continue
					if self.Check_Caution( wID )==True :
						continue
					
					### 自分には警告しない
					if str(gVal.STR_UserInfo['id'])==wID  :
						continue
					### VIPには警告しない
					if wID in gVal.ARR_NotReactionUser :
						if gVal.ARR_NotReactionUser[wID]['vip']==True :
							continue
					
					wSubRes = self.SendTweet_Caution( wListRes['Responce'][wID], gVal.STR_UserInfo['Account'], wListName, inFLG_ListCaution=True )
					if wSubRes['Result']!=True :
						wRes['Reason'] = "SendTweet_Caution is failed(1): user=" + wListRes['Responce'][wID]['screen_name'] + " list=" + wListName
						gVal.OBJ_L.Log( "B", wRes )
						continue
					
					### ユーザレベル変更
					wUserLevel = "L"
					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, wUserLevel )
		
		#############################
		# ListFavo一覧のうち
		# 警告ありのリストをチェックする
		wKeylist = list( gVal.ARR_ListFavo.keys() )
		for wKey in wKeylist :
			if gVal.ARR_ListFavo[wKey]['caution']!=True :
				### 警告なしはスキップ
				continue
			
			wStr = "〇チェック中リスト: " + gVal.ARR_ListFavo[wKey]['list_name']
			CLS_OSIF.sPrn( wStr )
			#############################
			# Twitterからリストの登録ユーザ一覧を取得
			wListRes = gVal.OBJ_Tw_IF.GetListSubscribers(
			   inListName=gVal.ARR_ListFavo[wKey]['list_name'],
			   inScreenName=gVal.ARR_ListFavo[wKey]['screen_name'] )
			
			if wListRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(GetListSubscribers): " + wListRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if len(wListRes['Responce'])==0 :
				### 登録者なしはスキップ
				continue
			
			wKeylistUser = list( wListRes['Responce'].keys() )
			for wID in wKeylistUser :
				wID = str(wID)
				
				### 警告済はスキップ
###				if wID in gVal.ARR_CautionTweet :
###					continue
###				wFLG_Caution = False
###				for wCautionIndex in gVal.ARR_CautionTweet :
###					if gVal.ARR_CautionTweet[wCautionIndex]['id']==wID :
###						wFLG_Caution = True
###				if wFLG_Caution==True :
###					continue
				if self.Check_Caution( wID )==True :
					continue
				
				### 自分には警告しない
				if str(gVal.STR_UserInfo['id'])==wID  :
					continue
				### VIPには警告しない
				if wID in gVal.ARR_NotReactionUser :
					if gVal.ARR_NotReactionUser[wID]['vip']==True :
						continue
				
				# ※警告確定
				wSubRes = self.SendTweet_Caution( wListRes['Responce'][wID], gVal.ARR_ListFavo[wKey]['screen_name'], gVal.ARR_ListFavo[wKey]['list_name'], inFLG_ListCaution=True )
				if wSubRes['Result']!=True :
					wRes['Reason'] = "SendTweet_Caution is failed(1): user=" + wListRes['Responce'][wID]['screen_name'] + " list=" + gVal.ARR_ListFavo[wKey]['list_name']
					gVal.OBJ_L.Log( "B", wRes )
					continue
				
				### ユーザレベル変更
				wUserLevel = "L"
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, wUserLevel )
		
		wStr = "チェック終了" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 所有リストの登録者のうち、フォロワーじゃない人にフォローを促す
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "全リストの登録ユーザチェック" )
		
		#############################
		# リストの取得
		wGetListsRes = gVal.OBJ_Tw_IF.GetLists( gVal.STR_UserInfo['Account'] )
		if wGetListsRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(31): " + wGetListsRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		wARR_Lists = wGetListsRes['Responce']
		
		wListFavo_Keylist = list( gVal.ARR_ListFavo.keys() )
		wKeylist = list( wARR_Lists.keys() )
		for wKey in wKeylist :
			### 自分のリスト以外はスキップ
			if wARR_Lists[wKey]['me']==False :
				continue
			
			### リストいいね登録中
			###   警告ありのものはスキップ(上で処理済)
			wFLG_ListFavo_Caution = False
			for wListFavoKey in wListFavo_Keylist :
				if wARR_Lists[wKey]['user']['screen_name']==gVal.ARR_ListFavo[wListFavoKey]['screen_name'] and \
				   wARR_Lists[wKey]['name']==gVal.ARR_ListFavo[wListFavoKey]['list_name'] :
					if gVal.ARR_ListFavo[wListFavoKey]['caution']==True :
						wFLG_ListFavo_Caution = True
						break
			
			if wFLG_ListFavo_Caution==True :
				### リストいいねで警告対象のリストはスキップ
				continue
			
			wStr = "〇チェック中リスト: " + wARR_Lists[wKey]['name']
			CLS_OSIF.sPrn( wStr )
			#############################
			# Twitterからリストの登録ユーザ一覧を取得
			wListRes = gVal.OBJ_Tw_IF.GetListSubscribers(
			   inListName=wARR_Lists[wKey]['name'],
			   inScreenName=wARR_Lists[wKey]['user']['screen_name'] )
			
			if wListRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(GetListSubscribers(2)): " + wListRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if len(wListRes['Responce'])==0 :
				### 登録者なしはスキップ
				continue
			
			wARR_ListUsers = wListRes['Responce']
			
			wKeylistUser = list( wARR_ListUsers.keys() )
			for wID in wKeylistUser :
				wID = str(wID)
				
				### 警告済はスキップ
###				if wID in gVal.ARR_CautionTweet :
###					continue
				if self.Check_Caution( wID )==True :
					continue
				### 自分には警告しない
				if str(gVal.STR_UserInfo['id'])==wID  :
					continue
				### フォロワーはスキップ
				if gVal.OBJ_Tw_IF.CheckFollower( wID )==True :
					continue
				### 禁止ユーザはスキップ
				wUserRes = self.CheckExtUser( wARR_ListUsers[wID], "全リストチェック中の検出", inFLG_Log=False )
				if wUserRes['Result']!=True :
					wRes['Reason'] = "CheckExtUser failed"
					gVal.OBJ_L.Log( "B", wRes )
					continue
				if wUserRes['Responce']==False :
					### 禁止あり=除外
					continue
				
				# ※警告確定
				#############################
				# Twitterからユーザ情報を取得する
				wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inScreenName=wARR_ListUsers[wID]['screen_name'] )
				if wUserInfoRes['Result']!=True :
					wRes['Reason'] = "Twitter API Error(GetUserinfo): " + wUserInfoRes['Reason'] + " screen_name=" + wARR_ListUsers[wID]['screen_name']
					gVal.OBJ_L.Log( "B", wRes )
					continue
				
				#############################
				# 次のユーザはブロック→リムーブする(リスト強制解除)
				# ・非フォロワー
				# ・ツイート数=0
				# ・鍵アカウント
				if wUserInfoRes['Responce']['statuses_count']==0 or \
				   wUserInfoRes['Responce']['protected']==True :
					wBlockRes = gVal.OBJ_Tw_IF.BlockRemove( wID )
					if wBlockRes['Result']!=True :
						wRes['Reason'] = "Twitter API Error(BlockRemove): " + wBlockRes['Reason'] + " screen_name=" + wARR_ListUsers[wID]['screen_name']
						gVal.OBJ_L.Log( "B", wRes )
						continue
					
					### ユーザレベル変更
###					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, "G-" )
###					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, "Z-" )
					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, "G-" )
					
					### トラヒック記録（フォロワー減少）
					CLS_Traffic.sP( "d_follower" )
					
					### ログに記録
###					gVal.OBJ_L.Log( "R", wRes, "追い出し: screen_name=" + wARR_ListUsers[wID]['screen_name'] )
					gVal.OBJ_L.Log( "R", wRes, "追い出し: screen_name=" + wARR_ListUsers[wID]['screen_name'], inID=wID )
				
				#############################
				# 通常アカウントへは警告ツイートを送信
				else:
					wSubRes = self.SendTweet_Caution( wARR_ListUsers[wID], gVal.STR_UserInfo['Account'], wARR_Lists[wKey]['name'], inFLG_ListCaution=False )
					if wSubRes['Result']!=True :
						wRes['Reason'] = "SendTweet_Caution is failed(2): user=" + wARR_ListUsers[wID]['screen_name'] + " list=" + wARR_Lists[wKey]['name']
						gVal.OBJ_L.Log( "B", wRes )
						continue
					
					### ユーザレベル変更
					wUserLevel = "L"
					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, wUserLevel )
		
		wStr = "チェック終了" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes

	#####################################################
	# 警告ツイート送信
	#####################################################
	def SendTweet_Caution( self, inUser, inOwnerName, inListName, inFLG_ListCaution=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "SendTweet_Caution"
		
		wRes['Responce'] = False
		
		wScreenName = inUser['screen_name']
		
		wTweetID = gVal.DEF_NOTEXT
		#############################
		# 警告ツイートを作成
		if inFLG_ListCaution==True :
			### 警告リスト登録者への警告
			wTweet = "@" + wScreenName + '\n'
			wTweet = wTweet + "[ご注意] ユーザ " + str(inOwnerName) + " のリスト " + str(inListName) + " はフォロー禁止です。" + '\n'
			wTweet = wTweet + "[Caution] Excuse me. The list " + str(inListName) + " for user " + str(inOwnerName) + " is unfollowable."
		
		else:
			### 非フォロワーのリスト登録者への警告
			wTweet = "@" + wScreenName + '\n'
			wTweet = wTweet + "[お願い] リスト " + str(inListName) + " をフォローするには当アカウント " + str(inOwnerName) + " もフォローしてください。" + '\n'
			wTweet = wTweet + "[Request] To follow the list " + str(inListName) + ", please also follow this account " + str(inOwnerName) + "."
		
		#############################
		# 送信したツイートのパターン生成
		wNoRet_Tweet = wTweet.replace( "@", "" )
		wNoRet_Tweet = wNoRet_Tweet.replace( "[", "" )
		wNoRet_Tweet = wNoRet_Tweet.replace( "]", "" )
		
		#############################
		# Twitterへの送信が有効の場合
		if gVal.DEF_STR_TLNUM['sendListUsersCaution']==True :
			#############################
			# ツイート送信
			wTweetRes = gVal.OBJ_Tw_IF.Tweet( wTweet )
			if wTweetRes['Result']!=True :
			###	if wTweetRes['StatusCode']=="403" :
				wRes['Reason'] = "Twitter API Error(Tweet): " + wTweetRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			else:
				### Tweet完了→Twitter再取得可能になるまで約10秒遅延待機
				CLS_OSIF.sSleep(10)
				
				wTweetRes = gVal.OBJ_Tw_IF.GetSearch( wNoRet_Tweet )
				if wTweetRes['Result']!=True :
					wRes['Reason'] = "Twitter API Error(GetSearch): " + wTweetRes['Reason']
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				#############################
				# 送信したツイートのツイートIDを取得する
				if len(wTweetRes['Responce'])==1 :
					wTweetID = str( wTweetRes['Responce'][0]['id'] )
				else:
					### 1ツイート以外はありえない？
					wRes['Reason'] = "Twitter is dual ttweet, or not one screen_name=" + wScreenName
					gVal.OBJ_L.Log( "D", wRes )
					return wRes
				
				### ログに記録
				wStr = "リスト登録者へ警告(規定外ユーザ): screen_name=" + wScreenName + " tweetid=" + wTweetID + " list=" + str(inListName)
###				gVal.OBJ_L.Log( "RR", wRes, wStr )
				gVal.OBJ_L.Log( "RR", wRes, wStr, inID=inUser['id'] )
			
			wRes['Responce'] = True	#Twitterへ送信済
		
		#############################
		# Twitterへの送信が無効の場合
		else:
			### ログに記録
			wStr = "リスト登録者へ警告(規定外ユーザ・Twitter未送信): screen_name=" + wScreenName + " tweetid=" + wTweetID + " list=" + str(inListName)
###			gVal.OBJ_L.Log( "RR", wRes, wStr )
			gVal.OBJ_L.Log( "RR", wRes, wStr, inID=inUser['id'] )
		
		#############################
		# IDを警告済に追加
		wSubRes = gVal.OBJ_DB_IF.SetCautionTweet( inUser, wTweetID )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "SetCautionTweet is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	# 警告有無チェック
	#####################################################
	def Check_Caution( self, inID ):
		for wCautionIndex in gVal.ARR_CautionTweet :
			if gVal.ARR_CautionTweet[wCautionIndex]['id']==inID :
				return True
		return False



#####################################################
# 自動リムーブチェック
#####################################################
	def CheckAutoRemove( self, inFLG_Force=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "CheckAutoRemove"
		
		wRes['Responce'] = False
		#############################
		# 自動リムーブが無効ならここで終わる
		if gVal.STR_UserInfo['AutoRemove']==False :
			wRes['Result'] = True
			return wRes
		
		#############################
		# 取得可能時間か？
		wGetLag = CLS_OSIF.sTimeLag( str( gVal.STR_Time['auto_remove'] ), inThreshold=gVal.DEF_STR_TLNUM['forCheckAutoRemoveSec'] )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		###強制じゃなければ判定する
		if inFLG_Force==False :
			if wGetLag['Beyond']==False :
				### 規定以内は除外
				wStr = "●自動リムーブチェック期間外 処理スキップ: 次回処理日時= " + str(wGetLag['RateTime']) + '\n'
				CLS_OSIF.sPrn( wStr )
				wRes['Result'] = True
				return wRes
		
		#############################
		# 取得開始の表示
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "自動リムーブチェック" )
		
		#############################
		# 自動リムーブが有効なら、相互フォローリスト、片フォロワーリストのチェック
		wARR_IndListName = []
		if gVal.STR_UserInfo['AutoRemove']==True and \
		   ( gVal.STR_UserInfo['mListID']!=gVal.DEF_NOTEXT or \
		     gVal.STR_UserInfo['fListID']!=gVal.DEF_NOTEXT ) :
			wARR_IndListName.append( gVal.STR_UserInfo['mListName'] )
			wARR_IndListName.append( gVal.STR_UserInfo['fListName'] )
		
		for wListName in wARR_IndListName :
			wStr = "〇チェック中リスト: " + wListName
			CLS_OSIF.sPrn( wStr )
			
			#############################
			# Twitterからリストの登録ユーザ一覧を取得
			wListRes = gVal.OBJ_Tw_IF.GetListMember(
			   inListName=wListName,
			   inScreenName=gVal.STR_UserInfo['Account'] )
			
			if wListRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(GetListMember:List): " + wListRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if len(wListRes['Responce'])==0 :
				### 登録者なしはスキップ
				continue
			
			wKeylistUser = list( wListRes['Responce'].keys() )
			for wID in wKeylistUser :
				wID = str(wID)
				
				###自分は除外する
				if str(gVal.STR_UserInfo['id'])==wID :
					continue
				
				#############################
				# 自動リムーブ
				wSubRes = self.OBJ_TwitterFollower.AutoRemove( wListRes['Responce'][wID] )
				if wSubRes['Result']!=True :
					wRes['Reason'] = "AutoRemove is failed"
					gVal.OBJ_L.Log( "B", wRes )
###					return wRes
					continue
		
		#############################
		# ListFavo一覧のうち
		# 自動リムーブ有効のリストをチェックする
		wKeylist = list( gVal.ARR_ListFavo.keys() )
		for wKey in wKeylist :
			if gVal.ARR_ListFavo[wKey]['auto_rem']!=True :
				### 自動リムーブ無効はスキップ
				continue
			
			wStr = "〇チェック中リスト: " + gVal.ARR_ListFavo[wKey]['list_name']
			CLS_OSIF.sPrn( wStr )
			#############################
			# Twitterからリストの登録ユーザ一覧を取得
			wListRes = gVal.OBJ_Tw_IF.GetListMember(
			   inListName=gVal.ARR_ListFavo[wKey]['list_name'],
			   inScreenName=gVal.ARR_ListFavo[wKey]['screen_name'] )
			
			if wListRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(GetListMember): " + wListRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if len(wListRes['Responce'])==0 :
				### 登録者なしはスキップ
				continue
			
			wKeylistUser = list( wListRes['Responce'].keys() )
			for wID in wKeylistUser :
				wID = str(wID)
				
				###自分は除外する
				if str(gVal.STR_UserInfo['id'])==wID :
					continue
				
				#############################
				# 自動リムーブ
				wSubRes = self.OBJ_TwitterFollower.AutoRemove( wListRes['Responce'][wID] )
				if wSubRes['Result']!=True :
					wRes['Reason'] = "AutoRemove is failed"
					gVal.OBJ_L.Log( "B", wRes )
###					return wRes
					continue
		
		#############################
		# 現時間を設定
		wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "auto_remove", gVal.STR_Time['TimeDate'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "SetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		###	gVal.STR_Time['auto_remove']
		
		wStr = "チェック終了" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# 除外文字チェック
#####################################################
	def CheckExtWord( self, inData, inWord ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "CheckExtWord"
		
		wWord = inWord.replace( '\n', '' )
		
		wRes['Responce'] = False
		#############################
		# 除外文字があるかチェック
		for wExeWord in gVal.ARR_ExeWordKeys :
			if wWord.find( wExeWord )>=0 :
				if gVal.ARR_ExeWord[wExeWord]['report']==True :
					### 報告対象の表示と、ログに記録
					gVal.OBJ_L.Log( "RR", wRes, "●報告対象の文字除外: id=" + inData['screen_name'] + " word=" + inWord, inID=inData['id'] )
				else:
					### ログに記録
					gVal.OBJ_L.Log( "N", wRes, "文字除外: id=" + inData['screen_name'] + " word=" + inWord )
				
				### 除外
				wRes['Result'] = True
				return wRes
		
		#############################
		# 正常終了
		wRes['Responce'] = True
		wRes['Result'] = True
		return wRes



#####################################################
# 除外プロフ文字チェック
#####################################################
	def CheckExtProf( self, inData, inWord ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "CheckExtProf"
		
		wWord = inWord.replace( '\n', '' )
		
		wRes['Responce'] = False
		#############################
		# 除外プロフ文字があるかチェック
		for wExeWord in gVal.ARR_ExeProfKeys :
			if wWord.find( wExeWord )>=0 :
				if gVal.ARR_ExeProf[wExeWord]['report']==True :
					### 報告対象の表示と、ログに記録
					gVal.OBJ_L.Log( "RR", wRes, "●報告対象の文字除外: id=" + inData['screen_name'] + " word=" + inWord, inID=inData['id'] )
				else:
					### ログに記録
					gVal.OBJ_L.Log( "N", wRes, "文字除外: id=" + inData['screen_name'] + " word=" + inWord )
				
				### 除外
				wRes['Result'] = True
				return wRes
		
		#############################
		# 正常終了
		wRes['Responce'] = True
		wRes['Result'] = True
		return wRes



#####################################################
# 禁止ユーザチェック
#####################################################
	def CheckExtUser( self, inData, inReason, inFLG_Log=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "CheckExtUser"
		
		wUserID = str(inData['id'])
		
		wRes['Responce'] = False
		#############################
		# 禁止ユーザかチェック
		if wUserID in gVal.ARR_NotReactionUser :
			if gVal.ARR_NotReactionUser[wUserID]['vip']==True :
				### VIPは除外する
				wStr = "VIPのため除外: screen_name=" + str(inData['screen_name'])
				CLS_OSIF.sPrn( wStr )
				
				wRes['Result'] = True
				return wRes
			
			if gVal.ARR_NotReactionUser[wUserID]['report']==True and inFLG_Log==True :
				### 報告対象の表示と、ログに記録
###				gVal.OBJ_L.Log( "RR", wRes, "●禁止ユーザ: screen_name=" + inData['screen_name'] + " reason=" + inReason )
				gVal.OBJ_L.Log( "RR", wRes, "●禁止ユーザ: screen_name=" + inData['screen_name'] + " reason=" + inReason, inID=wUserID )
			
			### 除外
			wRes['Result'] = True
			return wRes
		
		#############################
		# 正常終了
		wRes['Responce'] = True
		wRes['Result'] = True
		return wRes



#####################################################
# VIPユーザチェック
#####################################################
	def CheckVIPUser( self, inData ):
		
		wUserID = str(inData['id'])
		
		#############################
		# 禁止ユーザかチェック
		if wUserID in gVal.ARR_NotReactionUser :
			if gVal.ARR_NotReactionUser[wUserID]['vip']==True :
				### VIP
				return True
		
		return False



#####################################################
# VIP監視ユーザリスト取得
#####################################################
	def GetVIPUser(self):
		
		wARR_List = []
		wKeylist = list( gVal.ARR_NotReactionUser.keys() )
		for wID in wKeylist :
			wID = str( wID )
			
			### 自分は監視しない
			if wID==str(gVal.STR_UserInfo['id']) :
				continue
			
			if gVal.ARR_NotReactionUser[wID]['ope']==True :
				wARR_List.append( wID )
		
		return wARR_List

	#####################################################
	def GetVIPUserInfo(self, inUserID ):
		wUserID = str(inUserID)
		if wUserID not in gVal.ARR_NotReactionUser :
			return None
		return gVal.ARR_NotReactionUser[wUserID]



#####################################################
# 新規いいね情報の設定
#####################################################
	def SetNewFavoData( self, inUser, inData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "SetNewFavoData"
		
		if inData['level_tag']!=gVal.DEF_NOTEXT :
			### 既にレベルが設定されてたら終わる
			wRes['Result'] = True
			return wRes
		
		wID = str(inData['id'])
		
		wMyFollow = None
		wFollower = None
		wUserLevel = "F"
		#############################
		# 関係性チェック
		wFollowInfoRes = gVal.OBJ_Tw_IF.GetFollowInfo( wID )
		if wFollowInfoRes['Result']!=True :
			wRes['Reason'] = "GetFollowInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wFollowInfoRes['Responce']['blocked_by']==True :
			### 被ブロック検知
###			wUserLevel = "G"
			wUserLevel = "Z"
			
			wStr = "●被ブロック検知"
###			gVal.OBJ_L.Log( "R", wRes, wStr + ": " + inData['screen_name'] )
			gVal.OBJ_L.Log( "R", wRes, wStr + ": " + inData['screen_name'], inID=wID )
			
			### ブロック検知の送信
			self.SendBeenBlock( inData )
		
		### 公式垢の場合
		elif gVal.OBJ_Tw_IF.CheckSubscribeListUser( wID )==True :
			wMyFollow = wFollowInfoRes['Responce']['following']
			wFollower = wFollowInfoRes['Responce']['followed_by']
			wUserLevel = "A"
		
		### 片フォロー者の場合
		elif wFollowInfoRes['Responce']['following']==True and \
		     wFollowInfoRes['Responce']['followed_by']==False :
			wMyFollow = True
			wUserLevel = "D"
			
			### 相互フォローリストに追加
			wTwitterRes = gVal.OBJ_Tw_IF.MutualList_AddUser( inData )
		
		### フォロワーの場合
		elif wFollowInfoRes['Responce']['following']==False and \
		     wFollowInfoRes['Responce']['followed_by']==True :
			wFollower = True
			wUserLevel = "E"
			
			### 片フォロワーリストに追加
			wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_AddUser( inData )
		
		### 相互フォローの場合
		elif wFollowInfoRes['Responce']['following']==True and \
		     wFollowInfoRes['Responce']['followed_by']==True :
			wMyFollow = True
			wFollower = True
			wUserLevel = "C+"
			
			### 相互フォローリストに追加
			wTwitterRes = gVal.OBJ_Tw_IF.MutualList_AddUser( inData )
		
		#############################
		# ユーザレベル変更
		wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, wUserLevel )
		
		#############################
		# フォロー情報をDBへ反映する
		if wMyFollow!=None or wFollower!=None :
			wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Follower( wID, wMyFollow, wFollower )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "UpdateFavoData_Follower is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# 更新によりデータリロード
		wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( inUser, inFLG_New=False )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetFavoDataOne is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wRes['Responce'] = wSubRes['Responce']
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# 被ブロックのお知らせ
#####################################################
	def SendBeenBlock( self, inUser ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "SendBeenBlock"
		
		wTweet = ""
		#############################
		# ツイートの作成
		wTweet = "[自動] ブロックを検知しました" + '\n'
		wTweet = wTweet + "[Auto] block detected" + '\n'
		wTweet = wTweet + "user name: " + str(inUser['screen_name']) + '\n'
		wTweet = wTweet + gVal.STR_UserInfo['DelTag'] + '\n'
		
		#############################
		# 送信
		wTweetRes = gVal.OBJ_Tw_IF.Tweet( wTweet )
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTweetRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 送信完了
		wStr = "ブロック検知通知を送信しました。" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# ログに記録
		gVal.OBJ_L.Log( "T", wRes, "ブロック検知通知送信(Twitter)" )
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# 監視状態のお知らせ
#####################################################
	def SendUserOpeInd( self, inUser, inFLG_Ope ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "SendBeenBlock"
		
		wOpe   = "OFF"
		wTweet = ""
		#############################
		# ツイートの作成
		
		### 監視OFFの場合
		if inFLG_Ope==False :
			wTweet = "[自動] フォロー一覧からフォロー者を選出" + '\n'
		
		### 監視ONの場合
		else:
			wOpe   = "ON"
			wTweet = "[自動] リアクション再開" + '\n'
			wTweet = wTweet + "[Automatic] Resume reaction" + '\n'
		
		wTweet = wTweet + "user name: " + str(inUser['screen_name']) + '\n'
		wTweet = wTweet + gVal.STR_UserInfo['DelTag'] + '\n'
		
		#############################
		# 送信
		wTweetRes = gVal.OBJ_Tw_IF.Tweet( wTweet )
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTweetRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 送信完了
		wStr = "監視状態を送信しました。[" + wOpe + "]" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# ログに記録
		gVal.OBJ_L.Log( "T", wRes, "監視状態送信(Twitter) [" + wOpe + "]" )
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# 全ミュート解除・ミュート忘れをミュート
#####################################################
	def AllMuteRemove(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "AllMuteRemove"
		
		wRes['Responce'] = False
		
		wARR_MuteID = []
		#############################
		# ミュート一覧 取得
		wMuteRes = gVal.OBJ_Tw_IF.GetMuteList()
		if wMuteRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetMuteList): " + wMuteRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		if len(wMuteRes['Responce'])>=1 :
			for wID in wMuteRes['Responce']:
				wID = str( wID )
				wARR_MuteID.append( wID )
		
		wARR_MutualFollow = gVal.OBJ_Tw_IF.GetMutualListUser()
		#############################
		# ミュートID一覧の作成（ミュート忘れ）
		wARR_MuteAddID = []
		for wMutualID in wARR_MutualFollow :
			###フォロー者でミュートなければ対象
			if wMutualID not in wARR_MuteID :
				wARR_MuteAddID.append( wMutualID )
		
		#############################
		# ミュート解除ID一覧の作成
		wARR_MuteRemoveID = []
###		if len(wMuteRes['Responce'])>=1 :
###			for wID in wMuteRes['Responce']:
###				wID = str( wID )
###				
###				###フォロー者は対象外
###				if gVal.OBJ_Tw_IF.CheckMyFollow( wID )==True :
###					continue
###				
###				wARR_MuteRemoveID.append( wID )
		for wID in wARR_MuteID:
			###フォロー者はミュート解除対象
			if gVal.OBJ_Tw_IF.CheckMyFollow( wID )==False :
				wARR_MuteRemoveID.append( wID )
		
		#############################
		# ミュート実行
		if len( wARR_MuteAddID )>=1 :
			#############################
			# ミュートしていく
			wStr = "ミュート実行対象数: " + str(len( wARR_MuteAddID )) + '\n'
			CLS_OSIF.sPrn( wStr )
			
			for wID in wARR_MuteAddID :
				### DBからいいね情報を取得する(1個)
				wDBRes = gVal.OBJ_DB_IF.GetFavoDataOne( inID=wID, inFLG_New=False )
				if wDBRes['Result']!=True :
					###失敗
					wRes['Reason'] = "GetFavoDataOne is failed(2)"
					gVal.OBJ_L.Log( "B", wRes )
					continue
				### DB未登録ならスキップ
				if wDBRes['Responce']['Data']==None :
					continue
				wARR_DBData = wDBRes['Responce']['Data']
				
				###  実行中ユーザ情報の表示
				wStr = "ミュート実行中: " + wARR_DBData['screen_name']
				CLS_OSIF.sPrn( wStr )
				
				###  ミュート実行する
				wRemoveRes = gVal.OBJ_Tw_IF.Mute( wID )
				if wRemoveRes['Result']!=True :
					wRes['Reason'] = "Twitter API Error(Mute): " + wRemoveRes['Reason']
					gVal.OBJ_L.Log( "B", wRes )
					
					wStr = "●実行失敗"
					CLS_OSIF.sPrn( wStr )
					continue
				else:
					wStr = "〇実行成功"
					CLS_OSIF.sPrn( wStr )
				
				### Twitter Wait
				CLS_OSIF.sSleep( 5 )
				
				###  ミュート一覧にないID=ミュート解除してない 場合は待機スキップ
				if wRemoveRes['Responce']==False :
					continue
		
###		###対象者なし
###		if len( wARR_MuteRemoveID )==0 :
###			wRes['Result'] = True
###			return wRes
###		
		#############################
		# 解除実行
###		else:
		if len( wARR_MuteRemoveID )>=1 :
			#############################
			# ミュート解除していく
			wStr = "ミュート解除対象数: " + str(len( wARR_MuteRemoveID )) + '\n'
			CLS_OSIF.sPrn( wStr )
			
			for wID in wARR_MuteRemoveID :
				### DBからいいね情報を取得する(1個)
				wDBRes = gVal.OBJ_DB_IF.GetFavoDataOne( inID=wID, inFLG_New=False )
				if wDBRes['Result']!=True :
					###失敗
					wRes['Reason'] = "GetFavoDataOne is failed(2)"
					gVal.OBJ_L.Log( "B", wRes )
					continue
				### DB未登録ならスキップ
				if wDBRes['Responce']['Data']==None :
					continue
				wARR_DBData = wDBRes['Responce']['Data']
				
				###  解除中ユーザ情報の表示
				wStr = "ミュート解除中: " + wARR_DBData['screen_name']
				CLS_OSIF.sPrn( wStr )
				
				###  ミュート解除する
				wRemoveRes = gVal.OBJ_Tw_IF.OBJ_Twitter.RemoveMute( wID )
				if wRemoveRes['Result']!=True :
					wRes['Reason'] = "Twitter API Error(RemoveMute): " + wRemoveRes['Reason']
					gVal.OBJ_L.Log( "B", wRes )
					
					wStr = "●解除失敗"
					CLS_OSIF.sPrn( wStr )
					continue
				else:
					wStr = "〇解除成功"
					CLS_OSIF.sPrn( wStr )
				
				### Twitter Wait
				CLS_OSIF.sSleep( 5 )
				
				###  ミュート一覧にないID=ミュート解除してない 場合は待機スキップ
				if wRemoveRes['Responce']==False :
					continue
		
		#############################
		# 完了
		wRes['Responce'] = True
		wRes['Result'] = True
		return wRes



#####################################################
# 被登録リストの表示
#####################################################
	def View_SubsList(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "View_SubsList"
		
		#############################
		# 取得開始の表示
		CLS_MyDisp.sViewHeaderDisp( "被登録リスト一覧の表示", False )
		
		#############################
		# 被登録一覧を取得する
		wARR_SubsList = gVal.OBJ_Tw_IF.GetSubsList()
		if len(wARR_SubsList)==0 :
			wStr = "(リストなし)"
			CLS_OSIF.sPrn( wStr )
		
		wStr = ""
		wKeylist = list( wARR_SubsList.keys() )
		for wID in wKeylist :
			wID = str(wID)
			
			wStr = wStr + "  "
			### ユーザ名（screen_name）
			wListData = wARR_SubsList[wID]['user']['screen_name']
			wListNumSpace = gVal.DEF_SCREEN_NAME_SIZE - len(wListData)
			if wListNumSpace>0 :
				wListData = wListData + " " * wListNumSpace
			wStr = wStr + wListData + ": "
			
			### リスト名
			wListData = wARR_SubsList[wID]['name']
			wStr = wStr + wListData + '\n'
		
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# VIPフォロー監視
#####################################################
	def CheckVipFollow(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "CheckVipFollow"
		
		#############################
		# 取得開始の表示
		CLS_MyDisp.sViewHeaderDisp( "VIPフォロー監視", False )
		
		#############################
		# VIPかつFollow監視を抽出
		wKeylist = list( gVal.ARR_NotReactionUser.keys() )
		for wID in wKeylist :
			wID = str(wID)
			
			if gVal.ARR_NotReactionUser[wID]['follow']==False :
				continue
			
			wSubRes = self.__checkVipFollow( gVal.ARR_NotReactionUser[wID] )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "__checkVipFollow is failed: user=" + gVal.ARR_NotReactionUser[wID]['screen_name']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes

	#####################################################
	def __checkVipFollow( self, inUser ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "CheckVipFollow"
		
		#############################
		# 監視ユーザの表示
		wStr = "VIP監視ユーザ: " + str(inUser['screen_name']) + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
###		# フォロー一覧の取得
		# フォロワー一覧の取得
###		wFollowRes = gVal.OBJ_Tw_IF.GetFollowIDList( inID=inUser['id'] )
		wFollowRes = gVal.OBJ_Tw_IF.GetFollowerIDList( inID=inUser['id'] )
###		wFollowRes = gVal.OBJ_Tw_IF.GetMyFollowIDList( inID=inUser['id'] )
		if wFollowRes['Result']!=True :
###			wRes['Reason'] = "GetFollowIDList is failed: user=" + str(inUser['screen_name'])
			wRes['Reason'] = "GetFollowerIDList is failed: user=" + str(inUser['screen_name'])
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wARR_FollowID = wFollowRes['Responce']
		if len(wARR_FollowID)==0 :
###			wStr = "(フォロー者なし)"
			wStr = "(フォロワーなし)"
###			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		else:
			wStr = "フォロワー数= " + str( len(wARR_FollowID) )
		CLS_OSIF.sPrn( wStr )
		
		###ウェイト初期化
		self.Wait_Init( inZanNum=len( wARR_FollowID ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
		#############################
###		# フォロー者
		# フォロワー
		for wID in wARR_FollowID :
			###ウェイトカウントダウン
			if self.Wait_Next()==False :
				break	###ウェイト中止
			
			wID = str(wID)
			
			#############################
			# 禁止ユーザは除外
			if wID in gVal.ARR_NotReactionUser :
				continue
			
			#############################
			# ユーザ情報の取得
			wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inID=wID )
			if wUserInfoRes['Result']!=True :
				wRes['Reason'] = "GetUserinfo is failed: user=" + str(inUser['screen_name'])
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			wUser = wUserInfoRes['Responce']
			
			wARR_DBData = None
			#############################
			# DBからユーザ情報を取得する(1個)
			wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( wUser, inFLG_New=False )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "GetFavoDataOne is failed: user=" + str(wUser['screen_name'])
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wSubRes['Responce']['Data']==None :
				### DBにユーザが存在しない
				wStr = "●未フォロー者: user=" + str(wUser['screen_name'])
				CLS_OSIF.sPrn( wStr )
				continue
			
			wARR_DBData = wSubRes['Responce']['Data']
			
			if wARR_DBData['follower']==True :
				### VIPフォロー者 かつ メインフォロワー
				wStr = "〇フォロー者  : user=" + str(wUser['screen_name']) + " level=" + str(wARR_DBData['level_tag'])
				CLS_OSIF.sPrn( wStr )
			
			else:
				if wARR_DBData['level_tag']=="A" or wARR_DBData['level_tag']=="A+" :
					### 監視外（公式垢）
					wStr = "〇監視外  : user=" + str(wUser['screen_name']) + " level=" + str(wARR_DBData['level_tag'])
					CLS_OSIF.sPrn( wStr )
				
				else:
					### VIPフォロー者 かつ メインフォロワーではない
					wStr = "●未フォロー者: user=" + str(wUser['screen_name']) + " level=" + str(wARR_DBData['level_tag'])
					CLS_OSIF.sPrn( wStr )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# レベルタグ出力
#####################################################
	def LevelTagSttring( self, inLevelTag ):
		wLevelTag = str(inLevelTag)
		if len(inLevelTag)<2 :
			wLevelTag = wLevelTag + " "
		return wLevelTag



#####################################################
# スケジュールの表示
#####################################################
	def View_Schedule(self):
		wRes = self.OBJ_TwitterAdmin.View_Schedule()
		return wRes



#####################################################
# システム情報の表示
#####################################################
	def View_Sysinfo(self):
		#############################
		# Twitter情報取得
		wFavoRes = self.GetTwitterInfo()
		if wFavoRes['Result']!=True :
			return wFavoRes
		
		wRes = self.OBJ_TwitterAdmin.View_Sysinfo()
		return wRes



