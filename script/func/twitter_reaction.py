#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : リアクション処理
#####################################################

from ktime import CLS_TIME
from osif import CLS_OSIF
from traffic import CLS_Traffic
from mydisp import CLS_MyDisp
from gval import gVal
#####################################################
class CLS_TwitterReaction():
#####################################################
	OBJ_Parent = ""				#親クラス実体

	VAL_TweetCnt    = 0			# リアクションで処理したツイート数
	VAL_ReactionCnt = 0			# リアクション回数
	ARR_ReactionTweet = {}		# リアクションツイート情報
	ARR_ReactionUser  = {}		# リアクションユーザ情報

	ARR_RandUserID = []

	DEF_REACTION_ACTION_TYPE = {# アクションタイプ
		"favo"		: "いいね",				# いいね	
		"retweet"	: "リツイート",			# リツイート
		"quoted"	: "引用リツイート",		# 引用リツイート
		"mention"	: "リプライ"			# メンション（リプライ）
	}

	DEF_REACTION_TEST = False
###	DEF_REACTION_TEST = True

	DEF_REACTION_SCORE_LEN = 3



#####################################################
# Init
#####################################################
	def __init__( self, parentObj=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterReaction"
		wRes['Func']  = "__init__"
		
		if parentObj==None :
			###親クラス実体の未設定
			wRes['Reason'] = "You have not set the parent class entity for parentObj"
			gVal.OBJ_L.Log( "A", wRes )
			return
		
		self.OBJ_Parent = parentObj
		return



#####################################################
# リアクション設定
#####################################################
	def __setReactionTweet( self, inUser, inTweet, inActionType=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterReaction"
		wRes['Func']  = "ReactionCheck"
		
		if inActionType==None :
			wRes['Result'] = True
			return wRes
		
		#############################
		# アクションタイプのチェック(念のため)
		if inActionType not in self.DEF_REACTION_ACTION_TYPE :
			wRes['Reason'] = "Action Type is not found: " + str(inActionType)
			gVal.OBJ_L.Log( "A", wRes )
			return wRes
		
		wID      = str(inUser['id'])
		wTweetID = str(inTweet['id'])
		wText    = str(inTweet['text']).replace( "'", "''" )
		
		#############################
		# リアクション情報の枠がなければ
		# 枠を作成する
		if wTweetID not in self.ARR_ReactionTweet :
			
			wType = "normal"			# 通常ツイート
			#############################
			# ツイートタイプの検出
			if "retweeted_status" in inTweet :
###				wType = "retweet"		# リツイート
				if inTweet['text'].find("@")>=0 or inTweet['in_reply_to_status_id']!=None :
					wType = "reply_retweet"	# リプライのリツイート
				else:
					wType = "retweet"		# リツイート
			
			elif "quoted_status" in inTweet :
###				wType = "quoted"		# 引用リツイート
				if inTweet['text'].find("@")>=0 or inTweet['in_reply_to_status_id']!=None :
					wType = "reply_quoted"	# リプライの引用リツイート
				else:
					wType = "quoted"		# 引用リツイート
			
###			elif inTweet['text'].find("@")>=0 :
			elif inTweet['text'].find("@")>=0 or inTweet['in_reply_to_status_id']!=None :
				wType = "other_reply"	# リプライ(他ユーザ)
				wIndex = inTweet['text'].find(" ")
				if wIndex>=0 :
					wReply_screen_name = inTweet['text'][1:wIndex]
					if inUser['screen_name']==wReply_screen_name :
						wType = "my_reply"	# リプライ(自分)
			
			#############################
			# 質問ツイートか
			elif gVal.STR_UserInfo['QuestionTag']!=gVal.DEF_NOTEXT :
				if inTweet['text'].find( gVal.STR_UserInfo['QuestionTag'] )>=0 :
					wType = "question"
			
			wCell = {
				"type"		: wType,			# ツイートタイプ
				"id"		: wID,				# ツイートID
				"text"		: wText,			# ツイートテキスト
				"users"		: []				# アクションしたユーザID
			}
			self.ARR_ReactionTweet.update({ wTweetID : wCell })
		
		#############################
		# リアクションユーザ情報の枠がなければ
		# 枠を作成する
		if wID not in self.ARR_ReactionUser :
			wCell = {
				"id"			: wID,
				"screen_name"	: inUser['screen_name'],
###				"score"			: 0
				"flg_some"		: False,		# 同一リアクション検出
				"hit_total"		: 0,			# 1タイムライン中のリアクション数
				"hit_new"		: 0				# 1タイムライン中の新しいリアクション数
			}
			self.ARR_ReactionUser.update({ wID : wCell })
		
		#############################
		# リアクション数の加算
		self.ARR_ReactionUser[wID]['hit_total'] += 1
		
###		#############################
###		# スコアの加算
###		
###		wFLG_Del = False
###		### 削除 ←いいね　+1
###		if gVal.STR_UserInfo['DelTag']!=gVal.DEF_NOTEXT :
###			if self.ARR_ReactionTweet[wTweetID]['text'].find( gVal.STR_UserInfo['DelTag'] )>=0 :
###				self.ARR_ReactionUser[wID]['score'] += gVal.DEF_STR_REN_SCORE['Score_Delete']
###				wFLG_Del = True
###		
###		if wFLG_Del==False :
####		### 通常ツイート ←いいね　+1
####		if self.ARR_ReactionTweet[wTweetID]['type']=="normal" and \
####		   inActionType=="favo" :
###			### 通常ツイート ←いいね　+1
###			if self.ARR_ReactionTweet[wTweetID]['type']=="normal" and \
###			   inActionType=="favo" :
###				self.ARR_ReactionUser[wID]['score'] += gVal.DEF_STR_REN_SCORE['Score_Normal']
###			
###			### リツイート　+5
###			elif self.ARR_ReactionTweet[wTweetID]['type']=="retweet" :
###				self.ARR_ReactionUser[wID]['score'] += gVal.DEF_STR_REN_SCORE['Score_Retweet']
###			
###			### 引用リツイート　+5
###			elif self.ARR_ReactionTweet[wTweetID]['type']=="quoted" :
###				self.ARR_ReactionUser[wID]['score'] += gVal.DEF_STR_REN_SCORE['Score_Quoted']
###			
###			### リプライ（他者）　+5
###			elif self.ARR_ReactionTweet[wTweetID]['type']=="other_reply" :
###				self.ARR_ReactionUser[wID]['score'] += gVal.DEF_STR_REN_SCORE['Score_Reply']
###			
###			### 質問 ←いいね　+5
###			elif self.ARR_ReactionTweet[wTweetID]['type']=="question" and \
###			   inActionType=="favo" :
###				self.ARR_ReactionUser[wID]['score'] += gVal.DEF_STR_REN_SCORE['Score_Question']
###		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

###	#####################################################
###	def __getReactionTweet( self, inTweetID ):
###		
###		wTweetID = str(inTweetID)
###		#############################
###		# リアクションツイート情報の枠
###		if wTweetID not in self.ARR_ReactionTweet :
###			return None
###		
###		return self.ARR_ReactionTweet[wTweetID]
###
###	#####################################################
###	def __getReactionUser( self, inUserID ):
###		
###		wUserID = str(inUserID)
###		#############################
###		# リアクションユーザ情報の枠
###		if wUserID not in self.ARR_ReactionUser :
###			return None
###		
###		return self.ARR_ReactionUser[wUserID]
###

	#####################################################
	# 同一リアクション検出設定
	def __setSomeReaction( self, inUserID ):
		
		wUserID  = str(inUserID)
		### リアクションユーザ情報の枠
		if wUserID not in self.ARR_ReactionUser :
			# ありえない
			return False
		
		self.ARR_ReactionUser[wUserID]['flg_some'] = True
		return True

	#####################################################
	# 受け入れリアクションの設定
	def __setReaction( self, inTweetID, inUserID,inActionType=None ):
		
		### アクションタイプのチェック
		if inActionType==None :
			# ありえない
			return True
		
		wTweetID = str(inTweetID)
		wUserID  = str(inUserID)
		### リアクションツイート情報の枠
		if wTweetID not in self.ARR_ReactionTweet :
			# ありえない
			return False
		
		### リアクションユーザ情報の枠
		if wUserID not in self.ARR_ReactionUser :
			# ありえない
			return False
		
		###同一リアクション検出
		if self.ARR_ReactionUser[wUserID]['flg_some']==True :
			return False
		
		#############################
		# 新リアクション数の加算
###		if self.ARR_ReactionTweet[wTweetID]['type']=="normal" :
###			self.ARR_ReactionUser[wUserID]['hit_new'] += 1
		if self.ARR_ReactionTweet[wTweetID]['text'].find( gVal.STR_UserInfo['DelTag'] )>=0 :
		     self.ARR_ReactionUser[wUserID]['hit_new'] += 0
		
		elif self.ARR_ReactionTweet[wTweetID]['text'].find( gVal.STR_UserInfo['QuestionTag'] )>=0 :
		     self.ARR_ReactionUser[wUserID]['hit_new'] += 8
		
		elif self.ARR_ReactionTweet[wTweetID]['type']=="normal" :
		     self.ARR_ReactionUser[wUserID]['hit_new'] += 1
		
###		elif self.ARR_ReactionTweet[wTweetID]['type']=="other_reply" or \
###		     self.ARR_ReactionTweet[wTweetID]['type']=="question" :
		elif self.ARR_ReactionTweet[wTweetID]['type']=="reply_retweet" or \
		     self.ARR_ReactionTweet[wTweetID]['type']=="reply_quoted" or \
		     self.ARR_ReactionTweet[wTweetID]['type']=="other_reply" or \
		     self.ARR_ReactionTweet[wTweetID]['type']=="question" :
			
			self.ARR_ReactionUser[wUserID]['hit_new'] += 5
		
		else:
			self.ARR_ReactionUser[wUserID]['hit_new'] += 2
		
		#############################
		# リアクションツイートへのユーザIDセット
		if wUserID in self.ARR_ReactionTweet[wTweetID]['users'] :
			# ユーザセット済み
			return False
		
		self.ARR_ReactionTweet[wTweetID]['users'].append( wUserID )
		return True

	#####################################################
	def __getReactionResult(self):
		wResult = {
			"Accept"		: False,	# 受け入れ           True=済み
			"reReaction"	: False,	# お返しリアクション True=済み
			"Reason"		: None		# 出力メッセージ
		}
		return wResult



#####################################################
# リアクションチェック
#####################################################
	def ReactionCheck( self, inFLG_Short=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterReaction"
		wRes['Func']  = "ReactionCheck"
		
		self.ARR_RandUserID = []
		#############################
		# 取得可能時間か？
		wGetLag = CLS_OSIF.sTimeLag( str( gVal.STR_Time['reaction'] ), inThreshold=gVal.DEF_STR_TLNUM['forReactionSec'] )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wGetLag['Beyond']==False and self.DEF_REACTION_TEST==False :

			### 規定以内は除外
			wStr = "●リアクション期間外 処理スキップ: 次回処理日時= " + str(wGetLag['RateTime']) + '\n'
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
		self.VAL_TweetCnt    = 0
		self.VAL_ReactionCnt = 0
		self.ARR_ReactionTweet = {}
		self.ARR_ReactionUser  = {}
		#############################
		# 取得開始の表示
		if inFLG_Short==False :
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "リアクションチェック中（通常）" )
			wCount = gVal.DEF_STR_TLNUM['reactionTweetLine']
		else :
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "リアクションチェック中（ショート）" )
			wCount = gVal.DEF_STR_TLNUM['reactionTweetLine_Short']
		
		#############################
		# 自分の直近のツイートを取得
		wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="user", inFLG_Rep=False, inFLG_Rts=False,
			 inID=gVal.STR_UserInfo['id'], inCount=wCount )
		if wTweetRes['Result']!=True :
			wRes['Reason'] = "Twitter Error: GetTL"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if len(wTweetRes['Responce'])==0 :
			wRes['Reason'] = "Tweet is not get: me"
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# チェック
		# いいね、リツイート、引用リツイートしたユーザ
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wTweetRes['Responce'] ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
		wFLG_ZanCountSkip = False
		for wTweet in wTweetRes['Responce'] :
			###ウェイトカウントダウン
			if self.OBJ_Parent.Wait_Next( inZanCountSkip=wFLG_ZanCountSkip )==False :
				break	###ウェイト中止
			wFLG_ZanCountSkip = False
			
			###日時の変換
			wTime = CLS_TIME.sTTchg( wRes, "(1)", wTweet['created_at'] )
			if wTime['Result']!=True :
				continue
			wTweet['created_at'] = wTime['TimeDate']
			
			#############################
			# 期間内のTweetか
			wGetLag = CLS_OSIF.sTimeLag( str( wTweet['created_at'] ), inThreshold=gVal.DEF_STR_TLNUM['forReactionTweetSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed(1)"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==True :
				###期間外= 古いツイートなので処理しない
				wFLG_ZanCountSkip = True
				continue
			
			#############################
			# ツイートチェック
			wSubRes = self.ReactionTweetCheck( str(gVal.STR_UserInfo['id']), wTweet )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "ReactionTweetCheck"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# チェック
		# メンションしたユーザ
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "リアクションチェック中：メンション" )
		
		wSubRes = gVal.OBJ_Tw_IF.GetMyMentionLookup()
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter Error(GetMyMentionLookup)"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		###ウェイト初期化
		self.OBJ_Parent.Wait_Init( inZanNum=len( wSubRes['Responce'] ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
		
		wFLG_ZanCountSkip = False
		wKeylist = list( wSubRes['Responce'].keys() )
		for wReplyID in wKeylist :
			###ウェイトカウントダウン
			if self.OBJ_Parent.Wait_Next( inZanCountSkip=wFLG_ZanCountSkip )==False :
				break	###ウェイト中止
			wFLG_ZanCountSkip = False
			
			#############################
			# 期間内のTweetか
			wGetLag = CLS_OSIF.sTimeLag( str( wSubRes['Responce'][wReplyID]['created_at'] ), inThreshold=gVal.DEF_STR_TLNUM['forReactionTweetSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed(2)"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==True :
				###期間外= 古いツイートなので処理しない
				wFLG_ZanCountSkip = True
				continue
			
			#############################
			# チェック対象のツイート表示
			wStr = '\n' + "--------------------" + '\n' ;
			wStr = wStr + "チェック中: " + '\n' ;
			wStr = wStr + wSubRes['Responce'][wReplyID]['text'] ;
			CLS_OSIF.sPrn( wStr )
			
			wID = str(wSubRes['Responce'][wReplyID]['user']['id'])
			###ユーザ単位のリアクションチェック
			wReactionRes = self.ReactionUserCheck( wSubRes['Responce'][wReplyID]['user'], wSubRes['Responce'][wReplyID], inAction="mention" )
			if wReactionRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(ReactionUserCheck 4): Tweet ID: " + wID
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# 現時間を設定
		if self.DEF_REACTION_TEST==False :
			wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "reaction", gVal.STR_Time['TimeDate'] )
			if wTimeRes['Result']!=True :
				wRes['Reason'] = "SetTimeInfo is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# リアクションツイートチェック
#####################################################
	def ReactionTweetCheck( self, inMyUserID, inTweet, inVIPuser=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterReaction"
		wRes['Func']  = "ReactionTweetCheck"
		
		wRes['Responce'] = False
		
		wTweet = inTweet
		
		wUserID      = str( wTweet['user']['id'] )
		wTweet['id'] = str(wTweet['id'])
		wTweetID     = wTweet['id']
		#############################
		# 警告ツイートは除外
		wSubRes = gVal.OBJ_DB_IF.CheckCautionTweet( wTweetID )
		if wSubRes==True :
			### 警告ツイートは除外＝正常終了
			wRes['Result'] = True
			return wRes
		
		#############################
		# チェック対象のツイート表示
		wStr = '\n' + "--------------------" + '\n' ;
		wStr = wStr + "チェック中: " + str(wTweet['created_at']) + '\n' ;
		wStr = wStr + wTweet['text'] + '\n' ;
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# いいねチェック
		wSubRes = gVal.OBJ_Tw_IF.GetLikesLookup( wTweetID )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter Error(GetLikesLookup): Tweet ID: " + wTweetID
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wKeylist = list( wSubRes['Responce'].keys() )
		for wID in wKeylist :
			wID = str(wID)
			###ユーザ単位のリアクションチェック
			wReactionRes = self.ReactionUserCheck( wSubRes['Responce'][wID], wTweet, inMyUserID=inMyUserID, inAction="favo", inVIPuser=inVIPuser )
			if wReactionRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(ReactionUserCheck): Tweet ID: " + wTweetID
				gVal.OBJ_L.Log( "B", wRes )
				continue
			if wReactionRes['Responce']['Accept']==True :
				wRes['Responce'] = True
		
		wFLG_VIPretweet = False
		#############################
		# VIP かつ VIPリツイートが有効で
		# VIPリツイートタグを含む場合
		#   VIPリツイート対象にする
		if inVIPuser!=None and \
		   gVal.STR_UserInfo['VipTag']!=gVal.DEF_NOTEXT :
			wTag = "#" + gVal.STR_UserInfo['VipTag']
			if wTweet['text'].find( wTag )>=0 :
				wFLG_VIPretweet = True
		
		#############################
		# リツイートチェック
		wSubRes = gVal.OBJ_Tw_IF.GetRetweetLookup( wTweetID )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter Error(GetRetweetLookup): Tweet ID: " + wTweetID
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wKeylist = list( wSubRes['Responce'].keys() )
		for wID in wKeylist :
			wID = str(wID)
			
			### VIPリツイート対象のツイートで
			### 既にリツイート済みなら フラグを落とす
			if wFLG_VIPretweet==True :
				if str(gVal.STR_UserInfo['id'])==wID :
					wFLG_VIPretweet = False	#フラグ落とす
			
			###ユーザ単位のリアクションチェック
			wReactionRes = self.ReactionUserCheck( wSubRes['Responce'][wID], wTweet, inMyUserID=inMyUserID, inAction="retweet", inVIPuser=inVIPuser )
			if wReactionRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(ReactionUserCheck 2): Tweet ID: " + wTweetID
				gVal.OBJ_L.Log( "B", wRes )
				continue
			if wReactionRes['Responce']['Accept']==True :
				wRes['Responce'] = True
		
		#############################
		# VIPリツイート対象なら
		# リツイートする
		if wFLG_VIPretweet==True :
			### リツイート実施
			wSubRes = gVal.OBJ_Tw_IF.Retweet( wTweetID )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(Retweet): Tweet ID: " + wTweetID
				gVal.OBJ_L.Log( "B", wRes )
			else:
				wStr = "〇VIPリツイート実行"
				CLS_OSIF.sPrn( wStr )
		
		#############################
		# 引用リツイートチェック
		wSubRes = gVal.OBJ_Tw_IF.GetRefRetweetLookup( wTweetID )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter Error(GetRefRetweetLookup): Tweet ID: " + wTweetID
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wKeylist = list( wSubRes['Responce'].keys() )
		for wID in wKeylist :
			wID = str(wID)
			###ユーザ単位のリアクションチェック
			wReactionRes = self.ReactionUserCheck( wSubRes['Responce'][wID], wTweet, inMyUserID=inMyUserID, inAction="quoted", inVIPuser=inVIPuser )
			if wReactionRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(ReactionUserCheck 3): Tweet ID: " + wTweetID
				gVal.OBJ_L.Log( "B", wRes )
				continue
			if wReactionRes['Responce']['Accept']==True :
				wRes['Responce'] = True
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# リアクションユーザチェック
#####################################################
	def ReactionUserCheck( self, inUser, inTweet, inMyUserID=None, inAction=None, inVIPuser=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterReaction"
		wRes['Func']  = "ReactionUserCheck"
		
		wRes['Responce'] = self.__getReactionResult()
		
		wUserID  = str(inUser['id'])
		wTweetID = str( inTweet['id'] )
		#############################
		# リアクション情報設定
		self.__setReactionTweet( inUser, inTweet, inActionType=inAction )
		
		wNewUser = False
		#############################
		# DBからいいね情報を取得する(1個)
		wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( inUser )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetFavoDataOne is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### DB未登録
		if wSubRes['Responce']['Data']==None :
			wRes['Reason'] = "GetFavoDataOne is no data"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wSubRes['Responce']['FLG_New']==True :
			wNewUser = True	#新規登録
			#############################
			# 新規情報の設定
			wSubRes = self.OBJ_Parent.SetNewFavoData( inUser, wSubRes['Responce']['Data'] )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "SetNewFavoData is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		wARR_DBData = wSubRes['Responce']['Data']
		
		#############################
		# 同じアクションはノーリアクション
		if wARR_DBData['rfavo_id']==wTweetID :
			### 除外
			wStr = "●同一アクションにより処理スキップ: tweet_id=" + str(wTweetID) + " user=" + str(wARR_DBData['screen_name'])
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
			#############################
			# 同一リアクション検出設定
			self.__setSomeReaction( inUserID=wUserID )
		
		else:
			#############################
			# リアクション情報設定
			self.__setReaction( inTweetID=wTweetID, inUserID=wUserID, inActionType=inAction )
		
		#############################
		# 前のリアクションより最新なら新アクション
		wSubRes = CLS_OSIF.sCmpTime( inTweet['created_at'], inDstTD=wARR_DBData['rfavo_date'] )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "sCmpTime is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wSubRes['Future']==False :
			### 古いアクションなので除外
			wStr = "●古いアクションにより処理スキップ: tweet_id=" + str(wTweetID) + " user=" + str(wARR_DBData['screen_name'])
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
		#############################
		# リアクション禁止ユーザか
		wUserRes = self.OBJ_Parent.CheckExtUser( wARR_DBData, "リアクション検出" )
		if wUserRes['Result']!=True :
			wRes['Reason'] = "CheckExtUser failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wUserRes['Responce']==False and \
		   self.DEF_REACTION_TEST==False :
			
			### 禁止あり=除外
			
			### いいね情報を更新する
			if self.DEF_REACTION_TEST==False :
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Recive( inUser, inTweet, wARR_DBData, True )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "UpdateFavoData is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			wRes['Result'] = True
			return wRes
		
		#############################
		# 無反応のレベルタグ
###		if wARR_DBData['level_tag']=="C-" or wARR_DBData['level_tag']=="D-" or wARR_DBData['level_tag']=="E+" or wARR_DBData['level_tag']=="E-" or \
###		   wARR_DBData['level_tag']=="G-" or wARR_DBData['level_tag']=="L"  or wARR_DBData['level_tag']=="Z" :
		if wARR_DBData['level_tag']=="C-" or wARR_DBData['level_tag']=="D-" or wARR_DBData['level_tag']=="E+" or wARR_DBData['level_tag']=="E-" or \
		   wARR_DBData['level_tag']=="L"  or wARR_DBData['level_tag']=="Z" :
			
			### 報告対象の表示と、ログに記録
			gVal.OBJ_L.Log( "T", wRes, "●リアクション拒否(レベルタグ) ユーザ: screen_name=" + inUser['screen_name'] + " level=" + wARR_DBData['level_tag'], inID=wUserID )
			
			### いいね情報を更新する
			if self.DEF_REACTION_TEST==False :
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Recive( inUser, inTweet, wARR_DBData, True )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "UpdateFavoData is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			wRes['Result'] = True
			return wRes
		
		#############################
		# Bot判定ユーザ除外
		if wARR_DBData['renfavo_cnt']>gVal.DEF_STR_TLNUM['renFavoBotNoactionCnt'] :
			### 報告対象の表示と、ログに記録
			gVal.OBJ_L.Log( "T", wRes, "●リアクション拒否(Bot判定ユーザ) ユーザ: screen_name=" + inUser['screen_name'] + " level=" + wARR_DBData['level_tag'], inID=wUserID )
			
			### いいね情報を更新する
			if self.DEF_REACTION_TEST==False :
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Recive( inUser, inTweet, wARR_DBData, True )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "UpdateFavoData is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			wRes['Result'] = True
			return wRes
		
		#############################
		# 既に除外済み
		elif wUserID in self.ARR_RandUserID :
			### 報告対象の表示と、ログに記録
			gVal.OBJ_L.Log( "T", wRes, "●リアクション拒否(ランダム選出済) ユーザ: screen_name=" + inUser['screen_name'] + " level=" + wARR_DBData['level_tag'], inID=wUserID )
			
			### いいね情報を更新する
			if self.DEF_REACTION_TEST==False :
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Recive( inUser, inTweet, wARR_DBData, True )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "UpdateFavoData is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			wRes['Result'] = True
			return wRes
		
		elif wARR_DBData['renfavo_cnt']>gVal.DEF_STR_TLNUM['renFavoBotCnt'] :
			#############################
			# ランダム除外
			wRand = CLS_OSIF.sGetRand(100)
			if wRand>=gVal.DEF_STR_TLNUM['forRenFavoReiineRand'] :
				### 乱数による拒否
				
				### 報告対象の表示と、ログに記録
				gVal.OBJ_L.Log( "T", wRes, "●リアクション拒否(ランダム) ユーザ: screen_name=" + inUser['screen_name'] + " level=" + wARR_DBData['level_tag'], inID=wUserID )
				
				### いいね情報を更新する
				if self.DEF_REACTION_TEST==False :
					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Recive( inUser, inTweet, wARR_DBData, True )
					if wSubRes['Result']!=True :
						###失敗
						wRes['Reason'] = "UpdateFavoData is failed"
						gVal.OBJ_L.Log( "B", wRes )
						return wRes
				
				self.ARR_RandUserID.append( wUserID )
				
				wRes['Result'] = True
				return wRes
		
###		### 追い出しユーザの受け入れ
###		elif wARR_DBData['level_tag']=="G-" :
###			#############################
###			# 最後のいいね受信から期間を過ぎた場合は除外
###			wGetLag = CLS_OSIF.sTimeLag( str( wARR_DBData['rfavo_date'] ), inThreshold=gVal.DEF_STR_TLNUM['forAutoRemoveReliefSec'] )
###			if wGetLag['Result']!=True :
###				wRes['Reason'] = "sTimeLag failed"
###				gVal.OBJ_L.Log( "B", wRes )
###				return wRes
###			if wGetLag['Beyond']==True :
###				### 規定外 =古いツイートなので除外
###				
###				### 報告対象の表示と、ログに記録
###				gVal.OBJ_L.Log( "T", wRes, "●リアクション拒否(レベルタグ) ユーザ: screen_name=" + inUser['screen_name'] + " level=" + wARR_DBData['level_tag'], inID=wUserID )
###				
###				### いいね情報を更新する
###				if self.DEF_REACTION_TEST==False :
###					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Recive( inUser, inTweet, wARR_DBData, True )
###					if wSubRes['Result']!=True :
###						###失敗
###						wRes['Reason'] = "UpdateFavoData is failed"
###						gVal.OBJ_L.Log( "B", wRes )
###						return wRes
###				
###				wRes['Result'] = True
###				return wRes
		
###		#############################
###		# リムーブしたけど、まだフォロワーでアクションが継続した場合
###		#   アクションは受け入れる
###		elif wARR_DBData['level_tag']=="D-" :
###			
###			wFLG_Denial = False
###			if wARR_DBData['myfollow']==True :
###				### フォロー中
###				wFLG_Denial = True
###			
###			if gVal.STR_UserInfo['AutoRemove']==False :
###				### 自動リムーブOFF
###				wFLG_Denial = True
###			
###			if wARR_DBData['rfavo_n_cnt']<gVal.DEF_STR_TLNUM['forAutoRemoveReliefCnt'] :
###				### いいね規定以内
###				wFLG_Denial = True
###			
###			if wFLG_Denial==False :
###				#############################
###				# ユーザ情報の取得
###				wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inID=wUserID )
###				if wUserInfoRes['Result']!=True :
###					wRes['Reason'] = "Twitter Error: @" + wARR_DBData['screen_name']
###					gVal.OBJ_L.Log( "B", wRes )
###					return wRes
###				
###				wUser = wUserInfoRes['Responce']
###				
###				#############################
###				# ユーザの状態チェック
###				# 以下は除外
###				# ・鍵垢
###				# ・公式垢
###				if wUser['protected']==True or \
###				   wUser['verified']==True :
###					wFLG_Denial = True
###			
###			# ※ここまでで拒否じゃなければ
###			#   救済確定
###			if wFLG_Denial==False :
###				#############################
###				# フォローする
###				wTweetRes = gVal.OBJ_Tw_IF.Follow( wUserID, inMute=True )
###				if wTweetRes['Result']!=True :
###					wRes['Reason'] = "Twitter API Error(Follow): " + wTweetRes['Reason'] + " screen_name=" + str(wARR_DBData['screen_name'])
###					gVal.OBJ_L.Log( "B", wRes )
###					return wRes
###				
###				### 相互フォローリストに追加
###				wTwitterRes = gVal.OBJ_Tw_IF.MutualList_AddUser( wARR_DBData )
###				
###				### ユーザレベル変更
###				wUserLevel = "C"
###				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wUserID, wUserLevel )
###				
###				### トラヒック記録（フォロー者増加）
###				CLS_Traffic.sP( "p_myfollow" )
###				
###				### ユーザ記録
###				wStr = "〇自動フォロー（救済）"
###				gVal.OBJ_L.Log( "R", wRes, wStr + ": " + str(wARR_DBData['screen_name']), inID=wUserID )
###				
###				#############################
###				# DBに反映
###				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Follower( wUserID, inFLG_MyFollow=True )
###				if wSubRes['Result']!=True :
###					###失敗
###					wRes['Reason'] = "UpdateFavoData_Follower is failed"
###					gVal.OBJ_L.Log( "B", wRes )
###					return wRes
###		
###		#############################
###		# レベルタグによるランダム実行
###		elif wARR_DBData['level_tag']=="G" or wARR_DBData['level_tag']=="G+" or wARR_DBData['level_tag']=="H" or wARR_DBData['level_tag']=="H+" :
###			wRand = CLS_OSIF.sGetRand(100)
###			if wRand>=gVal.DEF_STR_TLNUM['forAutoFavoLevelRunRand'] :
###				### 乱数による拒否
###				
###				### いいね情報を更新する
###				if self.DEF_REACTION_TEST==False :
###					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Recive( inUser, inTweet, wARR_DBData, True )
###					if wSubRes['Result']!=True :
###						###失敗
###						wRes['Reason'] = "UpdateFavoData is failed"
###						gVal.OBJ_L.Log( "B", wRes )
###						return wRes
###				
###				### 報告対象の表示と、ログに記録
###				gVal.OBJ_L.Log( "T", wRes, "●リアクション拒否(ランダム) ユーザ: screen_name=" + inUser['screen_name'] + " level=" + wARR_DBData['level_tag'], inID=wUserID )
###				
###				wRes['Result'] = True
###				return wRes
###			
###			#############################
###			# 期間を過ぎたツイートは除外
###			wGetLag = CLS_OSIF.sTimeLag( str( inTweet['created_at'] ), inThreshold=gVal.DEF_STR_TLNUM['forAutoFavoTweet_B_Sec'] )
###			if wGetLag['Result']!=True :
###				wRes['Reason'] = "sTimeLag failed"
###				gVal.OBJ_L.Log( "B", wRes )
###				return wRes
###			if wGetLag['Beyond']==True :
###				### 規定外 =古いツイートなので除外
###				
###				### いいね情報を更新する
###				if self.DEF_REACTION_TEST==False :
###					wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Recive( inUser, inTweet, wARR_DBData, True )
###					if wSubRes['Result']!=True :
###						###失敗
###						wRes['Reason'] = "UpdateFavoData is failed"
###						gVal.OBJ_L.Log( "B", wRes )
###						return wRes
###				
###				### 報告対象の表示と、ログに記録
###				gVal.OBJ_L.Log( "T", wRes, "●リアクション拒否(古いツイート) ユーザ: screen_name=" + inUser['screen_name'] + " level=" + wARR_DBData['level_tag'], inID=wUserID )
###				
###				wRes['Result'] = True
###				return wRes
		
		#############################
		# ※リアクション受け入れ※
		#############################
		
		#############################
		# アクション回数加算
		self.VAL_ReactionCnt += 1
		### テスト時表示
		if self.DEF_REACTION_TEST==True :
			wStr = "〇リアクション受信: " + str(wTweetID) + " user=" + str(wARR_DBData['screen_name'])
			CLS_OSIF.sPrn( wStr )
		
		#############################
		# いいね情報を更新する
		if self.DEF_REACTION_TEST==False :
			wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Recive( inUser, inTweet, wARR_DBData )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "UpdateFavoData is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
###		#############################
###		# リアクション情報設定
###		self.__setReaction( inTweetID=wTweetID, inUserID=wUserID, inActionType=inAction )
###		
		#############################
		# トラヒックの記録
		if self.DEF_REACTION_TEST==False :
			if str(gVal.STR_UserInfo['id'])==wUserID :
				CLS_Traffic.sP( "r_reaction" )
				if gVal.OBJ_Tw_IF.CheckFollower( wUserID )==True :
					CLS_Traffic.sP( "r_in" )
				else:
					CLS_Traffic.sP( "r_out" )
			else:
				CLS_Traffic.sP( "r_vip" )
			
			wStr = ""
			### アクション別処理
			if inAction=="favo" :
				### いいね受信
				wStr = "〇いいね検出"
				CLS_Traffic.sP( "r_favo" )
			
			elif inAction=="retweet" :
				### リツイート受信
				wStr = "〇リツイート検出"
				CLS_Traffic.sP( "r_retweet" )
			
			elif inAction=="quotted" :
				### 引用リツイート受信
				wStr = "〇引用リツイート検出"
				CLS_Traffic.sP( "r_iret" )
			
			else :
				### メンション受信
				wStr = "〇メンション検出"
				CLS_Traffic.sP( "r_rep" )
			
			wStr = wStr + ": " + wARR_DBData['screen_name']
			wRes['Responce']['Reason'] = wStr
			gVal.OBJ_L.Log( "T", wRes, wStr, inID=wUserID )
		
		#############################
		# リアクション済みID
		wRes['Responce']['Accept'] = True	#リアクション受け入れ
		
		#############################
		# レベル昇格
		# 前提: フォロワー
		wUserLevel = None
		wCnt = wARR_DBData['rfavo_n_cnt'] + 1
###		if wARR_DBData['level_tag']=="G" :
###		if wARR_DBData['level_tag']=="G" or wARR_DBData['level_tag']=="G-" :
		if wARR_DBData['level_tag']=="G" or self.ARR_ReactionTweet[wTweetID]['type']=='normal' :
			wUserLevel = "E"
			wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wUserID, wUserLevel )
			
			### 報告対象の表示と、ログに記録
			gVal.OBJ_L.Log( "RR", wRes, "〇リアクションにより昇格 ユーザ: screen_name=" + inUser['screen_name'] + " level=" + wUserLevel, inID=wUserID )
			
###			### 片フォロワーリストに追加
###			if gVal.OBJ_Tw_IF.CheckFollowListUser( wUserID )==False :
###				wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_AddUser( inUser )
###			
			### 監視ONの送信
			self.OBJ_Parent.SendUserOpeInd( inUser, inFLG_Ope=True )
		
		#############################
		# レベルG-
###		elif wARR_DBData['level_tag']=="G-" :
		elif wARR_DBData['level_tag']=="G-" or self.ARR_ReactionTweet[wTweetID]['type']=='normal' :
			
			### 既にリムーブされていたらスルー
			if wARR_DBData['follower']==False :
				wRes['Result'] = True
				return wRes
			
			wUserLevel = "E"
			wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wUserID, wUserLevel )
			
			### 片フォロワーリストに追加
			if gVal.OBJ_Tw_IF.CheckFollowListUser( wUserID )==False :
				wTwitterRes = gVal.OBJ_Tw_IF.FollowerList_AddUser( inUser )
			
			### 報告対象の表示と、ログに記録
			gVal.OBJ_L.Log( "RR", wRes, "〇リアクションにより昇格 ユーザ: screen_name=" + inUser['screen_name'] + " level=" + wUserLevel, inID=wUserID )
			
			### 監視ONの送信
			self.OBJ_Parent.SendUserOpeInd( inUser, inFLG_Ope=True )
		
		#############################
		# 相互レベルCへ昇格
		# ・トロフィー資格者
		# ・レベルE
		# ・フォロー者OFF
		# ・フォロワーON
		elif wCnt>=gVal.DEF_STR_TLNUM['favoSendsCnt'] and \
		     wARR_DBData['level_tag']=="E" and \
		     gVal.OBJ_Tw_IF.CheckMyFollow( wUserID )==False and \
		     gVal.OBJ_Tw_IF.CheckFollower( wUserID )==True :
			
			if self.DEF_REACTION_TEST==False :
				### フォロー＆ミュートする
				wTweetRes = gVal.OBJ_Tw_IF.Follow( wUserID, inMute=True )
				if wTweetRes['Result']!=True :
					wRes['Reason'] = "Twitter API Error: Follow" + wTweetRes['Reason']
					gVal.OBJ_L.Log( "B", wRes )
				
				### 相互フォローリストに追加
				wTwitterRes = gVal.OBJ_Tw_IF.MutualList_AddUser( wARR_DBData )
				
				### ユーザレベル変更
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wUserID, "C" )
				
				### トラヒック記録（フォロー者増加）
				CLS_Traffic.sP( "p_myfollow" )
			
			### ログに記録
			gVal.OBJ_L.Log( "R", wRes, "自動フォロー（昇格）: " + wARR_DBData['screen_name'], inID=wUserID )
			
			### DBに反映
			if self.DEF_REACTION_TEST==False :
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Follower( wUserID, inFLG_MyFollow=True )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "UpdateFavoData_Follower is failed"
					gVal.OBJ_L.Log( "B", wRes )
		
		#############################
		# リアクションへのリアクション
		wSubRes = self.__ReactionUserCheck_PutReaction( inUser, wARR_DBData, inTweet, wNewUser, inAction=inAction, inVIPuser=inVIPuser )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "__ReactionUserCheck_ListInd is failed"
			gVal.OBJ_L.Log( "B", wRes )
		
		#############################
		# リアクション済み
		wRes['Responce']['reReaction'] = True	#お返しリアクション済み
		
		wRes['Result'] = True
		return wRes



	#####################################################
	# リアクションユーザへのリアクション
	#####################################################
	def __ReactionUserCheck_PutReaction( self, inUser, inData, inTweet, inNewUser=False, inAction=None, inVIPuser=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterReaction"
		wRes['Func']  = "__ReactionUserCheck_PutReaction"
		
		wUserID = str(inUser['id'])
		#############################
		# 自分のツイートの場合
		# おかえしを返す
###		if str(gVal.STR_UserInfo['id'])==wUserID :
		if str(gVal.STR_UserInfo['id'])==wUserID and inData['level_tag']!="G-" :
			#############################
			# 期間外のTweetで 新規ユーザに対しては
			# リアクションを返さない(仕様)
			if inNewUser==True :
				wGetLag = CLS_OSIF.sTimeLag( str( inTweet['created_at'] ), inThreshold=gVal.DEF_STR_TLNUM['forReactionTweetSec'] )
				if wGetLag['Result']!=True :
					wRes['Reason'] = "sTimeLag failed(1)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				if wGetLag['Beyond']==True :
					###期間外= とりま通知しない
					wStr = "●新規ユーザのため非通知: " + inData['screen_name'] + '\n' ;
					CLS_OSIF.sPrn( wStr )
					
					wRes['Result'] = True
					return wRes
			
			#############################
			# 相互フォローリスト かつ 片フォローの場合
			# リムーブ処理する
			if gVal.OBJ_Tw_IF.CheckMutualListUser( inUser['id'] )==True and \
			   inData['myfollow']==True and inData['follower']==False :
				### 自動リムーブする
				if self.DEF_REACTION_TEST==False :
					wSubRes = self.OBJ_Parent.OBJ_TwitterFollower.AutoRemove( inUser=inUser, inFLG_Force=True )
					if wSubRes['Result']!=True :
						###失敗
						wRes['Reason'] = "AutoRemove is failed"
						gVal.OBJ_L.Log( "B", wRes )
						return wRes
					
					if wSubRes['Responce']==True :
						### 自動リムーブしたらここで終わる
						wRes['Result'] = True
						return wRes
				else:
					wStr = "〇自動リムーブ実行: " + inUser['screen_name']
					CLS_OSIF.sPrn( wStr )
			
			#############################
			# 自動おかえしいいねする
			if gVal.DEF_STR_TLNUM['autoRepFavo']==True and \
			   ( inAction=="favo" or inAction=="quotted" ) :
				
				if self.DEF_REACTION_TEST==False :
					wSubRes = self.OBJ_Parent.OBJ_TwitterFavo.AutoFavo( inUser, gVal.DEF_STR_TLNUM['forAutoFavoReturnFavoSec'] )
					if wSubRes['Result']!=True :
						###失敗
						wRes['Reason'] = "AutoFavo is failed"
						gVal.OBJ_L.Log( "B", wRes )
						return wRes
				else:
					wStr = "〇自動おかえし実行: " + inUser['screen_name']
					CLS_OSIF.sPrn( wStr )
		
		#############################
		# リスト通知をおこなう
		if gVal.STR_UserInfo['ListName']!=gVal.DEF_NOTEXT :
			if self.DEF_REACTION_TEST==False :
				wSubRes = self.__ReactionUserCheck_ListInd( inData )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "__ReactionUserCheck_ListInd is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			else:
				wStr = "〇リスト通知発行: " + inUser['screen_name']
				CLS_OSIF.sPrn( wStr )
		
		#############################
		# 自動フォローする
		if gVal.OBJ_Tw_IF.CheckMyFollow( wUserID )==False :
			if self.DEF_REACTION_TEST==False :
###				wSubRes = self.OBJ_Parent.OBJ_TwitterFollower.AutoFollow( inUser )
				wSubRes = self.OBJ_Parent.OBJ_TwitterFollower.AutoFollow( inUser['id'] )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "AutoFollow is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			else:
				wStr = "〇自動フォロー実行: " + inUser['screen_name']
				CLS_OSIF.sPrn( wStr )
		
		#############################
		# 引用リツイート
		if inVIPuser!=None and \
		   (inAction=="quoted" or inAction=="mention") :
			wSubRes = self.__send_VIP_ReactionTweet(
			   inVIPuser=inVIPuser,
			   inSrcUser=inUser['screen_name'],
			   inAction=inAction,
			   inTweet=inTweet
			   )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "__send_VIP_ReactionTweet is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		wRes['Result'] = True
		return wRes



	#####################################################
	# リスト通知をおこなう
	#####################################################
	def __ReactionUserCheck_ListInd( self, inData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterReaction"
		wRes['Func']  = "__ReactionUserCheck_ListInd"
		
		#############################
		# 前回が今日以外なら通知する
		wNowDate = str(gVal.STR_Time['TimeDate'])
		wNowDate = wNowDate.split(" ")
		wNowDate = wNowDate[0]
		wRateDate = str(inData['list_ind_date'])
		wRateDate = wRateDate.split(" ")
		wRateDate = wRateDate[0]
		if wNowDate==wRateDate :
			### 今日なので通知しない
			wStr = "●今日は通知済み: " + inData['screen_name'] + '\n' ;
			CLS_OSIF.sPrn( wStr )
			
			wRes['Result'] = True
			return wRes
		
		#############################
		# リストがTwitterにあるか確認
		wSubRes = gVal.OBJ_Tw_IF.ListInd_AddUser( inData )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(InserttListIndUser): " + wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wSubRes['Responce']==False :
			### 既に登録済み
			wStr = "●リスト通知済み: " + inData['screen_name'] + '\n' ;
			CLS_OSIF.sPrn( wStr )
			
			wRes['Result'] = True
			return wRes
		
		#############################
		# DBに登録する
		wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_ListIndData( inData )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "UpdateFavoData_ListIndData Error"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wTextReason = "リスト通知: " + inData['screen_name']
		gVal.OBJ_L.Log( "RR", wRes, wTextReason, inID=inData['id'] )
		
		wRes['Result'] = True
		return wRes



	#####################################################
	def __send_VIP_ReactionTweet( self, inVIPuser, inSrcUser, inAction, inTweet ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterReaction"
		wRes['Func']  = "__send_VIP_ReactionTweet"
		
		if self.DEF_REACTION_TEST==True :
			print(str(inTweet))
		
		#############################
		# メッセージの組み立て
		wStr = "@" + inVIPuser + " 次のユーザに" + self.DEF_REACTION_ACTION_TYPE[inAction] + "されました。" + '\n'
		wStr = wStr + "user=" + inSrcUser + '\n'
		wStr = wStr + "https://twitter.com/" + str(inSrcUser) + '\n'
		wStr = wStr + "https://twitter.com/" + str(inVIPuser) + "/status/" + str(inTweet['id']) + '\n'
		
		#############################
		# ツイート送信
		if self.DEF_REACTION_TEST==False :
			wSubRes = gVal.OBJ_Tw_IF.Tweet( wStr )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(Tweet): " + wSubRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		else:
			wStr = "Tweet送信: " + wStr
			CLS_OSIF.sPrn( wStr )
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes


		#		@vip_user 次のユーザに いいね されました。
		#		@ユーザ名
		#		ツイートURL
		# サンプル
		# https://twitter.com/korei_dev/status/1590166443290943488



#####################################################
# リアクション結果表示
#####################################################
###	def ReactionResult(self):
###		#############################
###		# 応答形式の取得
###		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
###		wRes = CLS_OSIF.sGet_Resp()
###		wRes['Class'] = "CLS_TwitterReaction"
###		wRes['Func']  = "ReactionResult"
###		
###		#############################
###		# メンション情報 表示
###		wStr = "------------------------------" + '\n'
###		wStr = wStr + "メンション結果" + '\n'
###		wStr = wStr + "------------------------------" + '\n'
###		CLS_OSIF.sPrn( wStr )
###		
###		wStr = ""
###		wKeylist = list( self.ARR_ReactionTweet.keys() )
###		wFLG_Mention = False
###		for wID in wKeylist :
###			if self.ARR_ReactionTweet[wID]['type']!="mention" :
###				continue
###			
###			### メンションユーザ名
###			wUserName = self.__getReactionUser( inUserID )
###			if wUserName==None :
###				### ありえない
###				wUserName = "(?none?)"
###			
###			wStr = wStr + self.ARR_Mentions[wID]['text'] + '\n'
###			wStr = wStr + "  user: " + wUserName['screen_name'] + '\n' + '\n'
###			wFLG_Mention = True
###		
###		if wFLG_Mention==False :
###			### 情報なしの場合
###			wStr = "(情報なし)" + '\n'
###		
###		CLS_OSIF.sPrn( wStr )
###		
###		#############################
######		# 非絡みユーザ一覧の取得（自動設定のみ）
######		wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserBList( inAutoOnly=True )
###		# 非絡みユーザ一覧の取得
###		wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserBList()
###		if wSubRes['Result']!=True :
###			###失敗
###			wRes['Reason'] = "UpdateFavoData_UserLevel is failed"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		wARR_RateUserB = wSubRes['Responce']
###		
###		#############################
###		# 自動非絡みでリアクションがなかったら、
###		#   解除する
###		wKeylist = list( wARR_RateUserB.keys() )
###		for wID in wKeylist :
###			wID = str(wID)
###			
###			### リアクションがなければ
###			###  0 を設定しておく
###			if wID not in self.ARR_ReactionUser :
###				wCell = {
###					"id"			: wID,
###					"screen_name"	: wARR_RateUserB[wID]['screen_name'],
###					"score"			: 0
###				}
###				self.ARR_ReactionUser.update({ wID : wCell })
###		
###		#############################
###		# 結果表示
###		wStr = "------------------------------" + '\n'
###		wStr = wStr + "リアクション結果" + '\n'
###		wStr = wStr + "------------------------------" + '\n'
###		wStr = wStr + "  新規受信数: " + str( self.VAL_ReactionCnt ) + " .件" + '\n'
###		CLS_OSIF.sPrn( wStr )
###		
###		if len(self.ARR_ReactionUser)==0 :
###			### リアクションがなければ、ここで終わり
###			wStr = "(情報なし)" + '\n'
###			CLS_OSIF.sPrn( wStr )
###			
###			wRes['Result'] = True
###			return wRes
###		
###		#############################
###		# ヘッダ
###		wStr =        "SCORE CNT   BOT   LV   USER" + '\n'
###		wStr = wStr + "-------------------------------" + '\n'
###		CLS_OSIF.sPrn( wStr )
###		
###		#############################
###		# 非絡みユーザのユーザレベル変更
###		wKeylist = list( self.ARR_ReactionUser.keys() )
###		for wID in wKeylist :
###			#############################
###			# DBからいいね情報を取得する(1個)
###			wDBRes = gVal.OBJ_DB_IF.GetFavoDataOne( self.ARR_ReactionUser[wID], inFLG_New=False )
###			if wDBRes['Result']!=True :
###				###失敗
###				wRes['Reason'] = "GetFavoDataOne is failed"
###				gVal.OBJ_L.Log( "B", wRes )
###				continue
###			### DB未登録ならスキップ
###			if wDBRes['Responce']['Data']==None :
###				continue
###			wARR_DBData = wDBRes['Responce']['Data']
###			
###			#############################
###			# 最後のいいねからの期間
###			wFLG_RateRec = False
###			wGetLag = CLS_OSIF.sTimeLag( str( wARR_DBData['rfavo_date'] ), inThreshold=gVal.DEF_STR_TLNUM['forRenFavoSec'] )
###			if wGetLag['Result']!=True :
###				wRes['Reason'] = "sTimeLag failed(1)"
###				gVal.OBJ_L.Log( "B", wRes )
###				return wRes
###			if wGetLag['Beyond']==True :
###				### 規定外 =古くなった
###				wFLG_RateRec = True
###			
######			#############################
######			# スコアを処理する
###			if self.ARR_ReactionUser[wID]['score']==0 :
###				###  0点
###				if wARR_DBData['renfavo_cnt']>=1 and \
###				   wFLG_RateRec==False :
###					### カウンタ減らす
###					if wARR_DBData['level_tag']=="G" or wARR_DBData['level_tag']=="G+" or \
###					   wARR_DBData['level_tag']=="H" or wARR_DBData['level_tag']=="H+" or wARR_DBData['level_tag']=="H-" :
###						wCnt = wARR_DBData['renfavo_cnt'] - 1
###					else:
###						wCnt = 0
###				else:
###					### 最後のいいねから古かったら解除
###					wCnt = 0
###			
###			elif self.ARR_ReactionUser[wID]['score']>=gVal.DEF_STR_REN_SCORE['NoFollowScore'] :
###				### 規定以上
###				if wFLG_RateRec==False :
###					if wARR_DBData['renfavo_cnt']==0 :
###						### 初回なら強制ON
###						wCnt = gVal.DEF_STR_TLNUM['renFavoForceCnt']
###					else:
###						### カウンタ増やす
###						wCnt = wARR_DBData['renfavo_cnt'] + 1
###				else:
###					### 最後のいいねから古かったら解除
###					wCnt = 0
###			
###			else:
###				### 1点以上、規定未満
###				if wFLG_RateRec==False :
###					### カウンタ増やす
###					wCnt = wARR_DBData['renfavo_cnt'] + 1
###				else:
###					### 最後のいいねから古かったら解除
###					wCnt = 0
###			
###			#############################
###			# 登録ユーザはスルー
###			if gVal.OBJ_Tw_IF.CheckSubscribeListUser( wID )!=False :
###				continue
###			
###			wUserLevel = None
###			wBotCnt = None
###			if wCnt>=gVal.DEF_STR_TLNUM['renFavoOnCnt'] :
###				#############################
###				# 相互フォロー中か
###				if wARR_DBData['level_tag']=="B" or wARR_DBData['level_tag']=="B+" or \
###				   wARR_DBData['level_tag']=="C" or wARR_DBData['level_tag']=="C+" :
###					
###					wBotCnt = wARR_DBData['renbot_cnt'] + 1
###					if wBotCnt<gVal.DEF_STR_TLNUM['renFavoBotCnt'] :
###						wUserLevel = "G"
###					else:
###						wUserLevel = "G+"
###						### 報告対象の表示と、ログに記録
###						gVal.OBJ_L.Log( "RR", wRes, "●bot判定固定 ユーザ: screen_name=" + wARR_DBData['screen_name'] + " level=" + wUserLevel, inID=wID )
###				
###				#############################
###				# 片フォロワーか
###				elif wARR_DBData['level_tag']=="E" :
###					
###					wBotCnt = wARR_DBData['renbot_cnt'] + 1
###					if wBotCnt<gVal.DEF_STR_TLNUM['renFavoBotCnt'] :
###						wUserLevel = "H"
###					else:
###						wUserLevel = "H+"
###						### 報告対象の表示と、ログに記録
###						gVal.OBJ_L.Log( "RR", wRes, "●bot判定固定 ユーザ: screen_name=" + wARR_DBData['screen_name'] + " level=" + wUserLevel, inID=wID )
###				
######				#############################
######				# 固定化
######				elif wARR_DBData['level_tag']=="G" or wARR_DBData['level_tag']=="H" :
###					if wCnt>=gVal.DEF_STR_TLNUM['renFavoForceBotCnt'] :
###						if wARR_DBData['level_tag']=="G" :
###							wUserLevel = "G+"
###						else:
###							wUserLevel = "H+"
###						
###						### 報告対象の表示と、ログに記録
###						gVal.OBJ_L.Log( "RR", wRes, "●bot判定固定 ユーザ: screen_name=" + wARR_DBData['screen_name'] + " level=" + wUserLevel, inID=wID )
###			
###			elif wCnt==0 :
###				#############################
###				# 相互フォロー中 解除か
###				if wARR_DBData['level_tag']=="G" :
###					if wARR_DBData['send_cnt']>=gVal.DEF_STR_TLNUM['LEVEL_B_Cnt'] :
###						wUserLevel = "B+"
###					elif wARR_DBData['send_cnt']>=1 :
###						wUserLevel = "B"
###					else:
###						wUserLevel = "C+"
###				
###				#############################
###				# 片フォロワー 解除か
###				elif wARR_DBData['level_tag']=="H" :
###					
###					wUserLevel = "E"
###				
###				#############################
###				# 強制解除か
###				elif wARR_DBData['level_tag']=="G+" or wARR_DBData['level_tag']=="H+" :
###					#############################
###					# 最後のいいねからの期間
###					wFLG_RateRec = False
###					wGetLag = CLS_OSIF.sTimeLag( str( wARR_DBData['rfavo_date'] ), inThreshold=gVal.DEF_STR_TLNUM['forRenFavoForceSec'] )
###					if wGetLag['Result']!=True :
###						wRes['Reason'] = "sTimeLag failed(2)"
###						gVal.OBJ_L.Log( "B", wRes )
###						return wRes
###					if wGetLag['Beyond']==True :
###						### 規定外 =古くなった
###						if wARR_DBData['level_tag']=="G+" :
###							if wARR_DBData['send_cnt']>=gVal.DEF_STR_TLNUM['LEVEL_B_Cnt'] :
###								wUserLevel = "B+"
###							elif wARR_DBData['send_cnt']>=1 :
###								wUserLevel = "B"
###							else:
###								wUserLevel = "C+"
###						
###						elif wARR_DBData['level_tag']=="H+" :
###							
###							wUserLevel = "E"
###			
###			#############################
###			# ユーザの表示
###				### スコア
###			wListData = str(self.ARR_ReactionUser[wID]['score'])
###			wSpace = self.DEF_REACTION_SCORE_LEN - len( str(self.ARR_ReactionUser[wID]['score']) )
###			wStr = wListData + " " * wSpace + "  :  "
###			
###				### 連ファボカウント
###			wListData = str(wCnt)
###			wSpace = self.DEF_REACTION_SCORE_LEN - len( str(wCnt) )
###			wStr = wStr + wListData + " " * wSpace + ":  "
###			
###				### bot判定カウント
###			if wBotCnt==None :
###				wListData = "0"
###			else:
###				wListData = str(wBotCnt)
###			wSpace = self.DEF_REACTION_SCORE_LEN - len( str(wListData) )
###			wStr = wStr + wListData + " " * wSpace + ":  "
###			
###				### 今のレベル
###			if wUserLevel==None :
###				wListData = str(wARR_DBData['level_tag'])
###			else:
###				wListData = wUserLevel
###			wSpace = self.DEF_REACTION_SCORE_LEN - len( wListData )
###			wStr = wStr + wListData + " " * wSpace + ":  "
###			
###				### ユーザ名
###			wStr = wStr + self.ARR_ReactionUser[wID]['screen_name']
###			CLS_OSIF.sPrn( wStr )
###			
###			#############################
###			# テストモードなら以下はスキップ
###			if self.DEF_REACTION_TEST==True :
###				continue
###			
###			#############################
###			# 連ファボカウント更新
###			if wARR_DBData['renfavo_cnt']!=wCnt :
###				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_RenFavo( wID, wCnt, wBotCnt )
###				if wSubRes['Result']!=True :
###					###失敗
###					wRes['Reason'] = "UpdateFavoData_RenFavo is failed"
###					gVal.OBJ_L.Log( "B", wRes )
###					return wRes
###			
###			#############################
###			# ユーザレベルの変更の実行
###			if wUserLevel!=None :
###				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wID, wUserLevel )
###				if wSubRes['Result']!=True :
###					###失敗
###					wRes['Reason'] = "UpdateFavoData_UserLevel is failed"
###					gVal.OBJ_L.Log( "B", wRes )
###					return wRes
###		
###		#############################
###		# 正常
###		wRes['Result'] = True
###		return wRes
###
###



#####################################################
# 連ファボ測定
#####################################################
	def CheckRenFavo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterReaction"
		wRes['Func']  = "CheckRenFavo"
		
		#############################
		# 取得開始の表示
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "連ファボ測定中" )
		
		#############################
		# リアクションユーザ
		wKeylist = list( self.ARR_ReactionUser.keys() )
		for wID in wKeylist :
			wID = str(wID)
			
			#############################
			# 連ファボ判定
			if self.ARR_ReactionUser[wID]['hit_new']<gVal.DEF_STR_TLNUM['renFavoUpCnt'] :
				continue
			
			#############################
			# DBからいいね情報を取得する(1個)
			wDBRes = gVal.OBJ_DB_IF.GetFavoDataOne( self.ARR_ReactionUser[wID], inFLG_New=False )
			if wDBRes['Result']!=True :
				###失敗
				wRes['Reason'] = "GetFavoDataOne is failed(1)"
				gVal.OBJ_L.Log( "B", wRes )
				continue
			### DB未登録ならスキップ
			if wDBRes['Responce']['Data']==None :
				continue
			wARR_DBData = wDBRes['Responce']['Data']
			
			#############################
			# カウントアップ
			wCnt = wARR_DBData['renfavo_cnt'] + 1
			
###			if wCnt>gVal.DEF_STR_TLNUM['renFavoBotCnt'] :
###				### 報告対象の表示と、ログに記録
###				gVal.OBJ_L.Log( "RR", wRes, "●bot判定 ユーザ: screen_name=" + wARR_DBData['screen_name'] + " level=" + wARR_DBData['level_tag'], inID=wID )
###				wStr = "●bot判定 ユーザ:"
###				wStr = wStr + " screen_name=" + str( wARR_DBData['screen_name'] )
###				wStr = wStr + " level=" + wARR_DBData['level_tag']
###				wStr = wStr + " renfavo_cnt=" + str( wCnt )
###				wStr = wStr + " hit=" + str( self.ARR_ReactionUser[wID]['hit_new'] )
###				gVal.OBJ_L.Log( "RR", wRes, wStr, inID=wID )
###			
			#############################
			# 連ファボカウント更新
			if wARR_DBData['renfavo_cnt']!=wCnt :
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_RenFavo( wID, wCnt )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "UpdateFavoData_RenFavo is failed(1)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
		
		#############################
		# 連ファボのリセット
		
		#############################
		# 連ファボ一覧の取得
		wDBRes = gVal.OBJ_DB_IF.GetFavoData_RenFavoList()
		if wDBRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetFavoData_RenFavoList is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wARR_RenFavo = wDBRes['Responce']
		
		wBotNum = 0
		wKeylist = list( wARR_RenFavo.keys() )
		for wID in wKeylist :
			wID = str(wID)
			
			#############################
			# DBからいいね情報を取得する(1個)
			wDBRes = gVal.OBJ_DB_IF.GetFavoDataOne( wARR_RenFavo[wID], inFLG_New=False )
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
			# 最後のいいねからの期間
			wGetLag = CLS_OSIF.sTimeLag( str( wARR_DBData['rfavo_date'] ), inThreshold=gVal.DEF_STR_TLNUM['forRenFavoResetSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed(2)"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			if wGetLag['Beyond']==True :
				### 規定外 =古い
				
				#############################
				# 連ファボカウントのリセット
				wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_RenFavo( wID, 0 )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "UpdateFavoData_RenFavo is failed(2)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				wStr = "〇bot解除 " + str( wARR_DBData['screen_name'])
				wStr = wStr + " level=" + wARR_DBData['level_tag']
				wStr = wStr + " rdate=" + str( wARR_DBData['rfavo_date'] )
				wStr = wStr + " rcnt=" + str( wARR_DBData['rfavo_cnt'] )
				CLS_OSIF.sPrn( wStr )
			
			else:
				if wARR_DBData['renfavo_cnt']>gVal.DEF_STR_TLNUM['renFavoBotCnt'] :
					wStr = "●bot判定 " + str( wARR_DBData['screen_name'])
					wStr = wStr + " level=" + wARR_DBData['level_tag']
					wStr = wStr + " rdate=" + str( wARR_DBData['rfavo_date'] )
					wStr = wStr + " rcnt=" + str( wARR_DBData['rfavo_cnt'] )
					wStr = wStr + " renfavo_cnt=" + str( wARR_DBData['renfavo_cnt'] )
					CLS_OSIF.sPrn( wStr )
					wBotNum += 1
					
					#############################
					# 結果送信
###					self.__sendRenFavoTweet( jnCnt=wBotNum )
					self.__sendRenFavoTweet( jnScreenName=str( wARR_DBData['screen_name']), jnCnt=str( wARR_DBData['renfavo_cnt'] ) )
		
###		#############################
###		# 結果送信
###		self.__sendRenFavoTweet( jnCnt=wBotNum )
###		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	# 連ファボ測定結果送信
	#####################################################
###	def __sendRenFavoTweet( self, jnCnt=0 ):
	def __sendRenFavoTweet( self, jnScreenName, jnCnt=0 ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterReaction"
		wRes['Func']  = "__sendRenFavoTweet"
		
		#############################
		# bot判定者がいるか
		if jnCnt==0 :
			### いない場合は処理しない
			wRes['Result'] = True
			return wRes
		
		#############################
		# 今日は連ファボ送信したか
		wARR_DateNow = str( gVal.STR_Time['TimeDate'] )
		wARR_DateNow = wARR_DateNow.split(" ")
		wARR_DateNow = wARR_DateNow[0]
		
		wARR_DateRen = str( gVal.STR_Time['send_ren'] )
		wARR_DateRen = wARR_DateRen.split(" ")
		wARR_DateRen = wARR_DateRen[0]
		
		if wARR_DateNow==wARR_DateRen :
			### 送信済
			wRes['Result'] = True
			return wRes
		
		wTweet = ""
		#############################
		# ツイートの作成
###		wTweet = "[自動] bot判定数=" + str(jnCnt) + '\n'
###		wTweet = wTweet + "[Automatic] Number of bot decisions=" + str(jnCnt) + '\n'
		wTweet = "[自動] 連続いいね受信" + '\n'
		wTweet = wTweet + "[Automatic] Receiving consecutive likes" + '\n'
		wTweet = wTweet + "user name: " + str(jnScreenName) + '\n'
		wTweet = wTweet + "point: " + str(jnCnt) + '\n'
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
		wStr = "Bot判定数を送信しました。" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# ログに記録
		gVal.OBJ_L.Log( "T", wRes, "Bot判定数送信(Twitter)" )
		
		#############################
		# 現時間を設定
		wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "send_ren", gVal.STR_Time['TimeDate'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "SetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		###	gVal.STR_Time['mffavo']
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# VIPリアクション監視チェック
#####################################################
	def VIP_ReactionCheck( self ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterReaction"
		wRes['Func']  = "VIP_ReactionCheck"
		
		#############################
		# VIP監視ユーザの取得
		wARR_VIPuser = self.OBJ_Parent.GetVIPUser()
		if len( wARR_VIPuser )==0 :
			### 規定以内は除外
			wStr = "●VIP監視対象がないため 処理スキップ" + '\n'
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
		#############################
		# 取得可能時間か？
		wGetLag = CLS_OSIF.sTimeLag( str( gVal.STR_Time['vip_ope'] ), inThreshold=gVal.DEF_STR_TLNUM['forVipOperationSec'] )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wGetLag['Beyond']==False :
			### 規定以内は除外
			wStr = "●VIPリアクション監視期間外 処理スキップ: 次回処理日時= " + str(wGetLag['RateTime']) + '\n'
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
		for wUserID in wARR_VIPuser :
			wUserID = str(wUserID)	# VIPユーザ
			
			#############################
			# VIPユーザ名
			wVIPuserName = self.OBJ_Parent.GetVIPUserInfo( wUserID )
			if wVIPuserName==None :
				wRes['Reason'] = "GetVIPUserInfo is not get: user_id=" + str(wUserID)
				gVal.OBJ_L.Log( "A", wRes )
				continue
			wVIPuserName = wVIPuserName['screen_name']
			
			#############################
			# 取得開始の表示
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "VIPリアクションチェック中: user=" + gVal.ARR_NotReactionUser[wUserID]['screen_name'] )
			wCount = gVal.DEF_STR_TLNUM['vipReactionTweetLine']
			
			#############################
			# 直近のツイートを取得
			wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="user", inFLG_Rep=False, inFLG_Rts=False,
				 inID=wUserID, inCount=wCount )
			if wTweetRes['Result']!=True :
				wRes['Reason'] = "Twitter Error: GetTL"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if len(wTweetRes['Responce'])==0 :
				wRes['Reason'] = "Tweet is not get: user=" + gVal.ARR_NotReactionUser[wUserID]['screen_name']
				gVal.OBJ_L.Log( "D", wRes )
				continue
			
			#############################
			# チェック
			# いいね、リツイート、引用リツイートしたユーザ
			
			###ウェイト初期化
			self.OBJ_Parent.Wait_Init( inZanNum=len( wTweetRes['Responce'] ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
			
			wFLG_ZanCountSkip = False
			for wTweet in wTweetRes['Responce'] :
				###ウェイトカウントダウン
				if self.OBJ_Parent.Wait_Next( inZanCountSkip=wFLG_ZanCountSkip )==False :
					break	###ウェイト中止
				wFLG_ZanCountSkip = False
				
				###日時の変換
				wTime = CLS_TIME.sTTchg( wRes, "(1)", wTweet['created_at'] )
				if wTime['Result']!=True :
					continue
				wTweet['created_at'] = wTime['TimeDate']
				
				#############################
				# 期間内のTweetか
				wGetLag = CLS_OSIF.sTimeLag( str( wTweet['created_at'] ), inThreshold=gVal.DEF_STR_TLNUM['forVipReactionTweetSec'] )
				if wGetLag['Result']!=True :
					wRes['Reason'] = "sTimeLag failed(1)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				if wGetLag['Beyond']==True :
					###期間外= 古いツイートなので処理しない
					wFLG_ZanCountSkip = True
					continue
				
				#############################
				# ツイートチェック
				wSubRes = self.ReactionTweetCheck( wUserID, wTweet, inVIPuser=wVIPuserName )
				if wSubRes['Result']!=True :
					wRes['Reason'] = "ReactionTweetCheck is failed"
					gVal.OBJ_L.Log( "B", wRes )
					continue
			
			#############################
			# チェック
			# メンションしたユーザ
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "VIPリアクションチェック中：メンション: user=" + gVal.ARR_NotReactionUser[wUserID]['screen_name'] )
			
			wSubRes = gVal.OBJ_Tw_IF.GetMyMentionLookup( wUserID )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "Twitter Error(GetRefRetweetLookup): Tweet ID: " + wTweetID + " user=" + gVal.ARR_NotReactionUser[wUserID]['screen_name']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			###ウェイト初期化
			self.OBJ_Parent.Wait_Init( inZanNum=len( wSubRes['Responce'] ), inWaitSec=gVal.DEF_STR_TLNUM['defLongWaitSec'] )
			
			wFLG_ZanCountSkip = False
			wKeylist = list( wSubRes['Responce'].keys() )
			for wReplyID in wKeylist :
				###ウェイトカウントダウン
				if self.OBJ_Parent.Wait_Next( inZanCountSkip=wFLG_ZanCountSkip )==False :
					break	###ウェイト中止
				wFLG_ZanCountSkip = False
				
				#############################
				# 期間内のTweetか
				wGetLag = CLS_OSIF.sTimeLag( str( wSubRes['Responce'][wReplyID]['created_at'] ), inThreshold=gVal.DEF_STR_TLNUM['forVipReactionTweetSec'] )
				if wGetLag['Result']!=True :
					wRes['Reason'] = "sTimeLag failed(2)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				if wGetLag['Beyond']==True :
					###期間外= 古いツイートなので処理しない
					wFLG_ZanCountSkip = True
					continue
				
				#############################
				# チェック対象のツイート表示
				wStr = '\n' + "--------------------" + '\n' ;
				wStr = wStr + "チェック中: " + '\n' ;
				wStr = wStr + wSubRes['Responce'][wReplyID]['text'] ;
				CLS_OSIF.sPrn( wStr )
				
				wID = str(wSubRes['Responce'][wReplyID]['user']['id'])
				###ユーザ単位のリアクションチェック
				wReactionRes = self.ReactionUserCheck( wSubRes['Responce'][wReplyID]['user'], wSubRes['Responce'][wReplyID], inAction="mention", inVIPuser=wVIPuserName )
				if wReactionRes['Result']!=True :
					wRes['Reason'] = "Twitter Error(ReactionUserCheck 4): Tweet ID: " + str(wSubRes['Responce'][wReplyID]['id'])
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
		
		#############################
		# 現時間を設定
		if self.DEF_REACTION_TEST==False :
			wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "vip_ope", gVal.STR_Time['TimeDate'] )
			if wTimeRes['Result']!=True :
				wRes['Reason'] = "SetTimeInfo is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



