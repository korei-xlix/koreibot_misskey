#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : ついったーユーズ
#####################################################
# 参考：
#   twitter api rate
#     https://developer.twitter.com/en/docs/basics/rate-limits
#
#####################################################
import time
import math
import json
###import subprocess as sp
import subprocess
###import pings
###import base64
from requests_oauthlib import OAuth1Session

#####################################################
class CLS_Twitter_Use():
#####################################################
	Twitter_use = ''						#Twitterモジュール実体
	TwStatus = ""
	##	"Init"     : False
	##	"Reason"   : None
	##	"Responce" : None

	STR_TWITTERdata = {
		"TwitterID"		: "",				#Twitter ID
		"APIkey"		: "",				#API key
		"APIsecret"		: "",				#API secret key
		"ACCtoken"		: "",				#Access token
		"ACCsecret"		: "",				#Access token secret
		"Bearer"		: ""				#Bearer token *oauth2.0
	}
	
	CHR_TWITTERheader = {}
	
	VAL_TwitNum       = 200
	VAL_TwitListNum   = 5000
	VAL_TwitSearchNum = 100

	DEF_TWITTER_HOSTNAME = "twitter.com"	#Twitterホスト名
	DEF_MOJI_ENCODE      = 'utf-8'			#ファイル文字エンコード
	DEF_TWITTER_PING_COUNT   = "2"			#Ping回数 (文字型)
##	DEF_TWITTER_PING_TIMEOUT = "1000"		#Pingタイムアウト秒 (文字型)

	#トレンド地域ID
#	DEF_WOEID = "1"				#グローバル
	DEF_WOEID = "23424856"		#日本
		# idにはWOEID Lookupの地域IDを入れる
		#   http://woeid.rosselliot.co.nz/
		#   なんだけどエラー？で取得できない。なんやこれ...


	STR_TWITTER_STATUS_CODE = {
		"200"	: "OK",
		"304"	: "Not Modified",
		"400"	: "Bad Request",
		"401"	: "Unauthorized",
		"403"	: "Forbidden",
		"404"	: "Not Found",
		"406"	: "Not Acceptable",
		"410"	: "Gone",
		"420"	: "Enhance Your Calm",
		"422"	: "Unprocessable Entity",
		"429"	: "Too Many Requests",
		"500"	: "Internal Server Error",
		"502"	: "Bad Gateway",
		"503"	: "Service Unavailable",
		"504"	: "Gateway timeout"
	}
	### http://westplain.sakuraweb.com/translate/twitter/API-Overview/Error-Codes-and-Responses.cgi

	ARR_TwitterList = {}	#Twitterリスト
	# id    リストid
	# name  リスト名
	# me    自分か True=自分

	ARR_TwitterSubsList = {}	#Twitterリスト(被登録)
	# id    リストid
	# name  リスト名
	# me    自分か True=自分

	ARR_MuteList = []	#ミュートIDs(リスト)

	CHR_TimeDate = "1901-01-01 00:00:00"
###	DEF_VAL_SLEEP = 5			#Twitter処理遅延（秒）
###	DEF_VAL_SLEEP_SEMI = 10		#Twitter処理遅延（秒）
###	DEF_VAL_SLEEP_LONG = 20		#Twitter処理遅延（秒）
	DEF_VAL_SLEEP_SHORT = 5		#Twitter処理遅延（秒）
	DEF_VAL_SLEEP       = 15	#Twitter処理遅延（秒）
	DEF_VAL_SLEEP_LONG  = 30	#Twitter処理遅延（秒）



#####################################################
# Twitter状態取得
#####################################################
	def GetTwStatus(self):
		return self.TwStatus	#返すだけ



#####################################################
# ユーザ名取得
#####################################################
	def GetUsername(self):
		if self.STR_TWITTERdata['TwitterID']=='' :
			return ""
		
		wUser = self.STR_TWITTERdata['TwitterID'] + "@" + self.DEF_TWITTER_HOSTNAME
		return wUser



#####################################################
# Twitter状態取得
#####################################################
	def __initTwStatus(self):
		self.TwStatus = {
			"Init"     : False,
			"Reason"   : None,
			"Responce" : None,
			"APIrect"  : None
		}
		
		#############################
		# API規制値
		#   ※アプリでの規制値は 15分 * 80% で計算する
		self.TwStatus['APIrect'] = {}
		###	POST														# リクエストとTwitter規制値
		self.__set_API( "status",      20 )			# POST: 3h/300 (ツイートとリツイは共通)
		self.__set_API( "favorites",    8 )			# POST: 24h/1000
		self.__set_API( "friendships",  3 )			# POST: 24h/400
		self.__set_API( "muted",       20 )			# POST: 3h/300
		self.__set_API( "directmsg",    8 )			# POST: 24h/400
		
		###	GET
		self.__set_API( "home_timeline",	12 )	# GET: 15m/15
		self.__set_API( "mention_timeline",	60 )	# GET: 15m/75
		self.__set_API( "user_timeline",	720 )	# GET: 15m/900
		self.__set_API( "lists_status",		720 )	# GET: 15m/900
		self.__set_API( "search_tweets",	144 )	# GET: 15m/180
		self.__set_API( "friends_list",		12 )	# GET: 15m/15
		self.__set_API( "friends_show",		12 )	# GET: 15m/15
		self.__set_API( "friends_ids",		12 )	# GET: 15m/15
		self.__set_API( "followers_ids",	12 )	# GET: 15m/15
		self.__set_API( "followers_list",	12 )	# GET: 15m/15
		self.__set_API( "favorites_list",	60 )	# GET: 15m/75
		self.__set_API( "lists_list",		12 )	# GET: 15m/15
		self.__set_API( "lists_subs_list",	60 )	# GET: 15m/75
		self.__set_API( "lists_members",	720 )	# GET: 15m/900
		self.__set_API( "lists_subscribers", 144 )	# GET: 15m/180
		self.__set_API( "trends_place",		60 )	# GET: 15m/75
		self.__set_API( "users_show",		900 )	# GET: 15m/900
		self.__set_API( "friendships_show",	144 )	# GET: 15m/180
		self.__set_API( "mute_list",		12 )	# GET: 15m/15
		self.__set_API( "tweet_status",		240 )	# GET: 15m/300
		self.__set_API( "tweet_lookup",		240 )	# GET: 15m/300
		self.__set_API( "mention_lookup",	144 )	# GET: 15m/180
		self.__set_API( "likes_lookup",		40 )	# GET: 15m/50
		self.__set_API( "retweet_lookup",	60 )	# GET: 15m/75
		self.__set_API( "search_tweets_v2",	144 )	# GET: 15m/180
		self.__set_API( "fleet_list",		144 )	# GET: 15m/180
		self.__set_API( "fleet_users",		80 )	# GET: 15m/100
		return

	#####################################################
	def __set_API( self, inName, inMAX ):
		wCell = {
			"num"	: 0,
			"max"	: inMAX,
			"rect"	: False
		}
		self.TwStatus['APIrect'].update({ inName : wCell })
		return



#####################################################
# API規制値カウント
#####################################################
	def __set_APIcount( self, inName ):
		if self.TwStatus['APIrect'][inName]['rect']==True :
			return	#規制中はカウントしない
		
		self.TwStatus['APIrect'][inName]['num'] += 1
		if self.TwStatus['APIrect'][inName]['max']<=self.TwStatus['APIrect'][inName]['num'] :
			self.TwStatus['APIrect'][inName]['rect'] = True	#規制
		return

	#####################################################
	def __get_APIrect( self, inName ):
		if self.TwStatus['APIrect'][inName]['rect']==True :
			return False	#規制中
		return True			#規制なし

	#####################################################
	### ※外部の時間差が分かる処理から呼び出してリセットすること
	def ResetAPI(self):
		wKeylist = self.TwStatus['APIrect'].keys()
		for wKey in wKeylist :
			self.TwStatus['APIrect'][wKey]['num']  = 0
			self.TwStatus['APIrect'][wKey]['rect'] = False
		return



#####################################################
# レスポンス取得
#####################################################

##		#############################
##		# 応答形式の取得
##		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
##		wRes = self.__Get_Resp()
##		wRes['Func'] = "Function"

	def __Get_Resp(self):
		wRes = {
			"Result"   : False,
			"Class"    : "CLS_Twitter_Use",
			"Func"     : None,
			"Reason"   : None,
			"Responce" : None,
			"StatusCode" : None,
			"RunAPI"   : 0
		}
		
		return wRes



#####################################################
# 初期化
#####################################################
	def __init__(self):
		return



#####################################################
# 接続情報の作成
#####################################################
	def Create( self, inTwitterID, inAPIkey, inAPIsecret, inACCtoken, inACCsecret, inBearer, inGetNum=200 ):
		#############################
		# Twitter状態 全初期化
		self.__initTwStatus()
		
		#############################
		# 接続情報の仮セット
		self.STR_TWITTERdata['TwitterID'] = inTwitterID
		self.STR_TWITTERdata['APIkey']    = inAPIkey
		self.STR_TWITTERdata['APIsecret'] = inAPIsecret
		self.STR_TWITTERdata['ACCtoken']  = inACCtoken
		self.STR_TWITTERdata['ACCsecret'] = inACCsecret
		self.STR_TWITTERdata['Bearer']    = inBearer
		
		self.VAL_TwitNum = inGetNum
		
		#############################
		# Twitter接続テスト
		if self.__twConnect()!=True :
			return False	#失敗
		
		#############################
		# 遅延
###		time.sleep( self.DEF_VAL_SLEEP )
		time.sleep( self.DEF_VAL_SLEEP_SHORT )
		
		#############################
		# 初期化完了
		self.TwStatus['Init'] = True
		return True



#####################################################
# 接続
#####################################################
	def Connect(self):
		#############################
		# 初期化状態の確認
		if self.TwStatus['Init']!=True :
			self.TwStatus['Reason'] = "CLS_Twitter_Use: Connect: TwStatusが初期化されていません"
			return False
		
		#############################
		# Twitter接続
		if self.__twConnect()!=True :
			return False
		
		#############################
		# リストクリア
		self.ARR_TwitterList = {}
		
		return True

	#####################################################
	def __twConnect(self):

		#############################
		# 通信テスト
###		if self.__TwitterPing()!=True :
		wRes = self.__TwitterPing()
		if wRes['Result']!=True :
			self.TwStatus['Reason'] = "CLS_Twitter_Use: __twConnect: Twitter host no responce: " + wRes['Reason']
			return False
		
		#############################
		# Twitterクラスの生成
		wRes = self.__twSetAPI()
		
		#############################
		# ヘッダ作成(oauth v2.0向け)
		#   Bearerを設定する
		self.CHR_TWITTERheader = {
			"Authorization" : "Bearer {}".format( self.STR_TWITTERdata['Bearer'] )
		}
		
		return wRes



	#####################################################
	def __twSetAPI(self):

		#############################
		# Twitterクラスの生成
		try:
			self.Twitter_use = OAuth1Session(
				self.STR_TWITTERdata["APIkey"],
				self.STR_TWITTERdata["APIsecret"],
				self.STR_TWITTERdata["ACCtoken"],
				self.STR_TWITTERdata["ACCsecret"]
			)
		except ValueError as err :
			self.IniStatus['Reason'] = "CLS_Twitter_Use: __twConnect: Twitter error: " + str(err)
			return False
		
		return True



#####################################################
# twitterサーバのPing確認
#####################################################
###	def __TwitterPing(self):
##		wStatus, wResult = sp.getstatusoutput( "ping -c " + str(inCount) + " " + str( self.DEF_TWITTER_HOSTNAME ) )
##		wPingComm = "ping -c " + self.DEF_TWITTER_PING_COUNT + " -w " + self.DEF_TWITTER_PING_TIMEOUT + " " + self.DEF_TWITTER_HOSTNAME
##		wPingComm = "ping -c " + self.DEF_TWITTER_PING_COUNT + " " + self.DEF_TWITTER_HOSTNAME
###		wPingComm = "ping -n " + self.DEF_TWITTER_PING_COUNT + " " + self.DEF_TWITTER_HOSTNAME
###		
###		wPingComm = open( wPingComm, encoding='CP932' )
###		
##		wPingComm = "ping -c " + self.DEF_TWITTER_PING_COUNT + " " + self.DEF_TWITTER_HOSTNAME
##		wStatus, wResult = sp.getstatusoutput( wPingComm )
##		if wStatus==0 :
##		wRes = subprocess.run([ "ping", str(self.DEF_TWITTER_HOSTNAME), "-c", str(self.DEF_TWITTER_PING_COUNT), "-W" , "300" ], stdout=subprocess.PIPE )
###	    print(res.stdout.decode("cp932"))

	def __TwitterPing( self, inHost=None ):
		
		wResult = {
			"Result"	: False,
			"Reason"	: None
		}
		
		#############################
		# ホスト名の設定
		if inHost==None or inHost=="none" :
			wHost = str( self.DEF_TWITTER_HOSTNAME )
		else:
			wHost = str( inHost )
		
###		b64_auth = base64.b64encode(wHost.encode()).decode("utf-8")
###		
###		wOBJ_Ping = pings.Ping()	# Pingオブジェクト作成
###		wRes = wOBJ_Ping.ping( b64_auth, times=self.DEF_TWITTER_PING_COUNT )
###		if wRes.is_reached() :
###		wRes = subprocess.run([ "ping", wHost, "-c", str(self.DEF_TWITTER_PING_COUNT), "-W" , "5000" ], stdout=subprocess.PIPE )
		
		#############################
		# Pingテスト
#		wRes = subprocess.run([ "ping", "-w", "1000", "-c", str(self.DEF_TWITTER_PING_COUNT), wHost], stdin=subprocess.PIPE, stdout=subprocess.PIPE )

		wRes = subprocess.run([ "ping", wHost], stdin=subprocess.PIPE, stdout=subprocess.PIPE )

###		print( str(wRes) )
###		print(wRes.stdout.decode("cp932"))
###
###		if wRes.returncode == 0 :
###			return True	# Link UP
###		
###		return False	# Link Down
		#############################
		# 結果
		if wRes.returncode == 0 :
			wResult['Result'] = wRes.stdout.decode("cp932")
		
		#############################
		# 正常
		wResult['Result'] = True
		return wResult



#####################################################
	def Ping( self, inHost=None ):
		wRes = self.__TwitterPing( inHost=inHost )
###		if wRes==False :
###			
###			return False	# NG
###		
###		return True			# OK
		return wRes



#####################################################
# ついーと処理
#####################################################
	def Tweet( self, inTweet ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "Tweet"
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "status" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		#############################
		# 入力チェック
		if inTweet=='' :
			wRes['Reason'] = "Twitter内容がない"
			return wRes
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/statuses/update.json"
		
		#############################
		# パラメータの生成
		wParams = { "status" : inTweet }
		
		#############################
		# APIカウント
		self.__set_APIcount( "status" )
		
		#############################
		# ついーと
		try:
			wRes['RunAPI'] += 1	#実行
			wTweetRes = self.Twitter_use.post( wAPI, params=wParams )
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 遅延
		time.sleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wRes['Reason'] = "Twitter responce failed: " + str(wTweetRes.status_code)
			return wRes
		
		wRes['Result'] = True
		return wRes



#####################################################
# ついーと削除処理
#####################################################
	def DelTweet( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "DelTweet"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/statuses/destroy.json"
		
		#############################
		# パラメータの生成
		wParams = { "id" : inID }
		
		#############################
		# ついーと
		try:
			wRes['RunAPI'] += 1	#実行
			wTweetRes = self.Twitter_use.post( wAPI, params=wParams )
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 遅延
		time.sleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wRes['Reason'] = "Twitter responce failed: " + str(wTweetRes.status_code)
			return wRes
		
		wRes['Result'] = True
		return wRes



#####################################################
# DM送信処理
#####################################################
	def SendDM( self, inID, inTweet ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "SendDM"
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "directmsg" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		#############################
		# 入力チェック
		if inTweet=='' :
			wRes['Reason'] = "Twitter内容がない"
			return wRes
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/direct_messages/events/new.json"
		
		#############################
		# パラメータの生成
		wHeaders = { "content-type" : "application/json" }
		wPayload = { "event" : { "type" : "message_create",
						"message_create" : {
							"target" : { "recipient_id" : inID },
							"message_data" : { "text" : inTweet, }
						}
					}
		}
		
		#############################
		# APIカウント
		self.__set_APIcount( "directmsg" )
		
		#############################
		# ついーと
		try:
			wRes['RunAPI'] += 1	#実行
			wPayload = json.dumps( wPayload )
			wTweetRes = self.Twitter_use.post( wAPI, headers=wHeaders, data=wPayload )
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 遅延
		time.sleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wRes['Reason'] = "Twitter responce failed: " + str(wTweetRes.status_code)
			return wRes
		
		wRes['Result'] = True
		return wRes



#####################################################
# タイムライン読み込み処理
#####################################################
	def GetTL( self, inTLmode="home", inFLG_Rep=True, inFLG_Rts=False, inCount=VAL_TwitNum, inID=None, inListID=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "GetTL"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		if inTLmode=="home" :
			wAPI = "https://api.twitter.com/1.1/statuses/home_timeline.json"
			wAPIname = "home_timeline"
		elif inTLmode=="user" :
			wAPI = "https://api.twitter.com/1.1/statuses/user_timeline.json"
			wAPIname = "user_timeline"
		elif inTLmode=="list" :
			try:
				wListID = int(inListID)
			except ValueError:
				wRes['Reason'] = "inListID is invalid: " + str(inListID)
				return wRes
			
			wAPI = "https://api.twitter.com/1.1/lists/statuses.json"
			wAPIname = "lists_status"
		else :
			wRes['Reason'] = "inTLmode is invalid: " + str(inTLmode)
			return wRes
		
		#############################
		# API規制チェック
		if self.__get_APIrect( wAPIname )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		#############################
		# ループ数の計算
		if inCount>200 :
			###取得数 200超の場合
			wZan = inCount + 1
			wZan -= 1
			wCount = 200
			wLoop = inCount / 200
			wLoop = math.floor( wLoop )
		else :
			###取得数 200未満の場合
			wZan = inCount + 1
			wZan -= 1
			wCount = inCount + 1
			wCount -= 1
			wLoop = 1
		
		#############################
		# IDの補填
		if inID==None :
			wID = self.STR_TWITTERdata['TwitterID']
		else:
			wID = inID
		
		#############################
		# パラメータの生成
		if inTLmode=="list" :
			wParams = {
				"count"           : wCount,
				"user_id"         : wID,
				"exclude_replies" : inFLG_Rep,
				"include_rts"     : inFLG_Rts,
				"list_id"         : wListID
			}
		else :
			wParams = {
				"count"           : wCount,
				"user_id"         : wID,
				"exclude_replies" : inFLG_Rep,
				"include_rts"     : inFLG_Rts
			}
			## exclude_replies  : リプライを除外する True=除外
			## include_rts      : リツイートを含める True=含める
		
		#############################
		# タイムライン読み込み
		wNowID = -1
		wARR_TL = []
		try:
			while True :
				#############################
				# APIカウント
				self.__set_APIcount( wAPIname )
				
				wRes['RunAPI'] += 1	#実行
				wTweetRes = self.Twitter_use.get( wAPI, params=wParams )
				wTL = json.loads( wTweetRes.text )
				
				wFLG_Add = False
				###情報抜き出し
				if len(wTL)>0 :
					if "errors" in wTL or \
					   "error" in wTL :
						continue
					
					for wLine in wTL :
						if wNowID==wLine['id'] :
							continue
						wARR_TL.append( wLine )
						wNowID   = wLine['id']
						wFLG_Add = True
				
				#############################
				# API規制チェック
				if self.__get_APIrect( wAPIname )!=True :
					break
				###ページング処理
				if wFLG_Add==False :
					break
				
				wZan  -= 200
				wLoop -= 1
				if wZan<1 or wLoop<=0 :
					###残り取得数=0以下 or ループ数=0以下
					break
				if wZan<200 :
					wParams['count'] = wZan
				wParams['max_id'] = wNowID
				
				#############################
				# 遅延
				time.sleep( self.DEF_VAL_SLEEP )
###				time.sleep( self.DEF_VAL_SLEEP_SEMI )
		
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wCHR_StatusCode = str(wTweetRes.status_code)
			if wCHR_StatusCode in self.STR_TWITTER_STATUS_CODE :
				###定義コードがあるなら文字出力する
				wCHR_StatusCode = self.STR_TWITTER_STATUS_CODE[wCHR_StatusCode]
			else :
				wCHR_StatusCode = "unknown code"
			
			###直前エラーならデコードする
			if 'errors' in wTL :
				wCHR_StatusCode = wCHR_StatusCode + ": Error Code=" + str(wTL['errors'][0]['code']) + ":" + str(wTL['errors'][0]['message'])
			
			wRes['Reason'] = "Twitter responce failed: Status Code=" + str(wTweetRes.status_code) + ":" + wCHR_StatusCode
			return wRes
		
		#############################
		# TLを取得
		wRes['Responce'] = wARR_TL
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# Tweet Tweet Lookup取得
# ★ Twitter Oauth v2.0
#
# 
#
#####################################################
	def GetTweetLookup( self, inID=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "GetTweetLookup"
		
		#############################
		# 入力チェック
		if inID=='' or inID==None :
			wRes['Reason'] = "IDがない"
			return wRes
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/2/tweets/{id}"
		wAPI = wAPI.format( id=inID )
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "tweet_lookup" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		#############################
		# パラメータの生成
		wEXPANSIONS = ",".join(
						[
							"in_reply_to_user_id",
							"referenced_tweets.id",
							"referenced_tweets.id.author_id"
						]
		)
		wTWEET_FIELDS = ",".join(
						[
							"entities",
							"in_reply_to_user_id",
							"referenced_tweets",
							"reply_settings",
							"author_id",
							"context_annotations",
							"conversation_id",
							"created_at",
							"id",
							"public_metrics",
							"text",
						]
		)
		wMEDIA_FIELDS = ",".join(
						[
#							"duration_ms",
#							"height",
#							"media_key",
#							"preview_image_url",
#							"type",
#							"url",
#							"width",
#							"public_metrics",
#							"non_public_metrics",
#							"organic_metrics",
#							"promoted_metrics"
#							"alt_text"
						]
		)
		wUSER_FIELDS = ",".join(
						[
							"id",
							"username",	# v1.1でいうscreen_name
							"name",
							"description"
						]
		)
		
		wParam = {
					"expansions"    : wEXPANSIONS,
					"tweet.fields"  : wTWEET_FIELDS,
#					"media.fields"  : wMEDIA_FIELDS,
					"user.fields"   : wUSER_FIELDS,
		}
		
		#############################
		# APIカウント
		self.__set_APIcount( "tweet_lookup" )
		
		#############################
		# タイムライン読み込み
		try:
			wRes['RunAPI'] += 1	#実行
			wTweetRes = self.Twitter_use.get( wAPI, params=wParam, headers=self.CHR_TWITTERheader )
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 遅延
		time.sleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wRes['Reason'] = "Twitter responce failed: " + str(wTweetRes.status_code)
			return wRes
		
		#############################
		# TLを取得
		wRes['Responce'] = json.loads( wTweetRes.text )
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# Tweet Mention Lookup取得
# ★ Twitter Oauth v2.0
#
# ユーザIDに対するメンションを取得する
#
#####################################################
	def GetMentionLookup( self, inID=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "GetMentionLookup"
		
		#############################
		# 入力チェック
		if inID=='' or inID==None :
			wRes['Reason'] = "IDがない"
			return wRes
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/2/users/{id}/mentions"
		wAPI = wAPI.format( id=inID )
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "mention_lookup" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		#############################
		# パラメータの生成
		wEXPANSIONS = ",".join(
						[
							"attachments.poll_ids",
							"attachments.media_keys",
							"author_id",
							"entities.mentions.username",
							"geo.place_id",
							"in_reply_to_user_id",
							"referenced_tweets.id",
							"referenced_tweets.id.author_id"
						]
		)
		wTWEET_FIELDS = ",".join(
						[
							"author_id",
							"context_annotations",
							"conversation_id",
							"created_at",
							"entities",
							"id",
							"in_reply_to_user_id",
							"public_metrics",
							"reply_settings",
							"text",
						]
		)
		wUSER_FIELDS = ",".join(
						[
							"id",
							"username",	# v1.1でいうscreen_name
							"name",
							"description"
						]
		)
		
		wParam = {
					"expansions"    : wEXPANSIONS,
					"tweet.fields"  : wTWEET_FIELDS,
					"user.fields"   : wUSER_FIELDS,
		}
		
		#############################
		# APIカウント
		self.__set_APIcount( "mention_lookup" )
		
		#############################
		# タイムライン読み込み
		try:
			wRes['RunAPI'] += 1	#実行
			wTweetRes = self.Twitter_use.get( wAPI, params=wParam, headers=self.CHR_TWITTERheader )
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 遅延
		time.sleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wRes['Reason'] = "Twitter responce failed: " + str(wTweetRes.status_code)
			return wRes
		
		#############################
		# TLを取得
		wRes['Responce'] = json.loads( wTweetRes.text )
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# Tweet Likes Lookup取得
# ★ Twitter Oauth v2.0
#
# いいねした人のユーザ情報を取得する
#
#####################################################
	def GetLikesLookup( self, inID=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "GetLikesLookup"
		
		#############################
		# 入力チェック
		if inID=='' or inID==None :
			wRes['Reason'] = "IDがない"
			return wRes
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/2/tweets/{id}/liking_users"
		wAPI = wAPI.format( id=inID )
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "likes_lookup" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		#############################
		# パラメータの生成
		wUSER_FIELDS = ",".join(
						[
							"id",
							"username",	# v1.1でいうscreen_name
							"name",
							"description"
						]
		)
		
		wParam = {
					"user.fields"   : wUSER_FIELDS,
		}
		
		#############################
		# APIカウント
		self.__set_APIcount( "likes_lookup" )
		
		#############################
		# タイムライン読み込み
		try:
			wRes['RunAPI'] += 1	#実行
			wTweetRes = self.Twitter_use.get( wAPI, params=wParam, headers=self.CHR_TWITTERheader )
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 遅延
		time.sleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wRes['Reason'] = "Twitter responce failed: " + str(wTweetRes.status_code)
			return wRes
		
		#############################
		# TLを取得
		wRes['Responce'] = json.loads( wTweetRes.text )
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# Tweet retweeted by 取得
# ★ Twitter Oauth v2.0
#
# リツイートした人のユーザ情報を取得する
#   {'data': [{'id': '1377268611983712259', 'name': 'lucida3rd', 'username': 'lucida3rd'}], 'meta': {'result_count': 1}}
#
#####################################################
	def GetRetweetLookup( self, inID=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "GetRetweetLookup"
		
		#############################
		# 入力チェック
		if inID=='' or inID==None :
			wRes['Reason'] = "IDがない"
			return wRes
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/2/tweets/{id}/retweeted_by"
		wAPI = wAPI.format( id=inID )
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "retweet_lookup" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		#############################
		# パラメータの生成
		wUSER_FIELDS = ",".join(
						[
							"id",
							"username",	# v1.1でいうscreen_name
							"name",
							"description"
						]
		)
		
		wParam = {
					"user.fields"   : wUSER_FIELDS,
		}
		
		#############################
		# APIカウント
		self.__set_APIcount( "retweet_lookup" )
		
		#############################
		# タイムライン読み込み
		try:
			wRes['RunAPI'] += 1	#実行
			wTweetRes = self.Twitter_use.get( wAPI, params=wParam, headers=self.CHR_TWITTERheader )
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 遅延
		time.sleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wRes['Reason'] = "Twitter responce failed: " + str(wTweetRes.status_code)
			return wRes
		
		#############################
		# TLを取得
		wRes['Responce'] = json.loads( wTweetRes.text )
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# Tweet Search
# ★ Twitter Oauth v2.0
#
# ツイートを検索する
#
#####################################################
	def GetTweetSearch_v2( self, inQuery=None, inMaxResult=40 ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "GetTweetSearch_v2"
		
		#############################
		# 入力チェック
		if inQuery=='' or inQuery==None :
			wRes['Reason'] = "検索ワードがない"
			return wRes
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/2/tweets/search/recent"
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "search_tweets_v2" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		#############################
		# パラメータの生成
		wEXPANSIONS = ",".join(
						[
							"attachments.poll_ids",
							"attachments.media_keys",
							"author_id",
							"entities.mentions.username",
							"geo.place_id",
							"in_reply_to_user_id",
							"referenced_tweets.id",
							"referenced_tweets.id.author_id"
						]
		)
		wTWEET_FIELDS = ",".join(
						[
							"entities",
							"in_reply_to_user_id",
							"referenced_tweets",
							"reply_settings",
							"author_id",
							"context_annotations",
							"conversation_id",
							"created_at",
							"id",
							"public_metrics",
							"text",
						]
		)
		wUSER_FIELDS = ",".join(
						[
							"id",
							"username",	# v1.1でいうscreen_name
							"name",
							"description"
						]
		)
		
		wParam = {
					"expansions"    : wEXPANSIONS,
					"tweet.fields"  : wTWEET_FIELDS,
					"max_results"   : inMaxResult,
					"query"         : inQuery,
					"user.fields"   : wUSER_FIELDS,
		}
		
		#############################
		# APIカウント
		self.__set_APIcount( "search_tweets_v2" )
		
		#############################
		# タイムライン読み込み
		try:
			wRes['RunAPI'] += 1	#実行
			wTweetRes = self.Twitter_use.get( wAPI, params=wParam, headers=self.CHR_TWITTERheader )
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 遅延
		time.sleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wRes['Reason'] = "Twitter responce failed: " + str(wTweetRes.status_code)
			return wRes
		
		#############################
		# TLを取得
		wRes['Responce'] = json.loads( wTweetRes.text )
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# 検索 読み込み処理
#####################################################
	def GetSearch( self, inKeyword=None, inRoundNum=1 ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "GetSearch"
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "search_tweets" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		#############################
		# 入力チェック
		if inKeyword=='' or inKeyword==None :
			wRes['Reason'] = "検索キーがない"
			return wRes
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/search/tweets.json"
		
		#############################
		# パラメータの生成
		wParams = {
			"count"			: self.VAL_TwitSearchNum,
			"q"				: inKeyword,
			"result_type"	: "recent"
		}
		
		#############################
		# タイムライン読み込み
		wARR_TL = []
		wRound  = 0
		try:
			while True :
				#############################
				# APIカウント
				self.__set_APIcount( "search_tweets" )
				
				wRes['RunAPI'] += 1	#実行
				wTweetRes = self.Twitter_use.get( wAPI, params=wParams )
				wTimeline = json.loads( wTweetRes.text )
				
				###要素チェック
				if 'statuses' not in wTimeline :
					break
				
				###情報抜き出し
				if len(wTimeline['statuses'])>0 :
					for wLine in wTimeline['statuses'] :
						wARR_TL.append( wLine )
				
				#############################
				# API規制チェック
				if self.__get_APIrect( "search_tweets" )!=True :
					break
				###ページング処理
				wRound += 1
				if inRoundNum<=wRound :
					break
				wIndex = len(wTimeline['statuses']) - 1
				if wIndex<0 :
					###キーがない =全ツイート読んだ
					break
				wParams['max_id'] = wTimeline['statuses'][wIndex]['id']
				
				#############################
				# 遅延
				time.sleep( self.DEF_VAL_SLEEP )
###				time.sleep( self.DEF_VAL_SLEEP_SEMI )
			
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wCHR_StatusCode = str(wTweetRes.status_code)
			if wCHR_StatusCode in self.STR_TWITTER_STATUS_CODE :
				###定義コードがあるなら文字出力する
				wCHR_StatusCode = self.STR_TWITTER_STATUS_CODE[wCHR_StatusCode]
			else :
				wCHR_StatusCode = "unknown code"
			
			###直前エラーならデコードする
			if 'errors' in wTimeline :
				wCHR_StatusCode = wCHR_StatusCode + ": Error Code=" + str(wTimeline['errors'][0]['code']) + ":" + str(wTimeline['errors'][0]['message'])
			
			wRes['Reason'] = "Twitter responce failed: Status Code=" + str(wTweetRes.status_code) + ":" + wCHR_StatusCode
			return wRes
		
		#############################
		# TLを取得
		wRes['Responce'] = wARR_TL
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# 自ユーザ情報取得処理
#####################################################
	def GetMyUserinfo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "GetMyUserinfo"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/users/show.json"
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "users_show" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		#############################
		# パラメータの生成
		wParams = { "screen_name" : self.STR_TWITTERdata['TwitterID'] }
		
		#############################
		# 実行
		try:
			wRes['RunAPI'] += 1	#実行
			wTweetRes = self.Twitter_use.get( wAPI, params=wParams )
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 遅延
		time.sleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wRes['Reason'] = "Twitter responce failed: " + str(wTweetRes.status_code)
			return wRes
		
		#############################
		# TLを取得
		wRes['Responce'] = json.loads( wTweetRes.text )
		
		wRes['Result'] = True
		return wRes



#####################################################
# ユーザ情報取得処理
#####################################################
	def GetUserinfo( self, inID=-1, inScreenName=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "GetUserinfo"
		
		#############################
		# 入力チェック
		if inID==-1 and inScreenName==None :
			wRes['Reason'] = "Input is Undefined"
			return wRes
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/users/show.json"
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "users_show" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		#############################
		# パラメータの生成
		if inID!=-1 :
			wParams = { "user_id" : inID }
		else :
			wParams = { "screen_name" : inScreenName }
		
		#############################
		# 実行
		try:
			wRes['RunAPI'] += 1	#実行
			wTweetRes = self.Twitter_use.get( wAPI, params=wParams )
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 遅延
		time.sleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wRes['Reason'] = "Twitter responce failed: " + str(wTweetRes.status_code)
			return wRes
		
		#############################
		# TLを取得
		wRes['Responce'] = json.loads( wTweetRes.text )
		
		wRes['Result'] = True
		return wRes



#####################################################
# フォロー関係取得処理
#####################################################
	def GetFollowInfo( self, inSrcID, inDstID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "GetFollowInfo"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/friendships/show.json"
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "friendships_show" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		#############################
		# パラメータの生成
		wParams = {
			"source_id"		: inSrcID,
			"target_id"		: inDstID
		}
		
		#############################
		# 実行
		try:
			wRes['RunAPI'] += 1	#実行
			wTweetRes = self.Twitter_use.get( wAPI, params=wParams )
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 遅延
		time.sleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wRes['Reason'] = "Twitter responce failed: " + str(wTweetRes.status_code)
			return wRes
		
		#############################
		# TLを取得
		wRes['Responce'] = json.loads( wTweetRes.text )
		
		wRes['Result'] = True
		return wRes



#####################################################
# フォロー一覧読み込み処理
#####################################################
	def GetMyFollowList(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "GetMyFollowList"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/friends/list.json"
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "friends_list" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		#############################
		# パラメータの生成
		wParams = {
			"count"			: self.VAL_TwitNum,
			"cursor"		: "-1",
			"skip_status"	: "True"
		}
		
		#############################
		# タイムライン読み込み
		wARR_TL = []
		try:
			while True :
				#############################
				# APIカウント
				self.__set_APIcount( "friends_list" )
				
				wRes['RunAPI'] += 1	#実行
				wTweetRes = self.Twitter_use.get( wAPI, params=wParams )
				wUsers = json.loads( wTweetRes.text )
				
				###要素チェック
				if 'next_cursor_str' not in wUsers :
					break
				if 'users' not in wUsers :
					break
				
				###情報抜き出し
				if len(wUsers['users'])>0 :
					for wLine in wUsers['users'] :
						wARR_TL.append( wLine )
				
				#############################
				# API規制チェック
				if self.__get_APIrect( "friends_list" )!=True :
					break
				###ページング処理
				if wParams['cursor']==wUsers['next_cursor_str'] :
					break
				if wUsers['next_cursor_str']=="0" :
					break
				wParams['cursor'] = wUsers['next_cursor_str']
				
				#############################
				# 遅延
				time.sleep( self.DEF_VAL_SLEEP )
###				time.sleep( self.DEF_VAL_SLEEP_SEMI )
			
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wCHR_StatusCode = str(wTweetRes.status_code)
			if wCHR_StatusCode in self.STR_TWITTER_STATUS_CODE :
				###定義コードがあるなら文字出力する
				wCHR_StatusCode = self.STR_TWITTER_STATUS_CODE[wCHR_StatusCode]
			else :
				wCHR_StatusCode = "unknown code"
			
			###直前エラーならデコードする
			if 'errors' in wUsers :
				wCHR_StatusCode = wCHR_StatusCode + ": Error Code=" + str(wUsers['errors'][0]['code']) + ":" + str(wUsers['errors'][0]['message'])
			
			wRes['Reason'] = "Twitter responce failed: Status Code=" + str(wTweetRes.status_code) + ":" + wCHR_StatusCode
			return wRes
		
		#############################
		# TLを取得
		wRes['Responce'] = wARR_TL
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# フォロワー一覧読み込み処理
#####################################################
	def GetFollowerList(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "GetFollowerList"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/followers/list.json"
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "followers_list" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		#############################
		# パラメータの生成
		wParams = {
			"count"			: self.VAL_TwitNum,
			"cursor"		: "-1",
			"skip_status"	: "True"
		}
		
		#############################
		# タイムライン読み込み
		wARR_TL = []
		try:
			while True :
				#############################
				# APIカウント
				self.__set_APIcount( "followers_list" )
				
				wRes['RunAPI'] += 1	#実行
				wTweetRes = self.Twitter_use.get( wAPI, params=wParams )
				wUsers = json.loads( wTweetRes.text )
				
				###要素チェック
				if 'next_cursor_str' not in wUsers :
					break
				if 'users' not in wUsers :
					break
				
				###情報抜き出し
				if len(wUsers['users'])>0 :
					for wLine in wUsers['users'] :
						wARR_TL.append( wLine )
				
				#############################
				# API規制チェック
				if self.__get_APIrect( "followers_list" )!=True :
					break
				###ページング処理
				if wParams['cursor']==wUsers['next_cursor_str'] :
					break
				if wUsers['next_cursor_str']=="0" :
					break
				wParams['cursor'] = wUsers['next_cursor_str']
				
				#############################
				# 遅延
				time.sleep( self.DEF_VAL_SLEEP )
			
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wCHR_StatusCode = str(wTweetRes.status_code)
			if wCHR_StatusCode in self.STR_TWITTER_STATUS_CODE :
				###定義コードがあるなら文字出力する
				wCHR_StatusCode = self.STR_TWITTER_STATUS_CODE[wCHR_StatusCode]
			else :
				wCHR_StatusCode = "unknown code"
			
			###直前エラーならデコードする
			if 'errors' in wUsers :
				wCHR_StatusCode = wCHR_StatusCode + ": Error Code=" + str(wUsers['errors'][0]['code']) + ":" + str(wUsers['errors'][0]['message'])
			
			wRes['Reason'] = "Twitter responce failed: Status Code=" + str(wTweetRes.status_code) + ":" + wCHR_StatusCode
			return wRes
		
		#############################
		# TLを取得
		wRes['Responce'] = wARR_TL
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# 他フォロー一覧読み込み処理
#####################################################
###	def GetFollowIDList( self, inID ):
	def GetMyFollowIDList( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
###		wRes['Func'] = "GetFollowIDList"
		wRes['Func'] = "GetMyFollowIDList"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/friends/ids.json"
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "friends_ids" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		#############################
		# パラメータの生成
		wParams = {
			"user_id"		: inID,
			"count"			: self.VAL_TwitNum,
			"cursor"		: "-1"
		}
		
		#############################
		# タイムライン読み込み
		wARR_TL = []
		try:
			while True :
				#############################
				# APIカウント
				self.__set_APIcount( "friends_ids" )
				
				wRes['RunAPI'] += 1	#実行
				wTweetRes = self.Twitter_use.get( wAPI, params=wParams )
				wUsers = json.loads( wTweetRes.text )
				
				###要素チェック
				if 'next_cursor_str' not in wUsers :
					break
				if 'ids' not in wUsers :
					break
				
				###情報抜き出し
				if len(wUsers['ids'])>0 :
					for wLine in wUsers['ids'] :
						wARR_TL.append( wLine )
				
				#############################
				# API規制チェック
				if self.__get_APIrect( "friends_ids" )!=True :
					break
				###ページング処理
				if wParams['cursor']==wUsers['next_cursor_str'] :
					break
				if wUsers['next_cursor_str']=="0" :
					break
				wParams['cursor'] = wUsers['next_cursor_str']
				
				#############################
				# 遅延
				time.sleep( self.DEF_VAL_SLEEP )
			
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wCHR_StatusCode = str(wTweetRes.status_code)
			if wCHR_StatusCode in self.STR_TWITTER_STATUS_CODE :
				###定義コードがあるなら文字出力する
				wCHR_StatusCode = self.STR_TWITTER_STATUS_CODE[wCHR_StatusCode]
			else :
				wCHR_StatusCode = "unknown code"
			
			###直前エラーならデコードする
			if 'errors' in wUsers :
				wCHR_StatusCode = wCHR_StatusCode + ": Error Code=" + str(wUsers['errors'][0]['code']) + ":" + str(wUsers['errors'][0]['message'])
			
			wRes['Reason'] = "Twitter responce failed: Status Code=" + str(wTweetRes.status_code) + ":" + wCHR_StatusCode
			return wRes
		
		#############################
		# TLを取得
		wRes['Responce'] = wARR_TL
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# 他フォロワー一覧読み込み処理
#####################################################
	def GetFollowerIDList( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "GetFollowerIDList"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/followers/ids.json"
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "followers_ids" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		#############################
		# パラメータの生成
		wParams = {
			"user_id"		: inID,
			"count"			: self.VAL_TwitNum,
			"cursor"		: "-1"
		}
		
		#############################
		# タイムライン読み込み
		wARR_TL = []
		try:
			while True :
				#############################
				# APIカウント
				self.__set_APIcount( "followers_ids" )
				
				wRes['RunAPI'] += 1	#実行
				wTweetRes = self.Twitter_use.get( wAPI, params=wParams )
				wUsers = json.loads( wTweetRes.text )
				
				###要素チェック
				if 'next_cursor_str' not in wUsers :
					break
				if 'ids' not in wUsers :
					break
				
				###情報抜き出し
				if len(wUsers['ids'])>0 :
					for wLine in wUsers['ids'] :
						wARR_TL.append( wLine )
				
				#############################
				# API規制チェック
				if self.__get_APIrect( "friends_ids" )!=True :
					break
				###ページング処理
				if wParams['cursor']==wUsers['next_cursor_str'] :
					break
				if wUsers['next_cursor_str']=="0" :
					break
				wParams['cursor'] = wUsers['next_cursor_str']
				
				#############################
				# 遅延
				time.sleep( self.DEF_VAL_SLEEP )
			
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wCHR_StatusCode = str(wTweetRes.status_code)
			if wCHR_StatusCode in self.STR_TWITTER_STATUS_CODE :
				###定義コードがあるなら文字出力する
				wCHR_StatusCode = self.STR_TWITTER_STATUS_CODE[wCHR_StatusCode]
			else :
				wCHR_StatusCode = "unknown code"
			
			###直前エラーならデコードする
			if 'errors' in wUsers :
				wCHR_StatusCode = wCHR_StatusCode + ": Error Code=" + str(wUsers['errors'][0]['code']) + ":" + str(wUsers['errors'][0]['message'])
			
			wRes['Reason'] = "Twitter responce failed: Status Code=" + str(wTweetRes.status_code) + ":" + wCHR_StatusCode
			return wRes
		
		#############################
		# TLを取得
		wRes['Responce'] = wARR_TL
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# フォロー処理
#####################################################
	def CreateFollow( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "CreateFollow"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/friendships/create.json"
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "friendships" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		#############################
		# パラメータの生成
		wParams = { "id" : inID }
		
		#############################
		# 実行
		try:
			wRes['RunAPI'] += 1	#実行
			wTweetRes = self.Twitter_use.post( wAPI, params=wParams )
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 遅延
		time.sleep( self.DEF_VAL_SLEEP_LONG )
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wRes['Reason'] = "Twitter responce failed: " + str(wTweetRes.status_code)
			return wRes
		
		wRes['Result'] = True
		return wRes



#####################################################
# フォロー解除処理
#####################################################
	def RemoveFollow( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "RemoveFollow"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/friendships/destroy.json"
		
		#############################
		# パラメータの生成
		wParams = { "id" : inID }
		
		#############################
		# 実行
		try:
			wRes['RunAPI'] += 1	#実行
			wTweetRes = self.Twitter_use.post( wAPI, params=wParams )
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 遅延
		time.sleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wRes['Reason'] = "Twitter responce failed: " + str(wTweetRes.status_code)
			return wRes
		
		wRes['Result'] = True
		return wRes



#####################################################
# ブロック処理
#####################################################
	def CreateBlock( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "CreateBlock"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/blocks/create.json"
		
		#############################
		# パラメータの生成
		wParams = { "user_id" : inID }
		
		#############################
		# 実行
		try:
			wRes['RunAPI'] += 1	#実行
			wTweetRes = self.Twitter_use.post( wAPI, params=wParams )
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 遅延
		wRateTime = self.DEF_VAL_SLEEP * 2
		time.sleep( wRateTime )
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wRes['Reason'] = "Twitter responce failed: " + str(wTweetRes.status_code)
			return wRes
		
		wRes['Result'] = True
		return wRes



#####################################################
# ブロック解除処理
#####################################################
	def RemoveBlock( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "RemoveBlock"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/blocks/destroy.json"
		
		#############################
		# パラメータの生成
		wParams = { "user_id" : inID }
		
		#############################
		# 実行
		try:
			wRes['RunAPI'] += 1	#実行
			wTweetRes = self.Twitter_use.post( wAPI, params=wParams )
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 遅延
		wRateTime = self.DEF_VAL_SLEEP * 2
		time.sleep( wRateTime )
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wRes['Reason'] = "Twitter responce failed: " + str(wTweetRes.status_code)
			return wRes
		
		wRes['Result'] = True
		return wRes



#####################################################
# ミュートIDs
#####################################################
	def GetMuteIDs(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "GetMuteIDs"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/mutes/users/ids.json"
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "mute_list" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		#############################
		# パラメータの生成
		wParams = { "cursor"		: "-1"
		}
		
		#############################
		# タイムライン読み込み
		wARR_TL = []
		try:
			while True :
				#############################
				# APIカウント
				self.__set_APIcount( "mute_list" )
				
				wRes['RunAPI'] += 1	#実行
				wTweetRes = self.Twitter_use.get( wAPI, params=wParams )
				wIDs = json.loads( wTweetRes.text )
				
				###要素チェック
				if 'next_cursor_str' not in wIDs :
					break
				if 'ids' not in wIDs :
					break
				
				###情報抜き出し
				if len(wIDs['ids'])>0 :
					for wLine in wIDs['ids'] :
						wARR_TL.append( str(wLine) )
				
				#############################
				# API規制チェック
				if self.__get_APIrect( "mute_list" )!=True :
					break
				###ページング処理
				if wParams['cursor']==wIDs['next_cursor_str'] :
					break
				if wIDs['next_cursor_str']=="0" :
					break
				wParams['cursor'] = wIDs['next_cursor_str']
				
				#############################
				# 遅延
				time.sleep( self.DEF_VAL_SLEEP )
			
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wCHR_StatusCode = str(wTweetRes.status_code)
			if wCHR_StatusCode in self.STR_TWITTER_STATUS_CODE :
				###定義コードがあるなら文字出力する
				wCHR_StatusCode = self.STR_TWITTER_STATUS_CODE[wCHR_StatusCode]
			else :
				wCHR_StatusCode = "unknown code"
			
			###直前エラーならデコードする
			if 'errors' in wIDs :
				wCHR_StatusCode = wCHR_StatusCode + ": Error Code=" + str(wIDs['errors'][0]['code']) + ":" + str(wIDs['errors'][0]['message'])
			
			wRes['Reason'] = "Twitter responce failed: Status Code=" + str(wTweetRes.status_code) + ":" + wCHR_StatusCode
			return wRes
		
		#############################
		# TLを取得
		self.ARR_MuteList = wARR_TL
		wRes['Responce']  = wARR_TL
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# ミュート処理
#####################################################
	def CreateMute( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "CreateMute"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# ミュート一覧が空ならまず取得しにいく
		if len(self.ARR_MuteList)==0 :
			wResList = self.GetMuteIDs()
			if wResList['Result']!=True :
				wRes['Reason'] = "GetLists failed: " + str(wResList['Reason'])
				return wRes
		
		#############################
		# ミュート一覧にあったら終了
		if inID in self.ARR_MuteList :
			wRes['Responce'] = False
			wRes['Result']   = True
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/mutes/users/create.json"
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "muted" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		#############################
		# パラメータの生成
		wParams = { "id" : inID }
		
		#############################
		# 実行
		try:
			wRes['RunAPI'] += 1	#実行
			wTweetRes = self.Twitter_use.post( wAPI, params=wParams )
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		###ミュートしたIDを追加
		self.ARR_MuteList.append( inID )
		
		#############################
		# 遅延
		time.sleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wRes['Reason'] = "Twitter responce failed: " + str(wTweetRes.status_code)
			return wRes
		
		wRes['Responce'] = True
		wRes['Result']   = True
		return wRes



#####################################################
# ミュート解除処理
#####################################################
	def RemoveMute( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "RemoveFollow"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# ミュート一覧が空ならまず取得しにいく
		if len(self.ARR_MuteList)==0 :
			wResList = self.GetMuteIDs()
			if wResList['Result']!=True :
				wRes['Reason'] = "GetLists failed: " + str(wResList['Reason'])
				return wRes
		
		#############################
		# ミュート一覧になかったら終了
		if inID not in self.ARR_MuteList :
			wRes['Responce'] = False
			wRes['Result']   = True
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/mutes/users/destroy.json"
		
		#############################
		# パラメータの生成
		wParams = { "id" : inID }
		
		#############################
		# 実行
		try:
			wRes['RunAPI'] += 1	#実行
			wTweetRes = self.Twitter_use.post( wAPI, params=wParams )
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		###削除したIDを消す
		self.ARR_MuteList.remove( inID )
		
		#############################
		# 遅延
		time.sleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wRes['Reason'] = "Twitter responce failed: " + str(wTweetRes.status_code)
			return wRes
		
		wRes['Responce'] = True
		wRes['Result']   = True
		return wRes



#####################################################
# いいね一覧読み込み処理
#####################################################
	def GetFavolist(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "GetFavolist"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/favorites/list.json"
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "favorites_list" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		#############################
		# パラメータの生成
		wParams = {
			"count"			: self.VAL_TwitNum
		}
		
		#############################
		# タイムライン読み込み
		wNowID = -1
		wARR_TL = []
		try:
			while True :
				#############################
				# APIカウント
				self.__set_APIcount( "favorites_list" )
				
				wRes['RunAPI'] += 1	#実行
				wTweetRes = self.Twitter_use.get( wAPI, params=wParams )
				wTL = json.loads( wTweetRes.text )
				
				wFLG_Add = False
				###情報抜き出し
				if len(wTL)>0 :
					if "errors" not in wTL :
						for wLine in wTL :
							if wNowID==wLine['id'] :
								continue
							wARR_TL.append( wLine )
							wNowID   = wLine['id']
							wFLG_Add = True
				
				#############################
				# API規制チェック
				if self.__get_APIrect( "favorites_list" )!=True :
					break
				###ページング処理
				if wFLG_Add==False :
					break
				wParams['max_id'] = wNowID
				
				#############################
				# 遅延
				time.sleep( self.DEF_VAL_SLEEP )
			
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wCHR_StatusCode = str(wTweetRes.status_code)
			if wCHR_StatusCode in self.STR_TWITTER_STATUS_CODE :
				###定義コードがあるなら文字出力する
				wCHR_StatusCode = self.STR_TWITTER_STATUS_CODE[wCHR_StatusCode]
			else :
				wCHR_StatusCode = "unknown code"
			
			###直前エラーならデコードする
			if 'errors' in wTL :
				wCHR_StatusCode = wCHR_StatusCode + ": Error Code=" + str(wTL['errors'][0]['code']) + ":" + str(wTL['errors'][0]['message'])
			
			wRes['Reason'] = "Twitter responce failed: Status Code=" + str(wTweetRes.status_code) + ":" + wCHR_StatusCode
			return wRes
		
		#############################
		# TLを取得
		wRes['Responce'] = wARR_TL
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# いいね一覧読み込み処理
#####################################################
	def GetUserFavolist( self, inUserID, inPageCount=2 ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "GetUserFavolist"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/favorites/list.json"
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "favorites_list" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		#############################
		# パラメータの生成
		wParams = {
			"user_id"		: inUserID,
			"count"			: self.VAL_TwitNum
		}
		
		#############################
		# タイムライン読み込み
		wNowID = -1
		wPageCount = 0
		wARR_TL = []
		try:
			while True :
				#############################
				# APIカウント
				self.__set_APIcount( "favorites_list" )
				
				wRes['RunAPI'] += 1	#実行
				wTweetRes = self.Twitter_use.get( wAPI, params=wParams )
				wTL = json.loads( wTweetRes.text )
				
				wFLG_Add = False
				###情報抜き出し
				if len(wTL)>0 :
					if "errors" not in wTL :
						for wLine in wTL :
							if wNowID==wLine['id'] :
								continue
							wARR_TL.append( wLine )
							wNowID   = wLine['id']
							wFLG_Add = True
				
				#############################
				# API規制チェック
				if self.__get_APIrect( "favorites_list" )!=True :
					break
				###ページング処理
				if wFLG_Add==False :
					break
				###ページング数超え
				if inPageCount<=wPageCount :
					break
				wPageCount += 1
				
				wParams['max_id'] = wNowID
				
				#############################
				# 遅延
				time.sleep( self.DEF_VAL_SLEEP )
		
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wCHR_StatusCode = str(wTweetRes.status_code)
			if wCHR_StatusCode in self.STR_TWITTER_STATUS_CODE :
				###定義コードがあるなら文字出力する
				wCHR_StatusCode = self.STR_TWITTER_STATUS_CODE[wCHR_StatusCode]
			else :
				wCHR_StatusCode = "unknown code"
			
			###直前エラーならデコードする
			if 'errors' in wTL :
				wCHR_StatusCode = wCHR_StatusCode + ": Error Code=" + str(wTL['errors'][0]['code']) + ":" + str(wTL['errors'][0]['message'])
			
			wRes['Reason'] = "Twitter responce failed: Status Code=" + str(wTweetRes.status_code) + ":" + wCHR_StatusCode
			return wRes
		
		#############################
		# TLを取得
		wRes['Responce'] = wARR_TL
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# いいね処理
#####################################################
	def CreateFavo( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "CreateFavo"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/favorites/create.json"
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "favorites" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		#############################
		# パラメータの生成
		wParams = { "id" : inID }
		
		#############################
		# 実行
		try:
			wRes['RunAPI'] += 1	#実行
			wTweetRes = self.Twitter_use.post( wAPI, params=wParams )
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 遅延
		time.sleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wRes['Reason'] = "Twitter responce failed: " + str(wTweetRes.status_code)
			return wRes
		
		wRes['Result'] = True
		return wRes



#####################################################
# いいね解除処理
#####################################################
	def RemoveFavo( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "RemoveFavo"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/favorites/destroy.json"
		
		#############################
		# パラメータの生成
		wParams = { "id" : inID }
		
		#############################
		# 実行
		try:
			wRes['RunAPI'] += 1	#実行
			wTweetRes = self.Twitter_use.post( wAPI, params=wParams )
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 遅延
		time.sleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wRes['Reason'] = "Twitter responce failed: " + str(wTweetRes.status_code)
			return wRes
		
		wRes['Result'] = True
		return wRes



#####################################################
# リツイート処理
#####################################################
	def CreateRetweet( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "CreateRetweet"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/statuses/retweet.json"
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "status" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		#############################
		# パラメータの生成
		wParams = { "id" : inID }
		
		#############################
		# 実行
		try:
			wRes['RunAPI'] += 1	#実行
			wTweetRes = self.Twitter_use.post( wAPI, params=wParams )
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 遅延
		time.sleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wRes['Reason'] = "Twitter responce failed: " + str(wTweetRes.status_code)
			return wRes
		
		wRes['Result'] = True
		return wRes



#####################################################
# リスト一覧の取得
#####################################################
	def GetLists( self, inScreenName=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "GetLists"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + str(wResIni['Reason'])
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/lists/list.json"
###		wAPI = "https://api.twitter.com/1.1/lists/subscriptions.json"
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "lists_list" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		wFLG_Me = False
		#############################
		# 名前の設定
		wScreenName = inScreenName
		if wScreenName==None :
			wScreenName = self.STR_TWITTERdata['TwitterID']
			wFLG_Me = True
		elif wScreenName==self.STR_TWITTERdata['TwitterID'] :
			wFLG_Me = True
		
		#############################
		# リストがロード済なら終わる
		#   = Twittter Connect時にクリアされる
		if wScreenName in self.ARR_TwitterList :
			wRes['Responce'] = self.ARR_TwitterList[wScreenName]
			wRes['Result'] = True
			return wRes
		
		#############################
		# パラメータの生成
		wParams = {
			"screen_name" : wScreenName
		}
		
		#############################
		# APIカウント
		self.__set_APIcount( "lists_list" )
		
		#############################
		# タイムライン読み込み
		try:
			wRes['RunAPI'] += 1	#実行
			wTweetRes = self.Twitter_use.get( wAPI, params=wParams )
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 遅延
		time.sleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wRes['Reason'] = "Twitter responce failed: " + str(wTweetRes.status_code)
			return wRes
		
		#############################
		# リストを取得
		wTweetList = json.loads( wTweetRes.text )
		
		#############################
		# Twitterリストの作成
		wARR_List = {}
		wIndex = 0
		for wROW in wTweetList :
			wFLG_Me = True
			#自分のリストではない
			if wROW['user']['name']!=self.STR_TWITTERdata['TwitterID'] :
				wFLG_Me = False
			
			wCellUser = {
				"id"			: wROW['user']['id'],
				"screen_name"	: wROW['user']['screen_name']
			}
			wCell = {
				"id"		: wROW['id'],
				"name"		: wROW['name'],
				"me"		: wFLG_Me,
				"user"		: wCellUser
			}
			wARR_List.update({ wIndex : wCell })
			wIndex += 1
		
		#############################
		# グローバルに保存する
		self.ARR_TwitterList.update({ wScreenName : wARR_List })
		
		#############################
		# 一覧を返す
		wRes['Responce'] = wARR_List
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# ユーザに登録されているリスト一覧の取得
#####################################################
	def GetSubsLists( self, inScreenName=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "GetSubsLists"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + str(wResIni['Reason'])
			return wRes
		
		#############################
		# APIの指定
###		wAPI = "https://api.twitter.com/1.1/lists/ownerships.json"		#相手が作成したリスト
###		wAPI = "https://api.twitter.com/1.1/lists/subscriptions.json"	#自分が作成したリスト(相手が登録)
		wAPI = "https://api.twitter.com/1.1/lists/memberships.json"		#相手が登録されているリスト(全て)
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "lists_subs_list" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		wFLG_Me = False
		#############################
		# 名前の設定
		wScreenName = inScreenName
		if wScreenName==None :
			wScreenName = self.STR_TWITTERdata['TwitterID']
			wFLG_Me = True
		elif wScreenName==self.STR_TWITTERdata['TwitterID'] :
			wFLG_Me = True
		
		#############################
		# リストがロード済なら終わる
		#   = Twittter Connect時にクリアされる
		if wScreenName in self.ARR_TwitterSubsList :
			wRes['Responce'] = self.ARR_TwitterSubsList[wScreenName]
			wRes['Result'] = True
			return wRes
		
		#############################
		# パラメータの生成
		wParams = {
			"screen_name" : wScreenName
		}
		
		#############################
		# APIカウント
		self.__set_APIcount( "lists_subs_list" )
		
		#############################
		# タイムライン読み込み
		try:
			wRes['RunAPI'] += 1	#実行
			wTweetRes = self.Twitter_use.get( wAPI, params=wParams )
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 遅延
		time.sleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wRes['Reason'] = "Twitter responce failed: " + str(wTweetRes.status_code)
			return wRes
		
		#############################
		# リストを取得
		wTweetList = json.loads( wTweetRes.text )
		
		#############################
		# Twitterリストの作成
		wARR_List = {}
		wIndex = 0
		for wROW in wTweetList['lists'] :
			wFLG_Me = True
			#自分のリストではない
			if wROW['user']['name']!=self.STR_TWITTERdata['TwitterID'] :
				wFLG_Me = False
			
			wCellUser = {
				"id"			: wROW['user']['id'],
				"screen_name"	: wROW['user']['screen_name']
			}
			wCell = {
				"id"		: wROW['id'],
				"name"		: wROW['name'],
				"me"		: wFLG_Me,
				"user"		: wCellUser
			}
			wARR_List.update({ wIndex : wCell })
			wIndex += 1
		
### sample
###xxx: next_cursor
###xxx: next_cursor_str
###xxx: previous_cursor
###xxx: previous_cursor_str
###xxx: lists
		
		#############################
		# グローバルに保存する
		self.ARR_TwitterSubsList.update({ wScreenName : wARR_List })
		
		#############################
		# 一覧を返す
		wRes['Responce'] = wARR_List
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# リスト登録者一覧の取得
#####################################################
	def GetListMember( self, inListName, inScreenName=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "GetListMember"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + str(wResIni['Reason'])
			return wRes
		
		#############################
		# リスト一覧の取得
		wResList = self.GetLists( inScreenName=inScreenName )
		if wResList['Result']!=True :
			wRes['Reason'] = "GetLists failed: " + str(wResList['Reason'])
			return wRes
		
		#############################
		# リスト名のIDを取得
		wListID = -1
		wARR_Lists = wResList['Responce']
		wKeylist = list( wARR_Lists.keys() )
		for wKey in wKeylist :
			if wARR_Lists[wKey]['name']==inListName :
				###リスト発見 =idを取得する
				wListID = wARR_Lists[wKey]['id']
				break
		
		if wListID==-1 :
			wRes['Reason'] = "List is not found: " + inListName + " owner=" + inScreenName
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/lists/members.json"
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "lists_members" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内): countt=" + str(self.TwStatus['APIrect']['lists_members']['num'])
			return wRes
		
		#############################
		# パラメータの生成
		wParams = { "list_id"		: wListID,
					"count"			: self.VAL_TwitListNum,
					"cursor"		: "-1",
					"skip_status"	: "True"
		}
###		wParams = { "slug"				: inListName,
###					"owner_screen_name"	: wListOwner,
###					"count"			: self.VAL_TwitListNum,
###					"cursor"		: "-1",
###					"skip_status"	: "True"
###		}
###		※slugを使うとTwitterからエラーが返されるので使えない
		
		#############################
		# タイムライン読み込み
		wARR_TL = []
		try:
			while True :
				#############################
				# APIカウント
				self.__set_APIcount( "lists_members" )
				
				wRes['RunAPI'] += 1	#実行
				wTweetRes = self.Twitter_use.get( wAPI, params=wParams )
				wUsers = json.loads( wTweetRes.text )
				
				###要素チェック
				if 'next_cursor_str' not in wUsers :
					break
				if 'users' not in wUsers :
					break
				
				###情報抜き出し
				if len(wUsers['users'])>0 :
					for wLine in wUsers['users'] :
						wARR_TL.append( wLine )
				
				#############################
				# API規制チェック
				if self.__get_APIrect( "lists_members" )!=True :
					break
				###ページング処理
				if wParams['cursor']==wUsers['next_cursor_str'] :
					break
				if wUsers['next_cursor_str']=="0" :
					break
				wParams['cursor'] = wUsers['next_cursor_str']
				
				#############################
				# 遅延
				time.sleep( self.DEF_VAL_SLEEP )
			
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wCHR_StatusCode = str(wTweetRes.status_code)
			if wCHR_StatusCode in self.STR_TWITTER_STATUS_CODE :
				###定義コードがあるなら文字出力する
				wCHR_StatusCode = self.STR_TWITTER_STATUS_CODE[wCHR_StatusCode]
			else :
				wCHR_StatusCode = "unknown code"
			
			###直前エラーならデコードする
			if 'errors' in wUsers :
				wCHR_StatusCode = wCHR_StatusCode + ": Error Code=" + str(wUsers['errors'][0]['code']) + ":" + str(wUsers['errors'][0]['message'])
			
			wStr = "Twitter responce failed: Status Code=" + str(wTweetRes.status_code) + ":" + wCHR_StatusCode
###			wStr = wStr + " list_name=" + str(inListName) + " owner=" + wListOwner
			wStr = wStr + " list_name=" + str(inListName) + " owner=" + inScreenName
			wRes['Reason'] = wStr
			return wRes
		
		#############################
		# TLを取得
		wRes['Responce'] = wARR_TL
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# リスト登録 登録者一覧の取得
#####################################################
	def GetListSubscribers( self, inListName, inScreenName=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "GetListSubscribers"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + str(wResIni['Reason'])
			return wRes
		
		#############################
		# リスト一覧の取得
		wResList = self.GetLists( inScreenName=inScreenName )
		if wResList['Result']!=True :
			wRes['Reason'] = "GetLists failed: " + str(wResList['Reason'])
			return wRes
		
		#############################
		# リスト名のIDを取得
		wListID = -1
		wARR_Lists = wResList['Responce']
		wKeylist = list( wARR_Lists.keys() )
		for wKey in wKeylist :
			if wARR_Lists[wKey]['name']==inListName :
				###リスト発見 =idを取得する
				wListID = wARR_Lists[wKey]['id']
				break
		
		if wListID==-1 :
			wRes['Reason'] = "List is not found: " + inListName + " owner=" + inScreenName
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/lists/subscribers.json"
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "lists_subscribers" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		#############################
		# パラメータの生成
		wParams = { "list_id"		: wListID,
					"count"			: self.VAL_TwitListNum,
					"cursor"		: "-1",
					"skip_status"	: "True"
		}
###		wParams = { "slug"				: inListName,
###					"owner_screen_name"	: wListOwner,
###					"count"			: self.VAL_TwitListNum,
###					"cursor"		: "-1",
###					"skip_status"	: "True"
###		}
###		※slugを使うとTwitterからエラーが返されるので使えない
		
		#############################
		# タイムライン読み込み
		wARR_TL = []
		try:
			while True :
				#############################
				# APIカウント
				self.__set_APIcount( "lists_subscribers" )
				
				wRes['RunAPI'] += 1	#実行
				wTweetRes = self.Twitter_use.get( wAPI, params=wParams )
				wUsers = json.loads( wTweetRes.text )
				
				###要素チェック
				if 'next_cursor_str' not in wUsers :
					break
				if 'users' not in wUsers :
					break
				
				###情報抜き出し
				if len(wUsers['users'])>0 :
					for wLine in wUsers['users'] :
						wARR_TL.append( wLine )
				
				#############################
				# API規制チェック
				if self.__get_APIrect( "lists_subscribers" )!=True :
					break
				###ページング処理
				if wParams['cursor']==wUsers['next_cursor_str'] :
					break
				if wUsers['next_cursor_str']=="0" :
					break
				wParams['cursor'] = wUsers['next_cursor_str']
				
				#############################
				# 遅延
				time.sleep( self.DEF_VAL_SLEEP )
			
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wCHR_StatusCode = str(wTweetRes.status_code)
			if wCHR_StatusCode in self.STR_TWITTER_STATUS_CODE :
				###定義コードがあるなら文字出力する
				wCHR_StatusCode = self.STR_TWITTER_STATUS_CODE[wCHR_StatusCode]
			else :
				wCHR_StatusCode = "unknown code"
			
			###直前エラーならデコードする
			if 'errors' in wUsers :
				wCHR_StatusCode = wCHR_StatusCode + ": Error Code=" + str(wUsers['errors'][0]['code']) + ":" + str(wUsers['errors'][0]['message'])
			
			wStr = "Twitter responce failed: Status Code=" + str(wTweetRes.status_code) + ":" + wCHR_StatusCode
###			wStr = wStr + " list_name=" + str(inListName) + " owner=" + wListOwner
			wStr = wStr + " list_name=" + str(inListName) + " owner=" + str(inScreenName)
			wRes['Reason'] = wStr
			return wRes
		
		#############################
		# TLを取得
		wRes['Responce'] = wARR_TL
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# リストへ追加処理
#####################################################
	def AddUserList( self, inListName, inUserID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "AddUserList"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# 自分のリスト一覧がなければまず取得しにいく
		wMyScreenName = self.STR_TWITTERdata['TwitterID']
		if wMyScreenName not in self.ARR_TwitterList :
			wResList = self.GetLists()
			if wResList['Result']!=True :
				wRes['Reason'] = "GetLists failed: " + str(wResList['Reason'])
				return wRes
		
		#############################
		# リスト名のIDを取得
		wListID = -1
		wKeylist = self.ARR_TwitterList[wMyScreenName].keys()
		for wKey in wKeylist :
			if self.ARR_TwitterList[wMyScreenName][wKey]['name']==inListName :
				###リスト発見 =idを取得する
				wListID = self.ARR_TwitterList[wMyScreenName][wKey]['id']
				break
		
		if wListID==-1 :
			wRes['Reason'] = "List is not found: " + inListName
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/lists/members/create.json"
		
		#############################
		# パラメータの生成
		wParams = { "list_id" : wListID,
					"user_id" : inUserID
		}
		
		#############################
		# 実行
		try:
			wRes['RunAPI'] += 1	#実行
			wTweetRes = self.Twitter_use.post( wAPI, params=wParams )
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 遅延
		time.sleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wRes['Reason'] = "Twitter responce failed: " + str(wTweetRes.status_code)
			return wRes
		
		wRes['Result'] = True
		return wRes



#####################################################
# リストから削除処理
#####################################################
	def RemoveUserList( self, inListName, inUserID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "RemoveUserList"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# 自分のリスト一覧がなければまず取得しにいく
		wMyScreenName = self.STR_TWITTERdata['TwitterID']
		if wMyScreenName not in self.ARR_TwitterList :
			wResList = self.GetLists()
			if wResList['Result']!=True :
				wRes['Reason'] = "GetLists failed: " + str(wResList['Reason'])
				return wRes
		
		#############################
		# リスト名のIDを取得
		wListID = -1
		wKeylist = self.ARR_TwitterList[wMyScreenName].keys()
		for wKey in wKeylist :
			if self.ARR_TwitterList[wMyScreenName][wKey]['name']==inListName :
				###リスト発見 =idを取得する
				wListID = self.ARR_TwitterList[wMyScreenName][wKey]['id']
				break
		
		if wListID==-1 :
			wRes['Reason'] = "List is not found: " + inListName
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/lists/members/destroy.json"
		
		#############################
		# パラメータの生成
		wParams = { "list_id" : wListID,
					"user_id" : inUserID
		}
		
		#############################
		# 実行
		try:
			wRes['RunAPI'] += 1	#実行
			wTweetRes = self.Twitter_use.post( wAPI, params=wParams )
		except ValueError as err :
			wRes['Reason'] = "Twitter error: " + str( err )
			return wRes
		
		#############################
		# 遅延
		time.sleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wRes['Reason'] = "Twitter responce failed: " + str(wTweetRes.status_code)
			return wRes
		
		wRes['Result'] = True
		return wRes



#####################################################
# トレンド読み込み処理
#####################################################
	def GetTrends(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = self.__Get_Resp()
		wRes['Func'] = "GetTrends"
		
		#############################
		# Twitter状態のチェック
		wResIni = self.GetTwStatus()
		if wResIni['Init']!=True :
			wRes['Reason'] = "Twitter connect error: " + wResIni['Reason']
			return wRes
		
		#############################
		# APIの指定
		wAPI = "https://api.twitter.com/1.1/trends/place.json"
		
		#############################
		# API規制チェック
		if self.__get_APIrect( "trends_place" )!=True :
			wRes['Reason'] = "Twitter規制中(アプリ内)"
			return wRes
		
		#############################
		# パラメータの生成
		wParams = {
			"id" : self.DEF_WOEID
		}
		
		#############################
		# APIカウント
		self.__set_APIcount( "trends_place" )
		
		#############################
		# タイムライン読み込み
		try:
			wRes['RunAPI'] += 1	#実行
			wTweetRes = self.Twitter_use.get( wAPI, params=wParams )
		except ValueError as err :
			wRes['Reason'] = "GetTL: Twitter error: " + str( err )
			return wRes
		
		#############################
		# 遅延
		time.sleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 結果
		wRes['StatusCode'] = wTweetRes.status_code
		if wTweetRes.status_code != 200 :
			wRes['Reason'] = "Twitter responce failed: " + str(wTweetRes.status_code)
			return wRes
		
		#############################
		# TLを取得
		wRes['Responce'] = json.loads( wTweetRes.text )
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



