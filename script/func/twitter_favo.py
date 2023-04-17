#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : Twitter監視 いいね監視系
#####################################################

from ktime import CLS_TIME
from osif import CLS_OSIF
from traffic import CLS_Traffic
from mydisp import CLS_MyDisp
from gval import gVal
#####################################################
class CLS_TwitterFavo():
#####################################################
	OBJ_Parent = ""				#親クラス実体
	
	ARR_FavoUserID     = []
	ARR_OverFavoUserID = []
	ARR_RandUserID     = []
	

										###自動いいね 処理モード
	DEF_AUTOFAVO_RETURN_FAVO = 1		#    お返しいいね
	DEF_AUTOFAVO_FOLLOWER_FAVO = 19		#    フォロワー支援



#####################################################
# Init
#####################################################
	def __init__( self, parentObj=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "__init__"
		
		if parentObj==None :
			###親クラス実体の未設定
			wRes['Reason'] = "You have not set the parent class entity for parentObj"
			gVal.OBJ_L.Log( "A", wRes )
			return
		
		self.OBJ_Parent = parentObj
		return



#####################################################
# いいね解除
#####################################################
	def RemFavo( self, inFLG_FirstDisp=True, inFLG_All=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "RemFavo"
		
		#############################
		# 取得開始の表示
		if inFLG_FirstDisp==True :
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "いいね解除中" )
		
		#############################
		# ふぁぼ一覧 取得
		wFavoRes = gVal.OBJ_Tw_IF.GetFavo()
		if wFavoRes['Result']!=True :
			wRes['Reason'] = "GetFavoData is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# ふぁぼ一覧 取得
		wARR_TwData = gVal.OBJ_Tw_IF.GetFavoData()
		
		#############################
		# いいねがない場合、処理を終わる
		if len(wARR_TwData)==0 :
			wStr = "いいねがないため、処理を終わります。"
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True	#正常終了
			return wRes
		
		wARR_Tw_ID = list( wARR_TwData.keys() )
		wARR_Tw_ID.reverse()	#逆ソート
		
		#############################
		# 最古のいいねIDを算出
		wARR_Tw_ID_LastKey = wARR_Tw_ID[-1]
		
		wARR_RemoveID = []
		wRemTweet = 0
		wCancelNum = 0
		#############################
		# 期間を過ぎたいいねを選出する
		for wID in wARR_Tw_ID :
			wID = str( wID )
			
			###引用の元ツイートは実体ではないため、スキップ
			if wARR_TwData[wID]['kind']=="quoted" :
				continue
			
			###日時の変換
			if inFLG_All==False :
				wTime = CLS_TIME.sTTchg( wRes, "(1)", wARR_TwData[wID]['created_at'] )
				if wTime['Result']!=True :
					continue
				wARR_TwData[wID]['created_at'] = wTime['TimeDate']
				
				###期間を過ぎているか
				wGetLag = CLS_OSIF.sTimeLag( str(wARR_TwData[wID]['created_at']), inThreshold=gVal.DEF_STR_TLNUM['forRemFavoSec'] )
				if wGetLag['Result']!=True :
					wRes['Reason'] = "sTimeLag failed(1)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				if wGetLag['Beyond']==False :
					###期間内
					###  次へ
					wStr = "○解除対象外: " + str(wARR_TwData[wID]['created_at']) + " : " + str(wARR_TwData[wID]['user']['screen_name'])
					CLS_OSIF.sPrn( wStr )
					wCancelNum += 1
					if gVal.DEF_STR_TLNUM['favoCancelNum']<=wCancelNum :
						### 規定回数のスキップなので処理停止
						break
					continue
				
				wCancelNum = 0
			
			#############################
			# 対象なのでIDを詰める
			wARR_RemoveID.append( wID )
			
			#############################
			# 正常
			continue	#次へ
		
		#############################
		# 処理数の表示
		wStr = "いいね解除対象数= " + str(len( wARR_Tw_ID )) + " 個" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wARR_RemoveID ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
		wRemTweet = 0
		#############################
		# 選出したいいねを解除していく
		for wID in wARR_RemoveID :
			###ウェイトカウントダウン
			if self.OBJ_Parent.Wait_Next()==False :
				break	###ウェイト中止
			
			wID = str( wID )
			
			#############################
			# いいねを外す
			wRemoveRes = gVal.OBJ_Tw_IF.FavoRemove( wID )
			if wRemoveRes['Result']!=True :
				wRes['Reason'] = "Twitter Error"
				gVal.OBJ_L.Log( "B", wRes )
			
			if wRemoveRes['Responce']['Run']==True :
				wTextReason = "いいね解除: id=" + str(wID) + ": " + str(wRemoveRes['Responce']['Data']['created_at']) + " : " + str(wRemoveRes['Responce']['Data']['user']['screen_name'])
				gVal.OBJ_L.Log( "T", wRes, wTextReason )
				
				wRemTweet += 1
			else:
				wRes['Reason'] = "FavoRemove failed: id=" + str(wID)
				gVal.OBJ_L.Log( "D", wRes )
		
		#############################
		# 取得結果の表示
		wStr = ""
		if inFLG_FirstDisp==False :
			wStr = "------------------------------" + '\n'
		wStr = wStr + "Twitterいいね数  : " + str( len(wARR_Tw_ID) )+ '\n'
		wStr = wStr + "いいね解除対象数 : " + str( len( wARR_Tw_ID ) )+ '\n'
		wStr = wStr + "いいね解除実施数 : " + str( wRemTweet )+ '\n'
		wStr = wStr + "最古いいね日時   : " + str( str( wARR_TwData[wARR_Tw_ID_LastKey]['created_at'] ) )+ '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# リストいいね
#####################################################
	def ListFavo( self, inFLG_FirstDisp=True, inFLG_Test=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "ListFavo"
		
		#############################
		# 取得可能時間か？
		wGetLag = CLS_OSIF.sTimeLag( str( gVal.STR_Time['mffavo'] ), inThreshold=gVal.DEF_STR_TLNUM['forListFavoSec'] )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wGetLag['Beyond']==False and inFLG_Test==False :
			### 規定以内は除外
			wStr = "●リストいいね期間外 処理スキップ: 次回処理日時= " + str(wGetLag['RateTime']) + '\n'
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
		wResult = {
			"timeline"			: 0,		# タイムライン取得数
			"run"				: 0,		# 実施数
			"agent"				: 0,		# 候補数
			"cnt"				: 0			# 抽出数
		}
		
		#############################
		# 取得開始の表示
		if inFLG_FirstDisp==True :
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "リストいいね実行中" )
		
		#############################
		# リストいいね指定の処理
		wKeylist = list( gVal.ARR_ListFavo.keys() )
		for wKey in wKeylist :
			### 無効ならスキップ
			if gVal.ARR_ListFavo[wKey]['valid']!=True :
				continue
			
			#############################
			# リストの表示
			wStr = "******************************" + '\n'
			wStr = wStr + "処理中リスト: @" + gVal.ARR_ListFavo[wKey]['screen_name'] + "/ " + gVal.ARR_ListFavo[wKey]['list_name'] + '\n'
			CLS_OSIF.sPrn( wStr )
			
			#############################
			# ユーザIDの取得
			wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inScreenName=gVal.ARR_ListFavo[wKey]['screen_name'] )
			if wUserInfoRes['Result']!=True :
				wRes['Reason'] = "Twitter Error: @" + gVal.ARR_ListFavo[wKey]['screen_name']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			### IDの取得
			wUserID = str( wUserInfoRes['Responce']['id'] )
			
			#############################
			# リストIDの取得
			wListsRes = gVal.OBJ_Tw_IF.GetListID(
			   inListName=gVal.ARR_ListFavo[wKey]['list_name'],
			   inScreenName=gVal.ARR_ListFavo[wKey]['screen_name'] )
			
			if wListsRes['Result']!=True :
				wRes['Reason'] = "Twitter Error: GetListID"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			### List IDの取得
			wListID = str( wListsRes['Responce'] )
			
			#############################
			# 自動いいね
			wResFavo = self.AutoFavo( wUserInfoRes['Responce'], gVal.DEF_STR_TLNUM['forAutoFavoListFavoSec'], gVal.ARR_ListFavo[wKey]['follow'], gVal.ARR_ListFavo[wKey]['sensitive'], wListID )
			if wResFavo['Result']!=True :
				wRes['Reason'] = "Twitter Error"
				gVal.OBJ_L.Log( "B", wRes )
				continue
			
			wResult['timeline'] += wResFavo['Responce']['timeline']
			wResult['run']      += wResFavo['Responce']['run']
			wResult['agent']    += wResFavo['Responce']['agent']
			wResult['cnt']      += wResFavo['Responce']['cnt']
		
 		#############################
		# 取得結果の表示
		wStr = ""
		if inFLG_FirstDisp==False :
			wStr = "------------------------------" + '\n'
		wStr = wStr + "抽出タイムライン数 : " + str( wResult['timeline'] )+ '\n'
		wStr = wStr + "いいね抽出数       : " + str( wResult['cnt'] )+ '\n'
		wStr = wStr + "  いいね候補数     : " + str( wResult['agent'] )+ '\n'
		wStr = wStr + "  いいね実施数     : " + str( wResult['run'] )+ '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 現時間を設定
		wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "mffavo", gVal.STR_Time['TimeDate'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "SetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		###	gVal.STR_Time['mffavo']
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes

	#####################################################
	def ListFavo_single( self, inIndex, inFLG_FirstDisp=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "ListFavo_single"
		
		wResult = {
			"timeline"			: 0,		# タイムライン取得数
			"run"				: 0,		# 実施数
			"agent"				: 0,		# 候補数
			"cnt"				: 0			# 抽出数
		}
		
		#############################
		# 取得開始の表示
		if inFLG_FirstDisp==True :
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "リストいいね実行中" )
		
		#############################
		# リストの表示
		wStr = "******************************" + '\n'
		wStr = wStr + "処理中リスト: @" + gVal.ARR_ListFavo[inIndex]['screen_name'] + "/ " + gVal.ARR_ListFavo[inIndex]['list_name'] + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# ユーザIDの取得
		wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inScreenName=gVal.ARR_ListFavo[inIndex]['screen_name'] )
		if wUserInfoRes['Result']!=True :
			wRes['Reason'] = "Twitter Error: @" + gVal.ARR_ListFavo[inIndex]['screen_name']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		### IDの取得
		wUserID = str( wUserInfoRes['Responce']['id'] )
		
		#############################
		# リストIDの取得
		wListsRes = gVal.OBJ_Tw_IF.GetListID(
		   inListName=gVal.ARR_ListFavo[inIndex]['list_name'],
		   inScreenName=gVal.ARR_ListFavo[inIndex]['screen_name'] )
		
		if wListsRes['Result']!=True :
			wRes['Reason'] = "Twitter Error: GetListID"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		### List IDの取得
		wListID = str( wListsRes['Responce'] )
		
		#############################
		# 自動いいね
		wResFavo = self.AutoFavo( wUserInfoRes['Responce'], gVal.DEF_STR_TLNUM['forAutoFavoListFavoSec'], gVal.ARR_ListFavo[inIndex]['follow'], gVal.ARR_ListFavo[inIndex]['sensitive'], wListID )
		if wResFavo['Result']!=True :
			wRes['Reason'] = "Twitter Error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
			wResult['timeline'] += wResFavo['Responce']['timeline']
			wResult['run']      += wResFavo['Responce']['run']
			wResult['agent']    += wResFavo['Responce']['agent']
			wResult['cnt']      += wResFavo['Responce']['cnt']
		
		#############################
		# 取得結果の表示
		wStr = ""
		if inFLG_FirstDisp==False :
			wStr = "------------------------------" + '\n'
		wStr = wStr + "抽出タイムライン数 : " + str( wResult['timeline'] )+ '\n'
		wStr = wStr + "いいね抽出数       : " + str( wResult['cnt'] )+ '\n'
		wStr = wStr + "  いいね候補数     : " + str( wResult['agent'] )+ '\n'
		wStr = wStr + "  いいね実施数     : " + str( wResult['run'] )+ '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# フォロワーいいね
#####################################################
	def FollowerFavo( self, inFLG_FirstDisp=True, inTest=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "FollowerFavo"
		
		self.ARR_FavoUserID = []
		self.ARR_OverFavoUserID = []
		self.ARR_RandUserID = []
		#############################
		# フォロワー支援いいね
		# ・相互フォローリストかつ相互フォロー
		#     〇 フォロワーモード・ショート
		# ・相互フォローリストかつ片フォロー者
		#     〇 フォロワーモード・相互リスト・ショート
		# ・片フォロワーリストかつ期間内
		#     △ 外部いいねモード・ロング
		# ・片フォロワーリストかつ期間外
		#     〇 フォロワーモード・片フォローリスト・ロング
		# ・相互フォロー
		#     〇 フォロワーモード・ショート
		# ・フォロワーかつ期間内
		#     △ 外部いいねモード・ロング
		# ・フォロワーかつ期間外
		#     〇 フォロワーモード・ロング
		# ・禁止・VIP
		#     × スキップ
		
		#############################
		# 取得可能時間か？
		wGetLag = CLS_OSIF.sTimeLag( str( gVal.STR_Time['flfavo'] ), inThreshold=gVal.DEF_STR_TLNUM['forFollowerFavoSec'] )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wGetLag['Beyond']==False and inTest==False:
			### 規定以内は除外
			wStr = "●フォロワー支援いいね期間外 処理スキップ: 次回処理日時= " + str(wGetLag['RateTime']) + '\n'
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
		#############################
		# 相互いいね停止中か？
		if gVal.STR_UserInfo['mfvstop']==True :
			wGetLag = CLS_OSIF.sTimeLag( str( gVal.STR_UserInfo['mfvstop_date'] ), inThreshold=gVal.DEF_STR_TLNUM['forMultiFavoStopReleaseSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==True :
				### 規定外は解除
				
				#############################
				# 相互いいね停止設定 解除
				wSubRes = gVal.OBJ_DB_IF.SetMfvStop( inSet=False )
				if wSubRes['Result']!=True :
					wRes['Reason'] = "SetMfvStop is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			if gVal.STR_UserInfo['mfvstop']==True :
				wStr = "● 相互いいね停止中"
				CLS_OSIF.sPrn( wStr )
		
		wResult = {
			"timeline"	: 0,		# タイムライン取得数
			"run"		: 0,		# 実施数
			"agent"		: 0,		# 候補数
			"cnt"		: 0,		# 抽出数
			"no_cnt"	: 0,		# 除外数
			
			"myfollow"	: 0,	#相互フォロー、フォロー者 処理数
			"follower"	: 0,	#片フォロワー 処理数
			"overuser"	: 0		#外部いいね   処理数
			
		}
		
		wSTR_Param = {
			"Threshold"		: gVal.DEF_STR_TLNUM['defPeriodSec'],
			"Follower"		: True,
			"Sensitive"		: False,
			
			"set"			: False
		}
		
		#############################
		# 取得開始の表示
		if inFLG_FirstDisp==True :
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "フォロワー支援いいね実行中" )
		
		#############################
		# フォロー情報取得
		wARR_FollowData = gVal.OBJ_Tw_IF.GetFollowerData()
		
		#############################
		# フォロー、フォロワー含まないリストへの
		# フォロワーへのいいね支援
		wMyfollowCnt = 0
		wKeylist = list( wARR_FollowData.keys() )
		for wUserID in wKeylist :
			wUserID = str(wUserID)
			
			### 禁止・VIPの場合 スキップ
			###   相互フォローリスト、片フォローリストに未登録か
			if self.OBJ_Parent.CheckVIPUser( wARR_FollowData[wUserID] )==True :
				if gVal.OBJ_Tw_IF.CheckMutualListUser( wUserID )==False and \
				   gVal.OBJ_Tw_IF.CheckFollowListUser( wUserID )==False :
					###対象 =除外
					wFLG_ZanCountSkip = True
					continue
			
			#############################
			# DBからいいね情報を取得する(1個)
			wDBRes = gVal.OBJ_DB_IF.GetFavoDataOne( wARR_FollowData[wUserID], inFLG_New=False )
			if wDBRes['Result']!=True :
				###失敗
				wRes['Reason'] = "GetFavoDataOne is failed"
				gVal.OBJ_L.Log( "B", wRes )
				continue
			### DB未登録ならスキップ
			if wDBRes['Responce']['Data']==None :
				continue
			wARR_DBData = wDBRes['Responce']['Data']
			
			#############################
			# ユーザレベル除外
###			if wARR_DBData['level_tag']=="C-" or wARR_DBData['level_tag']=="D-" or wARR_DBData['level_tag']=="E+" or wARR_DBData['level_tag']=="E-" or \
###			   wARR_DBData['level_tag']=="F+" or wARR_DBData['level_tag']=="H-" or \
###			   wARR_DBData['level_tag']=="L" or wARR_DBData['level_tag']=="Z" or wARR_DBData['level_tag']=="Z-" :
			if wARR_DBData['level_tag']=="C-" or wARR_DBData['level_tag']=="D-" or wARR_DBData['level_tag']=="E+" or wARR_DBData['level_tag']=="E-" or \
			   wARR_DBData['level_tag']=="G" or wARR_DBData['level_tag']=="G-" or \
			   wARR_DBData['level_tag']=="L" or wARR_DBData['level_tag']=="Z" :
				
				wStr = "▲レベルタグ除外: level=" + wARR_DBData['level_tag'] + " user=" + wARR_FollowData[wUserID]['screen_name']
				CLS_OSIF.sPrn( wStr )
				###
				wResult['no_cnt'] += 1
				continue
			
###			#############################
###			# 非絡みユーザ除外
###			if wARR_DBData['level_tag']=="G" or wARR_DBData['level_tag']=="G+" or wARR_DBData['level_tag']=="H" or wARR_DBData['level_tag']=="H+" :
###				### いいね実行からの期間チェック
###				wGetLag = CLS_OSIF.sTimeLag( str( wARR_DBData['pfavo_date'] ), inThreshold=gVal.DEF_STR_TLNUM['forFollowerFavoNonFollowerSec'] )
###				if wGetLag['Result']!=True :
###					wRes['Reason'] = "sTimeLag failed"
###					gVal.OBJ_L.Log( "B", wRes )
###					continue
###				#############################
###				# いいね実行から期間内
###				if wGetLag['Beyond']==False :
###					wStr = "▲非絡みユーザ除外(期間内): level=" + wARR_DBData['level_tag'] + " user=" + wARR_FollowData[wUserID]['screen_name']
###					CLS_OSIF.sPrn( wStr )
###					###
###					wResult['no_cnt'] += 1
###					continue
###				
			#############################
			# Bot判定ユーザ除外
			#   長期間だけど定期的にいいねはする
###			if wARR_DBData['renfavo_cnt']>gVal.DEF_STR_TLNUM['renFavoBotCnt'] :
			if wARR_DBData['renfavo_cnt']>gVal.DEF_STR_TLNUM['renFavoBotNoactionCnt'] :
				if wARR_DBData['level_tag']=="A+" or wARR_DBData['level_tag']=="A" :
					### 公式botの場合は、拒否
					wStr = "▲Bot判定ユーザ除外除外(無条件無視): level=" + wARR_DBData['level_tag'] + " user=" + wARR_FollowData[wUserID]['screen_name']
					CLS_OSIF.sPrn( wStr )
					###
					wResult['no_cnt'] += 1
					continue
				else:
					### フォロワーbotの場合、長期間ごとにいいねする
					wGetLag = CLS_OSIF.sTimeLag( str( wARR_DBData['pfavo_date'] ), inThreshold=gVal.DEF_STR_TLNUM['forRenFavoBotFavoSec'] )
					if wGetLag['Result']!=True :
						wRes['Reason'] = "sTimeLag failed"
						gVal.OBJ_L.Log( "B", wRes )
						return wRes
					if wGetLag['Beyond']==False :
						### 期間内 =除外
						wStr = "▲Bot判定ユーザ除外除外(無条件無視): level=" + wARR_DBData['level_tag'] + " user=" + wARR_FollowData[wUserID]['screen_name']
						CLS_OSIF.sPrn( wStr )
						###
						wResult['no_cnt'] += 1
						continue
			
			#############################
			# 既に除外済み
			elif wUserID in self.ARR_RandUserID :
				wStr = "▲Bot判定ユーザ除外除外(ランダム選出済): level=" + wARR_DBData['level_tag'] + " user=" + wARR_FollowData[wUserID]['screen_name']
				CLS_OSIF.sPrn( wStr )
				###
				wResult['no_cnt'] += 1
				continue
			
			elif wARR_DBData['renfavo_cnt']>gVal.DEF_STR_TLNUM['renFavoBotCnt'] :
				#############################
				# ランダム除外
				wRand = CLS_OSIF.sGetRand(100)
###				if wRand>=gVal.DEF_STR_TLNUM['forFollowerFavoNonFollowerCnt'] :
				if wRand>=gVal.DEF_STR_TLNUM['forRenFavoReiineRand'] :
					### 乱数による拒否
					wStr = "▲Bot判定ユーザ除外除外(ランダム): level=" + wARR_DBData['level_tag'] + " user=" + wARR_FollowData[wUserID]['screen_name']
					CLS_OSIF.sPrn( wStr )
					###
					wResult['no_cnt'] += 1
					self.ARR_RandUserID.append( wUserID )
					continue
			
			#############################
			# 相互フォローリストかつ相互フォロー
			if gVal.OBJ_Tw_IF.CheckMutualListUser( wUserID )==True and \
			   wARR_FollowData[wUserID]['follower']==True and \
			   gVal.STR_UserInfo['AutoRemove']==True :
				if wARR_DBData['pfavo_cnt']==0 :
					wSTR_Param['Threshold'] = 0
					wSTR_Param['Follower']  = True	### フォロワーモード
					wSTR_Param['Sensitive'] = True
					wSTR_Param['set']       = True
					###
					wStr = "〇相互フォローリスト: 〇相互フォロー(初回): user=" + str( wARR_FollowData[wUserID]['screen_name'] )
					CLS_OSIF.sPrn( wStr )
					wResult['myfollow'] += 1
				else:
					if gVal.STR_UserInfo['mfvstop']==True :
						wSTR_Param['Threshold'] = gVal.DEF_STR_TLNUM['forFollowerFavoMListMutualSec']
						wSTR_Param['Follower']  = True	### フォロワーモード
						wSTR_Param['Sensitive'] = True
						wSTR_Param['set']       = True
						###
						wStr = "〇相互フォローリスト: 〇相互フォロー: user=" + str( wARR_FollowData[wUserID]['screen_name'] )
						CLS_OSIF.sPrn( wStr )
						wResult['myfollow'] += 1
			
			#############################
			# 相互フォローリストかつ片フォロー者
			elif gVal.OBJ_Tw_IF.CheckMutualListUser( wUserID )==True and \
			     wARR_FollowData[wUserID]['follower']==False and \
			     gVal.STR_UserInfo['AutoRemove']==True :
				if wARR_DBData['pfavo_cnt']==0 :
					wSTR_Param['Threshold'] = 0
					wSTR_Param['Follower']  = True	### フォロワーモード
					wSTR_Param['Sensitive'] = True
					wSTR_Param['set']       = True
					###
					wStr = "〇相互フォローリスト: ●片フォロー者(初回): user=" + str( wARR_FollowData[wUserID]['screen_name'] )
					CLS_OSIF.sPrn( wStr )
					wResult['myfollow'] += 1
				else:
					if gVal.STR_UserInfo['mfvstop']==True :
						wSTR_Param['Threshold'] = gVal.DEF_STR_TLNUM['forFollowerFavoMListMyFollowSec']
						wSTR_Param['Follower']  = True	### フォロワーモード
						wSTR_Param['Sensitive'] = True
						wSTR_Param['set']       = True
						###
						wStr = "〇相互フォローリスト: ●片フォロー者: user=" + str( wARR_FollowData[wUserID]['screen_name'] )
						CLS_OSIF.sPrn( wStr )
						wResult['myfollow'] += 1
			
			elif gVal.OBJ_Tw_IF.CheckFollowListUser( wUserID )==True and \
			     gVal.STR_UserInfo['AutoRemove']==True :
				#############################
				# いいねしたことなければ1回だけフォロワーモードでいいねする
				if wARR_DBData['pfavo_cnt']==0 :
					wSTR_Param['Threshold'] = 0
					wSTR_Param['Follower']  = True	### フォロワーモード
					wSTR_Param['Sensitive'] = False
					wSTR_Param['set']       = True
					###
					wStr = "●片フォロワーリスト: 初回: user=" + str( wARR_FollowData[wUserID]['screen_name'] )
					CLS_OSIF.sPrn( wStr )
					wResult['follower'] += 1
				else:
					wGetLag = CLS_OSIF.sTimeLag( str( wARR_DBData['rfavo_date'] ), inThreshold=gVal.DEF_STR_TLNUM['forFollowerFavoFListSec'] )
					if wGetLag['Result']!=True :
						wRes['Reason'] = "sTimeLag failed"
						gVal.OBJ_L.Log( "B", wRes )
						continue
					#############################
					# 片フォロワーリストかつ期間内
					if wGetLag['Beyond']==False :
						if gVal.STR_UserInfo['mfvstop']==True :
							wSTR_Param['Threshold'] = gVal.DEF_STR_TLNUM['forFollowerFavoFListIntimeSec']
							wSTR_Param['Follower']  = False	### 外部いいねモード
							wSTR_Param['Sensitive'] = False
							wSTR_Param['set']       = True
							###
							wStr = "●片フォロワーリスト: 〇期間内: user=" + str( wARR_FollowData[wUserID]['screen_name'] )
							CLS_OSIF.sPrn( wStr )
							wResult['overuser'] += 1
					
					#############################
					# 片フォロワーリストかつ期間外
					else:
						if gVal.STR_UserInfo['mfvstop']==True :
							### いいね実行からの期間チェック
							wGetLag = CLS_OSIF.sTimeLag( str( wARR_DBData['pfavo_date'] ), inThreshold=gVal.DEF_STR_TLNUM['forFollowerFavoFListpfavoSec'] )
							if wGetLag['Result']!=True :
								wRes['Reason'] = "sTimeLag failed"
								gVal.OBJ_L.Log( "B", wRes )
								continue
							#############################
							# いいね実行から期間内
							if wGetLag['Beyond']==False :
								### 今週いいねありならいいねする
								if wARR_DBData['rfavo_n_cnt']>=1 :
									wSTR_Param['Threshold'] = gVal.DEF_STR_TLNUM['forFollowerFavoFListOverSec']
									wSTR_Param['Follower']  = True	### フォロワーモード
									wSTR_Param['Sensitive'] = False
									wSTR_Param['set']       = True
									###
									wStr = "●片フォロワーリスト: ●期間外: user=" + str( wARR_FollowData[wUserID]['screen_name'] )
									CLS_OSIF.sPrn( wStr )
								### 今週いいねないなら、外部いいねする
								else:
									wSTR_Param['Threshold'] = gVal.DEF_STR_TLNUM['forFollowerFavoFListIntimeSec']
									wSTR_Param['Follower']  = False	### 外部いいねモード
									wSTR_Param['Sensitive'] = False
									wSTR_Param['ListID']    = None
									wSTR_Param['set']       = True
									###
									wStr = "●片フォロワーリスト: ▼期間外(外部): user=" + str( wARR_FollowData[wUserID]['screen_name'] )
									CLS_OSIF.sPrn( wStr )
							
							else:
								wSTR_Param['Threshold'] = gVal.DEF_STR_TLNUM['forFollowerFavoFListOverSec']
								wSTR_Param['Follower']  = True	### フォロワーモード
								wSTR_Param['Sensitive'] = False
								wSTR_Param['set']       = True
								###
								wStr = "●片フォロワーリスト: ●期間外: user=" + str( wARR_FollowData[wUserID]['screen_name'] )
								CLS_OSIF.sPrn( wStr )
							
							wResult['follower'] += 1
			
			elif wARR_FollowData[wUserID]['follower']==True :
				#############################
				# 相互フォロー
				if wARR_FollowData[wUserID]['myfollow']==True :
					wSTR_Param['Threshold'] = gVal.DEF_STR_TLNUM['forFollowerFavoMutualSec']
					wSTR_Param['Follower']  = True	### フォロワーモード
					wSTR_Param['Sensitive'] = True
					wSTR_Param['set']       = True
					###
					wStr = "▽相互フォロー: user=" + str( wARR_FollowData[wUserID]['screen_name'] )
					CLS_OSIF.sPrn( wStr )
					wResult['myfollow'] += 1
				
				#############################
				# フォロワー
				else:
					### DBからいいね情報を取得する(1個)
					wDBRes = gVal.OBJ_DB_IF.GetFavoDataOne( wARR_FollowData[wUserID], inFLG_New=False )
					if wDBRes['Result']!=True :
						###失敗
						wRes['Reason'] = "GetFavoDataOne is failed(2)"
						gVal.OBJ_L.Log( "B", wRes )
						continue
					### DB未登録ならスキップ
					if wDBRes['Responce']['Data']==None :
						continue
					wARR_DBData = wDBRes['Responce']['Data']
					
					#############################
					# いいねしたことなければ1回だけフォロワーモードでいいねする
					if wARR_DBData['pfavo_cnt']==0 :
						wSTR_Param['Threshold'] = gVal.DEF_STR_TLNUM['forFollowerFavoOverSec']
						wSTR_Param['Follower']  = True	### フォロワーモード
						wSTR_Param['Sensitive'] = False
						wSTR_Param['set']       = True
						###
						wStr = "▼フォロワー: 初回: user=" + str( wARR_FollowData[wUserID]['screen_name'] )
						CLS_OSIF.sPrn( wStr )
						wResult['follower'] += 1
					else:
						wGetLag = CLS_OSIF.sTimeLag( str( wARR_DBData['rfavo_date'] ), inThreshold=gVal.DEF_STR_TLNUM['forFollowerFavoFollowerSec'] )
						if wGetLag['Result']!=True :
							wRes['Reason'] = "sTimeLag failed"
							gVal.OBJ_L.Log( "B", wRes )
							continue
						
						#############################
						# フォロワーかつ期間内
						if wGetLag['Beyond']==False :
							wSTR_Param['Threshold'] = gVal.DEF_STR_TLNUM['forFollowerFavoIntimeSec']
							wSTR_Param['Follower']  = False	### 外部いいねモード
							wSTR_Param['Sensitive'] = False
							wSTR_Param['set']       = True
							###
							wStr = "▼フォロワー: 〇期間内: user=" + str( wARR_FollowData[wUserID]['screen_name'] )
							CLS_OSIF.sPrn( wStr )
							wResult['overuser'] += 1
						
						#############################
						# フォロワーかつ期間外
						else:
							wSTR_Param['Threshold'] = gVal.DEF_STR_TLNUM['forFollowerFavoOverSec']
							wSTR_Param['Follower']  = True	### フォロワーモード
							wSTR_Param['Sensitive'] = True
							wSTR_Param['set']       = True
							###
							wStr = "▼フォロワー: ●期間外: user=" + str( wARR_FollowData[wUserID]['screen_name'] )
							CLS_OSIF.sPrn( wStr )
							wResult['follower'] += 1
			
			#############################
			# 片フォロー者
			elif wARR_FollowData[wUserID]['myfollow']==True :
				#############################
				# 前回いいね実施から期間内なら除外
				wGetLag = CLS_OSIF.sTimeLag( str( wARR_DBData['pfavo_date'] ), inThreshold=gVal.DEF_STR_TLNUM['forFollowerFavoHarfMyfollowRunSec'] )
				if wGetLag['Result']!=True :
					wRes['Reason'] = "sTimeLag failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				if wGetLag['Beyond']==False :
					### 期間内 =除外
					continue
				
				### 最初の10回は通して、それ以降はランダム抽選する
				### 7割りは切り捨て
				if wMyfollowCnt>=gVal.DEF_STR_TLNUM['forFollowerFavoHarfMyfollowCnt'] :
					wRand = CLS_OSIF.sGetRand(100)
					if wRand>=gVal.DEF_STR_TLNUM['forFollowerFavoHarfMyfollowRand'] :
						continue
				
				wMyfollowCnt += 1
				wSTR_Param['Threshold'] = gVal.DEF_STR_TLNUM['forFollowerFavoHarfMyfollowSec']
				wSTR_Param['Follower']  = True	### フォロワーモード
				wSTR_Param['Sensitive'] = True
				wSTR_Param['set']       = True
				###
				wStr = "▽片フォロー者: " +str(wMyfollowCnt) + "個目: user=" + str( wARR_FollowData[wUserID]['screen_name'] )
				CLS_OSIF.sPrn( wStr )
				wResult['myfollow'] += 1
			
			else:
				continue
			
			if wSTR_Param['set']==True :
				#############################
				# 自動いいね実行
				wResFavo = self.AutoFavo( wARR_FollowData[wUserID], wSTR_Param['Threshold'], wSTR_Param['Follower'], wSTR_Param['Sensitive'] )
				if wResFavo['Result']!=True :
					wRes['Reason'] = "Twitter Error"
					gVal.OBJ_L.Log( "B", wRes )
					continue
				
				wResult['timeline'] += wResFavo['Responce']['timeline']
				wResult['run']      += wResFavo['Responce']['run']
				wResult['agent']    += wResFavo['Responce']['agent']
				wResult['cnt']      += wResFavo['Responce']['cnt']
		
 		#############################
		# 取得結果の表示
		wStr = ""
		if inFLG_FirstDisp==False :
			wStr = "------------------------------" + '\n'
		wStr = wStr + "抽出タイムライン数 : " + str( wResult['timeline'] )+ '\n'
		wStr = wStr + "いいね抽出数       : " + str( wResult['cnt'] )+ '\n'
		wStr = wStr + "  いいね候補数     : " + str( wResult['agent'] )+ '\n'
		wStr = wStr + "  いいね実施数     : " + str( wResult['run'] )+ '\n'
		wStr = wStr + "相互・片フォロー者 : " + str( wResult['myfollow'] )+ '\n'
		wStr = wStr + "片フォロワー       : " + str( wResult['follower'] )+ '\n'
		wStr = wStr + "外部いいね         : " + str( wResult['overuser'] )+ '\n'
		wStr = wStr + "除外数             : " + str( wResult['no_cnt'] )+ '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 現時間を設定
		wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "flfavo", gVal.STR_Time['TimeDate'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "SetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		###	gVal.STR_Time['flfavo']
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# 自動いいね
#####################################################
	def AutoFavo( self, inData, inThreshold, inFLG_Follower=True, inFLG_Sensitive=False, inListID=None ):
		#############################
		# inFLG_Follower  =フォロー者、フォロワーを含める
		#                    True= フォロワーモード：フォロー者、フォロワーを含め、リツイート、引用リツイートを含めない
		#                          フォロー者、フォロワーがない場合、リツイート、引用リツイートをいいねする
		#                    False=外部いいねモード：フォロー者、フォロワーを含めない。リツイート、引用リツイートをいいねする
		# inFLG_Sensitive =センシティブツイートを含める
		#                    True=含める
		
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "AutoFavo"
		
		#############################
		# いいね状態
		wRes['Responce'] = {
			"timeline"			: 0,		# タイムライン取得数
			"run"				: 0,		# 実施数
			"agent"				: 0,		# 候補数
			"cnt"				: 0			# 抽出数
		}
		
		wUserID = str( inData['id'] )
		
		#############################
		# 検索ユーザ表示
		wStr = "  自動いいね 検索中: user=" + str( inData['screen_name'] )
		CLS_OSIF.sPrn( wStr )
		
		if inListID==None :
			#############################
			# ユーザタイムラインを取得
			wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="user", inFLG_Rep=False, inFLG_Rts=True,
				 inID=wUserID, inCount=gVal.DEF_STR_TLNUM['getUserTimeLine'] )
			if wTweetRes['Result']!=True :
				wRes['Reason'] = "Twitter Error: GetTL(user timeline)"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		else:
			#############################
			# リストタイムラインを取得する
			wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="list", inFLG_Rep=False, inFLG_Rts=True,
				 inID=wUserID, inListID=inListID, inCount=gVal.DEF_STR_TLNUM['getUserTimeLine'] )
			if wTweetRes['Result']!=True :
				wRes['Reason'] = "Twitter Error: GetTL(list timeline)"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		if len(wTweetRes['Responce'])==0 :
			### ツイートなし
			wRes['Result'] = True
			return wRes
		wRes['Responce']['timeline'] = len(wTweetRes['Responce'])
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wTweetRes['Responce'] ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
		wFavoID = None	#いいね対象ツイートID
		wARR_Tweet = {}
		wFLG_ZanCountSkip = False
		for wTweet in wTweetRes['Responce'] :
			###ウェイトカウントダウン
			if self.OBJ_Parent.Wait_Next( inZanCountSkip=wFLG_ZanCountSkip )==False :
				break	###ウェイト中止
			wFLG_ZanCountSkip = False
			
			#############################
			# ツイートj情報を丸めこむ
			wTweetID = str( wTweet['id'] )
			wSTR_User = {		#ツイート元ユーザ
				"id"				: None,
				"name"				: None,
				"screen_name"		: None,
				"description"		: None
			}
			wSTR_SrcUser = {	#リツイートしたユーザ
				"id"				: None,
				"name"				: None,
				"screen_name"		: None,
				"description"		: None
			}
			wSTR_Tweet = {
				"kind"				: None,
				"id"				: wTweetID,
				"retweet_id"		: None,
				"text"				: wTweet['text'],
				"sensitive"			: False,
				"created_at"		: None,
				"user"				: wSTR_User,
				"src_user"			: wSTR_SrcUser,
				"FLG_agent"			: False,			# いいね候補
				"reason"			: None				# NG理由
			}
			
			### リツイート
			if "retweeted_status" in wTweet :
###				wSTR_Tweet['kind'] = "retweet"
				if wSTR_Tweet['text'].find("@")>=0 or wTweet['in_reply_to_status_id']!=None :
					wSTR_Tweet['kind'] = "reply"
				else:
					wSTR_Tweet['kind'] = "retweet"
				
				wSTR_Tweet['created_at'] = str(wTweet['retweeted_status']['created_at'])
				wSTR_Tweet['retweet_id'] = str(wTweet['retweeted_status']['id'])
				
				### リツイ元に置き換え
				wTweetID = str(wTweet['retweeted_status']['id'])
				wSTR_Tweet['id'] = wTweetID
				wSTR_Tweet['created_at'] = str(wTweet['retweeted_status']['created_at'])
				
				wSTR_Tweet['user']['id']   = str( wTweet['retweeted_status']['user']['id'] )
				wSTR_Tweet['user']['name'] = wTweet['retweeted_status']['user']['name'].replace( "'", "''" )
				wSTR_Tweet['user']['screen_name'] = wTweet['retweeted_status']['user']['screen_name']
				wSTR_Tweet['user']['description'] = wTweet['retweeted_status']['user']['description']
				
				wSTR_Tweet['src_user']['id']   = str( wTweet['user']['id'] )
				wSTR_Tweet['src_user']['name'] = wTweet['user']['name'].replace( "'", "''" )
				wSTR_Tweet['src_user']['screen_name'] = wTweet['user']['screen_name']
				wSTR_Tweet['src_user']['description'] = wTweet['user']['description']
			
			### 引用リツイート
			elif "quoted_status" in wTweet :
###				wSTR_Tweet['kind'] = "quoted"
				if wSTR_Tweet['text'].find("@")>=0 or wTweet['in_reply_to_status_id']!=None :
					wSTR_Tweet['kind'] = "reply"
				else:
					wSTR_Tweet['kind'] = "quoted"
				
				wSTR_Tweet['created_at'] = str(wTweet['quoted_status']['created_at'])
				wSTR_Tweet['retweet_id'] = str(wTweet['quoted_status']['id'])
				
				### リツイ元に置き換え
				wTweetID = str(wTweet['quoted_status']['id'])
				wSTR_Tweet['id'] = wTweetID
				wSTR_Tweet['created_at'] = str(wTweet['quoted_status']['created_at'])
				
				wSTR_Tweet['user']['id']   = str( wTweet['quoted_status']['user']['id'] )
				wSTR_Tweet['user']['name'] = wTweet['quoted_status']['user']['name'].replace( "'", "''" )
				wSTR_Tweet['user']['screen_name'] = wTweet['quoted_status']['user']['screen_name']
				wSTR_Tweet['user']['description'] = wTweet['quoted_status']['user']['description']
				
				wSTR_Tweet['src_user']['id']   = str( wTweet['user']['id'] )
				wSTR_Tweet['src_user']['name'] = wTweet['user']['name'].replace( "'", "''" )
				wSTR_Tweet['src_user']['screen_name'] = wTweet['user']['screen_name']
				wSTR_Tweet['src_user']['description'] = wTweet['user']['description']
			
			### リプライ
###			elif wSTR_Tweet['text'].find("@")>=0 :
###			elif wSTR_Tweet['text'].find("@")>=0 or wTweet['in_reply_to_status_id']==None :
			elif wSTR_Tweet['text'].find("@")>=0 or wTweet['in_reply_to_status_id']!=None :
				wSTR_Tweet['kind'] = "reply"
				wSTR_Tweet['created_at'] = str(wTweet['created_at'])
				
				wSTR_Tweet['user']['id']   = str( wTweet['user']['id'] )
				wSTR_Tweet['user']['name'] = wTweet['user']['name'].replace( "'", "''" )
				wSTR_Tweet['user']['screen_name'] = wTweet['user']['screen_name']
				wSTR_Tweet['user']['description'] = wTweet['user']['description']
			
			### 通常ツイート
			else:
				wSTR_Tweet['kind'] = "normal"
				wSTR_Tweet['created_at'] = str(wTweet['created_at'])
				
				wSTR_Tweet['user']['id']   = str( wTweet['user']['id'] )
				wSTR_Tweet['user']['name'] = wTweet['user']['name'].replace( "'", "''" )
				wSTR_Tweet['user']['screen_name'] = wTweet['user']['screen_name']
				wSTR_Tweet['user']['description'] = wTweet['user']['description']
			
			#############################
			# ●配列に格納●
			wARR_Tweet.update({ wTweetID : wSTR_Tweet })
			wRes['Responce']['cnt'] += 1
			
			### 日時の変換
			wTime = CLS_TIME.sTTchg( wRes, "(1)", wSTR_Tweet['created_at'] )
			if wTime['Result']!=True :
				wSTR_Tweet['reason'] = "時刻変換失敗"
				continue
			wSTR_Tweet['created_at'] = wTime['TimeDate']
			
			#############################
			# リツイ元が自分の場合は除外
			if wSTR_Tweet['kind']=="retweet" or wSTR_Tweet['kind']=="quoted" :
				if wSTR_Tweet['src_user']['id']==str(gVal.STR_UserInfo['id']) :
					### 自分は除外
					wSTR_Tweet['reason'] = "リツイ元が自分"
					wFLG_ZanCountSkip = True
					continue
			
			#############################
			# リツイ元で同一ユーザへの処理は除外
			if wSTR_Tweet['kind']=="retweet" or wSTR_Tweet['kind']=="quoted" :
				if wSTR_Tweet['src_user']['id'] in self.ARR_OverFavoUserID :
					### リツイ元同一ユーザ検出 =終了
					wSTR_Tweet['reason'] = "リツイ元が同一ユーザ"
					wFLG_ZanCountSkip = True
					continue
			
			else:
				### ユーザをメモする
				self.ARR_OverFavoUserID.append( wSTR_Tweet['src_user']['id'] )
			
			#############################
			# いいね一覧にあるいいねの重複があるか
			wFavoRes = gVal.OBJ_Tw_IF.CheckFavoUserID( wSTR_Tweet['id'] )
			if wFavoRes!=True :
				### いいね重複あり 除外
				wSTR_Tweet['reason'] = "いいね済ツイート"
				wFLG_ZanCountSkip = True
				continue
			else:
				### リツイート、引用リツイートの場合
				### リツイ元IDもチェックする
				if wSTR_Tweet['kind']=="retweet" or wSTR_Tweet['kind']=="quoted" :
					wFavoRes = gVal.OBJ_Tw_IF.CheckFavoUserID( wSTR_Tweet['retweet_id'] )
					if wFavoRes!=True :
						### いいね重複あり 除外
						wSTR_Tweet['reason'] = "いいね済ツイート(リツイ元)"
						wFLG_ZanCountSkip = True
						continue
			
			#############################
			# いいね一覧にあるユーザ
			wFavoUser = wSTR_Tweet['user']
			
			wSubRes = gVal.OBJ_Tw_IF.CheckFavoUser( wFavoUser['id'] )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter Error: CheckFavoUser"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wSubRes['Responce']==True :
				### いいね済み
				wSTR_Tweet['reason'] = "いいね済ユーザ"
				if inListID!=None :
					### リストいいねの場合はスキップ
					wFLG_ZanCountSkip = True
					continue
				else:
					break
			
			#############################
			# リプライの場合は除外
			#   リプはいいねしない
			if wSTR_Tweet['kind']=="reply" :
				wSTR_Tweet['reason'] = "リプライ"
				wFLG_ZanCountSkip = True
				continue
			
			#############################
			# センシティブなツイートは除外
			if "possibly_sensitive" in wTweet :
				if str(wTweet['possibly_sensitive'])=="true" :
					wSTR_Tweet['sensitive'] = True
			
			if inFLG_Sensitive==False and wSTR_Tweet['sensitive']==True :
				wSTR_Tweet['reason'] = "センシティブ"
				wFLG_ZanCountSkip = True
				continue
			
			#############################
			# 期間を過ぎたツイートは除外
			wGetLag = CLS_OSIF.sTimeLag( str( wSTR_Tweet['created_at'] ), inThreshold=gVal.DEF_STR_TLNUM['forAutoFavoTweetSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==True :
				### 規定外 =古いツイートなので除外
				wSTR_Tweet['reason'] = "古いツイート"
				wFLG_ZanCountSkip = True
				continue
			
			#############################
			# 禁止ユーザは除外
			wExtUserRes = self.OBJ_Parent.CheckExtUser( wFavoUser, "自動いいね" )
			if wExtUserRes['Result']!=True :
				wRes['Reason'] = "CheckExtUser failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wExtUserRes['Responce']==False :
				### 禁止あり=除外
				wSTR_Tweet['reason'] = "禁止ユーザ"
				if inListID!=None :
					### リストいいねの場合はスキップ
					wFLG_ZanCountSkip = True
					continue
				else:
					break
			
			#############################
			# 禁止文字を含む場合は除外
			
			### 外部いいねモードの場合
			### プロフ文字
###			if inFLG_Follower==False :
###				wWordRes = self.OBJ_Parent.CheckExtProf( wFavoUser, wFavoUser['description'] )
###				if wWordRes['Result']!=True :
###					wRes['Reason'] = "CheckExtProf failed(description)"
###					gVal.OBJ_L.Log( "B", wRes )
###					return wRes
###				if wWordRes['Responce']==False :
###					wFLG_ZanCountSkip = True
###					wSTR_Tweet['reason'] = "禁止文字（プロフ）"
###					if inListID!=None :
###						### リストいいねの場合はスキップ
###						wFLG_ZanCountSkip = True
###						continue
###					else:
###						break
###			
			### ツイート文
			wWordRes = self.OBJ_Parent.CheckExtWord( wFavoUser, wSTR_Tweet['text'] )
			if wWordRes['Result']!=True :
				wRes['Reason'] = "CheckExtWord failed(tweet text)"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wWordRes['Responce']==False :
				wFLG_ZanCountSkip = True
				wSTR_Tweet['reason'] = "禁止文字（ツイート）"
				continue
			
			#############################
			# DBからいいね情報を取得する(1個)
			wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( wFavoUser, inFLG_New=False )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "GetFavoDataOne is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wSubRes['Responce']['Data']!=None :
				wARR_DBData = wSubRes['Responce']['Data']
				#############################
				# レベルタグによる除外
###				if wARR_DBData['level_tag']=="C-" or wARR_DBData['level_tag']=="D-" or wARR_DBData['level_tag']=="E+" or wARR_DBData['level_tag']=="E-" or \
###				   wARR_DBData['level_tag']=="F+" or wARR_DBData['level_tag']=="G" or wARR_DBData['level_tag']=="G-" :
###				if wARR_DBData['level_tag']=="C-" or wARR_DBData['level_tag']=="D-" or wARR_DBData['level_tag']=="E+" or wARR_DBData['level_tag']=="E-" or \
###				   wARR_DBData['level_tag']=="H-" or wARR_DBData['level_tag']=="L" or wARR_DBData['level_tag']=="Z" or wARR_DBData['level_tag']=="Z-" :
				if wARR_DBData['level_tag']=="C-" or wARR_DBData['level_tag']=="D-" or wARR_DBData['level_tag']=="E+" or wARR_DBData['level_tag']=="E-" or \
				   wARR_DBData['level_tag']=="G" or wARR_DBData['level_tag']=="G-" or wARR_DBData['level_tag']=="L" or wARR_DBData['level_tag']=="Z" :
					
					wStr = "レベルタグ除外: level=" + wARR_DBData['level_tag'] + " user=" + wFavoUser['screen_name']
					wSTR_Tweet['reason'] = wStr
					wFLG_ZanCountSkip = True
					continue
				
###				#############################
###				# レベルタグによるランダム実行
###				if wARR_DBData['level_tag']=="B-" :
###					
###					wRand = CLS_OSIF.sGetRand(100)
###					if wRand>gVal.DEF_STR_TLNUM['forAutoFavoLevelRunRand'] :
###					if wRand>=gVal.DEF_STR_TLNUM['forAutoFavoLevelRunRand'] :
###						wStr = "レベルタグ乱数判定による除外: level=" + wARR_DBData['level_tag'] + " user=" + wFavoUser['screen_name']
###						wSTR_Tweet['reason'] = wStr
###						wFLG_ZanCountSkip = True
###						continue
###					
###					#############################
###					# 期間を過ぎたツイートは除外
###					wGetLag = CLS_OSIF.sTimeLag( str( wSTR_Tweet['created_at'] ), inThreshold=gVal.DEF_STR_TLNUM['forAutoFavoTweet_B_Sec'] )
###					if wGetLag['Result']!=True :
###						wRes['Reason'] = "sTimeLag failed"
###						gVal.OBJ_L.Log( "B", wRes )
###						return wRes
###					if wGetLag['Beyond']==True :
###						### 規定外 =古いツイートなので除外
###						wSTR_Tweet['reason'] = "レベルタグの古いツイート"
###						wFLG_ZanCountSkip = True
###						continue
###				
				#############################
				# 前回からのいいね期間内は除外
###				if wARR_DBData['pfavo_date']==gVal.DEF_NOTEXT :
				if wARR_DBData['pfavo_date']==gVal.DEF_NOTEXT or inThreshold!=0 :
					wGetLag = CLS_OSIF.sTimeLag( str( wARR_DBData['pfavo_date'] ), inThreshold=inThreshold )
					if wGetLag['Result']!=True :
						wRes['Reason'] = "sTimeLag failed"
						gVal.OBJ_L.Log( "B", wRes )
						return wRes
					if wGetLag['Beyond']==False :
						### 規定内は処理しない
						wStr = "いいね実施期間内" + " user=" + wFavoUser['screen_name']
						wSTR_Tweet['reason'] = wStr
						if inListID!=None :
							### リストいいねの場合はスキップ
							wFLG_ZanCountSkip = True
							continue
						else:
							break
			
			#############################
			# リツイート、引用リツイートは除外（フォロワーモードの場合除外）
			if inFLG_Follower==True :
				if wARR_Tweet[wTweetID]['kind']=="retweet" or wARR_Tweet[wTweetID]['kind']=="quoted" :
					wFLG_ZanCountSkip = True
					wSTR_Tweet['reason'] = "リツイート除外"
					continue
			
			#############################
			# フォロー者、フォロワーは除外（外部いいねモードの場合除外）
			if inFLG_Follower==False :
				if gVal.OBJ_Tw_IF.CheckMyFollow( wFavoUser['id'] )==True :
					wFLG_ZanCountSkip = True
					wSTR_Tweet['reason'] = "フォロー者"
					if inListID!=None :
						### リストいいねの場合はスキップ
						wFLG_ZanCountSkip = True
						continue
					else:
						break
				
				if gVal.OBJ_Tw_IF.CheckFollower( wFavoUser['id'] )==True :
					wFLG_ZanCountSkip = True
					wSTR_Tweet['reason'] = "フォロワー"
					if inListID!=None :
						### リストいいねの場合はスキップ
						wFLG_ZanCountSkip = True
						continue
					else:
						break
			
			# ※ほぼ確定
			#############################
			# 今処理で同一ユーザへの処理は除外
			if wSTR_Tweet['user']['id'] in self.ARR_FavoUserID :
				### 同一ユーザ検出
				wSTR_Tweet['reason'] = "同一ユーザ検出"
				wFLG_ZanCountSkip = True
				if inListID!=None :
					### リストいいねの場合はスキップ
					wFLG_ZanCountSkip = True
					continue
				else:
					break
				
			else:
				### ユーザをメモする
				self.ARR_FavoUserID.append( wSTR_Tweet['user']['id'] )
			
			# ※確定
			#############################
			# ●いいねツイート確定●
			wARR_Tweet[wTweetID]['FLG_agent'] = True
			wRes['Responce']['agent'] += 1
		
		#############################
		# フォロワーモード かつ 候補がない場合
		# リツイート、引用リツイートから候補を決める（再抽選）
		if inFLG_Follower==True and wRes['Responce']['agent']==0 :
			
			wStr = "  ::候補なしのためリツイートから再選出" + '\n'
			
			wKeylist2 = list( wARR_Tweet.keys() )
			for wIndex in wKeylist2 :
				wStr = wStr + "  id=" + str(wARR_Tweet[wIndex]['id'])
				wStr = wStr + " reason=" + wARR_Tweet[wIndex]['reason'] + '\n'
			
			CLS_OSIF.sPrn( wStr )
			
			wKeylist = list( wARR_Tweet.keys() )
			for wID in wKeylist :
				wID = str(wID)
				
				#############################
				# リツイート、引用リツイート以外は除外
				if wARR_Tweet[wID]['kind']!="retweet" and wARR_Tweet[wID]['kind']!="quoted" :
					continue
				
				#############################
				# ●いいねツイート確定●
				wARR_Tweet[wID]['FLG_agent'] = True
				wRes['Responce']['agent'] += 1
				break
		
		#############################
		# 候補なし
		if wRes['Responce']['agent']==0 :
			wStr = "  ::いいね候補なし" + '\n'
			
			wKeylist2 = list( wARR_Tweet.keys() )
			for wIndex in wKeylist2 :
				wStr = wStr + "  id=" + str(wARR_Tweet[wIndex]['id'])
				wStr = wStr + " reason=" + wARR_Tweet[wIndex]['reason'] + '\n'
			
			CLS_OSIF.sPrn( wStr )
			
			wRes['Result'] = True
			return wRes
		
		# ※処理確定
		wARR_FavoID = []
		wKeylist = list( wARR_Tweet.keys() )
		for wID in wKeylist :
			wFavoID = str(wID)
			
			if wARR_Tweet[wFavoID]['FLG_agent']==False :
				### 候補じゃなければ、スキップ
				continue
			
			# ※候補をいいねしていく
			#############################
			# ユーザ情報切替
			### 既いいねユーザは1回だけ
			if wARR_Tweet[wFavoID]['user']['id'] in wARR_FavoID :
				continue
			
			wFavoUser = wARR_Tweet[wFavoID]['user']
			wARR_FavoID.append( wARR_Tweet[wFavoID]['user']['id'] )
			
			#############################
			# いいねする
			wSubRes = gVal.OBJ_Tw_IF.Favo( wARR_Tweet[wFavoID] )
			if wSubRes['Result']!=True :
###				wRes['Reason'] = "Twitter API Error(Favo): user=" + wFavoUser['screen_name'] + " id=" + str(wFavoID)
				wResText = "Twitter API Error(Favo):"
				wResText = wResText + " id=" + str(wFavoID)
				wResText = wResText + " kind=" + str(wARR_Tweet[wFavoID]['kind'])
				wResText = wResText + " user=" + str(wARR_Tweet[wFavoID]['user']['screen_name'])
				if wARR_Tweet[wFavoID]['src_user']['screen_name']!=None :
					wResText = wResText + " src_user=" + str(wARR_Tweet[wFavoID]['src_user']['screen_name'])
				
				wRes['Reason'] = wResText
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			if wSubRes['Responce']['Run']==True :
###				wStr = "自動いいね 実施: user=" + wARR_Tweet[wFavoID]['user']['screen_name'] + " id=" + str(wFavoID)
				wStr = "自動いいね 実施:"
				wStr = wStr + " user=" + wARR_Tweet[wFavoID]['user']['screen_name']
				wStr = wStr + " kind=" + wARR_Tweet[wFavoID]['kind']
				wStr = wStr + " id=" + str(wFavoID)
				if wARR_Tweet[wFavoID]['kind']=="retweet" or wARR_Tweet[wFavoID]['kind']=="quoted" :
					wStr = wStr + " src_user=" + wARR_Tweet[wFavoID]['src_user']['screen_name']
				
				gVal.OBJ_L.Log( "T", wRes, wStr )
				wRes['Responce']['run'] += 1
			else :
				wStr = "  ::いいね済み(Twitter検出)"
				CLS_OSIF.sPrn( wStr )
			
			#############################
			# DBからいいね情報を取得する(1個)
			wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( wFavoUser )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "GetFavoDataOne is failed(2)"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			### DB未登録（ありえない）
			if wSubRes['Responce']['Data']==None :
				wRes['Reason'] = "GetFavoDataOne is no data"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wSubRes['Responce']['FLG_New']==True :
				#############################
				# 新規情報の設定
				wSubRes = self.OBJ_Parent.SetNewFavoData( wFavoUser, wSubRes['Responce']['Data'] )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "SetNewFavoData is failed(2)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			wARR_DBData = wSubRes['Responce']['Data']
			
			#############################
			# いいね情報：いいね送信更新
			wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Put( wFavoUser, wFavoID, wARR_DBData )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "UpdateListFavoData is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			### リストモードじゃない時は終わり
			if inListID==None :
				break
			
			### 規定数いいねしたら終わり
			if gVal.DEF_STR_TLNUM['forAutoFavoLevelCCnt']<=wRes['Responce']['run'] :
				break
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# リストいいね設定
#####################################################
	def SetListFavo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "SetListFavo"
		
		#############################
		# コンソールを表示
		while True :
			
			#############################
			# データ表示
			self.__view_ListFavo()
			
			#############################
			# 実行の確認
			wListNumber = CLS_OSIF.sInp( "コマンド？(\\q=中止)=> " )
			if wListNumber=="\\q" :
				###  設定をセーブして終わる
				wSubRes = gVal.OBJ_DB_IF.SaveListFavo()
				if wSubRes['Result']!=True :
					wRes['Reason'] = "SaveListFavo is failed"
					gVal.OBJ_L.Log( "B", wRes )

				wRes['Result'] = True
				return wRes
			
			#############################
			# コマンド処理
			wCommRes = self.__run_ListFavo( wListNumber )
			if wCommRes['Result']!=True :
				wRes['Reason'] = "__run_ListFavo is failed: " + wCommRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		wRes['Result'] = True
		return wRes

	#####################################################
	# 画面表示
	#####################################################
	def __view_ListFavo(self):
		
		wKeylist = list( gVal.ARR_ListFavo.keys() )
		wListNum = 1
		wStr = ""
		for wI in wKeylist :
			wStr = wStr + "   : "
			
			### リスト番号
			wListData = str(gVal.ARR_ListFavo[wI]['list_number'])
			wListNumSpace = 4 - len( wListData )
			if wListNumSpace>0 :
				wListData = wListData + " " * wListNumSpace
			wStr = wStr + wListData + "  "
			
			### 有効/無効
			if gVal.ARR_ListFavo[wI]['valid']==True :
				wStr = wStr + "[〇]"
			else:
				wStr = wStr + "[  ]"
			wStr = wStr + "  "
			
			### フォロー者、フォロワーを含める
			if gVal.ARR_ListFavo[wI]['follow']==True :
				wStr = wStr + "[〇]"
			else:
				wStr = wStr + "[  ]"
			wStr = wStr + "  "
			
			### 警告の有無
			if gVal.ARR_ListFavo[wI]['caution']==True :
				wStr = wStr + "[〇]"
			else:
				wStr = wStr + "[  ]"
			wStr = wStr + "  "
			
			### センシティブツイートを含める
			if gVal.ARR_ListFavo[wI]['sensitive']==True :
				wStr = wStr + "[〇]"
			else:
				wStr = wStr + "[  ]"
			wStr = wStr + "  "
			
			### 自動リムーブ
			if gVal.ARR_ListFavo[wI]['auto_rem']==True :
				wStr = wStr + "[〇]"
			else:
				wStr = wStr + "[  ]"
			wStr = wStr + "    "
			
			### ユーザ名（screen_name）
			wListData = gVal.ARR_ListFavo[wI]['screen_name']
			wListNumSpace = gVal.DEF_SCREEN_NAME_SIZE - len(wListData)
			if wListNumSpace>0 :
				wListData = wListData + " " * wListNumSpace
			wStr = wStr + wListData + ": "
			
			### リスト名
			wListData = gVal.ARR_ListFavo[wI]['list_name']
			wStr = wStr + wListData
			
			wStr = wStr + '\n'
		
		wResDisp = CLS_MyDisp.sViewDisp( inDisp="ListFavoConsole", inIndex=-1, inData=wStr )
		if wResDisp['Result']==False :
			gVal.OBJ_L.Log( "D", wResDisp )
		
		return

	#####################################################
	# コマンド処理
	#####################################################
	def __run_ListFavo( self, inWord ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "__run_ListFavo"
		
		#############################
		# f: フォロー者反応
		if inWord=="\\f" :
			self.__view_ListFollower()
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# g: フォロワー支援
		elif inWord=="\\g" :
			wSubRes = self.FollowerFavo()
			if wSubRes['Result']!=True :
				wRes['Reason'] = "FollowerFavo"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# s: リスト追加
		elif inWord=="\\s" :
			self.__add_ListFavo()
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# チェック
		
		wARR_Comm = str(inWord).split("-")
		wCom = None
		if len(wARR_Comm)==1 :
			wNum = wARR_Comm[0]
			wCom = None
		elif len(wARR_Comm)==2 :
			wNum = wARR_Comm[0]
			wCom = wARR_Comm[1]
		else:
			CLS_OSIF.sPrn( "コマンドの書式が違います" + '\n' )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		### 整数か
		try:
			wNum = int(wNum)
		except ValueError:
			CLS_OSIF.sPrn( "LIST番号が整数ではありません" + '\n' )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		wKeylist = list( gVal.ARR_ListFavo.keys() )
		wGetIndex = None
		for wIndex in wKeylist :
			if gVal.ARR_ListFavo[wIndex]['list_number']==wNum :
				wGetIndex = wIndex
				break
		
		if wGetIndex==None :
			CLS_OSIF.sPrn( "LIST番号が範囲外です" + '\n' )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		wNum = wGetIndex
		
		#############################
		# コマンドの分岐
		
		#############################
		# コマンドなし: 指定の番号のリストの設定変更をする
		if wCom==None :
			if gVal.ARR_ListFavo[wNum]['valid']==True :
				gVal.ARR_ListFavo[wNum]['valid'] = False
			else:
				gVal.ARR_ListFavo[wNum]['valid'] = True
			
			gVal.ARR_ListFavo[wNum]['update'] = True
		
		#############################
		# f: フォロー者、フォロワーを含める ON/OFF
		elif wCom=="f" :
			if gVal.ARR_ListFavo[wNum]['follow']==True :
				gVal.ARR_ListFavo[wNum]['follow'] = False
			else:
				gVal.ARR_ListFavo[wNum]['follow'] = True
			
			gVal.ARR_ListFavo[wNum]['update'] = True
		
		#############################
		# c: 警告 ON/OFF
		elif wCom=="c" :
			if gVal.ARR_ListFavo[wNum]['caution']==True :
				gVal.ARR_ListFavo[wNum]['caution'] = False
			else:
				gVal.ARR_ListFavo[wNum]['caution'] = True
			
			gVal.ARR_ListFavo[wNum]['update'] = True
		
		#############################
		# n: センシティブツイートを含める
		elif wCom=="n" :
			if gVal.ARR_ListFavo[wNum]['sensitive']==True :
				gVal.ARR_ListFavo[wNum]['sensitive'] = False
			else:
				gVal.ARR_ListFavo[wNum]['sensitive'] = True
			
			gVal.ARR_ListFavo[wNum]['update'] = True
		
		#############################
		# r: 自動リムーブ
		elif wCom=="r" :
			if gVal.ARR_ListFavo[wNum]['auto_rem']==True :
				gVal.ARR_ListFavo[wNum]['auto_rem'] = False
			else:
				gVal.ARR_ListFavo[wNum]['auto_rem'] = True
			
			gVal.ARR_ListFavo[wNum]['update'] = True
		
		#############################
		# v: リストユーザ表示
		elif wCom=="v" :
			self.__view_ListFavoUser( gVal.ARR_ListFavo[wNum]['list_name'] )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
		
		#############################
		# g: リストいいね実行
		elif wCom=="g" :
			wSubRes = self.ListFavo_single( wNum )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "ListFavo_single is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
		
		#############################
		# d: リスト削除
		elif wCom=="d" :
			wSubRes = self.__del_ListFavo( wNum )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "__del_ListFavo is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
		
		#############################
		# 範囲外のコマンド
		else:
			CLS_OSIF.sPrn( "コマンドが違います" + '\n' )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		wRes['Result'] = True
		return wRes

	#####################################################
	# リストユーザ表示
	#####################################################
	def __view_ListFavoUser( self, inListName ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "__view_ListFavoUser"
		
		#############################
		# Twitterからリストのユーザ一覧を取得
		wSubRes = gVal.OBJ_Tw_IF.GetListMember( inListName=inListName )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetLists): " + wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 画面表示
		wSubRes = self.__view_ListFavoUser_Disp( wSubRes['Responce'] )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "__view_ListFavoUser_Disp is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes

	#####################################################
	# フォロー者反応表示
	#####################################################
	def __view_ListFollower(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "__view_ListFollower"
		
		#############################
		# Twitterからリストのユーザ一覧を取得
		wARR_FollowerData = gVal.OBJ_Tw_IF.GetFollowerData()
		if len(wARR_FollowerData)==0 :
			wRes['Reason'] = "FollowerData is zero"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 表示するユーザ情報の作成
		#   フォロー者 かつ FAVO送信ありユーザをセット
		wARR_ListUser = {}
		wKeylist = list( wARR_FollowerData.keys() )
		for wID in wKeylist :
			wID = str( wID )
			
			### フォロワーか
			if wARR_FollowerData[wID]['follower']==False :
				### フォロワーじゃない =除外
				continue
			
			### VIPの場合
			### 相互フォローリスト、片フォローリストに未登録か
			if self.OBJ_Parent.CheckVIPUser( wARR_FollowerData[wID] )==True :
				if gVal.OBJ_Tw_IF.CheckMutualListUser( wID )==False and \
				   gVal.OBJ_Tw_IF.CheckFollowListUser( wID )==False :
					###対象 =除外
					continue
			
			#############################
			# 対象なのでセット
			wCell = {
				"id"			: wARR_FollowerData[wID]['id'],
				"screen_name"	: wARR_FollowerData[wID]['screen_name']
			}
			wARR_ListUser.update({ wID : wCell })
		
		#############################
		# 対象ユーザなし
		if len(wARR_ListUser)==0 :
			CLS_OSIF.sPrn( "対象ユーザがありません" + '\n' )
			wRes['Result'] = True
			return wRes
		
		#############################
		# 画面表示
		wSubRes = self.__view_ListFavoUser_Disp( wARR_ListUser )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "__view_ListFavoUser_Disp is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes

	#####################################################
	# リスト画面表示
	#####################################################
	def __view_ListFavoUser_Disp( self, inARR_Data ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "__view_ListFavoUser_Disp"
		
		#############################
		# ユーザなし
		if len( inARR_Data )==0 :
			CLS_OSIF.sPrn( "リスト登録のユーザはありません" )
			
			wRes['Result'] = True
			return wRes
		
		#############################
		# ヘッダの表示
		wStr = "USER NAME         LV  FW者  FAVO受信(回数/日)         FAVO送信日(回数)     最終活動日" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# いいねユーザデータを作成する
		wKeylist = list( inARR_Data.keys() )
		for wID in wKeylist :
			wID = str( wID )
			
			wARR_DBData = {
				"level_tag"		: None,
				"rfavo_cnt"		: 0,
				"rfavo_n_cnt"	: 0,
				"rfavo_date"	: gVal.DEF_TIMEDATE,
				"pfavo_date"	: gVal.DEF_TIMEDATE,
				"pfavo_cnt"		: 0,
				
				"update_date"	: gVal.DEF_TIMEDATE,
				"my_tweet"		: False
			}
			
			#############################
			# タイムラインを取得する
			#   最初の1ツイートの日時を最新の活動日とする
			wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="user", inFLG_Rep=False, inFLG_Rts=True,
				 inID=wID, inCount=gVal.DEF_STR_TLNUM['getUserTimeLine'] )
			if wTweetRes['Result']!=True :
				wRes['Reason'] = "Twitter Error: GetTL"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if len(wTweetRes['Responce'])>=1 :
				### 最新の活動日時
				
				wTweetIndex = 0
				for wTweet in wTweetRes['Responce'] :
					wTweetIndex += 1
					if wTweetIndex==1 :
						### 1行目の日付を活動日にする
						###日時の変換をして、設定
						wTime = CLS_TIME.sTTchg( wRes, "(4)", wTweet['created_at'] )
						if wTime['Result']!=True :
							return wRes
						wARR_DBData['update_date'] = wTime['TimeDate']
						
						if ("retweeted_status" not in wTweet) and ("quoted_status" not in wTweet) :
							### リツイート もしくは 引用でなければ自分
							wARR_DBData['my_tweet'] = True

						continue
					
					### 2行目以降
					### リツイート もしくは 引用でなければ活動日にする(自分のツイート)
					if ("retweeted_status" not in wTweet) and ("quoted_status" not in wTweet) :
						wTime = CLS_TIME.sTTchg( wRes, "(5)", wTweet['created_at'] )
						if wTime['Result']!=True :
							return wRes
						wARR_DBData['update_date'] = wTime['TimeDate']
						wARR_DBData['my_tweet'] = True
						break	#おわり
			
			#############################
			# DBからいいね情報を取得する(1個)
			#   
			#   
			wDBRes = gVal.OBJ_DB_IF.GetFavoDataOne( inARR_Data[wID] )
			if wDBRes['Result']!=True :
				###失敗
				wRes['Reason'] = "GetFavoDataOne is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			### DB登録
			if wDBRes['Responce']['Data']==None :
				wRes['Reason'] = "GetFavoDataOne is no data"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wDBRes['Responce']['FLG_New']==None :
				wNewUser = True	#新規登録
				#############################
				# 新規情報の設定
				wDBRes = self.OBJ_Parent.SetNewFavoData( inUser, wDBRes['Responce']['Data'] )
				if wDBRes['Result']!=True :
					###失敗
					wRes['Reason'] = "SetNewFavoData is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			wARR_DBData['level_tag']   = self.OBJ_Parent.LevelTagSttring( wDBRes['Responce']['Data']['level_tag'] )
			wARR_DBData['rfavo_cnt']   = wDBRes['Responce']['Data']['rfavo_cnt']
			wARR_DBData['rfavo_n_cnt'] = wDBRes['Responce']['Data']['rfavo_n_cnt']
			wARR_DBData['rfavo_date']  = wDBRes['Responce']['Data']['rfavo_date']
			wARR_DBData['pfavo_date']  = wDBRes['Responce']['Data']['pfavo_date']
			wARR_DBData['pfavo_cnt']   = wDBRes['Responce']['Data']['pfavo_cnt']
			
			#############################
			# 表示するデータ組み立て
			wStr = ""
			
			### 名前
			wListNumSpace = gVal.DEF_SCREEN_NAME_SIZE - len(inARR_Data[wID]['screen_name'])
			if wListNumSpace>0 :
				wListData = inARR_Data[wID]['screen_name'] + " " * wListNumSpace
			wStr = wStr + wListData + "  "
			
			### レベル
			wStr = wStr + wARR_DBData['level_tag'] + "  "
			
			### フォロー者
			if gVal.OBJ_Tw_IF.CheckMyFollow( wID )==True :
				wListData = "〇"
			else:
				wListData = "--"
			wStr = wStr + wListData + "    "
			
			### いいね受信日
			if str(wARR_DBData['rfavo_date'])==gVal.DEF_TIMEDATE :
				wListData = "----/--/--"
			else:
				wListData = str(wARR_DBData['rfavo_date']).split(" ")
				wListData = wListData[0]
			wStr = wStr + wListData + "("
			
			### いいね回数
			if wARR_DBData['rfavo_cnt']>0 :
				wListNumSpace = 5 - len( str(wARR_DBData['rfavo_cnt']) )
				wListData = str(wARR_DBData['rfavo_cnt']) + " " * wListNumSpace
				wListData = wListData + "/"
				wListData = wListData + str(wARR_DBData['rfavo_n_cnt']) + " " * wListNumSpace
			else:
				wListNumSpace = 5 - 1
				wListData = "-" + " " * wListNumSpace
				wListData = wListData + "/"
				wListData = wListData + "-" + " " * wListNumSpace
			wStr = wStr + wListData + ")   "
			
			### いいね送信日
			if str(wARR_DBData['pfavo_date'])==gVal.DEF_TIMEDATE :
				wListData = "----/--/--"
			else:
				wListData = str(wARR_DBData['pfavo_date']).split(" ")
				wListData = wListData[0]
			wStr = wStr + wListData + "("
			
			### いいね実施回数
			if wARR_DBData['pfavo_cnt']>0 :
				wListNumSpace = 5 - len( str(wARR_DBData['pfavo_cnt']) )
				wListData = str(wARR_DBData['pfavo_cnt']) + " " * wListNumSpace
			else:
				wListNumSpace = 5 - 1
				wListData = "-" + " " * wListNumSpace
			wStr = wStr + wListData + ")   "
			
			### 最終活動日
			if str(wARR_DBData['update_date'])==gVal.DEF_TIMEDATE :
				wListData = "----/--/--"
			else:
				if wARR_DBData['my_tweet']==True :
					###自分のツイート
					wListData = str(wARR_DBData['update_date']).split(" ")
					wListData = " " + wListData[0]
				else:
					###引用リツイート
					wListData = str(wARR_DBData['update_date']).split(" ")
					wListData = "(" + wListData[0] + ")"
			wStr = wStr + wListData
			
			CLS_OSIF.sPrn( wStr )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes

	#####################################################
	# リスト追加
	#####################################################
	def __add_ListFavo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "__add_ListFavo"
		
		#############################
		# 入力画面表示
		wStr = "いいねリストを追加します。" + '\n'
		wStr = wStr + "追加したいユーザ名、リスト名を順番に入力してください。" + '\n'
		wStr = wStr + "\\q でキャンセルできます。" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 入力
		while True :
			#############################
			# ユーザ名
			wInputName = CLS_OSIF.sInp( "  Twitter User Name ？=> " )
			if wInputName=="" :
				continue
			elif wInputName=="\\q" :
				# 戻る
				break
			wUserName = wInputName
			
			#############################
			# リスト名
			wInputName = CLS_OSIF.sInp( "  Twitter List Name ？=> " )
			if wInputName=="" :
				continue
			elif wInputName=="\\q" :
				# 戻る
				break
			wListName = wInputName
			
			#############################
			# 名称被りチェック
			if gVal.STR_UserInfo['Account']==wUserName :
				if gVal.STR_UserInfo['ListName']==wInputName or \
				   gVal.STR_UserInfo['mListName']==wInputName or \
				   gVal.STR_UserInfo['fListName']==wInputName :
					CLS_OSIF.sPrn( "設定済みリストのため設定できません" + '\n' )
					continue
			
			wFLG_Detect = False
			wKeylist = list( gVal.ARR_ListFavo.keys() )
			for wKey in wKeylist :
				if gVal.ARR_ListFavo[wKey]['screen_name']==wUserName and \
				   gVal.ARR_ListFavo[wKey]['list_name']==wListName :
					wFLG_Detect = True
					break
			if wFLG_Detect==True :
				CLS_OSIF.sPrn( "いいねリスト設定済みため設定できません" + '\n' )
				continue
			
			#############################
			# ユーザIDの取得
			if gVal.STR_UserInfo['Account']==wUserName :
				### 自IDの場合
				wUserID = str( gVal.STR_UserInfo['id'] )
			else:
				### 自分でない場合、IDを取得する
				wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inScreenName=wFollowerData[wID]['screen_name'] )
				if wUserInfoRes['Result']!=True :
					if wUserInfoRes['StatusCode']==404 :
						CLS_OSIF.sPrn( "存在しないユーザです" + '\n' )
						continue
					else:
						wRes['Reason'] = "Twitter API Error(GetUserinfo): " + wUserInfoRes['Reason'] + " screen_name=" + wFollowerData[wID]['screen_name']
						gVal.OBJ_L.Log( "B", wRes )
						return wRes
				wUserID = str( wUserInfoRes['Responce']['id'] )
			
			#############################
			# リストがTwitterにあるか確認
			wSubRes = gVal.OBJ_Tw_IF.GetListID( inListName=wListName, inScreenName=wUserName )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "GetListID is failed"
				gVal.OBJ_L.Log( "B", wRes )
				continue
			if wSubRes['Responce']==None :
				CLS_OSIF.sPrn( "Twitterにないリストです" + '\n' )
				continue
			
			###ここまでで入力は完了した
			wListID = wSubRes['Responce'] # ListID
			
			#############################
			# リストの登録
			wDBRes = gVal.OBJ_DB_IF.InsertListFavo( wUserID, wUserName, wListID, wListName )
			if wDBRes['Result']!=True :
				###失敗
				wRes['Reason'] = "InsertListFavo is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wDBRes['Responce']==False :
				CLS_OSIF.sPrn( "重複したリストは設定できません" + '\n' )
				continue
			
			#※完了
			break
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes

	#####################################################
	# リスト削除
	#####################################################
	def __del_ListFavo( self, inListID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "__del_ListFavo"
		
		#############################
		# リストの登録
		wDBRes = gVal.OBJ_DB_IF.DeleteListFavo( inListID )
		if wDBRes['Result']!=True :
			###失敗
			wRes['Reason'] = "DeleteListFavo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wDBRes['Responce']==False :
			CLS_OSIF.sPrn( "存在しないリスト番号です" + '\n' )
			wRes['Result'] = True
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



