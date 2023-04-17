#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : Twitter I/F
#####################################################
from twitter_use import CLS_Twitter_Use

from traffic import CLS_Traffic
from ktime import CLS_TIME
from osif import CLS_OSIF
from mydisp import CLS_MyDisp
from gval import gVal
#####################################################
class CLS_Twitter_IF() :
#####################################################
	OBJ_Twitter = ""		#Twitterオブジェクト
	
							#Twitter情報
	ARR_MyFollowID = []		#  フォロー者ID	
	ARR_FollowerID = []		#  フォロワーID
	
	CHR_GetFollowDate = None
	ARR_FollowData = []		#退避用
	
	ARR_Favo       = {}		#  いいね一覧
	ARR_FavoUser = {}		#  いいね一覧のユーザ
	
	DEF_VAL_SLEEP = 10				#Twitter処理遅延（秒）
	DEF_VAL_FAVO_1DAYSEC = 86400	#いいね1日経過時間  1日 (60x60x24)x1

	ARR_SubscribeListUserID = []		#リスト登録しているユーザID
									# ※リスト通知、両フォロワー、片フォローは除く

	ARR_MutualListUserID = []		#相互フォローリスト登録しているユーザID
	ARR_FollowerListUserID = []		#片フォロワーリスト登録しているユーザID

	ARR_SubsList = {}		# 被登録リスト



#####################################################
# Init
#####################################################
	def __init__(self):
		return



#####################################################
# フォロー取得
#####################################################
	def GetFollow(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetFollow"
		
		#############################
		# 取得可能時間か？
		if self.CHR_GetFollowDate!=None :
			### 範囲時間内のツイートか
			wGetLag = CLS_OSIF.sTimeLag( str( self.CHR_GetFollowDate ), inThreshold=gVal.DEF_STR_TLNUM['forGetUserSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==False :
				### 規定以内は除外
				wRes['Result'] = True
				return wRes
		
		self.CHR_GetFollowDate = None	#一度クリアしておく(異常時再取得するため)
		
		#############################
		# フォロー情報取得
		CLS_MyDisp.sViewHeaderDisp( "フォロー情報取得" )
		
		#############################
		# フォロー一覧 取得
		wMyFollowRes = self.OBJ_Twitter.GetMyFollowList()
		CLS_Traffic.sP( "run_api", wMyFollowRes['RunAPI'] )
		if wMyFollowRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetMyFollowList): " + wMyFollowRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### Twitter Wait
		CLS_OSIF.sSleep( self.DEF_VAL_SLEEP )
		
		#############################
		# フォロワー一覧 取得
		wFollowerRes = self.OBJ_Twitter.GetFollowerList()
		CLS_Traffic.sP( "run_api", wFollowerRes['RunAPI'] )
		if wFollowerRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetFollowerList): " + wFollowerRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		self.ARR_MyFollowID = []	#  フォロー者ID	
		self.ARR_FollowerID = []	#  フォロワーID
		wARR_FollowData = {}
		#############################
		# フォローデータの加工
		wARR_MyFollowData = {}
		for wROW in wMyFollowRes['Responce'] :
			
			wID = str( wROW['id'] )
			wName = str(wROW['name']).replace( "'", "''" )
			###情報の詰め込み
			wCell = {
				"id"			: wID,
				"name"			: wName,
				"screen_name"	: str( wROW['screen_name'] ),
				"description"	: str( wROW['description'] ),
				"statuses_count"	: wROW['statuses_count'],
				"myfollow"		: True,
				"follower"		: False
			}
			wARR_FollowData.update({ wID : wCell })
			self.ARR_MyFollowID.append( wID )
		
		#############################
		# フォロワーデータの加工
		for wROW in wFollowerRes['Responce'] :
			
			wID = str( wROW['id'] )
			wName = str(wROW['name']).replace( "'", "''" )
			###情報の詰め込み
			if wID in self.ARR_MyFollowID :
				###相互
				wARR_FollowData[wID]['follower'] = True
			else :
				###片フォロワー
				wCell = {
					"id"			: wID,
					"name"			: wName,
					"screen_name"	: str( wROW['screen_name'] ),
					"description"	: str( wROW['description'] ),
					"statuses_count"	: wROW['statuses_count'],
					"myfollow"		: False,
					"follower"		: True
				}
				wARR_FollowData.update({ wID : wCell })
			
			self.ARR_FollowerID.append( wID )
		
		#############################
		# トラヒック計測：フォロワー監視情報
		CLS_Traffic.sP( "myfollow", len( self.ARR_MyFollowID ), False )
		CLS_Traffic.sP( "follower", len( self.ARR_FollowerID ), False )
		
		#############################
		# 正常
		
		###現時刻をメモる
		self.CHR_GetFollowDate = str(gVal.STR_Time['TimeDate'])
		self.ARR_FollowData    = wARR_FollowData
		
		wRes['Result'] = True
		return wRes



#####################################################
# ふぁぼ取得
#####################################################
	def GetFavo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetFavo"
		
		#############################
		# いいね情報取得
		CLS_MyDisp.sViewHeaderDisp( "いいね情報取得" )
		
		#############################
		# いいね一覧 取得
		wTwitterRes = self.OBJ_Twitter.GetFavolist()
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# トラヒック計測：いいね情報
		CLS_Traffic.sP( "favo", len( wTwitterRes['Responce'] ), False )
		
		#############################
		# いいね情報の作成
		self.ARR_FavoUser = {}
		self.ARR_Favo = {}
		
		for wROW in wTwitterRes['Responce'] :
			wResSub =self.AddFavoData( wROW, False )
			if wResSub['Result']!=True :
				wRes['Reason'] = "AddFavoData is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	# いいね情報追加
	#####################################################
	def AddFavoData( self, inTweet, inFLG_CheckUser=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "AddFavoData"
		
		wRes['Responce'] = {
			"dual"	: False,	#重複なし True=なし, False=あり
			"id"	: None
		}
		#############################
		# データが空の場合
		if "id" not in inTweet :
			wRes['Reason'] = "data error: not cell id"
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		wTweetID = str( inTweet['id'] )
		wRes['Responce']['id'] = wTweetID
		#############################
		# 重複があるか
		if wTweetID in self.ARR_Favo :
			wRes['Result'] = True
			return wRes
		
		#############################
		# ユーザ情報の追加
		wSubRes = self.__addFavoUserData( inTweet )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "__addFavoUserData error: reason=" + wSubRes['Reason']
			gVal.OBJ_L.Log( "A", wRes )
			return wRes
		if wSubRes['Responce']==False and inFLG_CheckUser==True :
			### ユーザ更新なし かつ チェックモード=ON
			### 終わり
			return wRes
		
		#############################
		# 本ツイートの処理
		wSubRes = self.__addFavoData( "normal", inTweet )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "__addFavoData error(normal): reason=" + wSubRes['Reason']
			gVal.OBJ_L.Log( "A", wRes )
			return wRes
		
		#############################
		# リツイートの場合、リツイート部分を追加
		if "retweeted_status" in inTweet :
			wSubRes = self.__addFavoData( "retweet", inTweet['retweeted_status'] )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "__addFavoData error(retweet): reason=" + wSubRes['Reason']
				gVal.OBJ_L.Log( "A", wRes )
				return wRes
		
		#############################
		# 引用リツイートの場合、リツイート部分を追加
		if "quoted_status" in inTweet :
			wSubRes = self.__addFavoData( "quoted", inTweet['quoted_status'] )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "__addFavoData error(quoted): reason=" + wSubRes['Reason']
				gVal.OBJ_L.Log( "A", wRes )
				return wRes
		
		wRes['Responce']['dual'] = True		#重複なし
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	# いいね情報追加
	#####################################################
	def __addFavoData( self, inKind, inTweet ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "__addFavoData"
		
		### 時間の変換
		wTime = CLS_TIME.sTTchg( wRes, "sTTchg: kind="+inKind, inTweet['created_at'] )
		if wTime['Result']!=True :
			wRes['Reason'] = wTime['Reason']
			return wRes
		
		wUserID = str(inTweet['user']['id'])
		
		#############################
		# いいね情報
		
		### 本文'の加工
		wText = str(inTweet['text']).replace( "'", "''" )
		
		### いいね情報の詰め込み
		wCellUser = {
			"id"			: wUserID,
			"screen_name"	: inTweet['user']['screen_name'],
			"description"	: inTweet['user']['description']
		}
		wCell = {
			"kind"			: inKind,
			"id"			: str(inTweet['id']),
			"text"			: wText,
			"created_at"	: str(wTime['TimeDate']),
			"user"			: wCellUser
		}
		self.ARR_Favo.update({ str(inTweet['id']) : wCell })
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	# いいね ユーザ情報追加
	#####################################################
	def __addFavoUserData( self, inTweet ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "__addFavoUserData"
		
		wRes['Responce'] = False	#新規or更新 True=あり, False=なし
		
		### 時間の変換
		wTime = CLS_TIME.sTTchg( wRes, "sTTchg", inTweet['created_at'] )
		if wTime['Result']!=True :
			wRes['Reason'] = wTime['Reason']
			return wRes
		
		wUserID = str(inTweet['user']['id'])
		
		#############################
		# ユーザ情報
		if wUserID not in self.ARR_FavoUser :
			### 未登録済なら枠追加
			wCellUser = {
				"id"			: wUserID,
				"screen_name"	: inTweet['user']['screen_name'],
				"description"	: inTweet['user']['description'],
				"created_at"	: str(wTime['TimeDate'])
			}
			self.ARR_FavoUser.update({ wUserID : wCellUser })
		else:
			#############################
			# 前の日付より新しければ新アクション
			wSubRes = CLS_OSIF.sCmpTime( str(wTime['TimeDate']), self.ARR_FavoUser[wUserID]['created_at'] )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "sCmpTime is failed"
				return wRes
			if wSubRes['Future']==True :
				### 最新
				self.ARR_FavoUser[wUserID]['created_at'] = str(wTime['TimeDate'])
			else:
				### 古い
				wRes['Result'] = True
				return wRes
		
		wRes['Responce'] = True		#新規or更新 あり
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

###	#####################################################
###	# 排他ユーザ追加
###	#####################################################
###	def AddFavoUserID( self, inTweet ):
###		#############################
###		# 応答形式の取得
###		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
###		wRes = CLS_OSIF.sGet_Resp()
###		wRes['Class'] = "CLS_Twitter_IF"
###		wRes['Func']  = "AddFavoUserID"
###		
####		#############################
####		# ツイート本文部分
####		wSubRes = self.__add_AddFavoUserID( inTweet, "normal" )
####		if wSubRes['Result']!=True :
####			wRes['Reason'] = "__add_AddFavoUserID is failed(1)"
####			gVal.OBJ_L.Log( "B", wRes )
####			return wRes
####		
####		#############################
####		# リツイートの場合、リツイート部分を追加
####		if "retweeted_status" in inTweet :
####			wSubRes = self.__add_AddFavoUserID( inTweet['retweeted_status'], "retweet" )
####			if wSubRes['Result']!=True :
####				wRes['Reason'] = "__add_AddFavoUserID is failed(2)"
####				gVal.OBJ_L.Log( "B", wRes )
####				return wRes
####		
####		#############################
####		# 引用リツイートの場合、引用リツイート部分を追加
####		if "quoted_status" in inTweet :
####			wSubRes = self.__add_AddFavoUserID( inTweet['quoted_status'], "quoted" )
####			if wSubRes['Result']!=True :
####				wRes['Reason'] = "__add_AddFavoUserID is failed(3)"
####				gVal.OBJ_L.Log( "B", wRes )
####				return wRes
####		
###		#############################
###		# データが空の場合
###		if "id" not in inTweet :
###			wRes['Reason'] = "data error: not cell id"
###			gVal.OBJ_L.Log( "D", wRes )
###			return wRes
###		
###		wID = str( inTweet['id'] )
###		wText = str(inTweet['text']).replace( "'", "''" )
###		wUserID = str( inTweet['user']['id'] )
###		
###		wRes['Responce'] = False	#重複なし True=なし, False=あり
###		#############################
###		# 時間の変換
###		wTime = CLS_TIME.sTTchg( wRes, "(1)", inTweet['created_at'] )
###		if wTime['Result']!=True :
###			return wRes
###		
###		#############################
###		# 種別のチェック
###		wKind  = "normal"
###		wRetID = None
###		if "retweeted_status" in inTweet :
###			wKind = "retweet"
###			wRetID = str(inTweet['retweeted_status']['id'])
###		elif "quoted_status" in inTweet :
###			wKind = "quoted"
###			wRetID = str(inTweet['quoted_status']['id'])
###		
###		#############################
###		# 重複があるか
###		if wID in self.ARR_Favo :
###			wRes['Result'] = True
###			return wRes
###		
###		### リツイートの場合、ツイ元のIDの重複もみる
######		if wKind=="retweet" :
###		if wKind!="normal" :
###			wKeylist = list( self.ARR_Favo.keys() )
###			for wIndex in wKeylist :
######				if self.ARR_Favo[wIndex]['ret_id']==wID :
###				if self.ARR_Favo[wIndex]['ret_id']==wRetID :
###					wRes['Result'] = True
###					return wRes
###		
###		#############################
###		# いいね情報の詰め込み
###		wCellUser = {
###			"id"			: wUserID,
###			"screen_name"	: inTweet['user']['screen_name'],
###			"description"	: inTweet['user']['description']
###		}
###		
###		wCell = {
###			"kind"			: wKind,
###			"id"			: wID,
###			"ret_id"		: wRetID,
###			"text"			: wText,
###			"created_at"	: str(wTime['TimeDate']),
###			"user"			: wCellUser
###		}
###		self.ARR_Favo.update({ wID : wCell })
###		
###		#############################
###		# ユーザの重複があるか
###		
###		#############################
###		# 重複なし
###		#   新規追加
###		if wUserID not in self.ARR_FavoUser :
###			wCellUser = {
###				"id"			: wUserID,
###				"screen_name"	: inTweet['user']['screen_name'],
###				"description"	: inTweet['user']['description']
###			}
###			wCell = {
###				"id"			: wID,
###				"created_at"	: str(wTime['TimeDate']),
###				"user"			: wCellUser
###			}
###			self.ARR_FavoUser.update({ wUserID : wCell })
###			wRes['Responce'] = True		#重複なし
###		
###		#############################
###		# 重複あり
###		else:
###			#############################
###			# 前の日付より新しければ新アクション
###			wSubRes = CLS_OSIF.sCmpTime( str(wTime['TimeDate']), self.ARR_FavoUser[wUserID]['created_at'] )
###			if wSubRes['Result']!=True :
###				###失敗
###				wRes['Reason'] = "sCmpTime is failed"
###				gVal.OBJ_L.Log( "B", wRes )
###				return wRes
###			if wSubRes['Future']==True :
###				### 最新
###				self.ARR_FavoUser[wUserID]['id']         = wID
###				self.ARR_FavoUser[wUserID]['created_at'] = str(wTime['TimeDate'])
###				wRes['Responce'] = True		#重複なし
### 		
###		#############################
###		# 正常
###		wRes['Result'] = True
###		return wRes

###	#####################################################
###	# 排他ユーザ追加
###	#####################################################
###	def __add_AddFavoUserID( self, inTweet, inKind ):
###		#############################
###		# 応答形式の取得
###		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
###		wRes = CLS_OSIF.sGet_Resp()
###		wRes['Class'] = "CLS_Twitter_IF"
###		wRes['Func']  = "__add_AddFavoUserID"
###		
###		wID = str( inTweet['id'] )
###		wText = str(inTweet['text']).replace( "'", "''" )
###		wUserID = str( inTweet['user']['id'] )
###		#############################
###		# 時間の変換
###		wTime = CLS_TIME.sTTchg( wRes, "(1)", inTweet['created_at'] )
###		if wTime['Result']!=True :
###			return wRes
###		
###		#############################
###		# 重複があるか
###		if wID in self.ARR_Favo :
###			wRes['Result'] = True
###			return wRes
###		
###		#############################
###		# いいね情報の詰め込み
###		wCellUser = {
###			"id"			: wUserID,
###			"screen_name"	: inTweet['user']['screen_name'],
###			"description"	: inTweet['user']['description']
###		}
###		
###		wCell = {
###			"kind"			: inKind,
###			"id"			: wID,
###			"text"			: wText,
###			"created_at"	: str(wTime['TimeDate']),
###			"user"			: wCellUser
###		}
###		self.ARR_Favo.update({ wID : wCell })
###		
###		#############################
###		# ユーザの重複があるか
###		
###		#############################
###		# 重複なし
###		#   新規追加
###		if wUserID not in self.ARR_FavoUser :
###			wCellUser = {
###				"id"			: wUserID,
###				"screen_name"	: inTweet['user']['screen_name'],
###				"description"	: inTweet['user']['description']
###			}
###			wCell = {
###				"id"			: wID,
###				"created_at"	: str(wTime['TimeDate']),
###				"user"			: wCellUser
###			}
###			self.ARR_FavoUser.update({ wUserID : wCell })
###
###		#############################
###		# 重複あり
###		else:
###			#############################
###			# 前の日付より新しければ新アクション
###			wSubRes = CLS_OSIF.sCmpTime( str(wTime['TimeDate']), self.ARR_FavoUser[wUserID]['created_at'] )
###			if wSubRes['Result']!=True :
###				###失敗
###				wRes['Reason'] = "sCmpTime is failed"
###				gVal.OBJ_L.Log( "B", wRes )
###				return wRes
###			if wSubRes['Future']==True :
###				### 最新
###				self.ARR_FavoUser[wUserID]['id']         = wID
###				self.ARR_FavoUser[wUserID]['created_at'] = str(wTime['TimeDate'])
###		
###		#############################
###		# 正常
###		wRes['Result'] = True
###		return wRes
###
	#####################################################
	# いいねデータ取得
	#####################################################
	def GetFavoData(self):
		return self.ARR_Favo

	#####################################################
	# チェックいいねID重複
	#####################################################
	def CheckFavoUserID( self, inID ):
		wID = str(inID)
		### 重複があるか
###		if wID not in self.ARR_Favo :
		if wID in self.ARR_Favo :
			return False	#あったらFalse= いいね済み
		return True			#いいねなし True



#####################################################
# Twitter接続設定
#####################################################
	def SetTwitter( self, inTwitterAccount ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "SetTwitter"
		
		#############################
		# Twitterオブジェクトの作成
		self.OBJ_Twitter = CLS_Twitter_Use()
		
		wRes['Responce'] = {}
		wRes['Responce'].update({
			"Account"   : inTwitterAccount,
			"APIkey"    : "(none)",
			"APIsecret" : "(none)",
			"ACCtoken"  : "(none)",
			"ACCsecret" : "(none)",
			"Bearer"    : "(none)"
		})
		
		#############################
		# Twitterキーの入力
		CLS_OSIF.sPrn( "Twitter APIキーの設定をおこないます。" )
		CLS_OSIF.sPrn( "---------------------------------------" )
		while True :
			###初期化
			wRes['Responce']['APIkey']    = "(none)"
			wRes['Responce']['APIsecret'] = "(none)"
			wRes['Responce']['ACCtoken']  = "(none)"
			wRes['Responce']['ACCsecret'] = "(none)"
			wRes['Responce']['Bearer']    = "(none)"
			
			#############################
			# 実行の確認
			wSelect = CLS_OSIF.sInp( "キャンセルしますか？(y)=> " )
			if wSelect=="y" :
				# 完了
				wRes['Result'] = True
				return wRes
			
			#############################
			# 入力
			wStr = "Twitter Devで取得した API key を入力してください。"
			CLS_OSIF.sPrn( wStr )
			wKey = CLS_OSIF.sGpp( "API key？=> " )
			if wKey=="" :
				CLS_OSIF.sPrn( "キーが未入力です" + '\n' )
				continue
			wRes['Responce']['APIkey'] = wKey
			
			wStr = "Twitter Devで取得した API secret key を入力してください。"
			CLS_OSIF.sPrn( wStr )
			wKey = CLS_OSIF.sGpp( "API secret key？=> " )
			if wKey=="" :
				CLS_OSIF.sPrn( "キーが未入力です" + '\n' )
				continue
			wRes['Responce']['APIsecret'] = wKey
			
			wStr = "Twitter Devで取得した Access token を入力してください。"
			CLS_OSIF.sPrn( wStr )
			wKey = CLS_OSIF.sGpp( "Access token？=> " )
			if wKey=="" :
				CLS_OSIF.sPrn( "キーが未入力です" + '\n' )
				continue
			wRes['Responce']['ACCtoken'] = wKey
			
			wStr = "Twitter Devで取得した Access token secret を入力してください。"
			CLS_OSIF.sPrn( wStr )
			wKey = CLS_OSIF.sGpp( "Access token secret？=> " )
			if wKey=="" :
				CLS_OSIF.sPrn( "キーが未入力です" + '\n' )
				continue
			wRes['Responce']['ACCsecret'] = wKey
			
			wStr = "Twitter Devで取得した Bearer token secret を入力してください。"
			CLS_OSIF.sPrn( wStr )
			wKey = CLS_OSIF.sGpp( "Bearer token secret？=> " )
			if wKey=="" :
				CLS_OSIF.sPrn( "キーが未入力です" + '\n' )
				continue
			wRes['Responce']['Bearer'] = wKey
			
			###ここまでで入力は完了した
			break
		
		#############################
		# Twitter接続テスト
		wTwitterRes_Create = self.OBJ_Twitter.Create(
					wRes['Responce']['Account'],
					wRes['Responce']['APIkey'],
					wRes['Responce']['APIsecret'],
					wRes['Responce']['ACCtoken'],
					wRes['Responce']['ACCsecret'],
					wRes['Responce']['Bearer']
				)
		wTwitterRes = self.OBJ_Twitter.GetTwStatus()
		if wTwitterRes_Create!=True :
			wRes['Reason'] = "Twitterの接続に失敗しました: reason=" + wTwitterRes['Reason']
			return wRes
		
		###結果の確認
		if wTwitterRes['Init']!=True :
			wRes['Reason'] = "Twitterが初期化できてません"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wStr = "Twitterへ正常に接続しました。" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		wRes['Result'] = True
		return wRes



#####################################################
# Twitter接続
#####################################################
	def Connect( self, inData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "Connect"
		
		#############################
		# 入力チェック
		if "apikey" not in inData or \
		   "apisecret" not in inData or \
		   "acctoken" not in inData or \
		   "accsecret" not in inData or \
		   "bearer" not in inData :
			
			wRes['Reason'] = "入力チェックエラー"
			gVal.OBJ_L.Log( "B", wRes )
			
			self.__connectFailView()
			return False
		
		#############################
		# Twitter生成→接続
		self.OBJ_Twitter = CLS_Twitter_Use()
		wTwitterRes_Create = self.OBJ_Twitter.Create(
			gVal.STR_UserInfo['Account'],
			inData['apikey'],
			inData['apisecret'],
			inData['acctoken'],
			inData['accsecret'],
			inData['bearer']
			)
		
		#############################
		# Twitter状態の取得
		wTwitterRes = self.OBJ_Twitter.GetTwStatus()
		if wTwitterRes_Create!=True :
			wRes['Reason'] = "Twitterの接続失敗: reason=" + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			
			self.__connectFailView()
			return False
		
		###結果の確認
		if wTwitterRes['Init']!=True :
			wRes['Reason'] = "Twitter初期化失敗"
			gVal.OBJ_L.Log( "B", wRes )
			
			self.__connectFailView()
			return False
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes

	def __connectFailView(self):
		if gVal.FLG_Test_Mode==False :
			return	#テストモードでなければ終わる
		
		#############################
		# DB接続情報を表示
		wStr =        "******************************" + '\n'
		wStr = wStr + "API Key    : " + inAPIkey + '\n'
		wStr = wStr + "API Secret : " + inAPIsecret + '\n'
		wStr = wStr + "ACC Token  : " + inACCtoken + '\n'
		wStr = wStr + "ACC Secret : " + inACCsecret + '\n'
		wStr = wStr + "Bearer     : " + inBearer + '\n'
		wStr = wStr + "******************************" + '\n'
		CLS_OSIF.sPrn( wStr )
		return



#####################################################
# Twitter再接続
#####################################################
	def ReConnect(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "ReConnect"
		
		#############################
		# APIカウントリセット
		self.OBJ_Twitter.ResetAPI()
		
		#############################
		# Twitter再接続
		wTwitterRes = self.OBJ_Twitter.Connect()
		
		#############################
		# Twitter状態の取得
		if wTwitterRes!=True :
			wTwitterStatus = self.OBJ_Twitter.GetTwStatus()
			wRes['Reason'] = "Twitterの再接続失敗: reason=" + wTwitterStatus['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# ログ
		gVal.OBJ_L.Log( "S", wRes, "Twitter規制解除＆再接続" )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# Pingテスト
#####################################################
	def Ping( self , inHost=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "Ping"
		
		self.OBJ_Twitter = CLS_Twitter_Use()
		#############################
		# Pingテスト
		wTwitterRes = self.OBJ_Twitter.Ping( inHost=inHost )
		
		#############################
		# Twitter状態の取得
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "pingテスト失敗: " + wTwitterRes['Reason']
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# タイムライン読み込み処理
#####################################################
	def GetTL( self, inTLmode="home", inFLG_Rep=True, inFLG_Rts=False, inCount=CLS_Twitter_Use.VAL_TwitNum, inID=None, inListID=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetTL"
		
		#############################
		# ユーザツイートを取得
		wTwitterRes = self.OBJ_Twitter.GetTL( inTLmode=inTLmode, inFLG_Rep=inFLG_Rep, inFLG_Rts=inFLG_Rts, inCount=inCount, inID=inID, inListID=inListID )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# トラヒック計測：取得タイムライン数
		CLS_Traffic.sP( "timeline", len( wTwitterRes['Responce'] ) )
		
		#############################
		# 完了
		wRes['Responce'] = wTwitterRes['Responce']
		wRes['Result'] = True
		return wRes



#####################################################
# タイムライン検索
#####################################################
	def GetSearch( self, inQuery, inMaxResult=40 ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetSearch"
		
		#############################
		# 検索を利用する
		wTwitterRes = self.OBJ_Twitter.GetTweetSearch_v2( inQuery=inQuery, inMaxResult=inMaxResult )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTwitterRes['Reason'] + " query=" + str(inQuery)
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# データ加工
		#   いいねがない場合はセットなし
		wARR_Tweets = {}
		if wTwitterRes['Responce']['meta']['result_count']>0 and \
		   "includes" in wTwitterRes['Responce'] and \
		   "data" in wTwitterRes['Responce'] :
			
			### Tweetデータから対象引用リツイートを抽出
			for wTweet in wTwitterRes['Responce']['data'] :
				### 枠の作成
				wSTR_CellUser = {
					"id"			: None,
					"name"			: None,
					"screen_name"	: None,
					"description"	: None
				}
				wSTR_Cell = {
					"type"				: None,
					"reply_settings"	: None,
					"id"				: None,
					"text"				: None,
					"created_at"		: None,
					"referenced_id"		: None,
					"user"				: wSTR_CellUser
				}
				
				### リプライの抜き取り
				if "referenced_tweets" not in wTweet :
					### 通常ツイート
					wID = str( wTweet['id'] )
					wSTR_Cell['type'] = "normal"
					wSTR_Cell['reply_settings'] = str( wTweet['reply_settings'] )
					wSTR_Cell['id']             = wID
					wSTR_Cell['text']           = str( wTweet['text'] )
					wSTR_Cell['created_at']     = str( wTweet['created_at'] )
					wSTR_Cell['user']['id']     = str( wTweet['author_id'] )
					wSTR_Cell.update({ "set_data" : False })
					wARR_Tweets.update({ wID : wSTR_Cell })
				
				else :
					for wTweetCont in wTweet['referenced_tweets'] :
						if "id" not in wTweetCont :
							continue
						if wTweetCont['type']!="replied_to" and \
						   wTweetCont['type']!="quoted" and \
						   wTweetCont['type']!="retweeted" :
							continue
						
						### 値の抜き取り
						wID = str( wTweet['id'] )
						wSTR_Cell['type']           = str( wTweetCont['type'] )
						wSTR_Cell['referenced_id']  = str( wTweetCont['id'] )
						
						wSTR_Cell['reply_settings'] = str( wTweet['reply_settings'] )
						wSTR_Cell['id']             = wID
						wSTR_Cell['text']           = str( wTweet['text'] )
						wSTR_Cell['created_at']     = str( wTweet['created_at'] )
						wSTR_Cell['user']['id']     = str( wTweet['author_id'] )
						wSTR_Cell.update({ "set_data" : False })
						wARR_Tweets.update({ wID : wSTR_Cell })
			
			### Tweetデータから関連ユーザ情報を抜き出す
			wARR_Users = {}
			for wUser in wTwitterRes['Responce']['includes']['users'] :
				wID = str( wUser['id'] )
				if wID in wARR_Users :
					continue
				wName = wUser['name'].replace( "'", "''" )
				
				wSTR_Cell = {
					"id"			: wID,
					"name"			: wName,
					"screen_name"	: wUser['username'],
					"description"	: wUser['description']
				}
				wARR_Users.update({ wID : wSTR_Cell })
			
			### ユーザ情報を反映する
			wKeylist  = list( wARR_Tweets.keys() )
			for wID in wKeylist :
				wUserID = wARR_Tweets[wID]['user']['id']
				if wUserID not in wARR_Users :
					### ユーザ情報がない
					continue
				
				###日時の変換
				wTime = CLS_TIME.sTTchg( wRes, "(2)", wARR_Tweets[wID]['created_at'] )
				if wTime['Result']!=True :
					continue
				wARR_Tweets[wID]['created_at'] = wTime['TimeDate']
				
				wARR_Tweets[wID]['user']['name']        = wARR_Users[wUserID]['name']
				wARR_Tweets[wID]['user']['screen_name'] = wARR_Users[wUserID]['screen_name']
				wARR_Tweets[wID]['user']['description'] = wARR_Users[wUserID]['description']
				wARR_Tweets[wID]['set_data'] = True
		
		###返すデータを設定する
		wResTweet = []
		wKeylist  = list( wARR_Tweets.keys() )
		for wID in wKeylist :
			if wARR_Tweets[wID]['set_data']==True :
				wResTweet.append( wARR_Tweets[wID] )
		
		#############################
		# トラヒック計測：取得タイムライン数
		CLS_Traffic.sP( "timeline", len( wTwitterRes['Responce'] ) )
		
		#############################
		# 完了
		wRes['Responce'] = wResTweet
		wRes['Result'] = True
		return wRes



#####################################################
# Tweet Tweet Lookup取得
#####################################################
	def GetTweetLookup( self, inID=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetTweetLookup"
		
		#############################
		# ユーザツイートを取得
		wTwitterRes = self.OBJ_Twitter.GetTweetLookup( inID=inID )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# データ加工
###		wTweets = {}
		wTweets = None
		if "data" in wTwitterRes['Responce'] :
			
			wID     = str( wTwitterRes['Responce']['data']['id'] )
			wUserID = str( wTwitterRes['Responce']['data']['author_id'] )
			
			### screen_nameの取り出し
			wScreenName = ""
			for wUsers in wTwitterRes['Responce']['includes']['users'] :
				if str(wUsers['id'])==wUserID :
					wScreenName  = wUsers['username']
					wDescription = wUsers['description']
					break
			
			###日時の変換
			wTimeDate = wTwitterRes['Responce']['data']['created_at']
			wTimeRes = CLS_TIME.sTTchg( wRes, "(3)", wTimeDate )
			if wTimeRes['Result']!=True :
				return wRes
			wTimeDate = str( wTimeRes['TimeDate'] )
		 	
			wSTR_CellUser = {
				"id" 			: wUserID,
				"screen_name"	: wScreenName,
				"description"	: wDescription
			}
			wSTR_Cell = {
				"created_at"	: wTimeDate,
				"id"			: wID,
				"text"			: wTwitterRes['Responce']['data']['text'],
				"user"			: wSTR_CellUser
			}
			wSTR_Cell.update({ "data" : wTwitterRes['Responce'] })
			wTweets = wSTR_Cell
		
		#############################
		# トラヒック計測：取得タイムライン数
		CLS_Traffic.sP( "timeline", len( wTwitterRes['Responce'] ) )
		
		#############################
		# 完了
		wRes['Responce'] = wTweets
		wRes['Result'] = True
		return wRes



#####################################################
# Tweet Mention Lookup取得
# メンション情報を取得する
#####################################################
	def GetMyMentionLookup( self, inID=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetMyMentionLookup"
		
		#############################
		# IDの指定
		if inID!=None :
			wUserID = inID
		else:
			### 指定がなければ、自分を設定する
			wUserID = gVal.STR_UserInfo['id']
		
		#############################
		# メンション情報を取得
		wTwitterRes = self.OBJ_Twitter.GetMentionLookup( inID=wUserID )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# データ加工
		#   メンション情報がない場合はセットなし
		wMentions = {}
		if "meta" in wTwitterRes['Responce'] :
			if wTwitterRes['Responce']['meta']['result_count']>0 and \
			   "data" in wTwitterRes['Responce'] :
				
				for wTweet in wTwitterRes['Responce']['data'] :
					wReplyID     = str( wTweet['id'] )
					wReplyUserID = str( wTweet['author_id'] )
					wReplyText   = str( wTweet['text'] )
					
					###日時の変換
					wTimeDate = wTweet['created_at']
					wTimeRes = CLS_TIME.sTTchg( wRes, "(3)", wTimeDate )
					if wTimeRes['Result']!=True :
						return wRes
					wTimeDate = str( wTimeRes['TimeDate'] )
			 		
					if "referenced_tweets" not in wTweet :
						continue
					wTweetID = str( wTweet['referenced_tweets'][0]['id'] )
					
					### screen_nameの取り出し
					wScreenName = ""
					for wUsers in wTwitterRes['Responce']['includes']['users'] :
						if str(wUsers['id'])==wReplyUserID :
							wScreenName  = wUsers['username']
							wDescription = wUsers['description']
							break
					
					wSTR_CellUser = {
						"id" 			: wReplyUserID,
						"screen_name"	: wScreenName,
						"description"	: wDescription
					}
					wSTR_Cell = {
						"id"			: wReplyID,			# リプライツイートID（お相手のツイートID）
						"created_at"    : wTimeDate,		# リプライの時刻（お相手のツイート日時 Twitter時間）
						"text"			: wReplyText,		# リプライの内容・テキスト
						"tweet_id"		: wTweetID,			# リプライ先のツイートID（自分・ワシのツイートIDじゃけえ）
						"user"			: wSTR_CellUser		# ユーザ情報
					}
					wMentions.update({ wReplyID : wSTR_Cell })
			
			#############################
			# トラヒック計測：取得タイムライン数
			CLS_Traffic.sP( "timeline", len( wMentions ) )
		
		#############################
		# 完了
		wRes['Responce'] = wMentions
		wRes['Result'] = True
		return wRes



#####################################################
# Tweet Likes Lookup取得
#   いいねした人のユーザ情報を取得する
#####################################################
	def GetLikesLookup( self, inID=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetLikesLookup"
		
		#############################
		# ユーザツイートを取得
		wTwitterRes = self.OBJ_Twitter.GetLikesLookup( inID=inID )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# データ加工
		#   いいねがない場合はセットなし
		wUsers = {}
		if "meta" in wTwitterRes['Responce'] :
			if wTwitterRes['Responce']['meta']['result_count']>0 and \
			   "data" in wTwitterRes['Responce'] :
				for wUser in wTwitterRes['Responce']['data'] :
					wID = str(wUser['id'])
					wName = wUser['name'].replace( "'", "''" )
					
					wSTR_Cell = {
						"id"			: wID,
						"name"			: wName,
						"screen_name"	: wUser['username'],
						"description"	: wUser['description']
					}
					wUsers.update({ wID : wSTR_Cell })
		
		#############################
		# 完了
		wRes['Responce'] = wUsers
		wRes['Result'] = True
		return wRes



#####################################################
# Tweet retweeted by 取得
#   リツイートした人のユーザ情報を取得する
#####################################################
	def GetRetweetLookup( self, inID=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetRetweetLookup"
		
		#############################
		# ユーザツイートを取得
		wTwitterRes = self.OBJ_Twitter.GetRetweetLookup( inID=inID )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# データ加工
		#   いいねがない場合はセットなし
		wUsers = {}
		if "meta" in wTwitterRes['Responce'] :
			if wTwitterRes['Responce']['meta']['result_count']>0 and \
			   "data" in wTwitterRes['Responce'] :
				for wUser in wTwitterRes['Responce']['data'] :
					wID = str(wUser['id'])
					wName = wUser['name'].replace( "'", "''" )
					
					wSTR_Cell = {
						"id"			: wID,
						"name"			: wName,
						"screen_name"	: wUser['username'],
						"description"	: wUser['description']
					}
					wUsers.update({ wID : wSTR_Cell })
		
		#############################
		# 完了
		wRes['Responce'] = wUsers
		wRes['Result'] = True
		return wRes



#####################################################
# Tweet reference retweeted 取得
#   引用リツイートした人のユーザ情報を取得する
#####################################################
	def GetRefRetweetLookup( self, inID=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetRefRetweetLookup"
		
		#############################
		# 検索を利用する
		wQuery = "{id} -is:retweet"
		wQuery = wQuery.format( id=inID )
		wTwitterRes = self.OBJ_Twitter.GetTweetSearch_v2( inQuery=wQuery )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# データ加工
		#   いいねがない場合はセットなし
		wUsers = {}
		if "meta" in wTwitterRes['Responce'] :
			if wTwitterRes['Responce']['meta']['result_count']>0 and \
			   "includes" in wTwitterRes['Responce'] and \
			   "data" in wTwitterRes['Responce'] :
				
				### Tweetデータから対象引用リツイートを抽出
				for wTweet in wTwitterRes['Responce']['data'] :
					if "referenced_tweets" not in wTweet :
						continue
					for wTweetCont in wTweet['referenced_tweets'] :
						wSTR_Cell = {}
						if "id" not in wTweetCont :
							continue
						wID = str(wTweetCont['id'])
						if wID!=inID :
							continue
						
						wUserID = str( wTweet['author_id'] )
						wSTR_Cell = {
							"id"			: wUserID,
							"name"			: None,
							"screen_name"	: None,
							"description"	: None,
							"tweet_id"		: str(wTweet['id']),
							"text"			: wTweet['text'],
							"set_data"		: True
						}
						break
					if "set_data" in wSTR_Cell :
						wUsers.update({ wUserID : wSTR_Cell })
				
				### Tweetデータから関連ユーザ情報を抜き出す
				for wUser in wTwitterRes['Responce']['includes']['users'] :
					wUserID = str( wUser['id'] )
					if wUserID not in wUsers :
						continue
					wUsers[wUserID]['name'] = wUser['name'].replace( "'", "''" )
					wUsers[wUserID]['screen_name'] = wUser['username']
					wUsers[wUserID]['description'] = wUser['description']
		
		#############################
		# 完了
		wRes['Responce'] = wUsers
		wRes['Result'] = True
		return wRes



#####################################################
# ついーと処理
#####################################################
	def Tweet( self, inTweet ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "Tweet"
		
		#############################
		# ツイート
		wTwitterRes = self.OBJ_Twitter.Tweet( inTweet )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTwitterRes['Reason']
			wRes.update({ "StatusCode" : str(wTwitterRes['StatusCode']) })
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# トラヒック計測：ツイート送信数
		CLS_Traffic.sP( "p_tweet" )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# ついーと削除処理
#####################################################
	def DelTweet( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "DelTweet"
		
		#############################
		# ツイート
		wTwitterRes = self.OBJ_Twitter.DelTweet( inID )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# DM処理
#####################################################
	def SendDM( self, inID, inTweet ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "Tweet"
		
		#############################
		# DM送信
		wTwitterRes = self.OBJ_Twitter.SendDM( inID, inTweet )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# トラヒック計測：ツイート送信数
		CLS_Traffic.sP( "p_tweet" )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# フォロー
#####################################################
	def Follow( self, inID, inMute=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "Follow"

		#############################
		# フォローする
		wTwitterRes = self.OBJ_Twitter.CreateFollow( inID )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		### Twitter Wait
		CLS_OSIF.sSleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(CreateFollow): " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# フォローに追加
		if self.CheckMyFollow( inID )==False :
			self.ARR_MyFollowID.append( inID )
		#############################
		# 完了
		wRes['Result'] = True
		
		#############################
		# ミュートする
		if inMute==True :
			wTwitterRes = self.OBJ_Twitter.CreateMute( inID )
			CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
			if wTwitterRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(CreateMute): " + wTwitterRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
		
		return wRes

	#####################################################
	def CheckMyFollow( self, inID ):
		if str( inID ) not in self.ARR_MyFollowID :
			return False
		return True

	#####################################################
	def CheckFollower( self, inID ):
		if str( inID ) not in self.ARR_FollowerID :
			return False
		return True

	#####################################################
	def GetFollowerID(self):
		wSTR_Follower = {
			"MyFollowID" : self.ARR_MyFollowID,
			"FollowerID" : self.ARR_FollowerID
		}
		return wSTR_Follower

	#####################################################
	def GetFollowerData(self):
		return self.ARR_FollowData



#####################################################
# リムーブ
#####################################################
	def Remove( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "Remove"

		#############################
		# リムーブする
		wTwitterRes = self.OBJ_Twitter.RemoveFollow( inID )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		
		wRes['StatusCode'] = wTwitterRes['StatusCode']
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(RemoveFollow): " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# フォロー情報に反映
		if inID in self.ARR_MyFollowID :
			self.ARR_MyFollowID.remove( inID )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# ブロックリムーブ
#####################################################
	def BlockRemove( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "BlockRemove"
		
		#############################
		# ブロックする
		wTwitterRes = self.OBJ_Twitter.CreateBlock( inID )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(CreateBlock): " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### Twitter Wait
		CLS_OSIF.sSleep( self.DEF_VAL_SLEEP )
		
		#############################
		# ブロック解除する
		wTwitterRes = self.OBJ_Twitter.RemoveBlock( inID )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(RemoveBlock): " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# フォロー情報に反映
		if inID in self.ARR_MyFollowID :
			self.ARR_MyFollowID.remove( inID )
		if inID in self.ARR_FollowerID :
			self.ARR_FollowerID.remove( inID )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# 当該ユーザのいいね一覧 取得
#####################################################
	def GetUserFavolist( self, inID, inCount=2 ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetUserFavolist"
		
		#############################
		# いいね一覧を取得
		wTwitterRes = self.OBJ_Twitter.GetUserFavolist( inID, inCount )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Responce'] = wTwitterRes['Responce']
		wRes['Result'] = True
		return wRes



#####################################################
# いいね
#####################################################
###	def Favo( self, inID ):
	def Favo( self, inTweet ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "Favo"
		
		wRes['Responce'] = {
			"Run"	: False,
			"Data"	: None
		}
		#############################
		# いいね情報を登録する
		wResSub =self.AddFavoData( inTweet )
		if wResSub['Result']!=True :
			wRes['Reason'] = "AddFavoData is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wResSub['Responce']['dual']==False :
			### いいね情報更新なし 抜ける
			wRes['Result'] = True
			return wRes
		
		#############################
		# いいねする
###		wTwitterRes = self.OBJ_Twitter.CreateFavo( inID )
		wTwitterRes = self.OBJ_Twitter.CreateFavo( wResSub['Responce']['id'] )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wStr = "Twitter API Error(CreateFavo): " + wTwitterRes['Reason']
			wStr = wStr + " id=" + str(inTweet['id'])
###			wStr = wStr + " screen_name=" + wResSub['Responce']['user']['screen_name']
			wRes['Reason'] = wStr
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# トラヒック計測：いいね実施数
		CLS_Traffic.sP( "p_favo" )
		
		#############################
		# 完了
###		wRes['Responce']['Data'] = self.ARR_Favo[inID]
		wRes['Responce']['Run']  = True
		
		wRes['Result'] = True
		return wRes



#####################################################
# いいね解除
#####################################################
	def FavoRemove( self, inID, inFLG_Rem=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "FavoRemove"
		
		wRes['Responce'] = {
			"Run"	: False,
			"Data"	: None
		}
		#############################
		# いいねがないなら抜ける
		wID = str( inID )
		if wID not in self.ARR_Favo :
			### いいね済み
			wRes['Result'] = True
			return wRes
		
		wRes['Responce']['Data'] = self.ARR_Favo[wID]
		#############################
		# いいね解除する
		wTwitterRes = self.OBJ_Twitter.RemoveFavo( inID )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wStr = "Twitter API Error(RemoveFavo): " + wTwitterRes['Reason']
			wStr = wStr + " kind=" + self.ARR_Favo[inID]['kind']
			wStr = wStr + " id=" + str(inID)
			wStr = wStr + " screen_name=" + self.ARR_Favo[inID]['user']['screen_name']
			wRes['Reason'] = wStr
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# いいね情報を削除する
		if inFLG_Rem==True :
			self.ARR_Favo.pop( wID )
			### 通常、再度いいねしないよう削除しない
		
		#############################
		# トラヒック計測：いいね解除数
		CLS_Traffic.sP( "d_favo" )
		
		#############################
		# 完了
		wRes['Responce']['Run']  = True
		wRes['Result'] = True
		return wRes



#####################################################
# いいねユーザチェック
#####################################################
	def CheckFavoUser( self, inUserID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "CheckFavoUser"
		
		wRes['Responce'] = True
		### False = 重複いいねなし判定（現いいね有効）
		### True  = 重複いいねあり判定（現いいね無効）
		#############################
		# ユーザがない場合
		if inUserID not in self.ARR_FavoUser :
			wRes['Responce'] = False	# 重複いいねなし
			wRes['Result'] = True
			return wRes
		
		#############################
		# 1日超経過してるか？
		wGetLag = CLS_OSIF.sTimeLag( self.ARR_FavoUser[inUserID]['created_at'] , inThreshold=self.DEF_VAL_FAVO_1DAYSEC )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed(1)"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wGetLag['Beyond']==True :
			###期間外= 1日超経過
			wRes['Responce'] = False	# 重複いいねなし
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# リツイート
#####################################################
	def Retweet( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "Retweet"
		
		#############################
		# リツイートする
		wTwitterRes = self.OBJ_Twitter.CreateRetweet( inID )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# ミュート一覧取得
#####################################################
	def GetMuteList(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetMuteList"
		
		#############################
		# ミュート一覧 取得
		wMuteRes = self.OBJ_Twitter.GetMuteIDs()
		CLS_Traffic.sP( "run_api", wMuteRes['RunAPI'] )
		if wMuteRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetMuteIDs): " + wMuteRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Responce'] = wMuteRes['Responce']
		wRes['Result'] = True
		return wRes



#####################################################
# ミュート
#####################################################
	def Mute( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "Mute"
		
		#############################
		# ミュートする
		wTwitterRes = self.OBJ_Twitter.CreateMute( inID )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(CreateMute): " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# ミュート解除
#####################################################
	def RemoveMute( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "RemoveMute"
		
		#############################
		# ミュート解除する
		wTwitterRes = self.OBJ_Twitter.RemoveMute( inID )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(RemoveMute): " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# ミュート解除(できるだけ)
#####################################################
###	def AllMuteRemove(self):
###		#############################
###		# 応答形式の取得
###		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
###		wRes = CLS_OSIF.sGet_Resp()
###		wRes['Class'] = "CLS_Twitter_IF"
###		wRes['Func']  = "AllMuteRemove"
###		
###		wRes['Responce'] = False
###		#############################
###		# ミュート一覧 取得
###		wMuteRes = self.OBJ_Twitter.GetMuteIDs()
###		CLS_Traffic.sP( "run_api", wMuteRes['RunAPI'] )
###		if wMuteRes['Result']!=True :
###			wRes['Reason'] = "Twitter API Error(GetMuteIDs): " + wMuteRes['Reason']
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		
###		#############################
###		# ミュート解除ID一覧の作成
###		wARR_MuteRemoveID = []
###		if len(wMuteRes['Responce'])>=1 :
###			for wID in wMuteRes['Responce']:
###				wID = str( wID )
###				
###				###フォロー者は対象外
###				if self.CheckMyFollow( wID )==True :
###					continue
###				
###				wARR_MuteRemoveID.append( wID )
###		
###		###対象者なし
###		if len( wARR_MuteRemoveID )==0 :
###			wRes['Result'] = True
###			return wRes
###		
###		#############################
###		# 解除実行
###		else:
###			#############################
###			# ミュート解除していく
###			wStr = "ミュート解除対象数: " + str(len( wARR_MuteRemoveID )) + '\n'
###			wStr = wStr + "ミュート解除中......." + '\n'
###			CLS_OSIF.sPrn( wStr )
###			
###			for wID in wARR_MuteRemoveID :
###				###  ミュート解除する
###				wRemoveRes = self.OBJ_Twitter.RemoveMute( wID )
###				if wRemoveRes['Result']!=True :
###					wRes['Reason'] = "Twitter API Error(RemoveMute): " + wRemoveRes['Reason']
###					gVal.OBJ_L.Log( "B", wRes )
###					return wRes
###				### Twitter Wait
###				CLS_OSIF.sSleep( self.DEF_VAL_SLEEP )
###				
###				###  ミュート一覧にないID=ミュート解除してない 場合は待機スキップ
###				if wRemoveRes['Responce']==False :
###					continue
###		
###		#############################
###		# 完了
###		wRes['Responce'] = True
###		wRes['Result'] = True
###		return wRes
###
###

#####################################################
# 自ユーザ情報 取得
#####################################################
	def GetMyUserinfo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetMyUserinfo"
		
		#############################
		# Twitterから自ユーザ情報を取得する
		wTwitterRes = self.OBJ_Twitter.GetMyUserinfo()
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter Error: " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Responce'] = wTwitterRes['Responce']
		wRes['Result'] = True
		return wRes



#####################################################
# ユーザ情報 取得
#####################################################
	def GetUserinfo( self, inID=-1, inScreenName=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetUserinfo"
		
		#############################
		# Twitterからユーザ情報を取得する
		wTwitterRes = self.OBJ_Twitter.GetUserinfo( inID=inID, inScreenName=inScreenName )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		
		wRes['StatusCode'] = wTwitterRes['StatusCode']
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter Error: " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Responce'] = wTwitterRes['Responce']
		wRes['Result'] = True
		return wRes



#####################################################
# フォロー者ID一覧 取得
#####################################################
###	def GetFollowIDList( self, inID ):
	def GetMyFollowIDList( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
###		wRes['Func']  = "GetFollowIDList"
		wRes['Func']  = "GetMyFollowIDList"

		#############################
		# フォロー者ID一覧 取得
###		wTwitterRes = self.OBJ_Twitter.GetFollowIDList( inID )
		wTwitterRes = self.OBJ_Twitter.GetMyFollowIDList( inID )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Responce'] = wTwitterRes['Responce']
		wRes['Result'] = True
		return wRes



#####################################################
# フォロワーID一覧 取得
#####################################################
	def GetFollowerIDList( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetFollowerIDList"

		#############################
		# フォロワーID一覧 取得
		wTwitterRes = self.OBJ_Twitter.GetFollowerIDList( inID )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error: " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Responce'] = wTwitterRes['Responce']
		wRes['Result'] = True
		return wRes



#####################################################
# 関係チェック
#####################################################
	def GetFollowInfo( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetFollowInfo"
		
		#############################
		# Twitterから関係情報を取得
		wTwitterRes = self.OBJ_Twitter.GetFollowInfo( gVal.STR_UserInfo['id'], inID )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		
		#############################
		# 結果チェック
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "GetFollowInfo API Error: " + wTwitterRes['Reason']
			wRes['Responce'] = wTwitterRes['StatusCode']
			return wRes
		
		#############################
		# 完了
		wRes['Responce'] = wTwitterRes['Responce']['relationship']['source']
		wRes['Result'] = True
		return wRes



#####################################################
# トレンド取得
#####################################################
	def GetTrends(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetTrends"
		
		#############################
		# Twitterからトレンドを取得
		wTwitterRes = self.OBJ_Twitter.GetTrends()
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		
		wRes['Responce'] = {
			"trends"		: [],
			"as_of"			: None,		#リストが作られた日時
			"created_at"	: None		#最も古いトレンド日時
		}
		#############################
		# Twitter処理結果
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "GetTrends API Error: " + wTwitterRes['Reason']
			return wRes
		if len(wTwitterRes['Responce'])<=0 :
			wRes['Reason'] = "Trend Data error: not 0"
			return wRes
		if "trends" not in wTwitterRes['Responce'][0] :
			wRes['Reason'] = "Trend Data error: not trends"
			return wRes
		wTrendRes = wTwitterRes['Responce'][0]['trends']
		
		#############################
		# トレンド情報の詰め込み
		wARR_Trends = {}
		wIndex = 0
		for wROW in wTrendRes :
			wCell = {
				"name"				: str( wROW['name'] ),
				"promoted_content"	: wROW['promoted_content'],
				"tweet_volume"		: wROW['tweet_volume'],
				"hit"				: 0
			}
			wARR_Trends.update({ wIndex : wCell })
			wIndex += 1
		
		if len(wARR_Trends)==0 :
			wRes['Reason'] = "Trend Data error: set trend=0"
			return wRes
		
		#############################
		# データの設定
		wTime = CLS_TIME.sTTchg( wRes, "(4)", wTwitterRes['Responce'][0]['as_of'] )
		if wTime['Result']!=True :
			return wRes
		wRes['Responce']['as_of'] = wTime['TimeDate']
		
		wTime = CLS_TIME.sTTchg( wRes, "(5)", wTwitterRes['Responce'][0]['created_at'] )
		if wTime['Result']!=True :
			return wRes
		wRes['Responce']['created_at'] = wTime['TimeDate']
		
		wRes['Responce']['trends'] = wARR_Trends
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# リストID取得
#   リストチェックも兼ねる
#####################################################
	def GetListID( self, inListName, inScreenName=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetListID"
		
		wRes['Responce'] = None
		#############################
		# リスト取得
		wTwitterRes = self.OBJ_Twitter.GetLists( inScreenName=inScreenName )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetLists): " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# リストIDを抽出する
		wListID = None
		wKeylist = list( wTwitterRes['Responce'].keys() )
		for wKey in wKeylist :
			if wTwitterRes['Responce'][wKey]['name']==inListName :
				wListID = wTwitterRes['Responce'][wKey]['id']
				break
		
		if wListID==None :
			### 処理は正常だが、該当リストはない
			wRes['Result'] = True
			return wRes
		
		#############################
		# 正常、リストIDを返す
		wRes['Responce'] = wListID
		wRes['Result'] = True
		return wRes



#####################################################
# リストユーザ取得
#####################################################
	def GetListMember( self, inListName, inScreenName=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetListMember"
		
		wRes['Responce'] = {}
		#############################
		# リストがTwitterにあるか確認
		wTwitterRes = self.GetListID(
		   inListName=inListName,
		   inScreenName=inScreenName )
		
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "CheckList is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wTwitterRes['Responce']==None :
			wRes['Reason'] = "List is not found: list=" + inListName + " owner=" + str(inScreenName)
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# ユーザ一覧を取得する
		wARR_ListUser = {}
		
		wTwitterRes = self.OBJ_Twitter.GetListMember(
		   inListName=inListName,
		   inScreenName=inScreenName )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetListMember): " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		for wLine in wTwitterRes['Responce'] :
			wID = str( wLine['id'] )
			wCell = {
				"id"          : wID,
				"screen_name" : wLine['screen_name'],
				"description" : wLine['description']
			}
			wARR_ListUser.update({ wID : wCell })
		
		wRes['Responce'] = wARR_ListUser
		wRes['Result'] = True
		return wRes



#####################################################
# リスト登録者取得
#####################################################
	def GetListSubscribers( self, inListName, inScreenName=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetListSubscribers"
		
		wRes['Responce'] = {}
		#############################
		# リストがTwitterにあるか確認
		wTwitterRes = self.GetListID(
		   inListName=inListName,
		   inScreenName=inScreenName )
		
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "CheckList is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wTwitterRes['Responce']==None :
			wRes['Reason'] = "List is not found: list=" + inListName + " owner=" + str(inScreenName)
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# ユーザ一覧を取得する
		wARR_ListUser = {}
		
		wTwitterRes = self.OBJ_Twitter.GetListSubscribers(
		   inListName=inListName,
		   inScreenName=inScreenName )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetListSubscribers): " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		for wLine in wTwitterRes['Responce'] :
			wID = str( wLine['id'] )
			wCell = {
				"id"          : wID,
				"screen_name" : wLine['screen_name'],
				"description" : wLine['description']
			}
			wARR_ListUser.update({ wID : wCell })
		
		wRes['Responce'] = wARR_ListUser
		wRes['Result'] = True
		return wRes



#####################################################
# リスト通知
#####################################################

#####################################################
# リスト通知 ユーザ取得
#####################################################
	def ListInd_GetUser(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "ListInd_GetUser"
		
		wRes['Responce'] = {}
		#############################
		# リスト通知が有効か
		if gVal.STR_UserInfo['ListName']=="" :
			###リスト通知 =無効
			wRes['Result'] = True
			return wRes
		
		#############################
		# リストがTwitterにあるか確認
		wTwitterRes = self.GetListID( inListName=gVal.STR_UserInfo['ListName'] )
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "CheckList is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wTwitterRes['Responce']==None :
			wRes['Reason'] = "Twitter List not found: " + gVal.STR_UserInfo['ListName']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# リスト通知のユーザ一覧を取得する
		wARR_ListIndUser = {}
		
		wTwitterRes = self.OBJ_Twitter.GetListMember( inListName=gVal.STR_UserInfo['ListName'] )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter error(GetListMember)"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		for wLine in wTwitterRes['Responce'] :
			wID = str( wLine['id'] )
			wCell = {
				"id"          : wID,
				"screen_name" : wLine['screen_name'],
				"description" : wLine['description']
			}
			wARR_ListIndUser.update({ wID : wCell })
		
		wRes['Responce'] = wARR_ListIndUser
		wRes['Result'] = True
		return wRes



#####################################################
# リスト通知 ユーザチェック
#####################################################
	def ListInd_CheckUser( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "ListInd_CheckUser"
		
		wRes['Responce'] = False
		#############################
		# リスト通知が有効か
		if gVal.STR_UserInfo['ListName']=="" :
			###リスト通知 =無効
			wRes['Result'] = True
			return wRes
		
		#############################
		# リスト通知のユーザ取得
		wTwitterRes = self.ListInd_GetUser()
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "ListInd_GetUser is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		wARR_ListUser = wTwitterRes['Responce']
		
		#############################
		# リスト通知ユーザに ID が登録されているか
		if inID in wARR_ListUser :
			wRes['Responce'] = True		#登録あり
		
		wRes['Result'] = True
		return wRes



#####################################################
# リスト通知 追加
#####################################################
	def ListInd_AddUser( self, inUser ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "ListInd_AddUser"
		
		wID = str( inUser['id'] )
		
		wRes['Responce'] = False	#実行
		#############################
		# リスト通知が有効か
		if gVal.STR_UserInfo['ListName']=="" :
			###リスト通知 =無効
			wRes['Result'] = True
			return wRes
		
		#############################
		# リスト通知にユーザが存在するか
		wTwitterRes = self.ListInd_CheckUser( inID=wID )
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "ListInd_CheckUser is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wTwitterRes['Responce']==True :
			### リスト通知済み
			wRes['Result'] = True
			return wRes
		
		#############################
		# リスト通知にID追加
		wTwitterRes = self.OBJ_Twitter.AddUserList( gVal.STR_UserInfo['ListName'], wID )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(AddUserList): " + wTwitterRes['Reason'] + " : list=" + gVal.STR_UserInfo['ListName'] + " user=" + inUser['screen_name']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wRes['Responce'] = True		#新規通知
		wRes['Result'] = True
		return wRes



#####################################################
# リスト通知 クリア
#####################################################
	def ListInd_Clear(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "ListInd_Clear"
		
		wRes['Responce'] = False
		#############################
		# リスト通知が有効か
		if gVal.STR_UserInfo['ListName']=="" :
			###リスト通知 =無効
			wRes['Result'] = True
			return wRes
		
		#############################
		# リスト通知のユーザ取得
		wTwitterRes = self.ListInd_GetUser()
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "ListInd_GetUser is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		wARR_ListUser = wTwitterRes['Responce']
		
		#############################
		# 全クリア
		wKeylist = list( wARR_ListUser.keys() )
		for wID in wKeylist :
			wTwitterRes = self.OBJ_Twitter.RemoveUserList( gVal.STR_UserInfo['ListName'], wID )
			CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
			if wTwitterRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(RemoveUserList): " + wTwitterRes['Reason'] + " : list=" + gVal.STR_UserInfo['ListName'] + " user=" + wARR_ListUser[wID]['screen_name']
				gVal.OBJ_L.Log( "B", wRes )
				continue
		
		wRes['Responce'] = True
		wRes['Result'] = True
		return wRes



#####################################################
# リスト取得
#####################################################
	def GetLists( self, inScreenName=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetLists"
		
		#############################
		# リスト取得
		wTwitterRes = self.OBJ_Twitter.GetLists( inScreenName=inScreenName )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetLists): " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wRes['Responce'] = wTwitterRes['Responce']
		wRes['Result'] = True
		return wRes



#####################################################
# リスト表示
#####################################################
	def ViewList_User( self, inScreenName=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "ViewList_User"
		
		#############################
		# リスト取得
		wTwitterRes = self.OBJ_Twitter.GetLists( inScreenName=inScreenName )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetLists): " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		wARR_List = wTwitterRes['Responce']
		
		wTwitterRes = self.OBJ_Twitter.GetSubsLists( inScreenName=inScreenName )
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetSubsLists): " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		wARR_SubsList = wTwitterRes['Responce']
		
		#############################
		# リスト一覧
		wStr = '\n' + "--------------------" + '\n' ;
		wStr = wStr + "Twitterリスト一覧" + '\n' + '\n' ;
		CLS_OSIF.sPrn( wStr )
		
		wKeylist = list( wARR_List.keys() )
		wStr = ""
		for wIndex in wKeylist :
			wStr = wStr + str(wARR_List[wIndex]['id']) + " : "
			wStr = wStr + str(wARR_List[wIndex]['me']) + " : " 
			wStr = wStr + str(wARR_List[wIndex]['name']) + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# リスト一覧(被登録)
		wStr = '\n' + "--------------------" + '\n' ;
		wStr = wStr + "Twitterリスト一覧(被登録)" + '\n' + '\n' ;
		CLS_OSIF.sPrn( wStr )
		
		wKeylist = list( wARR_SubsList.keys() )
		wStr = ""
		for wIndex in wKeylist :
			wStr = wStr + str(wARR_SubsList[wIndex]['id']) + " : "
			wStr = wStr + str(wARR_SubsList[wIndex]['me']) + " : " 
			wStr = wStr + str(wARR_SubsList[wIndex]['name']) + '\n'
		CLS_OSIF.sPrn( wStr )
		
		wRes['Result'] = True
		return wRes



#####################################################
# 自動フォローリスト 追加
#####################################################
	def MutualList_AddUser( self, inUser ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "MutualList_AddUser"
		
		wID = str( inUser['id'] )
		
		wRes['Responce'] = False	#実行
		#############################
		# 自動リムーブが有効か
		if gVal.STR_UserInfo['AutoRemove']==False :
			###リスト通知 =無効
			wRes['Result'] = True
			return wRes
		
		#############################
		# 相互フォローリストに追加済みか
		if self.CheckMutualListUser( wID )==True :
			### 追加済なので終わり
			wRes['Result'] = True
			return wRes
		
		#############################
		# 相互フォローリストに追加
		wTwitterRes = self.OBJ_Twitter.AddUserList( gVal.STR_UserInfo['mListName'], wID )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(AddUserList): " + wTwitterRes['Reason'] + " : list=" + gVal.STR_UserInfo['mListName'] + " user=" + inUser['screen_name']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
###		gVal.OBJ_L.Log( "RC", wRes, "〇リスト追加: list=" + gVal.STR_UserInfo['mListName'] + " user=" + inUser['screen_name'] )
		gVal.OBJ_L.Log( "RC", wRes, "〇リスト追加: list=" + gVal.STR_UserInfo['mListName'] + " user=" + inUser['screen_name'], inID=wID )
		wRes['Responce'] = True		#追加
		
		self.ARR_MutualListUserID.append( wID )
		
		#############################
		# 片フォロワーリストに追加されていたら
		#   リストから削除する
		if self.CheckFollowListUser( wID )==True :
			wTwitterRes = self.OBJ_Twitter.RemoveUserList( gVal.STR_UserInfo['fListName'], wID )
			CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
			if wTwitterRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(RemoveUserList): " + wTwitterRes['Reason'] + " : list=" + gVal.STR_UserInfo['fListName'] + " user=" + inUser['screen_name']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
###			gVal.OBJ_L.Log( "RC", wRes, "●リスト解除: list=" + gVal.STR_UserInfo['fListName'] + " user=" + inUser['screen_name'] )
			gVal.OBJ_L.Log( "RC", wRes, "●リスト解除: list=" + gVal.STR_UserInfo['fListName'] + " user=" + inUser['screen_name'], inID=wID )
			
			self.ARR_FollowerListUserID.remove( wID )
		
		wRes['Result'] = True
		return wRes

	#####################################################
	def FollowerList_AddUser( self, inUser ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "FollowerList_AddUser"
		
		wID = str( inUser['id'] )
		
		wRes['Responce'] = False	#実行
		#############################
		# 自動リムーブが有効か
		if gVal.STR_UserInfo['AutoRemove']==False :
			###リスト通知 =無効
			wRes['Result'] = True
			return wRes
		
		#############################
		# 片フォロワーリストに追加済みか
		if self.CheckFollowListUser( wID )==True :
			### 追加済なので終わり
			wRes['Result'] = True
			return wRes
		
		#############################
		# 片フォロワーリストに追加
		wTwitterRes = self.OBJ_Twitter.AddUserList( gVal.STR_UserInfo['fListName'], wID )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(AddUserList): " + wTwitterRes['Reason'] + " : list=" + gVal.STR_UserInfo['fListName'] + " user=" + inUser['screen_name']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
###		gVal.OBJ_L.Log( "RC", wRes, "〇リスト追加: list=" + gVal.STR_UserInfo['fListName'] + " user=" + inUser['screen_name'] )
		gVal.OBJ_L.Log( "RC", wRes, "〇リスト追加: list=" + gVal.STR_UserInfo['fListName'] + " user=" + inUser['screen_name'], inID=wID )
		wRes['Responce'] = True		#追加
		
		self.ARR_FollowerListUserID.append( wID )
		
		#############################
		# 相互フォローリストに追加されていたら
		#   リストから削除する
		if self.CheckMutualListUser( wID )==True :
			wTwitterRes = self.OBJ_Twitter.RemoveUserList( gVal.STR_UserInfo['mListName'], wID )
			CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
			if wTwitterRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(RemoveUserList): " + wTwitterRes['Reason'] + " : list=" + gVal.STR_UserInfo['mListName'] + " user=" + inUser['screen_name']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
###			gVal.OBJ_L.Log( "RC", wRes, "●リスト解除: list=" + gVal.STR_UserInfo['mListName'] + " user=" + inUser['screen_name'] )
			gVal.OBJ_L.Log( "RC", wRes, "●リスト解除: list=" + gVal.STR_UserInfo['mListName'] + " user=" + inUser['screen_name'], inID=wID )
			
			self.ARR_MutualListUserID.remove( wID )
		
		wRes['Result'] = True
		return wRes

	#####################################################
	def FollowerList_Remove( self, inUser ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "FollowerList_Remove"
		
		wID = str( inUser['id'] )
		
		wRes['Responce'] = False	#実行
		#############################
		# 自動リムーブが有効か
		if gVal.STR_UserInfo['AutoRemove']==False :
			###リスト通知 =無効
			wRes['Result'] = True
			return wRes
		
		#############################
		# 片フォロワーリストに追加されていたら
		#   リストから削除する
###		if self.CheckMutualListUser( wID )==True :
		if self.CheckFollowListUser( wID )==True :
			wTwitterRes = self.OBJ_Twitter.RemoveUserList( gVal.STR_UserInfo['fListName'], wID )
			CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
			if wTwitterRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(RemoveUserList): " + wTwitterRes['Reason'] + " : list=" + gVal.STR_UserInfo['fListName'] + " user=" + inUser['screen_name']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
###			gVal.OBJ_L.Log( "RC", wRes, "●リスト解除: list=" + gVal.STR_UserInfo['fListName'] + " user=" + inUser['screen_name'] )
			gVal.OBJ_L.Log( "RC", wRes, "●リスト解除: list=" + gVal.STR_UserInfo['fListName'] + " user=" + inUser['screen_name'], inID=wID )
			
###			self.ARR_MutualListUserID.remove( wID )
			self.ARR_FollowerListUserID.remove( wID )
		
		#############################
		# 相互フォローリストに追加されていたら
		#   リストから削除する
		if self.CheckMutualListUser( wID )==True :
			wTwitterRes = self.OBJ_Twitter.RemoveUserList( gVal.STR_UserInfo['mListName'], wID )
			CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
			if wTwitterRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(RemoveUserList): " + wTwitterRes['Reason'] + " : list=" + gVal.STR_UserInfo['mListName'] + " user=" + inUser['screen_name']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
###			gVal.OBJ_L.Log( "RC", wRes, "●リスト解除: list=" + gVal.STR_UserInfo['mListName'] + " user=" + inUser['screen_name'] )
			gVal.OBJ_L.Log( "RC", wRes, "●リスト解除: list=" + gVal.STR_UserInfo['mListName'] + " user=" + inUser['screen_name'], inID=wID )
			
			self.ARR_MutualListUserID.remove( wID )
		
		#############################
		# その他リスト登録をしてたら
		#   リストから削除する
		
		#############################
		# 相手のリストを取得する
		wTwitterRes = self.OBJ_Twitter.GetSubsLists( inScreenName=inUser['screen_name'] )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetSubsLists): " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		wARR_SubsList = wTwitterRes['Responce']
		
		wListFavo_Keylist = list( gVal.ARR_ListFavo.keys() )
		#############################
		# 相手のリストのうち
		# 通知リスト、相互フォロー、片フォロワー以外のリストを削除する
		for wKey in wARR_SubsList :
			if wARR_SubsList[wKey]['me']==False :
				###自分じゃなければスキップ
				continue
			
			### リスト通知、相互フォロー、片フォロワーはスキップ
			if wARR_SubsList[wKey]['name']==gVal.STR_UserInfo['ListName'] or \
			   wARR_SubsList[wKey]['name']==gVal.STR_UserInfo['mListName'] or \
			   wARR_SubsList[wKey]['name']==gVal.STR_UserInfo['fListName'] :
				continue
			
			### リスト解除する
			wTwitterRes = self.OBJ_Twitter.RemoveUserList( wARR_SubsList[wKey]['name'], wID )
			CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
			if wTwitterRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(RemoveUserList): " + wTwitterRes['Reason'] + " : list=" + wARR_SubsList[wKey]['name'] + " user=" + inUser['screen_name']
				gVal.OBJ_L.Log( "B", wRes )
				continue
			
###			gVal.OBJ_L.Log( "U", wRes, "●リスト解除: list=" + wARR_SubsList[wKey]['name'] + " user=" + inUser['screen_name'] )
			gVal.OBJ_L.Log( "RC", wRes, "●リスト解除: list=" + wARR_SubsList[wKey]['name'] + " user=" + inUser['screen_name'], inID=wID )
		
		wRes['Result'] = True
		return wRes



#####################################################
# リスト登録ユーザ取得
#####################################################
	def GetFollowListUser( self, inScreenName=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetLists"
		
###		wRes['Responce'] = {}
		wRes['Responce'] = {
			"FollowList"	: {},
			"SubsList"		: {}
		}
		#############################
		# リスト登録ユーザ取得
		CLS_MyDisp.sViewHeaderDisp( "リスト登録ユーザ取得" )
		
		#############################
		# リスト取得
		wTwitterRes = self.OBJ_Twitter.GetLists( inScreenName=inScreenName )
		CLS_Traffic.sP( "run_api", wTwitterRes['RunAPI'] )
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetLists): " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 初期化
		self.ARR_SubscribeListUserID = []
		wARR_FollowList = {}
		
		#############################
		# リスト登録のIDを抽出
		# ・自分のリスト
		# ・リスト通知は除外
		# ・相互フォローリストは除外
		# ・片フォロワーリストは除外
		wKeylist = list( wTwitterRes['Responce'].keys() )
		for wKey in wKeylist :
			if wTwitterRes['Responce'][wKey]['me']==False :
				### 自分以外は除外
				continue
			
			wListID = str(wTwitterRes['Responce'][wKey]['id'])
			if gVal.STR_UserInfo['ListID']!=gVal.DEF_NOTEXT :
				if gVal.STR_UserInfo['ListID']==wListID :
					### リスト通知リストは除外
					continue
			
			if gVal.STR_UserInfo['mListID']!=gVal.DEF_NOTEXT :
				if gVal.STR_UserInfo['mListID']==wListID :
					### 相互フォローリストは除外
					continue
			
			if gVal.STR_UserInfo['fListID']!=gVal.DEF_NOTEXT :
				if gVal.STR_UserInfo['fListID']==wListID :
					### 片フォロワーリストは除外
					continue
			
			wListName = str(wTwitterRes['Responce'][wKey]['name'])
			wCell = {
				"id"		: wListID,
				"name"		: wListName,
				"user_ids"	: []
			}
			wARR_FollowList.update({ wListID : wCell })
			
			wStr = "リスト登録ユーザ取得中：list=" + wListName
			CLS_OSIF.sPrn( wStr )
			#############################
			# リスト通知のユーザ一覧を取得する
			wTwitterListRes = self.OBJ_Twitter.GetListMember( inListName=wListName )
			CLS_Traffic.sP( "run_api", wTwitterListRes['RunAPI'] )
			if wTwitterListRes['Result']!=True :
				wRes['Reason'] = "Twitter error(GetListMember)"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			for wLine in wTwitterListRes['Responce'] :
				wUserID = str( wLine['id'] )
				wARR_FollowList[wListID]['user_ids'].append( wUserID )
				
				if wUserID not in self.ARR_SubscribeListUserID :
					self.ARR_SubscribeListUserID.append( wUserID )
			
			wStr = "  ユーザ数=" + str(len( wARR_FollowList[wListID]['user_ids'] ))
			CLS_OSIF.sPrn( wStr )
		
		#############################
		# リスト登録のIDを抽出
		# ・自分のリスト
		wTwitterRes = self.OBJ_Twitter.GetSubsLists( inScreenName=inScreenName )
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetSubsLists): " + wTwitterRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		wARR_SubsList = wTwitterRes['Responce']
		
		wARR_SubsList = {}
		wKeylist = list( wTwitterRes['Responce'].keys() )
		for wKey in wKeylist :
			if wTwitterRes['Responce'][wKey]['me']==True :
				### 自分のリストは除外
				continue
			
			wListID = str(wTwitterRes['Responce'][wKey]['id'])
			wListName = str(wTwitterRes['Responce'][wKey]['name'])
			wCell = {
				"id"		: wListID,
				"name"		: wListName,
				"user"		: wTwitterRes['Responce'][wKey]['user']
			}
			wARR_SubsList.update({ wListID : wCell })
			
			wStr = "被登録リスト：list=" + wListName
			CLS_OSIF.sPrn( wStr )
		
		wRes['Responce']['FollowList'] = wARR_FollowList
		wRes['Responce']['SubsList']   = wARR_SubsList
		self.ARR_SubsList              = wARR_SubsList
		#############################
		# 総計表示
		wStr = '\n' + "リスト登録一覧数    =" + str(len( wARR_FollowList ))
		CLS_OSIF.sPrn( wStr )
		
		wStr = "リスト登録ユーザID数=" + str(len( self.ARR_SubscribeListUserID ))
		CLS_OSIF.sPrn( wStr )
		
###		wRes['Responce'] = wARR_FollowList
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def CheckSubscribeListUser( self, inID ):
		if inID not in self.ARR_SubscribeListUserID :
			return False
		return True

	#####################################################
	def GetSubsList(self):
		return self.ARR_SubsList



#####################################################
# 自動リスト登録ユーザ取得
#####################################################
	def GetAutoListUser( self ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Twitter_IF"
		wRes['Func']  = "GetAutoListUser"
		
		#############################
		# 自動リムーブが有効か
		if gVal.STR_UserInfo['AutoRemove']==False :
			### 有効でなければ終わる
			wRes['Result'] = True
			return wRes
		
		#############################
		# リスト登録ユーザ取得
		CLS_MyDisp.sViewHeaderDisp( "自動リスト登録ユーザ取得" )
		
		#############################
		# 初期化
		self.ARR_MutualListUserID = []
		self.ARR_FollowerListUserID = []
		wARR_FollowList = {}
		
		#############################
		# 相互フォローリストユーザIDを取得する
		wStr = "相互フォローリスト登録ユーザ取得中..."
		CLS_OSIF.sPrn( wStr )
		
		wTwitterListRes = self.OBJ_Twitter.GetListMember( inListName=gVal.STR_UserInfo['mListName'] )
		CLS_Traffic.sP( "run_api", wTwitterListRes['RunAPI'] )
		if wTwitterListRes['Result']!=True :
			wRes['Reason'] = "Twitter error(GetListMember)"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		for wLine in wTwitterListRes['Responce'] :
			wUserID = str( wLine['id'] )
			
			if wUserID not in self.ARR_MutualListUserID :
				self.ARR_MutualListUserID.append( wUserID )
		
		#############################
		# 片フォロワーリストユーザIDを取得する
		wStr = "片フォロワーリスト登録ユーザ取得中..."
		CLS_OSIF.sPrn( wStr )
		
		wTwitterListRes = self.OBJ_Twitter.GetListMember( inListName=gVal.STR_UserInfo['fListName'] )
		CLS_Traffic.sP( "run_api", wTwitterListRes['RunAPI'] )
		if wTwitterListRes['Result']!=True :
			wRes['Reason'] = "Twitter error(GetListMember)"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		for wLine in wTwitterListRes['Responce'] :
			wUserID = str( wLine['id'] )
			
			if wUserID not in self.ARR_FollowerListUserID :
				self.ARR_FollowerListUserID.append( wUserID )
		
		#############################
		# 総計表示
		wStr = '\n' + "相互フォローリストID一覧数=" + str(len( self.ARR_MutualListUserID ))
		CLS_OSIF.sPrn( wStr )
		
		wStr = "片フォロワーリストID一覧数=" + str(len( self.ARR_FollowerListUserID ))
		CLS_OSIF.sPrn( wStr )
		
		wRes['Responce'] = wARR_FollowList
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def CheckMutualListUser( self, inID ):
		if inID not in self.ARR_MutualListUserID :
			return False
		return True

	#####################################################
	def CheckFollowListUser( self, inID ):
		if inID not in self.ARR_FollowerListUserID :
			return False
		return True

	#####################################################
	def GetMutualListUser(self):
		return self.ARR_MutualListUserID



