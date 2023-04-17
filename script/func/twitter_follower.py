#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : Twitter監視 フォロワー監視系
#####################################################

from ktime import CLS_TIME
from osif import CLS_OSIF
from traffic import CLS_Traffic
from mydisp import CLS_MyDisp
from gval import gVal
#####################################################
class CLS_TwitterFollower():
#####################################################
	OBJ_Parent = ""				#親クラス実体
	
	ARR_AgentUsers  = {}
###	VAL_ReactionCnt = 0
###	ARR_Mentions    = {}
###	ARR_Reaction    = {}
	
#####################################################
# Init
#####################################################
	def __init__( self, parentObj=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFollower"
		wRes['Func']  = "__init__"
		
		if parentObj==None :
			###親クラス実体の未設定
			wRes['Reason'] = "You have not set the parent class entity for parentObj"
			gVal.OBJ_L.Log( "A", wRes )
			return
		
		self.OBJ_Parent = parentObj
		return



#####################################################
# いいね情報送信
#####################################################
	def SendFavoDate( self, inFLG_Force=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFollower"
		wRes['Func']  = "SendFavoDate"
		
		#############################
		# いいね情報を送信する日時か
		wGetLag = CLS_OSIF.sTimeLag( str(gVal.STR_Time['send_favo']), inThreshold=gVal.DEF_VAL_WEEK )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed(1)"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		###強制じゃなければ判定する
		if inFLG_Force==False :
			if wGetLag['Beyond']==False :
				###期間内
				###  次へ
				wStr = "●いいね送信期間外 処理スキップ: 次回処理日時= " + str(wGetLag['RateTime']) + '\n'
				CLS_OSIF.sPrn( wStr )
				wRes['Result'] = True
				return wRes
		
		wRes['Responce'] = False
		#############################
		# 取得開始の表示
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "いいね情報送信" )
		
		#############################
		# DBのいいね情報取得
		wResDB = gVal.OBJ_DB_IF.GetFavoData_SendFavo()
		if wResDB['Result']!=True :
			wRes['Reason'] = "GetFavoData_SendFavo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		wARR_RateFavoDate = wResDB['Responce']
		
		if len( wARR_RateFavoDate )==0 :
			#############################
			# 現時間を設定
			wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "send_favo", gVal.STR_Time['TimeDate'] )
			if wTimeRes['Result']!=True :
				wRes['Reason'] = "SetTimeInfo is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			###	gVal.STR_Time['send_favo']
			
			wStr = "●いいね情報 送信者はいませんでした" + '\n'
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
		### 計測開始日付
		wNowTD = str(wGetLag['InputTime']).split(" ")
		wNowTD = wNowTD[0]
		
		### ヘッダの設定
		wTrendHeader_Pattern = "いいね情報(回数)送信"
		wTrendHeader = wTrendHeader_Pattern + " (" + wNowTD + " から" + str(gVal.DEF_STR_TLNUM['favoSendsCnt']) + "回以上)"
		
		wSendUserNum = 0
		wSendTweet = []
		wSendTweet.append( wTrendHeader + '\n' )
		wSendTweetIndex = 0
		wSendCnt = 0
		#############################
		# タグの設定
		wTrendTag = ""
		if gVal.STR_UserInfo['TrendTag']!="" and \
		   gVal.STR_UserInfo['TrendTag']!=None :
			wTrendTag = '\n' + "#" + gVal.STR_UserInfo['TrendTag']
		
		wARR_SendID = []	#送信したID
		wFLG_Header = False
		wKeylist = list( wARR_RateFavoDate.keys() )
		for wID in wKeylist :
			wID = str( wID )
			
			#############################
			# リアクション 規定回以上は送信
			
			#############################
			# リアクション禁止ユーザは除外する
			wUserRes = self.OBJ_Parent.CheckExtUser( wARR_RateFavoDate[wID], "リアクション禁止ユーザ", False )
			if wUserRes['Result']!=True :
				wRes['Reason'] = "CheckExtUser failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wUserRes['Responce']==False :
				### 禁止あり=除外
				continue
			
			#############################
			# 無反応レベルは除外する
###			if wARR_RateFavoDate[wID]['level_tag']=="D-" or wARR_RateFavoDate[wID]['level_tag']=="G" or wARR_RateFavoDate[wID]['level_tag']=="G-" :
###			if wARR_RateFavoDate[wID]['level_tag']=="D-" or wARR_RateFavoDate[wID]['level_tag']=="G" or wARR_RateFavoDate[wID]['level_tag']=="G+" or \
###			   wARR_RateFavoDate[wID]['level_tag']=="H"  or wARR_RateFavoDate[wID]['level_tag']=="H+" :
			if wARR_RateFavoDate[wID]['level_tag']=="C-" or wARR_RateFavoDate[wID]['level_tag']=="D" or wARR_RateFavoDate[wID]['level_tag']=="D+" or \
			   wARR_RateFavoDate[wID]['level_tag']=="F"  or wARR_RateFavoDate[wID]['level_tag']=="E-" or wARR_RateFavoDate[wID]['level_tag']=="G"  or wARR_RateFavoDate[wID]['level_tag']=="G-" or \
			   wARR_RateFavoDate[wID]['level_tag']=="L"  or wARR_RateFavoDate[wID]['level_tag']=="Z" :
				continue
			
			#############################
			# リアクション 規定回以上は送信
			if wARR_RateFavoDate[wID]['rfavo_n_cnt']>=gVal.DEF_STR_TLNUM['favoSendsCnt'] :
				
				### 送信したIDで確定
				wARR_SendID.append( wID )
				
				wSendCnt += 1
				#############################
				# 1行設定
				wLine = wARR_RateFavoDate[wID]['screen_name'] + " : " + \
				        str(wARR_RateFavoDate[wID]['rfavo_n_cnt']) + \
				        "(" + str(wARR_RateFavoDate[wID]['rfavo_cnt']) + ")" + '\n'
				
				wFLG_Header = False
				if ( len( wSendTweet[wSendTweetIndex] ) + len( wLine ) + len( wTrendTag ) )<140 :
					wSendTweet[wSendTweetIndex] = wSendTweet[wSendTweetIndex] + wLine
				else:
					### タグの付加
					wSendTweet[wSendTweetIndex] = wSendTweet[wSendTweetIndex] + wTrendTag
					
					### 次のリストにヘッダの設定
					wSendTweet.append( wTrendHeader + '\n' + wLine )
					wSendTweetIndex += 1
					wFLG_Header = True
			
		if wSendCnt==0 :
			#############################
			# 送信者がいない場合
			
			#############################
			# 現時間を設定
			wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "send_favo", gVal.STR_Time['TimeDate'] )
			if wTimeRes['Result']!=True :
				wRes['Reason'] = "SetTimeInfo is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			###	gVal.STR_Time['send_favo']
			
			wStr = "●いいね情報 送信者はいませんでした" + '\n'
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
		### 最後のリストにタグの付加
		if wFLG_Header==False :
			wSendTweet[wSendTweetIndex] = wSendTweet[wSendTweetIndex] + wTrendTag
		
		#############################
		# 前のトレンドツイートを消す
		
		wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="user", inFLG_Rep=False, inFLG_Rts=False,
			 inID=gVal.STR_UserInfo['id'], inCount=gVal.DEF_STR_TLNUM['favoTweetLine'] )
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter Error: GetTL"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if len(wTweetRes['Responce'])>0 :
			for wTweet in wTweetRes['Responce'] :
				wID = str(wTweet['id'])
				
				if wTweet['text'].find( wTrendHeader_Pattern )==0 :
###					###日時の変換
###					wTime = CLS_TIME.sTTchg( wRes, "(3)", wTweet['created_at'] )
###					if wTime['Result']!=True :
###						continue
###					wTweet['created_at'] = wTime['TimeDate']
###					
###					###ユーザ単位のリアクションチェック
####				wReactionRes = self.OBJ_Parent.ReactionUserCheck( wTweet['user'], wTweet )
###					wReactionRes = self.OBJ_Parent.OBJ_TwitterReaction.ReactionUserCheck( wTweet['user'], wTweet )
###					if wReactionRes['Result']!=True :
###						wRes['Reason'] = "Twitter Error(ReactionUserCheck 4): Tweet ID: " + str(wTweet['id'])
###						gVal.OBJ_L.Log( "B", wRes )
###						continue
###					
					wTweetRes = gVal.OBJ_Tw_IF.DelTweet( wID )
					if wTweetRes['Result']!=True :
						wRes['Reason'] = "Twitter API Error(2): " + wTweetRes['Reason'] + " id=" + str(wID)
						gVal.OBJ_L.Log( "B", wRes )
					else:
						wStr = "いいね情報ツイートを削除しました。" + '\n'
						wStr = wStr + "------------------------" + '\n'
						wStr = wStr + wTweet['text'] + '\n'
						CLS_OSIF.sPrn( wStr )
		
		#############################
		# ツイートする
		for wLine in wSendTweet :
			wTweetRes = gVal.OBJ_Tw_IF.Tweet( wLine )
			if wTweetRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(3): " + wTweetRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			#############################
			# 送信完了
			wStr = "いいね情報を送信しました。" + '\n'
			wStr = wStr + "------------------------" + '\n'
			wStr = wStr + wLine + '\n'
			CLS_OSIF.sPrn( wStr )
			
		
		#############################
		# ログに記録
		gVal.OBJ_L.Log( "T", wRes, "いいね情報送信(Twitter)" )
		
		#############################
		# いいね者送信日時を更新する
		wResDB = gVal.OBJ_DB_IF.UpdateFavoData_SendFavo( wARR_SendID )
		if wResDB['Result']!=True :
			wRes['Reason'] = "UpdateFavoData_SendFavo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 自動リムーブONの場合
		# トロフィー送信者のうち
		# 規定回数を超えたら昇格して相互フォローにする
		for wID in wARR_SendID :
			wID = str(wID)
			
			if wARR_RateFavoDate[wID]['myfollow']==True :
				#############################
				# 既にフォロー済の場合
				#   かつフォロワーで レベルEの場合
				#   レベルBに昇格する
				if wARR_RateFavoDate[wID]['follower']==True and \
				   wARR_RateFavoDate[wID]['level_tag']=="E" :
					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, "B" )
				continue
			if wARR_RateFavoDate[wID]['follower']==False :
				### フォロワーでなければ、スキップ
				continue
			wCnt = wARR_RateFavoDate[wID]['send_cnt']
			#############################
			# レベルB or C以外か、B+じゃなければここで終わり
			if ( wARR_RateFavoDate[wID]['level_tag']!="B" and \
			   wARR_RateFavoDate[wID]['level_tag']!="C" ) or \
			   wARR_RateFavoDate[wID]['level_tag']=="B+" :
				continue
			
			wCnt += 1
			#############################
			# 昇格トロフィー回数か
			if gVal.DEF_STR_TLNUM['LEVEL_B_Cnt']>wCnt :
				### 規定外 =昇格なし
				continue
			
			### ※昇格あり
			#############################
			# レベルB+昇格へ
			wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, "B+" )
		
		#############################
		# 現時間を設定
		wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "send_favo", gVal.STR_Time['TimeDate'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "SetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		###	gVal.STR_Time['send_favo']
		
		wRes['Result'] = True
		return wRes



#####################################################
# 自動リムーブ
#####################################################
	def AutoRemove( self, inUser, inFLG_Force=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFollower"
		wRes['Func']  = "AutoRemove"
		
		wRes['Responce'] = False	#自動リムーブ実行有無
		
		wUserID = str(inUser['id'])
		
		#############################
		# 自動リムーブが無効ならここで終わる
		if gVal.STR_UserInfo['AutoRemove']==False :
			wRes['Result'] = True
			return wRes
		
		wARR_DBData = None
		#############################
		# DBからいいね情報を取得する(1個)
		wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( inUser, inFLG_New=False )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetFavoDataOne is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### DB未登録
		if wSubRes['Responce']['Data']==None :
			wStr = "▽DB未登録ユーザに対する自動リムーブ検出"
			wRes['Reason'] = wStr + ": " + inUser['screen_name']
			gVal.OBJ_L.Log( "N", wRes )
		else:
			wARR_DBData = wSubRes['Responce']['Data']
		
		wFLG_Remove = False
		#############################
		# フォロー者の場合
		#   Twitterからリムーブする
		if gVal.OBJ_Tw_IF.CheckMyFollow( wUserID )==True :
			if wARR_DBData!=None and inFLG_Force==False:
				#############################
				# 期間比較値
				# いいねありの場合、
				#   =いいね日時
				# いいねなしの場合、
				#   =登録日時
				if str(wARR_DBData['rfavo_date'])!=gVal.DEF_TIMEDATE :
					### いいねあり= いいね日時
					wCompTimeDate = str(wARR_DBData['rfavo_date'])
					wThreshold = gVal.DEF_STR_TLNUM['forListFavoAutoRemoveSec']
				
				else:
					### いいねなし= 登録日時
					wCompTimeDate = str(wARR_DBData['regdate'])
					
					if ( wARR_DBData['level_tag']=="D" or wARR_DBData['level_tag']=="D+" ) and \
					   gVal.OBJ_Tw_IF.CheckFollower( wUserID )==False and \
					   str(wARR_DBData['pfavo_date'])!=gVal.DEF_TIMEDATE :
						### 片フォロー者で、いいねしたことがあるユーザは期間が短い
						wThreshold = gVal.DEF_STR_TLNUM['forListFavoAutoRemoveSec_Short']
					else:
						wThreshold = gVal.DEF_STR_TLNUM['forListFavoAutoRemoveSec']
				
				#############################
				# 自動リムーブ期間か
				wGetLag = CLS_OSIF.sTimeLag( wCompTimeDate, inThreshold=wThreshold )
				if wGetLag['Result']!=True :
					wRes['Reason'] = "sTimeLag failed(1)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				if wGetLag['Beyond']==True :
					###期間外= 自動リムーブ対象
					wFLG_Remove = True
			else:
				wFLG_Remove = True
			
			if wFLG_Remove==True :
				#############################
				# リムーブ実行
				wTweetRes = gVal.OBJ_Tw_IF.Remove( wUserID )
				if wTweetRes['Result']!=True :
					wRes['Reason'] = "Twitter API Error: Remove" + wTweetRes['Reason']
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				if wARR_DBData['follower']==True :
					### フォロー者OFF・フォロワーON
					wUserLevel = "D-"
				
				else:
					### フォロー者OFF・フォロワーOFF
					wUserLevel = "E-"
				
				### ユーザレベル変更
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wUserID, wUserLevel )
				
				### トラヒック記録（フォロー者減少）
				CLS_Traffic.sP( "d_myfollow" )
				
				#############################
				# ログに記録
				if inFLG_Force==True :
					gVal.OBJ_L.Log( "R", wRes, "●自動リムーブ(強制): " + inUser['screen_name'], inID=wUserID )
				else:
					gVal.OBJ_L.Log( "R", wRes, "●自動リムーブ: " + inUser['screen_name'], inID=wUserID )
				
				#############################
				# DBに反映
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Follower( wUserID, inFLG_MyFollow=False )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "UpdateFavoData_Follower is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				wRes['Responce'] = True		#自動リムーブ実行
		
		#############################
		# 自動リムーブしていれば
		# フォロワーなら
		#   リスト解除→片フォロワーリストへ
		# フォロワーでなければ
		#   リスト解除のみ
		if wFLG_Remove==True :
			if gVal.OBJ_Tw_IF.CheckFollower( wUserID )==True :
				### 片フォロワーリストへ
				wTweetRes = gVal.OBJ_Tw_IF.FollowerList_AddUser( inUser )
				if wTweetRes['Result']!=True :
					wRes['Reason'] = "FollowerList_AddUser is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			else:
				### リスト解除へ
				wTweetRes = gVal.OBJ_Tw_IF.FollowerList_Remove( inUser )
				if wTweetRes['Result']!=True :
					wRes['Reason'] = "FollowerList_Remove is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
		
		wFLG_Remove = False
		#############################
		# 片フォロワー かつ 片フォローリストの場合
		# あまりにスルーが酷ければ追い出す
		if gVal.OBJ_Tw_IF.CheckFollowListUser( wUserID )==True and \
		   gVal.OBJ_Tw_IF.CheckMyFollow( wUserID )==False and \
		   gVal.OBJ_Tw_IF.CheckFollower( wUserID )==True :
			
			if wARR_DBData!=None :
				#############################
				# 期間比較値
				# いいねありの場合、
				#   =いいね日時
				# いいねなしの場合、
				#   =登録日時
				if str(wARR_DBData['rfavo_date'])!=gVal.DEF_TIMEDATE :
					### いいねあり= いいね日時
					wCompTimeDate = str(wARR_DBData['rfavo_date'])
				else:
					### いいねなし= 登録日時
					wCompTimeDate = str(wARR_DBData['regdate'])
				
				#############################
				# 比較値の設定
				if wARR_DBData['level_tag']=="G" :
					### 既に追い出し済
###					wThreshold = gVal.DEF_STR_TLNUM['forAutoRemoveByeByeSec']
					if wARR_DBData['rfavo_cnt']<gVal.DEF_STR_TLNUM['forAutoRemoveByeBye_ShortCnt'] :
						### いいねが少ない場合、短期
						wThreshold = gVal.DEF_STR_TLNUM['forAutoRemoveByeBye_ShortSec']
					
					else:
						wThreshold = gVal.DEF_STR_TLNUM['forAutoRemoveByeByeSec']
				
				elif wARR_DBData['level_tag']=="G-" :
					wThreshold = gVal.DEF_STR_TLNUM['forAutoRemoveReleaseSec']
				
				else :
					### その他は、追い出し初回
					wThreshold = gVal.DEF_STR_TLNUM['forAutoRemoveIgnoreCompletelySec']
				
				#############################
				# 自動リムーブ期間か
				wGetLag = CLS_OSIF.sTimeLag( wCompTimeDate, inThreshold=wThreshold )
				if wGetLag['Result']!=True :
					wRes['Reason'] = "sTimeLag failed(1)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				if wGetLag['Beyond']==True :
					###期間外= 自動リムーブ対象
					wFLG_Remove = True
			
			else:
				#############################
				# DBがなくてリスト＆フォローが残っていれば
				# ブロック→ブロック解除で追い出す
				wBlockRes = gVal.OBJ_Tw_IF.BlockRemove( wUserID )
				if wBlockRes['Result']!=True :
					wRes['Reason'] = "Twitter API Error(BlockRemove): " + wBlockRes['Reason'] + " screen_name=" +inUser['screen_name']
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				### DBへ反映
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Follower( wUserID, False, False )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "UpdateFavoData_Follower is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				wStr = "●DBがないため追い出し"
				gVal.OBJ_L.Log( "R", wRes, wStr + ": " + str(inUser['screen_name']), inID=wUserID )
				
				### 正常終了
				wRes['Result'] = True
				return wRes
			
			#############################
			# 追い出し判定された場合、
			# 追い出し設定する
			if wFLG_Remove==True :
				#############################
				# G の場合
				# G-設定して、追い出す
				if wARR_DBData['level_tag']=="G" :
					wUserLevel = "G-"
					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wUserID, wUserLevel )
					
###					### ブロック→ブロック解除で追い出す
###					wBlockRes = gVal.OBJ_Tw_IF.BlockRemove( wUserID )
###					if wBlockRes['Result']!=True :
###						wRes['Reason'] = "Twitter API Error(BlockRemove): " + wBlockRes['Reason'] + " screen_name=" +inUser['screen_name']
###						gVal.OBJ_L.Log( "B", wRes )
###						return wRes
###					
###					### DBへ反映
###					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Follower( wUserID, False, False )
###					if wSubRes['Result']!=True :
###						###失敗
###						wRes['Reason'] = "UpdateFavoData_Follower is failed"
###						gVal.OBJ_L.Log( "B", wRes )
###						return wRes
###					
					
					### リスト解除
					wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_Remove( inUser )
					
					### ユーザ記録
					wStr = "●無視期間経過のため追い出し"
					gVal.OBJ_L.Log( "R", wRes, wStr + ": " + str(inUser['screen_name']), inID=wUserID )
					
					### 監視OFFの送信
					self.OBJ_Parent.SendUserOpeInd( inUser, inFLG_Ope=False )
					
					#############################
					# 代わりにフォロー一覧から再フォロー
					wSubRes = self.AutoReFollow( wUserID )
					if wSubRes['Result']!=True :
						wRes['Reason'] = "AutoReFollow is failed"
						gVal.OBJ_L.Log( "B", wRes )
						return wRes
				
				#############################
				# G- の場合
				# さよなら
				elif wARR_DBData['level_tag']=="G-" :
					### ブロック→ブロック解除で追い出す
					wBlockRes = gVal.OBJ_Tw_IF.BlockRemove( wUserID )
					if wBlockRes['Result']!=True :
						wRes['Reason'] = "Twitter API Error(BlockRemove): " + wBlockRes['Reason'] + " screen_name=" +inUser['screen_name']
						gVal.OBJ_L.Log( "B", wRes )
						return wRes
					
					### DBへ反映
					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Follower( wUserID, False, False )
					if wSubRes['Result']!=True :
						###失敗
						wRes['Reason'] = "UpdateFavoData_Follower is failed"
						gVal.OBJ_L.Log( "B", wRes )
						return wRes
					
					### ユーザ記録
					wStr = "●追い出し(さよなら)"
					gVal.OBJ_L.Log( "R", wRes, wStr + ": " + str(inUser['screen_name']), inID=wUserID )
				
				#############################
				# その他の場合、
				#   送信回数が規定回数超えてれば、
				#   追い出し扱い(G)に設定する
				else :
					if gVal.DEF_STR_TLNUM['forAutoRemoveIgnoreCompletelyCnt']<=wARR_DBData['pfavo_cnt'] :
						### ユーザレベル変更
						wUserLevel = "G"
						wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wUserID, wUserLevel )
						
						### ユーザ記録
						wStr = "●完全スルー期間外のため、以後無視"
						gVal.OBJ_L.Log( "R", wRes, wStr + ": " + str(inUser['screen_name']), inID=wUserID )
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# 自動再フォロー
#####################################################
	def AutoReFollow( self, inUserID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFollower"
		wRes['Func']  = "AutoReFollow"
		
		wUserID = str(inUserID)
		
		#############################
		# 自動リムーブが無効ならここで終わる
		if gVal.STR_UserInfo['AutoRemove']==False :
			wRes['Result'] = True
			return wRes
		
		#############################
		# 再フォロー数を超えているか
		if gVal.VAL_AutoReFollowCnt>=gVal.DEF_STR_TLNUM['forAutoReFollowCnt'] :
			wRes['Result'] = True
			return wRes
		
###		#############################
###		# 再選出の表示
###		wStr = "フォロー者の再選出..."
###		CLS_OSIF.sPrn( wStr )
###		
		#############################
		# フォロー一覧の取得
###		wFollowRes = gVal.OBJ_Tw_IF.GetFollowIDList( inID=wUserID )
		wFollowRes = gVal.OBJ_Tw_IF.GetMyFollowIDList( inID=wUserID )
		if wFollowRes['Result']!=True :
###			wRes['Reason'] = "GetFollowIDList is failed"
			wRes['Reason'] = "GetMyFollowIDList is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wARR_FollowID = wFollowRes['Responce']
		
		gVal.VAL_AutoReFollowCnt += 1
		
		wLen = len( wARR_FollowID )
		#############################
		# 再選出の表示
		if wLen==0 :
			wStr = "フォロー者の再選出...: 候補0件のためスキップ"
			CLS_OSIF.sPrn( wStr )
			
			wRes['Result'] = True
			return wRes
		
		wStr = "フォロー者の再選出...: " + str(wLen) + " 件"
		CLS_OSIF.sPrn( wStr )
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wARR_FollowID ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
		wFollowNum = 0
		#############################
		# フォロー
###		wKeylist = list(wARR_FollowID)
		for wID in wARR_FollowID :
			###ウェイトカウントダウン
			if self.OBJ_Parent.Wait_Next()==False :
				break	###ウェイト中止
			
			wID = str(wID)
			
			#############################
			# フォロー人数が超えたか
			if wFollowNum>=gVal.DEF_STR_TLNUM['forAutoReFollowFollowCnt'] :
				wStr = "人数上限のため再選出終了"
				CLS_OSIF.sPrn( wStr )
				break
			
			### 進捗用にID表示
			CLS_OSIF.sPrn( wID )
			#############################
			# 自動フォロー
			wSubRes = self.AutoFollow( inUserID=wID )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "AutoFollow is failed"
				gVal.OBJ_L.Log( "B", wRes )
				continue
			
###			wFollowNum += 1
			if wSubRes['Responce']==True :
				### 自動フォロー実行 +カウントアップ
				wFollowNum += 1
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# 自動フォロー
#####################################################
	def AutoFollow( self, inUserID, inForce=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFollower"
		wRes['Func']  = "AutoFollow"
		
		wRes['Responce'] = False	#自動フォロー実行有無
		
		wUserID = str(inUserID)
		#############################
		# 自動リムーブが無効ならここで終わる
		if gVal.STR_UserInfo['AutoRemove']==False :
			wRes['Result'] = True
			return wRes
		
		#############################
		# ユーザ情報の取得
		wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inID=wUserID )
		if wUserInfoRes['Result']!=True :
			wRes['Reason'] = "GetUserinfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wUser = wUserInfoRes['Responce']
		#############################
		# ユーザの状態チェック
		# 以下は除外
		# ・鍵垢
		# ・公式垢
		# ・フォロー者数=0
		# ・フォロー者数=1000以上
		# ・フォロワー数=100未満
		# ・フォロー者＜フォロワー数
		# ・いいね数=0
		# ・ツイート数=100未満
		if wUser['protected']==True or \
		   wUser['verified']==True or \
		   wUser['friends_count']==0 or \
		   wUser['favourites_count']==0 or \
		   wUser['statuses_count']<100 :
			
			wRes['Result'] = True
			return wRes
		
		if inForce==False :
			if wUser['friends_count']>=1000 or \
			   wUser['followers_count']<100 or \
			   wUser['friends_count']<wUser['followers_count'] :
				
				wRes['Result'] = True
				return wRes
		
		#############################
		# DBからいいね情報を取得する(1個)
		wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( wUser )
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
			wSubRes = self.OBJ_Parent.SetNewFavoData( wUser, wSubRes['Responce']['Data'] )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "SetNewFavoData is failed(2)"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		wARR_DBData = wSubRes['Responce']['Data']
		
		#############################
		# いいね情報のチェック
		# 以下は除外
		# ・ユーザレベル E, F以外
		# ・フォロー者ON
		if inForce==False :
			if wARR_DBData['myfollow']==True or \
			   ( wARR_DBData['level_tag']!="F" and wARR_DBData['level_tag']!="E" ):
				wRes['Result'] = True
				return wRes
		
		#############################
		# 禁止プロフ文字チェック
		wWordRes = self.OBJ_Parent.CheckExtProf( wUser, wUser['description'] )
		if wWordRes['Result']!=True :
			wRes['Reason'] = "CheckExtProf failed(description)"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wWordRes['Responce']==False :
			wRes['Result'] = True
			return wRes
		
		#############################
		# フォローする
		wTweetRes = gVal.OBJ_Tw_IF.Follow( wUserID, inMute=True )
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(Follow): " + wTweetRes['Reason'] + " screen_name=" + str(wUser['screen_name'])
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wRes['Responce'] = True		#自動フォロー実行
		
		### 相互フォローリストに追加
		wTwitterRes = gVal.OBJ_Tw_IF.MutualList_AddUser( wARR_DBData )
		
		### ユーザレベル変更
		wUserLevel = "D+"
		wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wUserID, wUserLevel )
		
		### トラヒック記録（フォロー者増加）
		CLS_Traffic.sP( "p_myfollow" )
		
		### ユーザ記録
		wStr = "〇自動フォロー"
		gVal.OBJ_L.Log( "R", wRes, wStr + ": " + str(wUser['screen_name']), inID=wUserID )
		
		#############################
		# DBに反映
		wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Follower( wUserID, inFLG_MyFollow=True )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "UpdateFavoData_Follower is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# タイムラインフォロー
#####################################################
	def TimelineFollow( self , inCheck=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFollower"
		wRes['Func']  = "TimelineFollow"
		
		#############################
		# 取得可能時間か？
		wGetLag = CLS_OSIF.sTimeLag( str( gVal.STR_Time['tl_follow'] ), inThreshold=gVal.DEF_STR_TLNUM['forTimelineFollowSec'] )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wGetLag['Beyond']==False and inCheck==True :
			### 規定以内は除外
			wStr = "●タイムラインフォロー期間外 処理スキップ: 次回処理日時= " + str(wGetLag['RateTime']) + '\n'
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
		#############################
		# 取得開始の表示
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "タイムラインフォロー中" )
		
		#############################
		# ツイートj情報
		# ※元ソースは見ない仕様とする
		wSTR_User = {
			"id"				: None,
			"name"				: None,
			"screen_name"		: None,
			"description"		: None
		}
		wSTR_Tweet = {
			"kind"				: None,
			"id"				: None,
			"text"				: None,
			"created_at"		: None,
			"user"				: wSTR_User,
			"reason"			: None				# NG理由
		}
		
		#############################
		# 直近のホームタイムラインを取得
		wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="home", inFLG_Rep=False, inFLG_Rts=True,
			 inID=gVal.STR_UserInfo['id'], inCount=gVal.DEF_STR_TLNUM['TimelineFollowTweetLine'] )
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter Error: GetTL"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if len(wTweetRes['Responce'])==0 :
			wRes['Reason'] = "Tweet is not get: home timeline"
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wTweetRes['Responce'] ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
		#############################
		# チェック
		
		wFLG_ZanCountSkip  = False
		self.ARR_AgentUser = {}
		wTLCnt   = 0
		wFavoCnt = 0
		wFollowNum = 0
		for wTweet in wTweetRes['Responce'] :
			wTLCnt += 1
			###先頭スキップ
			if gVal.DEF_STR_TLNUM['TimelineFollowTweetLine_Skip']>=wTLCnt :
				continue
			
			###ウェイトカウントダウン
			if self.OBJ_Parent.Wait_Next( inZanCountSkip=wFLG_ZanCountSkip )==False :
				break	###ウェイト中止
			wFLG_ZanCountSkip = False
			
			### いいねチェック回数の限界
			if gVal.DEF_STR_TLNUM['TimelineFollowFavoCheckNum']<=wFavoCnt :
				wStr = "〇完了: いいねチェック回数に到達" ;
				CLS_OSIF.sPrn( wStr )
				break
			
			### フォロー人数の限界
			if gVal.DEF_STR_TLNUM['TimelineFollowNum']<=wFollowNum :
				wStr = "〇完了: フォロー人数の上限に到達" ;
				CLS_OSIF.sPrn( wStr )
				break
			
			###日時の変換
			wTime = CLS_TIME.sTTchg( wRes, "(1)", wTweet['created_at'] )
			if wTime['Result']!=True :
				continue
			wSTR_Tweet['created_at'] = wTime['TimeDate']
			
			#############################
			# ツイート情報を取得
			wSTR_Tweet['id']   = str(wTweet['id'])
			wSTR_Tweet['text'] = str(wTweet['text'])
			wSTR_Tweet['user']['id']          = str(wTweet['user']['id'])
			wSTR_Tweet['user']['name']        = str(wTweet['user']['name'])
			wSTR_Tweet['user']['screen_name'] = str(wTweet['user']['screen_name'])
			wSTR_Tweet['user']['description'] = str(wTweet['user']['description'])
			
			### リツイート
			if "retweeted_status" in wTweet :
				wSTR_Tweet['kind'] = "retweet"
			
			### 引用リツイート
			elif "quoted_status" in wTweet :
				wSTR_Tweet['kind'] = "quoted"
			
			### リプライ
###			elif wSTR_Tweet['text'].find("@")>=0 :
###			elif wSTR_Tweet['text'].find("@")>=0 or wTweet['in_reply_to_status_id']==None :
			elif wSTR_Tweet['text'].find("@")>=0 or wTweet['in_reply_to_status_id']!=None :
				wSTR_Tweet['kind'] = "reply"
			
			### 通常ツイート
			else:
				wSTR_Tweet['kind'] = "normal"
			
			#############################
			# チェック対象のツイート表示
			wStr = '\n' + "--------------------" + '\n' ;
			wStr = wStr + wSTR_Tweet['text'] + '\n' ;
			wStr = wStr + "  time: " + wSTR_Tweet['created_at'] + "  screen_name: " + wSTR_Tweet['user']['screen_name'] + '\n' ;
			CLS_OSIF.sPrn( wStr )
			
			#############################
			# 相互フォロー もしくは 片フォローの場合
			# スキップする
			if gVal.OBJ_Tw_IF.CheckMutualListUser( wSTR_Tweet['user']['id'] )==True or \
			   gVal.OBJ_Tw_IF.CheckFollowListUser( wSTR_Tweet['user']['id'] )==True :
				wStr = "●スキップ: 相互もしくは片フォロワー" ;
				CLS_OSIF.sPrn( wStr )
				continue
			
			#############################
			# いいね、リツイートしてるユーザ一覧を取得する
			
			#############################
			# いいねの場合
			wSubRes = gVal.OBJ_Tw_IF.GetLikesLookup( wSTR_Tweet['id'] )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(GetLikesLookup): Tweet ID: " + wSTR_Tweet['id']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			self.__add_TimelineFollow_AgentUser( wSubRes['Responce'] )
			
			#############################
			# リツイートの場合
			wSubRes = gVal.OBJ_Tw_IF.GetRetweetLookup( wSTR_Tweet['id'] )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(GetRetweetLookup): Tweet ID: " + wSTR_Tweet['id']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			self.__add_TimelineFollow_AgentUser( wSubRes['Responce'] )
			
			#############################
			# 引用リツイートの場合
			wSubRes = gVal.OBJ_Tw_IF.GetRefRetweetLookup( wSTR_Tweet['id'] )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(GetRefRetweetLookup): Tweet ID: " + wSTR_Tweet['id']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			self.__add_TimelineFollow_AgentUser( wSubRes['Responce'] )
			
			#############################
			# リプライの場合
			if wSTR_Tweet['kind']=="reply" and \
			   str(wSTR_Tweet['user']['id']) is not self.ARR_AgentUsers :
				wSTR_User = {
					"id"				: str(wSTR_Tweet['user']['id']),
					"name"				: str(wSTR_Tweet['user']['name']),
					"screen_name"		: str(wSTR_Tweet['user']['screen_name']),
					"description"		: str(wSTR_Tweet['user']['description'])
				}
				self.ARR_AgentUsers.update({ str(wSTR_Tweet['user']['id']) : wSTR_User })
			
			wFavoCnt += 1
		
		#############################
		# 自動フォローしていく
		wKeylist = list( self.ARR_AgentUsers.keys() )
		for wID in wKeylist :
			wID = str(wID)
			
			### フォロー人数の限界
			if gVal.DEF_STR_TLNUM['TimelineFollowNum']<=wFollowNum :
				break
			
			### 自動フォロー
###			wSubRes = self.OBJ_Parent.OBJ_TwitterFollower.AutoFollow( self.ARR_AgentUsers[wID] )
			wSubRes = self.OBJ_Parent.OBJ_TwitterFollower.AutoFollow( self.ARR_AgentUsers[wID]['id'] )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "AutoFollow is failed"
				gVal.OBJ_L.Log( "B", wRes )
				break	#失敗したら、ループ終わって処理を終わる
			
			if wSubRes['Responce']==False :
				### 未フォロー
				break
			
			wFollowNum += 1	#フォローしたのでカウント
		
		#############################
		# 現時間を設定
		wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "tl_follow", gVal.STR_Time['TimeDate'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "SetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		###	gVal.STR_Time['reaction']
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes

	#####################################################
	def __add_TimelineFollow_AgentUser( self, inARR_Users ):
		
		wKeylist = list( inARR_Users.keys() )
		for wID in wKeylist :
			wID = str(wID)
			
			if wID in self.ARR_AgentUsers :
				continue
			
			wSTR_User = {
				"id"				: str(inARR_Users[wID]['id']),
				"name"				: str(inARR_Users[wID]['name']),
				"screen_name"		: str(inARR_Users[wID]['screen_name']),
				"description"		: str(inARR_Users[wID]['description'])
			}
			self.ARR_AgentUsers.update({ wID : wSTR_User })
		
		return



