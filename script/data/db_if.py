#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : Database I/F
#####################################################
from postgresql_use import CLS_PostgreSQL_Use

from traffic import CLS_Traffic
from ktime import CLS_TIME
from osif import CLS_OSIF
from gval import gVal
#####################################################
class CLS_DB_IF() :
#####################################################
	OBJ_DB = ""				#DBオブジェクト
	
	ARR_FollowerDataID = []		#  フォロワー情報ID



#####################################################
# Init
#####################################################
	def __init__(self):
		return



#####################################################
# DB接続
#####################################################
	def Connect( self, inData ):
		#############################
		# inData構造
		#   = {
		#		"hostname"	:	"",
		#		"database"	:	"",
		#		"username"	:	"",
		#		"password"	:	""
		#	}
		
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "Connect"
		
		
		wRes['Responce'] = False
		#############################
		# Postgreオブジェクトの作成
		self.OBJ_DB = CLS_PostgreSQL_Use()
		
		#############################
		# テスト
		wResDBconn = self.OBJ_DB.Create( inData )
		wResDB = self.OBJ_DB.GetDbStatus()
		if wResDBconn!=True :
			wRes['Reason'] = "CLS_DB_IF: Connect: DBの接続に失敗しました: reason=" + wResDB['Reason']
			CLS_OSIF.sErr( wRes )
			
			self.__connectFailView()
			return wRes
		
		#############################
		# 結果の確認
		if wResDB['Init']!=True :
			wRes['Reason'] = "CLS_DB_IF: Connect: DBが初期化できてません"
			CLS_OSIF.sErr( wRes )
			
			self.__connectFailView()
			return wRes
		
		#############################
		# 接続は正常
		CLS_OSIF.sPrn( "データベースへ正常に接続しました。" + '\n' )
		wRes['Result'] = True
		
		#############################
		# DBの状態チェック
		wSubRes = self.CheckDB()
		if wSubRes['Result']!=True :
			return False
		if wSubRes['Responce']!=True :
			##テーブルがない= 初期化してない
			CLS_OSIF.sPrn( "CLS_DB_IF: Connect: テーブルが構築されていません" + '\n' )
			
			self.__connectFailView(inData)
			return wRes
		
		###全て正常
		wRes['Responce'] = True
		return wRes

	def __connectFailView( self, inData ):
		if gVal.FLG_Test_Mode==False :
			return	#テストモードでなければ終わる
		
		#############################
		# DB接続情報を表示
		wStr =        "******************************" + '\n'
		wStr = wStr + "HOST    : " + inData['hostname'] + '\n'
		wStr = wStr + "DB NAME : " + inData['database'] + '\n'
		wStr = wStr + "DB USER : " + inData['username'] + '\n'
		wStr = wStr + "DB PASS : (ナイチョ) " + '\n'
		wStr = wStr + "******************************" + '\n'
		CLS_OSIF.sPrn( wStr )
		return



#####################################################
# DB切断
#####################################################
	def Close(self):
		self.OBJ_DB.Close()
		return True



#####################################################
# クエリ実行
#####################################################
	def RunQuery( self, inQuery=None, inTraffic=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "RunQuery"
		
		#############################
		# 実行
		wResDB = self.OBJ_DB.RunQuery( inQuery )
		
		#############################
		# 実行結果の取得
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed: RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# ログ記録とトラヒックの計測
		if inTraffic==True :
			CLS_Traffic.sP( "db_req" )
			
			if wResDB['Command']=="insert" or wResDB['Command']=="create" :
				wQy = inQuery.split(" ")
				wQy = wQy[2]
				gVal.OBJ_L.Log( "P", wRes, "insert: " + wQy )
				CLS_Traffic.sP( "db_ins" )
			
			elif wResDB['Command']=="update" :
				wQy = inQuery.split(" ")
				wQy = wQy[1]
				gVal.OBJ_L.Log( "P", wRes, "update: " + wQy )
				CLS_Traffic.sP( "db_up" )
			
			elif wResDB['Command']=="delete" or wResDB['Command']=="drop" :
				wQy = inQuery.split(" ")
				wQy = wQy[2]
				gVal.OBJ_L.Log( "P", wRes, "update: " + wQy )
				CLS_Traffic.sP( "db_del" )
			
		
		#############################
		# 正常
		wRes['Responce'] = wResDB['Responce']
		wRes['Result'] = True
		return wRes

	#####################################################
	# 辞書型に整形
	def ChgDict( self, inData ):
		wARR_DBData = {}
		self.OBJ_DB.ChgDict( inData['Collum'], inData['Data'], outDict=wARR_DBData )
		return wARR_DBData

	#####################################################
	# リスト型に整形
	def ChgList( self, inData ):
		wARR_DBData = []
		self.OBJ_DB.ChgList( inData['Data'], outList=wARR_DBData )
		return wARR_DBData

	#####################################################
	# 添え字をIDに差し替える
	def ChgDataID( self, inData ):
		wKeylist = inData.keys()
		
		wARR_RateData = {}
		for wIndex in wKeylist :
			wID = str( inData[wIndex]['id'] )
			wARR_RateData.update({ wID : inData[wIndex] })
		
		return wARR_RateData



#####################################################
# レコード数取得
#####################################################
	def GetRecordNum( self, inTableName=None, inTraffic=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetRecordNum"
		
		#############################
		# 入力チェック
		if inTableName==None or inTableName=="" :
			##失敗
			wRes['Reason'] = "inTableName is invalid: " + str(inTableName)
			gVal.OBJ_L.Log( "A", wRes )
			return wRes
		
		#############################
		# クエリの作成
		wQy = "select count(*) from " + inTableName + ";"
		
		#############################
		# 実行
		wResDB = self.OBJ_DB.RunQuery( wQy )
		
		#############################
		# 実行結果の取得
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed: RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# レコード数の取り出し
		try:
			wNum = int( wResDB['Responce']['Data'][0][0] )
		except ValueError:
			##失敗
			wRes['Reason'] = "Data is failer"
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# 正常
		wRes['Responce'] = wNum
		wRes['Result'] = True
		return wRes



#####################################################
# チェックデータベース
#####################################################
	def CheckDB( self, inTraffic=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "CheckDB"
		
		#############################
		# DBの状態チェック
		wResDB = self.OBJ_DB.RunTblExist( "tbl_user_data" )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##クエリ失敗
			wRes['Reason'] = "DBの状態チェック失敗: RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# トラヒックの計測
		if inTraffic==True :
			CLS_Traffic.sP( "db_req" )
		
		wRes['Responce'] = wResDB['Responce']
		wRes['Result'] = True
		return wRes



#####################################################
# チェックユーザデータ
#####################################################
	def CheckUserData(self ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "CheckUserData"
		
		wRes['Responce'] = {
			"Account"	: None,
			"detect"	: False
		}
		
		#############################
		# TwitterIDの入力
		wStr = "botで使うユーザ登録をおこないます。" + '\n'
		wStr = wStr + "ここではTwitter IDと、Twitter Devで取得したキーを登録していきます。" + '\n'
		wStr = wStr + "Twitter IDを入力してください。"
		CLS_OSIF.sPrn( wStr )
		wTwitterAccount = CLS_OSIF.sInp( "Twitter ID？=> " )
		
		wRes['Responce']['Account'] = str( wTwitterAccount )
		#############################
		# ユーザ登録の確認 and 抽出
		wQy = "select * from tbl_user_data where "
		wQy = wQy + "twitterid = '" + wTwitterAccount + "'"
		wQy = wQy + ";"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			CLS_OSIF.sErr( wRes )
			return wRes
		
		##登録あり
		if len(wResDB['Responce']['Data'])==1 :
			wRes['Responce']['detect'] = True
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes



#####################################################
# ユーザデータ設定
#####################################################
	def SetUserData( self, inUserData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetUserData"
		
		#############################
		# 時間を取得
		wTD = CLS_TIME.sGet( wRes, "(1)" )
		
		#############################
		# テーブルチェック
		wQy = "select * from tbl_user_data where "
		wQy = wQy + "twitterid = '" + inUserData['Account'] + "'"
		wQy = wQy + ";"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# 登録してなければデータベースに登録する
		if len(wResDB['Responce']['Data'])==0 :
			wQy = "insert into tbl_user_data values ("
			wQy = wQy + "'" + inUserData['Account'] + "',"		# 記録したユーザ(Twitter ID)
			wQy = wQy + "'" + str( wTD['TimeDate'] ) + "',"		# 登録日時
			wQy = wQy + "False,"								# 排他ロック true=ロックON
			wQy = wQy + "'" + str( gVal.DEF_TIMEDATE ) + "',"	# 排他日時
			wQy = wQy + "'" + str( gVal.DEF_TIMEDATE ) + "',"	# 排他獲得日時
			wQy = wQy + "'" + str( gVal.DEF_TIMEDATE ) + "',"	# 排他解除日時
			wQy = wQy + "'" + gVal.DEF_NOTEXT + "', "			# トレンド送信タグ
			wQy = wQy + "'" + gVal.DEF_NOTEXT + "', "			# リスト通知 リストID(数値)
			wQy = wQy + "'" + gVal.DEF_NOTEXT + "', "			# リスト通知 リスト名
			wQy = wQy + "False,"								# 自動リムーブ true=ON
			wQy = wQy + "'" + gVal.DEF_NOTEXT + "', "			# 相互フォローリスト リストID(数値)
			wQy = wQy + "'" + gVal.DEF_NOTEXT + "', "			# 相互フォローリスト リスト名
			wQy = wQy + "'" + gVal.DEF_NOTEXT + "', "			# 片フォロワーリスト リストID(数値)
			wQy = wQy + "'" + gVal.DEF_NOTEXT + "', "			# 片フォロワーリスト リスト名
			wQy = wQy + "'" + gVal.DEF_NOTEXT + "', "			# VIPリツイート タグ
			wQy = wQy + "0,  " 									# 自動監視シーケンス
			wQy = wQy + "False,"								# 相互いいね停止 true=有効
			wQy = wQy + "'" + str( gVal.DEF_TIMEDATE ) + "',"	# 相互いいね停止 開始日
			wQy = wQy + "'" + gVal.DEF_NOTEXT + "', "			# 質問タグ
			wQy = wQy + "'" + gVal.DEF_NOTEXT + "' "			# 削除タグ
			wQy = wQy + ") ;"
			
			wResDB = self.OBJ_DB.RunQuery( wQy )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				gVal.OBJ_L.Log( "C", wRes )
				return wRes
			
			wQy = "insert into tbl_twitter_data values ("
			wQy = wQy + "'" + inUserData['Account'] + "',"
			wQy = wQy + "'" + inUserData['APIkey'] + "',"
			wQy = wQy + "'" + inUserData['APIsecret'] + "',"
			wQy = wQy + "'" + inUserData['ACCtoken'] + "',"
			wQy = wQy + "'" + inUserData['ACCsecret'] + "',"
			wQy = wQy + "'" + inUserData['Bearer'] + "' "
			wQy = wQy + ") ;"
			
			wResDB = self.OBJ_DB.RunQuery( wQy )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				gVal.OBJ_L.Log( "C", wRes )
				return wRes
			
			wResDB = self.InsertTimeInfo( inUserData['Account'] )
			if wResDB['Result']!=True :
				wRes['Reason'] = "InsertTimeInfo is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# 登録されていればキーを更新する
		elif len(wResDB['Responce']['Data'])==1 :
			wQy = "update tbl_twitter_data set "
			wQy = wQy + "apikey = '"    + inUserData['APIkey'] + "', "
			wQy = wQy + "apisecret = '" + inUserData['APIsecret'] + "', "
			wQy = wQy + "acctoken = '"  + inUserData['ACCtoken'] + "', "
			wQy = wQy + "accsecret = '" + inUserData['ACCsecret'] + "', "
			wQy = wQy + "bearer = '" + inUserData['Bearer'] + "'  "
			wQy = wQy + "where twitterid = '" + inUserData['Account'] + "' ;"
			
			wResDB = self.OBJ_DB.RunQuery( wQy )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(5): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				gVal.OBJ_L.Log( "C", wRes )
				return wRes
			
			wQy = "update tbl_user_data set "
			wQy = wQy + "locked = False, "
			wQy = wQy + "lok_date = '" + str(wTD['TimeDate']) + "' "
			wQy = wQy + "where twitterid = '" + inUserData['Account'] + "' ;"
			
			wResDB = self.OBJ_DB.RunQuery( wQy )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(6): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				gVal.OBJ_L.Log( "C", wRes )
				return wRes
		
		else:
			###ありえない
			wRes['Reason'] = "dual registed user: user=" + str(inUserData['Account'])
			gVal.OBJ_L.Log( "D", wRes )
			self.OBJ_DB.Close()
			return wRes
		
		#############################
		# ユーザ名の登録
		gVal.STR_UserInfo['Account'] = str(inUserData['Account'])
		
		#############################
		# ログに記録する
		gVal.OBJ_L.Log( "SC", wRes, "データ更新: user data: user=" + gVal.STR_UserInfo['Account'] )
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes



#####################################################
# Twitterデータ取得
#####################################################
	def GetTwitterData( self, inAccount ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetTwitterData"
		
		wRes['Responce'] = {
			"Account"	: None,
			"apikey"	: None,
			"apisecret"	: None,
			"acctoken"	: None,
			"accsecret"	: None,
			"bearer"	: None
		}
		
		#############################
		# データベースから除外文字を取得
		wQy = "select * from tbl_twitter_data "
		wQy = wQy + "where twitterid = '" + str(inAccount) + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# 取得チェック
		if len( wARR_DBData )!= 1 :
			##失敗
			wRes['Reason'] = "Get twitter data is not one: account=" + str(inAccount) + " num=" + str( len( wARR_DBData ) )
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# Twitterデータ取得
		wRes['Responce']['apikey']    = wARR_DBData[0]['apikey']
		wRes['Responce']['apisecret'] = wARR_DBData[0]['apisecret']
		wRes['Responce']['acctoken']  = wARR_DBData[0]['acctoken']
		wRes['Responce']['accsecret'] = wARR_DBData[0]['accsecret']
		wRes['Responce']['bearer']    = wARR_DBData[0]['bearer']
		
		wRes['Responce']['Account'] = str(inAccount)
		#############################
		# =正常
		wRes['Result'] = True
		return wRes



#####################################################
# 排他ロック取得
#####################################################
	def GetLock( self, inAccount ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetLock"
		
		wRes['Responce'] = {
			"Account"	: None,
			"locked"	: None,
			"lok_date"	: None,
			"get_date"	: None,
			"rel_date"	: None
		}
		
		#############################
		# データ取得
		wQy = "select locked, lok_date, get_date, rel_date from tbl_user_data "
		wQy = wQy + "where twitterid = '" + str(inAccount) + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# 取得チェック
		if len( wARR_DBData )!= 1 :
			##失敗
			wRes['Reason'] = "Get twitter data is not one: account=" + str(inAccount) + " num=" + str( len( wARR_DBData ) )
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# Twitterデータ取得
		wRes['Responce']['locked']    = wARR_DBData[0]['locked']
		wRes['Responce']['lok_date']  = wARR_DBData[0]['lok_date']
		wRes['Responce']['get_date']  = wARR_DBData[0]['get_date']
		wRes['Responce']['rel_date']  = wARR_DBData[0]['rel_date']
		
		wRes['Responce']['Account'] = str(inAccount)
		#############################
		# =正常
		wRes['Result'] = True
		return wRes



#####################################################
# 排他ロック設定
#####################################################
	def SetLock( self, inAccount, inLock, inDate ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetLock"
		
		wRes['Responce'] = 0
		#############################
		# データ取得
		wQy = "select locked, lok_date, get_date, rel_date from tbl_user_data "
		wQy = wQy + "where twitterid = '" + str(inAccount) + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# 取得チェック
		if len( wARR_DBData )!= 1 :
			##失敗
			wRes['Reason'] = "Get twitter data is not one: account=" + str(inAccount) + " num=" + str( len( wARR_DBData ) )
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# 変更する
		wQy = "update tbl_user_data set "
		if inLock==True :
			if wARR_DBData[0]['locked']==False :
				wQy = wQy + "lok_date = '" + str( inDate ) + "', "
				wQy = wQy + "get_date = '" + str( inDate ) + "', "
			else:
				wQy = wQy + "get_date = '" + str( inDate ) + "', "
		else:
			wQy = wQy + "rel_date = '" + str( inDate ) + "', "
		
		wQy = wQy + "locked = " + str( inLock ) + " "
		wQy = wQy + "where twitterid = '" + str(inAccount) + "' ;"
		wQy = wQy + ";"
		
		#############################
		# クエリの実行
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# ログに記録する
		if inLock==True :
			if wARR_DBData[0]['locked']==False :
				gVal.OBJ_L.Log( "SR", wRes, "排他: locked=True user=" + str(inAccount) )
			else:
				gVal.OBJ_L.Log( "SR", wRes, "排他(延長): locked=True user=" + str(inAccount) )
		
		#############################
		# 排他解除の場合
		#   獲得時間も返す
		else:
			wRunRes = CLS_OSIF.sTimeLagSec( inTimedate1=inDate, inTimedate2=wARR_DBData[0]['lok_date'] )
			if wRunRes['Result']!=True :
				##失敗
				wRes['Reason'] = "sTimeLagSec is error: " + str(wRunRes['Reason'])
				gVal.OBJ_L.Log( "A", wRes )
				return wRes
			
			CLS_Traffic.sP( "run_time", wRunRes['RateSec'] )
			
			wStr = "排他解除: locked=False user=" + str(inAccount)
			wStr = wStr + " runtime=" + str(wRunRes['RateSec']) + " daytime=" + str(gVal.STR_TrafficInfo['run_time'][0])
			
			gVal.OBJ_L.Log( "SR", wRes, wStr )
			
			wRes['Responce'] = wRunRes['RateSec']
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes



#####################################################
# 時間情報
#####################################################
	def GetTimeInfo( self, inAccount ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetTimeInfo"
		
		#############################
		# データ取得
		wQy = "select * from tbl_time_data "
		wQy = wQy + "where twitterid = '" + str(inAccount) + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# 取得チェック
		if len( wARR_DBData )!= 1 :
			##失敗
			wRes['Reason'] = "Get twitter data is not one: account=" + str(inAccount) + " num=" + str( len( wARR_DBData ) )
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# グローバルにロード
		wKeylist = list( wARR_DBData[0].keys() )
		for wKey in wARR_DBData[0] :
			if wKey=="twitterid" :
				continue
			
			if wKey not in gVal.STR_Time :
				wRes['Reason'] = "not col data: account=" + str(inAccount) + " key=" + str( wKey )
				gVal.OBJ_L.Log( "A", wRes )
				return wRes
			
			gVal.STR_Time[wKey] = wARR_DBData[0][wKey]
		
		#############################
		# 全部ロードしたかチェック
		wKeylist = list( gVal.STR_Time.keys() )
		for wKey in gVal.STR_Time :
			if wKey=="TimeDate" :
				continue
			
			if gVal.STR_Time[wKey]==None :
				wRes['Reason'] = "unload data: account=" + str(inAccount) + " key=" + str( wKey )
				gVal.OBJ_L.Log( "A", wRes )
				return wRes
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def AutoInsert_TimeInfo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "AutoInsert_TimeInfo"
		
		#############################
		# データ取得(twitteridのみ)
		wQy = "select twitterid from tbl_user_data "
		wQy = wQy + " ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# リスト型に整形
		wARR_Account = gVal.OBJ_DB_IF.ChgList( wResDB['Responce'] )
		
		#############################
		# いちお全レコードをdeleteしておく
		wQy = "delete from tbl_time_data "
		wQy = wQy + " ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# ユーザデータ分の枠を作成する
		for wAccount in wARR_Account :
			wAccount = str(wAccount)
			
			wSubRes = self.InsertTimeInfo( wAccount )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "InsertTimeInfo is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			### ログ用の措置
			gVal.STR_UserInfo['Account'] = wAccount
			
			wStr = "Insert new TimeInfo : user=" + str( wAccount )
			gVal.OBJ_L.Log( "SC", wRes, wStr )
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def InsertTimeInfo( self, inAccount ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "InsertTimeInfo"
		
		wQy = "insert into tbl_time_data values ("
		wQy = wQy + "'" + str(inAccount) + "',"				# 記録したユーザ(Twitter ID)
		
		wKeylist = list( gVal.STR_Time.keys() )
		for wKey in gVal.STR_Time :
			if wKey=="TimeDate" or wKey=="run" :
				continue
			
			wQy = wQy + "'" + str( gVal.DEF_TIMEDATE ) + "', "
		
		wQy = wQy + "'" + str( gVal.DEF_TIMEDATE ) + "' "	# run分の枠
		wQy = wQy + ") ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def SetTimeInfo( self, inAccount, inTag, inDate ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetTimeInfo"
		
		#############################
		# 入力チェック
		if inTag not in gVal.STR_Time :
			wRes['Reason'] = "not col data: account=" + str(inAccount) + " tag=" + str( inTag )
			gVal.OBJ_L.Log( "A", wRes )
			return wRes
		
		#############################
		# データ取得
		wQy = "select " + inTag + " from tbl_time_data "
		wQy = wQy + "where twitterid = '" + str(inAccount) + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# 取得チェック
		if len( wARR_DBData )!= 1 :
			##失敗
			wRes['Reason'] = "Get twitter data is not one: account=" + str(inAccount) + " num=" + str( len( wARR_DBData ) )
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# 変更する
		wQy = "update tbl_time_data set "
		wQy = wQy + str(inTag) + " = '" + str( inDate ) + "' "
		wQy = wQy + "where twitterid = '" + str(inAccount) + "' ;"
		
		#############################
		# クエリの実行
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# グローバルにセット
		gVal.STR_Time[inTag] = inDate
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def ResetTimeInfo( self, inAccount ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "ResetTimeInfo"
		
		wKeylist = list( gVal.STR_Time.keys() )
		for wKey in wKeylist :
			if wKey=="TimeDate" :
				### システム時間は、スキップ
				continue
			
			#############################
			# 時間リセット
			wQy = "update tbl_time_data set "
			wQy = wQy + wKey + " = '" + str( gVal.DEF_TIMEDATE ) + "' "
			wQy = wQy + "where twitterid = '" + str(inAccount) + "' ;"
			
			#############################
			# クエリの実行
			wResDB = self.OBJ_DB.RunQuery( wQy )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				gVal.OBJ_L.Log( "C", wRes )
				return wRes
			
			#############################
			# グローバルもリセット
			gVal.STR_Time[wKey] = str( gVal.DEF_TIMEDATE )
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes



#####################################################
# 除外文字
#####################################################
	def GetExeWord(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetExeWord"
		
		#############################
		# データベースから除外文字を取得
		wQy = "select * from tbl_exc_word "
		wQy = wQy + ";"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return False
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		wARR_ExeWord = {}
		#############################
		# 除外文字データを登録する
		wKeylist = list( wARR_DBData.keys() )
		for wIndex in wKeylist :
			wKey = wARR_DBData[wIndex]['word']
			wCell = {
				"word"		: wKey,
				"report"	: wARR_DBData[wIndex]['report']
			}
			wARR_ExeWord.update({ wKey : wCell })
		
		gVal.ARR_ExeWord = wARR_ExeWord
		gVal.ARR_ExeWordKeys = list( wARR_ExeWord.keys() )
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def SetExeWord( self, inARRData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetExeWord"
		
		#############################
		# 時間を取得
		wTD = CLS_TIME.sGet( wRes, "(2)" )
		
		#############################
		# データベースから除外文字を取得
		wQy = "select word from tbl_exc_word "
		wQy = wQy + ";"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return False
		
		### リスト型に整形
		wARR_RateWord = []
		self.OBJ_DB.ChgList( wResDB['Responce']['Data'], outList=wARR_RateWord )
		
		#############################
		# 登録データを作成する
		wARR_Word = {}
		for wLine in inARRData :
			
			### 通報設定ありか
			#      先頭が @@@ の場合
			wReport = False
			wIfind = wLine.find("@@@")
			if wIfind==0 :
				wLine = wLine.replace( "@@@", "" )
				wReport = True
			
			### ダブり登録は除外
			if wLine in wARR_Word :
				continue
			if wLine=="" or wLine==None :
				continue
			
			### データ登録
			wCell = {
				"word"		: wLine,
				"report"	: wReport
			}
			wARR_Word.update({ wLine : wCell })
		
		#############################
		# データベースに登録する
		wKeylist = list( wARR_Word.keys() )
		for wKey in wKeylist :
			#############################
			# 登録済みの場合
			#   通報情報を更新する
			if wKey in wARR_RateWord :
				wQy = "update tbl_exc_word set "
				wQy = wQy + "report = " + str(wARR_Word[wKey]['report']) + " "
				wQy = wQy + " ;"
			
			#############################
			# 登録なしの場合
			#   新規登録する
			else :
				wQy = "insert into tbl_exc_word values ("
				wQy = wQy + "'" + str(wTD['TimeDate']) + "', "
				wQy = wQy + "'" + wKey + "', "
				wQy = wQy + str(wARR_Word[wKey]['report']) + " "
				wQy = wQy + ") ;"
			
			#############################
			# クエリの実行
			wResDB = self.OBJ_DB.RunQuery( wQy )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				gVal.OBJ_L.Log( "C", wRes )
				return False
			
			#############################
			# 実行結果の表示
			if wKey in wARR_RateWord :
				### 更新
				wStr = "除外文字 更新: "
			else:
				### 新規
				wStr = "除外文字 追加: "
			
			### 通報有無
			if wARR_Word[wKey]['report']==True :
				wStr = wStr + " [〇有] "
			else:
				wStr = wStr + " [  無] "
			
			### 文字
			wStr = wStr + wKey
			
			CLS_OSIF.sPrn( wStr )
		
		#############################
		# データベースから削除
		#   登録データにないデータをデータベースから抹消する
		for wRateKey in wARR_RateWord :
			#############################
			# 登録データにある場合
			#   スキップする
			if wRateKey in wARR_Word :
				continue
			
			# ※登録なし：削除確定
			wQy = "delete from tbl_exc_word "
			wQy = wQy + "where word = '" + wRateKey + "' "
			wQy = wQy + " ;"
			
			#############################
			# クエリの実行
			wResDB = self.OBJ_DB.RunQuery( wQy )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				gVal.OBJ_L.Log( "C", wRes )
				return False
			
			#############################
			# 実行結果の表示
			wStr = "除外文字 ×削除×: " + wRateKey
			CLS_OSIF.sPrn( wStr )
		
		#############################
		# グローバルを更新する
		gVal.ARR_ExeWord = wARR_Word
		gVal.ARR_ExeWordKeys = list( wARR_Word.keys() )
		
		#############################
		# ログに記録する
		gVal.OBJ_L.Log( "SR", wRes, "データ更新: exe word" )
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes



#####################################################
# 除外プロフ文字
#####################################################
	def GetExeProf(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetExeProf"
		
		#############################
		# データベースから除外文字を取得
		wQy = "select * from tbl_exc_prof "
		wQy = wQy + ";"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return False
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		wARR_ExeWord = {}
		#############################
		# 除外文字データを登録する
		wKeylist = list( wARR_DBData.keys() )
		for wIndex in wKeylist :
			wKey = wARR_DBData[wIndex]['word']
			wCell = {
				"word"		: wKey,
				"report"	: wARR_DBData[wIndex]['report']
			}
			wARR_ExeWord.update({ wKey : wCell })
		
		gVal.ARR_ExeProf = wARR_ExeWord
		gVal.ARR_ExeProfKeys = list( wARR_ExeWord.keys() )
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def SetExeProf( self, inARRData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetExeProf"
		
		#############################
		# 時間を取得
		wTD = CLS_TIME.sGet( wRes, "(2)" )
		
		#############################
		# データベースから除外文字を取得
		wQy = "select word from tbl_exc_prof "
		wQy = wQy + ";"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return False
		
		### リスト型に整形
		wARR_RateWord = []
		self.OBJ_DB.ChgList( wResDB['Responce']['Data'], outList=wARR_RateWord )
		
		#############################
		# 登録データを作成する
		wARR_Word = {}
		for wLine in inARRData :
			
			### 通報設定ありか
			#      先頭が @@@ の場合
			wReport = False
			wIfind = wLine.find("@@@")
			if wIfind==0 :
				wLine = wLine.replace( "@@@", "" )
				wReport = True
			
			### ダブり登録は除外
			if wLine in wARR_Word :
				continue
			if wLine=="" or wLine==None :
				continue
			
			### データ登録
			wCell = {
				"word"		: wLine,
				"report"	: wReport
			}
			wARR_Word.update({ wLine : wCell })
		
		#############################
		# データベースに登録する
		wKeylist = list( wARR_Word.keys() )
		for wKey in wKeylist :
			#############################
			# 登録済みの場合
			#   通報情報を更新する
			if wKey in wARR_RateWord :
				wQy = "update tbl_exc_prof set "
				wQy = wQy + "report = " + str(wARR_Word[wKey]['report']) + " "
				wQy = wQy + " ;"
			
			#############################
			# 登録なしの場合
			#   新規登録する
			else :
				wQy = "insert into tbl_exc_prof values ("
				wQy = wQy + "'" + str(wTD['TimeDate']) + "', "
				wQy = wQy + "'" + wKey + "', "
				wQy = wQy + str(wARR_Word[wKey]['report']) + " "
				wQy = wQy + ") ;"
			
			#############################
			# クエリの実行
			wResDB = self.OBJ_DB.RunQuery( wQy )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				gVal.OBJ_L.Log( "C", wRes )
				return False
			
			#############################
			# 実行結果の表示
			if wKey in wARR_RateWord :
				### 更新
				wStr = "除外文字 更新: "
			else:
				### 新規
				wStr = "除外文字 追加: "
			
			### 通報有無
			if wARR_Word[wKey]['report']==True :
				wStr = wStr + " [〇有] "
			else:
				wStr = wStr + " [  無] "
			
			### 文字
			wStr = wStr + wKey
			
			CLS_OSIF.sPrn( wStr )
		
		#############################
		# データベースから削除
		#   登録データにないデータをデータベースから抹消する
		for wRateKey in wARR_RateWord :
			#############################
			# 登録データにある場合
			#   スキップする
			if wRateKey in wARR_Word :
				continue
			
			# ※登録なし：削除確定
			wQy = "delete from tbl_exc_prof "
			wQy = wQy + "where word = '" + wRateKey + "' "
			wQy = wQy + " ;"
			
			#############################
			# クエリの実行
			wResDB = self.OBJ_DB.RunQuery( wQy )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				gVal.OBJ_L.Log( "C", wRes )
				return False
			
			#############################
			# 実行結果の表示
			wStr = "除外文字 ×削除×: " + wRateKey
			CLS_OSIF.sPrn( wStr )
		
		#############################
		# グローバルを更新する
		gVal.ARR_ExeProf = wARR_Word
		gVal.ARR_ExeProfKeys = list( wARR_Word.keys() )
		
		#############################
		# ログに記録する
		gVal.OBJ_L.Log( "SR", wRes, "データ更新: exe prof" )
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes



#####################################################
# 禁止ユーザ
#####################################################
	def GetExeUser(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetExeUser"
		
		#############################
		# データベースから禁止ユーザを取得
		wQy = "select * from tbl_exc_user "
		wQy = wQy + ";"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# 添え字をIDに差し替える
		wARR_DBData = gVal.OBJ_DB_IF.ChgDataID( wARR_DBData )
		
		wARR_ExeUser = {}
		#############################
		# 禁止ユーザデータを登録する
		wKeylist = list( wARR_DBData.keys() )
		wListNo = 1
		for wID in wKeylist :
			wID = str(wID)
			wCell = {
				"list_number"	: wListNo,
				"id"			: wID,
				"screen_name"	: wARR_DBData[wID]['screen_name'],
				"report"		: wARR_DBData[wID]['report'],
				"vip"			: wARR_DBData[wID]['vip'],
				"ope"			: wARR_DBData[wID]['ope'],
				"follow"		: wARR_DBData[wID]['follow'],
				"rel_date"		: wARR_DBData[wID]['rel_date'],
				"memo"			: wARR_DBData[wID]['memo']
			}
			wARR_ExeUser.update({ wID : wCell })
			wListNo += 1
		
		gVal.ARR_NotReactionUser = wARR_ExeUser
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def SetExeUser( self, inARRData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetExeUser"
		
		#############################
		# 時間を取得
		wTD = CLS_TIME.sGet( wRes, "(3)" )
		
		#############################
		# データベースから禁止ユーザを取得
		wQy = "select * from tbl_exc_user "
		wQy = wQy + ";"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# 添え字をIDに差し替える
		wARR_RateWord = gVal.OBJ_DB_IF.ChgDataID( wARR_DBData )
###		wARR_RateWordID = list( wARR_RateWord )
		wARR_RateWordID = list( wARR_RateWord.keys() )
		
		wResult = {
			"insert"	: 0,
			"update"	: 0,
			"delete"	: 0
		}
		
		#############################
		# データベースに登録する
		wKeylist = list( inARRData.keys() )
		for wID in wKeylist :
			wID = str(wID)
			#############################
			# 登録済みの場合
			#   通報情報を更新する
			if wID in wARR_RateWordID :
				wQy = "update tbl_exc_user set "
				wQy = wQy + "report = " + str(inARRData[wID]['report']) + ", "
				wQy = wQy + "vip = " + str(inARRData[wID]['vip']) + ", "
				wQy = wQy + "ope = " + str(inARRData[wID]['ope']) + ", "
				wQy = wQy + "follow = " + str(inARRData[wID]['follow']) + ", "
				wQy = wQy + "rel_date = '" + str(inARRData[wID]['rel_date']) + "', "
				wQy = wQy + "memo = '" + str(inARRData[wID]['memo']) + "' "
				wQy = wQy + "where id = '" + str(inARRData[wID]['id']) + "' "
				wQy = wQy + " ;"
				
				wResult['update'] += 1
			
			#############################
			# 登録なしの場合
			#   新規登録する
			else :
				wQy = "insert into tbl_exc_user values ("
				wQy = wQy + "'" + str(wTD['TimeDate']) + "', "
				wQy = wQy + "'" + str(inARRData[wID]['id']) + "', "
				wQy = wQy + "'" + str(inARRData[wID]['screen_name']) + "', "
				wQy = wQy + str(inARRData[wID]['report']) + ", "
				wQy = wQy + str(inARRData[wID]['vip']) + ", "
				wQy = wQy + str(inARRData[wID]['ope']) + ", "
				wQy = wQy + str(inARRData[wID]['follow']) + ", "
				wQy = wQy + "'" + str( gVal.DEF_TIMEDATE ) + "',"
				wQy = wQy + "'' "
				wQy = wQy + ") ;"
				
				wResult['insert'] += 1
			
			#############################
			# クエリの実行
			wResDB = self.OBJ_DB.RunQuery( wQy )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				gVal.OBJ_L.Log( "C", wRes )
				return wRes
			
			#############################
			# 実行結果の表示
			if wID in inARRData :
				### 更新
				wStr = "禁止ユーザ 更新: "
			else:
				### 新規
				wStr = "禁止ユーザ 追加: "
			
			### 通報有無
			if inARRData[wID]['report']==True :
				wStr = wStr + " [〇有] "
			else:
				if inARRData[wID]['ope']==True :
					wStr = wStr + " [●監] "
				else:
					wStr = wStr + " [  無] "
			
			### 文字
			wStr = wStr + str(inARRData[wID]['screen_name'])
			
			CLS_OSIF.sPrn( wStr )
		
		#############################
		# データベースから削除
		#   登録データにないデータをデータベースから抹消する
		for wID in inARRData :
			wID = str(wID)
			#############################
			# 登録データにある場合
			#   スキップする
			if wID in inARRData :
				continue
			
			# ※登録なし：削除確定
			wQy = "delete from tbl_exc_user "
			wQy = wQy + "where id = '" + wID + "' "
			wQy = wQy + " ;"
			
			wResult['delete'] += 1
			
			#############################
			# クエリの実行
			wResDB = self.OBJ_DB.RunQuery( wQy )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				gVal.OBJ_L.Log( "C", wRes )
				return wRes
			
			#############################
			# 実行結果の表示
			wStr = "禁止ユーザ ×削除×: " + wARR_RateWord[wID]['screen_name']
			CLS_OSIF.sPrn( wStr )
		
		#############################
		# グローバルを更新する
		gVal.ARR_NotReactionUser = inARRData
		
		#############################
		# ログに記録する
		wStr = "データ更新: exe user data: insert=" + str(wResult['insert']) + " update=" + str(wResult['update']) + " delete=" + str(wResult['delete'])
		gVal.OBJ_L.Log( "RR", wRes, wStr )
		
		wRes['Result'] = True
		return wRes

	#####################################################
	def InsertExeUser( self, inData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "InsertExeUser"
		
		#############################
		# 入力チェック
		if "id" not in inData or \
		   "screen_name" not in inData :
			wRes['Reason'] = "input error: " + str(inData)
			gVal.OBJ_L.Log( "A", wRes )
			return wRes
		
		#############################
		# 時間を取得
		wTD = CLS_TIME.sGet( wRes, "(4)" )
		
		#############################
		# ダブりチェック
		if inData['id'] in gVal.ARR_NotReactionUser :
			wRes['Reason'] = "Duai Screen_Name: screen_name=" + str(inData['screen_name'])
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# 新規登録する
		wQy = "insert into tbl_exc_user values ("
		wQy = wQy + "'" + str(wTD['TimeDate']) + "', "
		wQy = wQy + "'" + str(inData['id']) + "', "
		wQy = wQy + "'" + str(inData['screen_name']) + "', "
		wQy = wQy + "False, "
		wQy = wQy + "False, "
		wQy = wQy + "False, "
		wQy = wQy + "False, "
		wQy = wQy + "'" + str( gVal.DEF_TIMEDATE ) + "',"
		wQy = wQy + "'' "
		wQy = wQy + ") ;"
		
		#############################
		# クエリの実行
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# リスト番号の取得
		wKeylist = list( gVal.ARR_NotReactionUser.keys() )
		wListNo = 1
		for wKey in wKeylist :
			### ダブり登録はスキップ
			if gVal.ARR_NotReactionUser[wKey]['list_number']!=wListNo :
				###決定
				break
			wListNo += 1
		
		#############################
		# データ登録
		wCell = {
			"list_number"	: wListNo,
			"id"			: str(inData['id']),
			"screen_name"	: str(inData['screen_name']),
			"report"		: False,
			"vip"			: False,
			"ope"			: False,
			"follow"		: False,
			"rel_date"		: str( gVal.DEF_TIMEDATE ),
			"memo"			: ""
		}
		gVal.ARR_NotReactionUser.update({ str(inData['id']) : wCell })
		
		#############################
		# ログに記録する
		wStr = "禁止ユーザ設定: exe user data: user=" + gVal.ARR_NotReactionUser[str(inData['id'])]['screen_name']
###		gVal.OBJ_L.Log( "RR", wRes, wStr )
		gVal.OBJ_L.Log( "RR", wRes, wStr, inID=inData['id'] )
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes

	#####################################################
###	def UpdateExeUser( self, inID, inReport=None, inVIP=None, inOpe=None, inRelDate=None, inMemo=None ):
	def UpdateExeUser( self, inID, inReport=None, inVIP=None, inOpe=None, inFollow=None, inRelDate=None, inMemo=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "UpdateExeUser"
		
		wUserID = str(inID)
		#############################
		# ダブりチェック
		if inID not in gVal.ARR_NotReactionUser :
			wRes['Reason'] = "No data Screen_Name: id=" + str(wUserID)
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# 入力チェック
		if inReport==None and inVIP==None and inOpe==None and inRelDate==None and inMemo==None :
			wRes['Reason'] = "input error: screen_name=" + str(gVal.ARR_NotReactionUser[wUserID]['screen_name'])
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# 現設定値のロード
		wSTR_Value = {
			"report"		: gVal.ARR_NotReactionUser[wUserID]['report'],
			"vip"			: gVal.ARR_NotReactionUser[wUserID]['vip'],
			"ope"			: gVal.ARR_NotReactionUser[wUserID]['ope'],
			"follow"		: gVal.ARR_NotReactionUser[wUserID]['follow'],
			"rel_date"		: gVal.ARR_NotReactionUser[wUserID]['rel_date'],
			"memo"			: gVal.ARR_NotReactionUser[wUserID]['memo']
		}
		
		#############################
		# 設定値の変更
		if inReport!=None :
			wSTR_Value['report'] = inReport
		if inVIP!=None :
			wSTR_Value['vip'] = inVIP
		if inOpe!=None :
			wSTR_Value['ope'] = inOpe
		if inFollow!=None :
			wSTR_Value['follow'] = inFollow
		
		if inRelDate!=None :
			wSTR_Value['rel_date'] = inRelDate
		else:
			wSTR_Value['rel_date'] = str( gVal.DEF_TIMEDATE )
		
		if inMemo!=None :
			wSTR_Value['memo'] = inMemo
		
		#############################
		# 変更する
		wQy = "update tbl_exc_user set "
		wQy = wQy + "report = " + str( wSTR_Value['report'] ) + ", "
		wQy = wQy + "vip = " + str( wSTR_Value['vip'] ) + ", "
		wQy = wQy + "ope = " + str( wSTR_Value['ope'] ) + ", "
		wQy = wQy + "follow = " + str( wSTR_Value['follow'] ) + ", "
		wQy = wQy + "rel_date = '" + str( wSTR_Value['rel_date'] ) + "', "
		wQy = wQy + "memo = '" + str( wSTR_Value['memo'] ) + "' "
		wQy = wQy + "where id = '" + wUserID + "' "
		wQy = wQy + ";"
		
		#############################
		# クエリの実行
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# データ変更
		gVal.ARR_NotReactionUser[wUserID]['report'] = wSTR_Value['report']
		gVal.ARR_NotReactionUser[wUserID]['vip']    = wSTR_Value['vip']
		gVal.ARR_NotReactionUser[wUserID]['ope']    = wSTR_Value['ope']
		gVal.ARR_NotReactionUser[wUserID]['follow'] = wSTR_Value['follow']
		gVal.ARR_NotReactionUser[wUserID]['rel_date'] = wSTR_Value['rel_date']
		gVal.ARR_NotReactionUser[wUserID]['memo']     = wSTR_Value['memo']
		
		#############################
		# ログに記録する
		wStr = "禁止ユーザ更新: exe user data: user=" + gVal.ARR_NotReactionUser[wUserID]['screen_name']
###		gVal.OBJ_L.Log( "RR", wRes, wStr )
		gVal.OBJ_L.Log( "RR", wRes, wStr, inID=inID )
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def DeleteExeUser( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "DeleteExeUser"
		
		wUserID = str(inID)
		#############################
		# ダブりチェック
		if inID not in gVal.ARR_NotReactionUser :
			wRes['Reason'] = "No data Screen_Name: id=" + str(wUserID)
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# 変更する
		wQy = "delete from tbl_exc_user where "
		wQy = wQy + "id = '" + wUserID + "' "
		wQy = wQy + ";"
		
		#############################
		# クエリの実行
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# データ削除
		wScreenName = gVal.ARR_NotReactionUser[wUserID]['screen_name']
		del gVal.ARR_NotReactionUser[wUserID]
		
		#############################
		# ログに記録する
		wStr = "禁止ユーザ解除: exe user data: user=" + wScreenName
###		gVal.OBJ_L.Log( "RR", wRes, wStr )
		gVal.OBJ_L.Log( "RR", wRes, wStr, inID=wUserID )
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes



#####################################################
# リストいいね指定
#####################################################
	def GetListFavo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetListFavo"
		
		#############################
		# データベースを取得
		wQy = "select * from tbl_list_favo "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		wARR_Data = {}
		#############################
		# 除外文字データを登録する
		wKeylist = list( wARR_DBData.keys() )
###		wListNo = 1
		for wIndex in wKeylist :
			wID = str( wARR_DBData[wIndex]['id'] )
			wCell = {
###				"list_number"	: wListNo,
				"list_number"	: -1,
				"id"			: wID,
				"list_name"		: wARR_DBData[wIndex]['list_name'],
				"user_id"		: str( wARR_DBData[wIndex]['user_id'] ),
				"screen_name"	: wARR_DBData[wIndex]['screen_name'],
				"valid"			: wARR_DBData[wIndex]['valid'],
				"follow"		: wARR_DBData[wIndex]['follow'],
				"caution"		: wARR_DBData[wIndex]['caution'],
				"sensitive"		: wARR_DBData[wIndex]['sensitive'],
				"auto_rem"		: wARR_DBData[wIndex]['auto_rem'],
				"update"		: False
			}
			wARR_Data.update({ wID : wCell })
###			wListNo += 1
		
		#############################
		# リスト通知リストと
		# 自動リムーブが有効なら 相互フォローリスト、片フォロワーリスト
		# を登録から除外する
		wKeylist = list( wARR_Data.keys() )
		wARR_Del = []
		for wIndex in wKeylist :
			wID = str( wARR_Data[wIndex]['id'] )
			
			if ( gVal.STR_UserInfo['ListID']==wID or \
			     gVal.STR_UserInfo['mListID']==wID and gVal.STR_UserInfo['AutoRemove']==True or \
			     gVal.STR_UserInfo['fListID']==wID and gVal.STR_UserInfo['AutoRemove']==True ) \
			   and str(gVal.STR_UserInfo['id'])==wARR_Data[wIndex]['user_id'] :
				wARR_Del.append( wID )
		
		#############################
		# 削除対象をリストとDBから削除する
		for wID in wARR_Del :
			wID = str( wID )
			
			### レコードを消す
			wQy = "delete from tbl_list_favo "
			wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' and "
			wQy = wQy + "id = '" + wID + "' ;"
			
			wResDB = self.OBJ_DB.RunQuery( wQy )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				gVal.OBJ_L.Log( "C", wRes )
				return wRes
			
			del wARR_Data[wID]
		
		#############################
		# リスト番号を振る
		wKeylist = list( wARR_Data.keys() )
		wListNo = 1
		for wIndex in wKeylist :
			wARR_Data[wIndex]['list_number'] = wListNo
			wListNo += 1
		
		gVal.ARR_ListFavo = wARR_Data
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def SetListFavo( self, inARRData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetListFavo"
		
		if len(inARRData)==0 :
			##失敗
			wRes['Reason'] = "get no data"
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# レコードを一旦全消す
		wQy = "delete from tbl_list_favo "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		wStr = "tbl_list_favo をクリアしました "
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# データベースに登録する
		wKeylist = list( inARRData.keys() )
		wInsertNum = 0
		for wKey in wKeylist :
			wQy = "insert into tbl_list_favo values ("
			wQy = wQy + "'" + gVal.STR_UserInfo['Account'] + "', "
			wQy = wQy + "'" + str(inARRData[wKey]['id']) + "', "
			wQy = wQy + "'" + str(inARRData[wKey]['list_name']) + "', "
			wQy = wQy + "'" + str(inARRData[wKey]['user_id']) + "', "
			wQy = wQy + "'" + str(inARRData[wKey]['screen_name']) + "', "
			wQy = wQy + "True, "
			wQy = wQy + str(inARRData[wKey]['follow']) + ", "
			wQy = wQy + str(inARRData[wKey]['caution']) + ", "
			wQy = wQy + str(inARRData[wKey]['sensitive']) + ", "
			wQy = wQy + str(inARRData[wKey]['auto_rem']) + " "
			wQy = wQy + ") ;"
			
			#############################
			# クエリの実行
			wResDB = self.OBJ_DB.RunQuery( wQy )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				gVal.OBJ_L.Log( "C", wRes )
				return wRes
			wInsertNum += 1
		
		#############################
		# グローバルを更新する
		gVal.ARR_ListFavo = inARRData
		
		#############################
		# ログに記録する
		wStr = "データ更新: list favo data: insert=" + str( wInsertNum ) + " and delete data"
		gVal.OBJ_L.Log( "SC", wRes, wStr )
		
		wRes['Result'] = True
		return wRes

	#####################################################
	def InsertListFavo( self, inUserID, inUserName, inListID, inListName ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "InsertListFavo"
		
		wRes['Responce'] = False
		#############################
		# 重複チェック
		wKeylist = list( gVal.ARR_ListFavo.keys() )
		for wID in wKeylist :
			wID = str(wID)
			
			if gVal.ARR_ListFavo[wID]['list_name']==inListName and \
			   gVal.ARR_ListFavo[wID]['screen_name']==inUserName :
###				wRes['Reason'] = "Dual input: user=" + inUserName + " list=" + inListName
###				gVal.OBJ_L.Log( "A", wRes )
				wRes['Result'] = True
				return wRes
		
		#############################
		# データの組み立て
		
		### リスト番号の割り当て
		wListNumber = 1
		wFLG_Detect = False
		while True :
			wFLG_Detect = False
			for wID in wKeylist :
				wID = str(wID)
				if gVal.ARR_ListFavo[wID]['list_number']==wListNumber :
					wListNumber += 1
					wFLG_Detect = True
					break
			if wFLG_Detect==False :
				break
		
		wCell = {
			"list_number"	: wListNumber,
			"id"			: str( inListID ),
			"list_name"		: inListName,
			"user_id"		: str( inUserID ),
			"screen_name"	: inUserName,
			"valid"			: True,
			"follow"		: False,
			"caution"		: False,
			"sensitive"		: False,
			"auto_rem"		: False,
			"update"		: False
		}
		
		#############################
		# データベースに登録する
		wQy = "insert into tbl_list_favo values ("
		wQy = wQy + "'" + gVal.STR_UserInfo['Account'] + "', "
		wQy = wQy + "'" + str( inListID ) + "', "
		wQy = wQy + "'" + str( inListName ) + "', "
		wQy = wQy + "'" + str( inUserID ) + "', "
		wQy = wQy + "'" + str( inUserName ) + "', "
		wQy = wQy + "True, "
		wQy = wQy + "False, "
		wQy = wQy + "False, "
		wQy = wQy + "False, "
		wQy = wQy + "False "
		wQy = wQy + ") ;"
		
		#############################
		# クエリの実行
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed: RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# グローバルを更新する
		gVal.ARR_ListFavo.update({ str( inListID ) : wCell })
		
		#############################
		# ログに記録する
		wStr = "データ更新: list favo data: user=" + str( inUserName ) + " list=" + str( inListName )
		gVal.OBJ_L.Log( "SC", wRes, wStr )
		
		wRes['Responce'] = True
		wRes['Result'] = True
		return wRes

	#####################################################
	def DeleteListFavo( self, inListID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "DeleteListFavo"
		
		wRes['Responce'] = False
		wKeyID = None
		#############################
		# 入力チェック
		if inListID not in gVal.ARR_ListFavo :
			### キーなし
			wRes['Result'] = True
			return wRes
		
		wObjUserName = gVal.ARR_ListFavo[inListID]['screen_name']
		wObjListName = gVal.ARR_ListFavo[inListID]['list_name']
		#############################
		# データの組み立て
		wQy = "delete from tbl_list_favo "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' and "
		wQy = wQy + "id = '" + str(gVal.ARR_ListFavo[inListID]['id']) + "' and "
		wQy = wQy + "user_id = '" + str(gVal.ARR_ListFavo[inListID]['user_id']) + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed: RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# グローバルを更新する
		del gVal.ARR_ListFavo[inListID]
		
		#############################
		# ログに記録する
		wStr = "データ削除: list favo data: user=" + str( wObjUserName ) + " list=" + str( wObjListName )
		gVal.OBJ_L.Log( "SC", wRes, wStr )
		
		wRes['Responce'] = True
		wRes['Result'] = True
		return wRes

	#####################################################
	def SaveListFavo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SaveListFavo"
		
		wUpdateNum = 0
		#############################
		# 更新があれば
		#   データベースを更新する
		wKeylist = list( gVal.ARR_ListFavo.keys() )
		for wKey in wKeylist :
			if gVal.ARR_ListFavo[wKey]['update']==False :
				### 更新なしはスキップ
				continue
			
			wQy = "update tbl_list_favo set "
			wQy = wQy + "valid = " + str(gVal.ARR_ListFavo[wKey]['valid']) + ", "
			wQy = wQy + "follow = " + str(gVal.ARR_ListFavo[wKey]['follow']) + ", "
			wQy = wQy + "caution = " + str(gVal.ARR_ListFavo[wKey]['caution']) + ", "
			wQy = wQy + "sensitive = " + str(gVal.ARR_ListFavo[wKey]['sensitive']) + ", "
			wQy = wQy + "auto_rem = " + str(gVal.ARR_ListFavo[wKey]['auto_rem']) + " "
			wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' and "
			wQy = wQy + "id = '" + gVal.ARR_ListFavo[wKey]['id'] + "' "
			wQy = wQy + ";"
			
			#############################
			# クエリの実行
			wResDB = self.OBJ_DB.RunQuery( wQy )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				gVal.OBJ_L.Log( "C", wRes )
				return wRes
			
			wUpdateNum += 1
		
		#############################
		# ログに記録する
		if wUpdateNum>0 :
			wStr = "データ更新: list favo data: update=" + str( wUpdateNum )
			gVal.OBJ_L.Log( "SC", wRes, wStr )
		
		wRes['Result'] = True
		return wRes



#####################################################
# 警告ツイート
#####################################################
	def GetCautionTweet(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetCautionTweet"
		
		#############################
		# データベースを取得
		wQy = "select * from tbl_caution_tweet "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return False
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# 添え字をIDに差し替える
		wARR_DBData = gVal.OBJ_DB_IF.ChgDataID( wARR_DBData )
		
		#############################
		# グローバルに保存する
		gVal.ARR_CautionTweet = {}
		#############################
		# 除外文字データを登録する
		wKeylist = list( wARR_DBData.keys() )
		wListNo = 1
		for wKey in wKeylist :
			wCell = {
				"list_number"	: wListNo,
				"regdate"		: str(wARR_DBData[wKey]['regdate']),
				"tweet_id"		: str(wARR_DBData[wKey]['tweet_id']),
				"id"			: str(wARR_DBData[wKey]['id']),
				"screen_name"	: str(wARR_DBData[wKey]['screen_name'])
			}
			gVal.ARR_CautionTweet.update({ wListNo : wCell })
			wListNo += 1
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def SetCautionTweet( self, inUser, inTweetID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetCautionTweet"
		
		wUserID = str( inUser['id'] )
		
		#############################
		# ダブりチェック
		if wUserID in gVal.ARR_CautionTweet :
			### ありえない？
			wRes['Reason'] = "Dual regist user: screen_name=" + str( inUser['screen_name'] )
			gVal.OBJ_L.Log( "E", wRes )
			return wRes
		
		#############################
		# データの組み立て
		wCell = {
			"twitterid"		: gVal.STR_UserInfo['Account'],
			"regdate"		: str( gVal.STR_Time['TimeDate'] ),
			"tweet_id"		: str( inTweetID ),
			"id"			: wUserID,
			"screen_name"	: str( inUser['screen_name'] )
		}
		
		#############################
		# データベースに登録する
		wQy = "insert into tbl_caution_tweet values ("
		wQy = wQy + "'" + wCell['twitterid'] + "', "
		wQy = wQy + "'" + wCell['regdate'] + "', "
		wQy = wQy + "'" + wCell['tweet_id'] + "', "
		wQy = wQy + "'" + wCell['id'] + "', "
		wQy = wQy + "'" + wCell['screen_name'] + "' "
		wQy = wQy + ") ;"
		
		#############################
		# クエリの実行
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# グローバルを更新する
		gVal.ARR_CautionTweet.update({ wUserID : wCell })
		
		#############################
		# ログに記録する
		wStr = "データ追加: caution tweet: screen_name=" + str(wCell['screen_name']) + " tweet_id=" + str(wCell['tweet_id'])
		gVal.OBJ_L.Log( "RR", wRes, wStr, inID=wUserID )
		
		wRes['Result'] = True
		return wRes

	#####################################################
	def DeleteCautionTweet( self, inListNum ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "DeleteCautionTweet"
		
		#############################
		# 登録チェック
		if inListNum not in gVal.ARR_CautionTweet :
			wRes['Reason'] = "Not regist user: list num=" + str( inListNum )
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		wUserID = str( gVal.ARR_CautionTweet[inListNum]['id'] )
		wSN     = str( gVal.ARR_CautionTweet[inListNum]['screen_name'] )
		#############################
		# レコードから削除する
		wQy = "delete from tbl_caution_tweet "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' and "
		wQy = wQy + "id = '" + wUserID + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return False
		
		#############################
		# グローバルを更新する
		del gVal.ARR_CautionTweet[inListNum]
		
		#############################
		# ログに記録する
		wStr = "データ削除: caution tweet: screen_name=" + wSN
		gVal.OBJ_L.Log( "RR", wRes, wStr, inID=wUserID )
		
		wRes['Result'] = True
		return wRes

	#####################################################
	def CheckCautionTweet( self, inTweetID ):
		
		wID = str(inTweetID)
		wFlg = False
		
		wKeylist = list( gVal.ARR_CautionTweet.keys() )
		for wIndex in wKeylist :
			if str(gVal.ARR_CautionTweet[wIndex]['tweet_id'])==wID :
				wFlg = True
				break
		
		return wFlg



#####################################################
# リスト名設定
#####################################################
	def GetListName( self, inAccount ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetListName"
		
		#############################
		# データ取得
		wQy = "select "
		wQy = wQy + "trendtag, list_id, list_name, "
###		wQy = wQy + "autoremove, mlist_id, mlist_name, flist_id, flist_name "
###		wQy = wQy + "autoremove, mlist_id, mlist_name, flist_id, flist_name, viptag "
###		wQy = wQy + "autoremove, mlist_id, mlist_name, flist_id, flist_name, viptag, questiontag "
		wQy = wQy + "autoremove, mlist_id, mlist_name, flist_id, flist_name, viptag, questiontag, deltag "
		wQy = wQy + "from tbl_user_data "
		wQy = wQy + "where twitterid = '" + str(inAccount) + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# 取得チェック
		if len( wARR_DBData )!= 1 :
			##失敗
			wRes['Reason'] = "Get list name is not one: account=" + str(inAccount) + " num=" + str( len( wARR_DBData ) )
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# データをグローバルに反映
		gVal.STR_UserInfo['TrendTag'] = wARR_DBData[0]['trendtag']
		gVal.STR_UserInfo['ListID']   = wARR_DBData[0]['list_id']
		gVal.STR_UserInfo['ListName'] = wARR_DBData[0]['list_name']
		gVal.STR_UserInfo['AutoRemove'] = wARR_DBData[0]['autoremove']
		gVal.STR_UserInfo['mListID']    = wARR_DBData[0]['mlist_id']
		gVal.STR_UserInfo['mListName']  = wARR_DBData[0]['mlist_name']
		gVal.STR_UserInfo['fListID']    = wARR_DBData[0]['flist_id']
		gVal.STR_UserInfo['fListName']  = wARR_DBData[0]['flist_name']
		gVal.STR_UserInfo['VipTag']     = wARR_DBData[0]['viptag']
		gVal.STR_UserInfo['QuestionTag'] = wARR_DBData[0]['questiontag']
		gVal.STR_UserInfo['DelTag']     = wARR_DBData[0]['deltag']
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def SetListName( self, inListName, inListID=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetListName"
		
		#############################
		# 入力切替
		wListName = gVal.DEF_NOTEXT
		wListID   = gVal.DEF_NOTEXT
		if inListName!=gVal.DEF_NOTEXT :
			wListName = inListName
			wListID   = inListID
		
		wQy = "update tbl_user_data set "
		wQy = wQy + "list_id = '" + str(wListID) + "', "
		wQy = wQy + "list_name = '" + str(wListName) + "' "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# データをグローバルに反映
		gVal.STR_UserInfo['ListID']   = wListID
		gVal.STR_UserInfo['ListName'] = wListName
		
		#############################
		# ログに記録する
		if inListName!=gVal.DEF_NOTEXT :
			wStr = "リスト通知設定: list name: name=" + str(wListName) + " screen_name=" + str(gVal.STR_UserInfo['Account'])
		else:
			wStr = "リスト通知解除: screen_name=" + str(gVal.STR_UserInfo['Account'])
		gVal.OBJ_L.Log( "SC", wRes, wStr )
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def SetTrendTag( self, inTrendName ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetTrendTag"
		
		#############################
		# 入力切替
		wTrendTag = gVal.DEF_NOTEXT
		if inTrendName!=gVal.DEF_NOTEXT :
			wTrendTag = inTrendName
		
		wQy = "update tbl_user_data set "
		wQy = wQy + "trendtag = '" + str(wTrendTag) + "' "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# データをグローバルに反映
		if inTrendName!=None :
			gVal.STR_UserInfo['TrendTag'] = wTrendTag
		
		#############################
		# ログに記録する
		if inTrendName!=gVal.DEF_NOTEXT :
			wStr = "トレンドタグ設定: name=" + str(wTrendTag) + " screen_name=" + str(gVal.STR_UserInfo['Account'])
		else:
			wStr = "トレンドタグ解除: screen_name=" + str(gVal.STR_UserInfo['Account'])
		gVal.OBJ_L.Log( "SC", wRes, wStr )
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def SetQuestionTag( self, inQuestionName ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetQuestionTag"
		
		#############################
		# 入力切替
		wQuestionTag = gVal.DEF_NOTEXT
		if inQuestionName!=gVal.DEF_NOTEXT :
			wQuestionTag = inQuestionName
		
		wQy = "update tbl_user_data set "
		wQy = wQy + "questiontag = '" + str(wQuestionTag) + "' "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# データをグローバルに反映
		if inQuestionName!=None :
			gVal.STR_UserInfo['QuestionTag'] = wQuestionTag
		
		#############################
		# ログに記録する
		if inQuestionName!=gVal.DEF_NOTEXT :
			wStr = "質問タグ設定: name=" + str(inQuestionName) + " screen_name=" + str(gVal.STR_UserInfo['Account'])
		else:
			wStr = "質問タグ解除: screen_name=" + str(gVal.STR_UserInfo['Account'])
		gVal.OBJ_L.Log( "SC", wRes, wStr )
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def SetAutoRemove(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetAutoRemove"
		
		#############################
		# フラグ反転
		wFLG_AutoRemove = True
		if gVal.STR_UserInfo['AutoRemove']==True :
			wFLG_AutoRemove = False
		
		wQy = "update tbl_user_data set "
		wQy = wQy + "autoremove = " + str(wFLG_AutoRemove) + " "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# データをグローバルに反映
		gVal.STR_UserInfo['AutoRemove'] = wFLG_AutoRemove
		
		#############################
		# ログに記録する
		if wFLG_AutoRemove==True :
			wStr = "自動リムーブ設定: screen_name=" + str(gVal.STR_UserInfo['Account'])
		else:
			wStr = "自動リムーブ解除: screen_name=" + str(gVal.STR_UserInfo['Account'])
		gVal.OBJ_L.Log( "SC", wRes, wStr )
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def SetAutoList( self, inMListName,inFListName, inMListID, inFListID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetAutoRemove"
		
		#############################
		# 入力チェック
		if inMListName==gVal.DEF_NOTEXT :
			if inFListName!=gVal.DEF_NOTEXT :
				wRes['Reason'] = "input error(inMListName=None)"
				gVal.OBJ_L.Log( "A", wRes )
				return wRes
		
		if inFListName==gVal.DEF_NOTEXT :
			if inMListName!=gVal.DEF_NOTEXT :
				wRes['Reason'] = "input error(inFListName=None)"
				gVal.OBJ_L.Log( "A", wRes )
				return wRes
		
		wQy = "update tbl_user_data set "
		wQy = wQy + "mlist_id = '" + str(inMListID) + "', "
		wQy = wQy + "mlist_name = '" + str(inMListName) + "', "
		wQy = wQy + "flist_id = '" + str(inFListID) + "', "
		wQy = wQy + "flist_name = '" + str(inFListName) + "' "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# データをグローバルに反映
		gVal.STR_UserInfo['mListID']   = inMListID
		gVal.STR_UserInfo['mListName'] = inMListName
		gVal.STR_UserInfo['fListID']   = inFListID
		gVal.STR_UserInfo['fListName'] = inFListName
		
		#############################
		# ログに記録する
		if inMListName!=gVal.DEF_NOTEXT :
			wStr = "相互フォローリスト設定: list name: name=" + str(inMListName) + " screen_name=" + str(gVal.STR_UserInfo['Account'])
			gVal.OBJ_L.Log( "SC", wRes, wStr )
			wStr = "片フォロワーリスト設定: list name: name=" + str(inFListName) + " screen_name=" + str(gVal.STR_UserInfo['Account'])
			gVal.OBJ_L.Log( "SC", wRes, wStr )
		else:
			wStr = "相互フォローリスト解除: screen_name=" + str(gVal.STR_UserInfo['Account'])
			gVal.OBJ_L.Log( "SC", wRes, wStr )
			wStr = "片フォロワーリスト解除: screen_name=" + str(gVal.STR_UserInfo['Account'])
			gVal.OBJ_L.Log( "SC", wRes, wStr )
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def SetVipTag( self, inTagName ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetVipTag"
		
		#############################
		# 入力切替
		wTrendTag = gVal.DEF_NOTEXT
		if inTagName!=gVal.DEF_NOTEXT :
			wTrendTag = inTagName
		
		wQy = "update tbl_user_data set "
		wQy = wQy + "viptag = '" + str(wTrendTag) + "' "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# データをグローバルに反映
		if inTagName!=None :
			gVal.STR_UserInfo['VipTag'] = wTrendTag
		
		#############################
		# ログに記録する
		if inTagName!=gVal.DEF_NOTEXT :
			wStr = "VIPタグ設定: name=" + str(wTrendTag) + " screen_name=" + str(gVal.STR_UserInfo['Account'])
		else:
			wStr = "VIPタグ解除: screen_name=" + str(gVal.STR_UserInfo['Account'])
		gVal.OBJ_L.Log( "SC", wRes, wStr )
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def SetDelTag( self, inTagName ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetDelTag"
		
		#############################
		# 入力切替
		wTrendTag = gVal.DEF_NOTEXT
		if inTagName!=gVal.DEF_NOTEXT :
			wTrendTag = inTagName
		
		wQy = "update tbl_user_data set "
		wQy = wQy + "deltag = '" + str(wTrendTag) + "' "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# データをグローバルに反映
		if inTagName!=None :
			gVal.STR_UserInfo['DelTag'] = wTrendTag
		
		#############################
		# ログに記録する
		if inTagName!=gVal.DEF_NOTEXT :
			wStr = "削除タグ設定: name=" + str(wTrendTag) + " screen_name=" + str(gVal.STR_UserInfo['Account'])
		else:
			wStr = "削除タグ解除: screen_name=" + str(gVal.STR_UserInfo['Account'])
		gVal.OBJ_L.Log( "SC", wRes, wStr )
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# 自動監視シーケンス設定
#####################################################
	def GetAutoSeq(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetAutoSeq"
		
		#############################
		# データ取得
		wQy = "select auto_seq "
		wQy = wQy + "from tbl_user_data "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# 取得チェック
		if len( wARR_DBData )!= 1 :
			##失敗
			wRes['Reason'] = "Get auto_seq name is not one: account=" + str(inAccount) + " num=" + str( len( wARR_DBData ) )
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# データをグローバルに反映
		wAutoSeq = wARR_DBData[0]['auto_seq']
		wSubRes = CLS_OSIF.sChgInt( wAutoSeq )
		if wSubRes['Result']!=True :
			##失敗
			wRes['Reason'] = "sChgInt is failer"
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		gVal.STR_UserInfo['AutoSeq'] = wSubRes['Value']
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def SetAutoSeq( self, inClear=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetAutoSeq"
		
		#############################
		# シーケンス値変更
		wAutoSeq = gVal.STR_UserInfo['AutoSeq']
		if inClear==True :
			### クリアの場合
			wAutoSeq = 0
		else:
			wAutoSeq += 1
		
		#############################
		# データ登録
		wQy = "update tbl_user_data set "
		wQy = wQy + "auto_seq = " + str( wAutoSeq ) + " "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# データをグローバルに反映
		gVal.STR_UserInfo['AutoSeq'] = wAutoSeq
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes



#####################################################
# 相互いいね停止設定
#####################################################
	def GetMfvStop(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetMfvStop"
		
		#############################
		# データ取得
		wQy = "select mfvstop, mfvstop_date "
		wQy = wQy + "from tbl_user_data "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# 取得チェック
		if len( wARR_DBData )!= 1 :
			##失敗
			wRes['Reason'] = "Get mfvstop name is not one: account=" + str(inAccount) + " num=" + str( len( wARR_DBData ) )
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# データをグローバルに反映
		gVal.STR_UserInfo['mfvstop']      = wARR_DBData[0]['mfvstop']
		gVal.STR_UserInfo['mfvstop_date'] = str(wARR_DBData[0]['mfvstop_date'])
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def SetMfvStop( self, inSet=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetMfvStop"
		
		#############################
		# 値変更
		if inSet==True :
			### セットの場合
			wMFvStop      = True
			wMFvStop_Date = str(gVal.STR_Time['TimeDate'])
		else:
			wMFvStop      = False
			wMFvStop_Date = gVal.DEF_TIMEDATE
		
		#############################
		# データ登録
		wQy = "update tbl_user_data set "
		wQy = wQy + "mfvstop = " + str( wMFvStop ) + ", "
		wQy = wQy + "mfvstop_date = '" + str( wMFvStop_Date ) + "' "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# データをグローバルに反映
		gVal.STR_UserInfo['mfvstop']      = wMFvStop
		gVal.STR_UserInfo['mfvstop_date'] = wMFvStop_Date
		
		#############################
		# ログに記録する
		if wMFvStop==True :
			wStr = "● 相互いいね停止 設定"
		else:
			wStr = "〇 相互いいね停止 解除"
		gVal.OBJ_L.Log( "SC", wRes, wStr )
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes



#####################################################
# いいね情報
#####################################################
	def InsertFavoData( self, inUser ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "InsertFavoData"
		
		#############################
		# ユーザ情報の加工
		wID = str(inUser['id'])
		wScreenName = inUser['screen_name']
		
		#############################
		# SQLの作成
		wQy = "insert into tbl_favouser_data values ("
		wQy = wQy + "'" + gVal.STR_UserInfo['Account'] + "', "		# 記録したユーザ(Twitter ID)
		wQy = wQy + "'" + str( gVal.STR_Time['TimeDate'] ) + "', "	# 登録日時
		wQy = wQy + "'" + str( gVal.STR_Time['TimeDate'] ) + "', "	# 更新日時(最終)
		                                                              
		wQy = wQy + "False, "										# 自動削除禁止 true=削除しない
		                                                              
		wQy = wQy + "'" + wID + "', "								# Twitter ID(数値)
		wQy = wQy + "'" + wScreenName + "', "						# Twitter ユーザ名(英語)
		wQy = wQy + "'" + gVal.DEF_NOTEXT + "', "					# レベルタグ(ユーザの親密度 指標)
		                                                              
		wQy = wQy + "'" + gVal.DEF_TIMEDATE + "', "					# トロフィー送信日時
		wQy = wQy + "0, "											# トロフィー送信回数(累計)
		
		wQy = wQy + "'" + gVal.DEF_NOTEXT + "', "					# いいね受信(このユーザがいいねした) ツイートID
		wQy = wQy + "'" + gVal.DEF_TIMEDATE + "', "					# いいね受信日時
		wQy = wQy + "0, "											# いいね受信回数(総数)
		wQy = wQy + "0, "											# いいね受信回数(今周)
		                                                              
		wQy = wQy + "'" + gVal.DEF_NOTEXT + "', "					# いいね送信(このユーザのツイート) ツイートID
		wQy = wQy + "'" + gVal.DEF_TIMEDATE + "', "					# いいね送信日時
		wQy = wQy + "0, "											# いいね送信回数(総数)
		                                                              
		wQy = wQy + "'" + gVal.DEF_TIMEDATE + "', "					# リスト日時
		                                                              
		wQy = wQy + "False, "										# フォロー者 true=フォロー者
		wQy = wQy + "'" + gVal.DEF_TIMEDATE + "', "					# フォロー日時
		wQy = wQy + "False, "										# フォロワー(被フォロー) true=フォロワー
		wQy = wQy + "'" + gVal.DEF_TIMEDATE + "', "					# 被フォロー日時
		
		wQy = wQy + "'', "											# memo
		wQy = wQy + "0  "											# 連ファボカウント
###		wQy = wQy + "0  "											# 非絡み回数
		wQy = wQy + ") ;"
		
		#############################
		# SQLの実行
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		self.ARR_FollowerDataID.append( wID )
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def GetFavoData(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetFavoData"
		
		wRes['Responce'] = {}
		#############################
		# リムーブ もしくは ブロックでTwitterから完全リムーブされたか
		#   DB上フォロー者 もしくは フォロワーを抽出
		wQy = "select * from tbl_favouser_data where "
		wQy = wQy + "twitterid = '" + gVal.STR_UserInfo['Account'] + "' and "
		wQy = wQy + "( myfollow = True or "
		wQy = wQy + "follower = True ) "
		wQy = wQy + ";"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# 添え字をIDに差し替える
		wARR_RateFavoDate = gVal.OBJ_DB_IF.ChgDataID( wARR_DBData )
		
		wRes['Responce'] = wARR_RateFavoDate
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
###	def GetFavoDataOne( self, inUser, inFLG_New=True ):
	def GetFavoDataOne( self, inUser=None, inID=None, inFLG_New=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetFavoDataOne"
		
		wRes['Responce'] = {
			"Data"		: None,
			"FLG_New"	: False
		}
		#############################
		# ユーザ情報の加工
###		wID = str(inUser['id'])
###		wScreenName = inUser['screen_name']
		if inUser!=None :
			if "id" in inUser :
				wID = str(inUser['id'])
			else:
				wRes['Reason'] = "inUser type error: " + str(inUser)
				gVal.OBJ_L.Log( "D", wRes )
				return wRes
		else:
			if inID!=None :
				wID = str(inID)
			else:
				wRes['Reason'] = "inID is none"
				gVal.OBJ_L.Log( "D", wRes )
				return wRes
		
		#############################
		# DBのいいね情報取得
		wQy = "select * from tbl_favouser_data where "
		wQy = wQy + "twitterid = '" + gVal.STR_UserInfo['Account'] + "' and "
		wQy = wQy + "id = '" + str( wID ) + "' "
		wQy = wQy + ";"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 1個取得できたか
		if len(wResDB['Responce']['Data'])==0 :
			if inFLG_New==True :
				### 新規モードであれば作成する
				wResDB = gVal.OBJ_DB_IF.InsertFavoData( inUser )
				if wResDB['Result']!=True :
					###失敗
					wRes['Reason'] = "InsertFavoData is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				### DBのいいね情報取得
				wQy = "select * from tbl_favouser_data where "
				wQy = wQy + "twitterid = '" + gVal.STR_UserInfo['Account'] + "' and "
				wQy = wQy + "id = '" + str( wID ) + "' "
				wQy = wQy + ";"
				
				wResDB = self.OBJ_DB.RunQuery( wQy )
				wResDB = self.OBJ_DB.GetQueryStat()
				if wResDB['Result']!=True :
					##失敗
					wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				
				if len(wResDB['Responce']['Data'])!=1 :
					## 1個ではない
					wRes['Reason'] = "Get data is failed(2): id=" + str(wID)
					gVal.OBJ_L.Log( "D", wRes )
					return wRes
				
				wRes['Responce']['FLG_New'] = True
			
			else:
				## ないのは正常で返す(ResponceはNoneのまま)
				wRes['Result'] = True
				return wRes
		
		elif len(wResDB['Responce']['Data'])!=1 :
			## 1個ではない
			wRes['Reason'] = "Get data is failed(1): id=" + str(wID)
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_RateFavoData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		wRes['Responce']['Data'] = wARR_RateFavoData[0]
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	# いいね情報：受信更新
	#####################################################
	def UpdateFavoData_Recive( self, inUser, inData, inFavoData, inCountUp=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "UpdateFavoData_Recive"
		
		wID = inUser['id']
		wScreenName = inUser['screen_name']
		
		wFavoID   = str( inData['id'] )
		wCnt      = inFavoData['rfavo_cnt']
		wNowCnt   = inFavoData['rfavo_n_cnt']
		if inCountUp==True :
			wCnt    += 1
			wNowCnt += 1
		
		#############################
		# 更新
		wQy = "update tbl_favouser_data set "
		wQy = wQy + "screen_name = '" + wScreenName + "', "
		
		wQy = wQy + "rfavo_cnt = " + str( wCnt ) + ", "
		wQy = wQy + "rfavo_n_cnt = " + str( wNowCnt ) + ", "
		wQy = wQy + "rfavo_id = '" + wFavoID + "', "
		wQy = wQy + "rfavo_date = '" + str( gVal.STR_Time['TimeDate'] ) + "', "
		
		wQy = wQy + "upddate = '" + str( gVal.STR_Time['TimeDate'] ) + "' "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "'"
		wQy = wQy + " and id = '" + str(wID) + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	# いいね情報：いいね送信更新
	#####################################################
	def UpdateFavoData_Put( self, inUser, inFavoID, inFavoData, inCountUp=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "UpdateListFavoData"
		
		#############################
		# いいねIDが一緒なら更新しない
		if str(inFavoData['pfavo_id'])==inFavoID :
			wRes['Result'] = True
			return wRes
		
		wID = inUser['id']
		wScreenName = inUser['screen_name']
		
		wFavoID   = str( inFavoID )
		wCnt      = inFavoData['pfavo_cnt']
		if inCountUp==True :
			wCnt    += 1
		
		#############################
		# 更新
		wQy = "update tbl_favouser_data set "
		wQy = wQy + "screen_name = '" + wScreenName + "', "
		
		wQy = wQy + "pfavo_cnt = " + str( wCnt ) + ", "
		wQy = wQy + "pfavo_id = '" + wFavoID + "', "
		wQy = wQy + "pfavo_date = '" + str( gVal.STR_Time['TimeDate'] ) + "', "
		
		wQy = wQy + "upddate = '" + str( gVal.STR_Time['TimeDate'] ) + "' "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "'"
		wQy = wQy + " and id = '" + str(wID) + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	# いいね情報：リスト通知情報更新
	#####################################################
	def UpdateFavoData_ListIndData( self, inUser ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "UpdateFavoData_ListIndData"
		
		wID = inUser['id']
		wScreenName = inUser['screen_name']
		#############################
		# 更新
		wQy = "update tbl_favouser_data set "
		wQy = wQy + "screen_name = '" + wScreenName + "', "
		wQy = wQy + "list_ind_date = '" + str(gVal.STR_Time['TimeDate']) + "', "
		
		wQy = wQy + "upddate = '" + str( gVal.STR_Time['TimeDate'] ) + "' "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "'"
		wQy = wQy + " and id = '" + str(wID) + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	# いいね情報：いいね送信更新
	#####################################################
	def UpdateFavoData_SendFavoInfo( self, inID, inFavoData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "UpdateFavoData_SendFavoInfo"
		
		wCnt = inFavoData['send_cnt']
		wCnt += 1
		
		#############################
		# 更新
		wQy = "update tbl_favouser_data set "
		wQy = wQy + "send_date = '" + str( gVal.STR_Time['TimeDate'] ) + "', "
		wQy = wQy + "send_cnt = " + str( wCnt ) + ", "
		
		wQy = wQy + "upddate = '" + str( gVal.STR_Time['TimeDate'] ) + "' "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' "
		wQy = wQy + " and id = '" + str(inID) + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	# いいね情報：フォロー情報更新
	#####################################################
	def UpdateFavoData_Follower( self, inID, inFLG_MyFollow=None, inFLG_Follower=None, inUserLevel=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "UpdateFavoData_Follower"
		
		#############################
		# 入力チェック
		if inFLG_MyFollow==None and inFLG_Follower==None :
			wRes['Reason'] = "set input is both None"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if inFLG_Follower==None and (inFLG_MyFollow!=True and inFLG_MyFollow!=False) :
			wRes['Reason'] = "set inFLG_MyFollow is not bool"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if inFLG_MyFollow==None and (inFLG_Follower!=True and inFLG_Follower!=False) :
			wRes['Reason'] = "set inFLG_Follower is not bool"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 更新
		
		#############################
		# フォロー者・フォロワー なし→あり
		if inFLG_MyFollow==True and inFLG_Follower==True :
			wQy = "update tbl_favouser_data set "
			wQy = wQy + "myfollow = True, " 
			wQy = wQy + "myfollow_date = '" + str(gVal.STR_Time['TimeDate']) + "', "
			wQy = wQy + "follower = True, "
			wQy = wQy + "follower_date = '" + str(gVal.STR_Time['TimeDate']) + "', "
			
			wQy = wQy + "upddate = '" + str( gVal.STR_Time['TimeDate'] ) + "' "
			wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "'"
			wQy = wQy + " and id = '" + str(inID) + "' ;"
		
		#############################
		# フォロー者・フォロワー あり→なし
		elif inFLG_MyFollow==False and inFLG_Follower==False :
			wQy = "update tbl_favouser_data set "
			wQy = wQy + "myfollow = False, "
			wQy = wQy + "follower = False, "
			
			wQy = wQy + "upddate = '" + str( gVal.STR_Time['TimeDate'] ) + "' "
			wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "'"
			wQy = wQy + " and id = '" + str(inID) + "' ;"
		
		#############################
		# フォロー者 なし→あり
		# フォロワー あり→なし
		elif inFLG_MyFollow==True and inFLG_Follower==False :
			wQy = "update tbl_favouser_data set "
			wQy = wQy + "myfollow = True, "
			wQy = wQy + "myfollow_date = '" + str(gVal.STR_Time['TimeDate']) + "', "
			wQy = wQy + "follower = False, "
			
			wQy = wQy + "upddate = '" + str( gVal.STR_Time['TimeDate'] ) + "' "
			wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "'"
			wQy = wQy + " and id = '" + str(inID) + "' ;"
		
		#############################
		# フォロー者 あり→なし
		# フォロワー なし→あり
		elif inFLG_MyFollow==False and inFLG_Follower==True :
			wQy = "update tbl_favouser_data set "
			wQy = wQy + "myfollow = False, "
			wQy = wQy + "follower = True, "
			wQy = wQy + "follower_date = '" + str(gVal.STR_Time['TimeDate']) + "', "
			
			wQy = wQy + "upddate = '" + str( gVal.STR_Time['TimeDate'] ) + "' "
			wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' "
			wQy = wQy + " and id = '" + str(inID) + "' ;"
		
		#############################
		# フォロー者 なし→あり
		elif inFLG_MyFollow==True :
			wQy = "update tbl_favouser_data set "
			wQy = wQy + "myfollow = True, "
			wQy = wQy + "myfollow_date = '" + str(gVal.STR_Time['TimeDate']) + "', "
			
			wQy = wQy + "upddate = '" + str( gVal.STR_Time['TimeDate'] ) + "' "
			wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' "
			wQy = wQy + " and id = '" + str(inID) + "' ;"
		
		#############################
		# フォロー者 あり→なし
		elif inFLG_MyFollow==False :
			wQy = "update tbl_favouser_data set "
			wQy = wQy + "myfollow = False, "
			
			wQy = wQy + "upddate = '" + str( gVal.STR_Time['TimeDate'] ) + "' "
			wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' "
			wQy = wQy + " and id = '" + str(inID) + "' ;"
		
		#############################
		# フォロワー なし→あり
		elif inFLG_Follower==True :
			wQy = "update tbl_favouser_data set "
			wQy = wQy + "follower = True, "
			wQy = wQy + "follower_date = '" + str(gVal.STR_Time['TimeDate']) + "', "
			
			wQy = wQy + "upddate = '" + str( gVal.STR_Time['TimeDate'] ) + "' "
			wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' "
			wQy = wQy + " and id = '" + str(inID) + "' ;"
		
		#############################
		# フォロワー あり→なし
		else :
			wQy = "update tbl_favouser_data set "
			wQy = wQy + "follower = False, "
			
			wQy = wQy + "upddate = '" + str( gVal.STR_Time['TimeDate'] ) + "' "
			wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' "
			wQy = wQy + " and id = '" + str(inID) + "' ;"
		
		#############################
		# クエリ実行
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	# いいね情報：ユーザレベル更新
	#####################################################
	def UpdateFavoData_UserLevel( self, inID, inUserLevel ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "UpdateFavoData_UserLevel"
		
		#############################
		# ユーザレベルを取得する
		wQy = "select screen_name, level_tag from tbl_favouser_data where "
		wQy = wQy + "twitterid = '" + gVal.STR_UserInfo['Account'] + "'"
###		wQy = wQy + " and id = '" + str(inID) + "' ;"
		wQy = wQy + " and id = '" + str(inID) + "' "
		wQy = wQy + ";"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		if len(wARR_DBData)!=1 :
			### 1つだけでなければNG（ありえない？）
			wRes['Reason'] = "data is not one: user id=" + str(inID)
			gVal.OBJ_L.Log( "A", wRes )
			return wRes
		
		### 現在のユーザレベル
		wRateUserLevel = wARR_DBData[0]['level_tag']
		
		#############################
		# ユーザレベルに変化がなければ終わり
		if wRateUserLevel==inUserLevel :
			wRes['Result'] = True
			return wRes
		
		#############################
		# ユーザレベルの更新
		wQy = "update tbl_favouser_data set "
		wQy = wQy + "level_tag = '" + inUserLevel + "', "
		
		wQy = wQy + "upddate = '" + str( gVal.STR_Time['TimeDate'] ) + "' "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "'"
		wQy = wQy + " and id = '" + str(inID) + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# ログの記録
		if wRateUserLevel==gVal.DEF_NOTEXT :
			### 新規の設定
			wStr = "ユーザレベル設定: user=" + str(wARR_DBData[0]['screen_name']) + " level=" + inUserLevel
		else:
			### レベル変更
			wStr = "ユーザレベル変更: user=" + str(wARR_DBData[0]['screen_name']) + " level:変更前=" + wRateUserLevel + " 変更後=" + inUserLevel
		
###		gVal.OBJ_L.Log( "RC", wRes, wStr )
		gVal.OBJ_L.Log( "RC", wRes, wStr, inID=inID )
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	# いいね情報：削除禁止
	#####################################################
	def UpdateFavoData_FLG_Save( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "UpdateFavoData_FLG_Save"
		
		#############################
		# 自動削除禁止を取得する
		wQy = "select screen_name, flg_save from tbl_favouser_data where "
		wQy = wQy + "twitterid = '" + gVal.STR_UserInfo['Account'] + "'"
###		wQy = wQy + " and id = '" + str(inID) + "' ;"
		wQy = wQy + " and id = '" + str(inID) + "' "
		wQy = wQy + ";"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		if len(wARR_DBData)!=1 :
			### 1つだけでなければNG（ありえない？）
			wRes['Reason'] = "data is not one: user id=" + str(inID)
			gVal.OBJ_L.Log( "A", wRes )
			return wRes
		
		### フラグを反転
		wFLG_Save = wARR_DBData[0]['flg_save']
		if wFLG_Save==True :
			wFLG_Save = False
		
		#############################
		# 更新
		wQy = "update tbl_favouser_data set "
		wQy = wQy + "flg_save = " + wFLG_Save + ", "
		
		wQy = wQy + "upddate = '" + str( gVal.STR_Time['TimeDate'] ) + "' "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "'"
		wQy = wQy + " and id = '" + str(inID) + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# ログの記録
		if wFLG_Save==True :
			### 新規の設定
			wStr = "自動削除禁止: ON"
		else:
			### レベル変更
			wStr = "自動削除禁止: OFF"
		wStr = wStr + " : user=" + str(wResDB['Responce']['Data'][0]['screen_name'])
		
###		gVal.OBJ_L.Log( "RC", wRes, wStr )
		gVal.OBJ_L.Log( "RC", wRes, wStr, inID=inID )
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	# いいね情報：memo
	#####################################################
	def UpdateFavoData_memo( self, inID, inMemo ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "UpdateFavoData_memo"
		
		#############################
		# 更新
		wQy = "update tbl_favouser_data set "
		wQy = wQy + "memo = '" + str(inMemo) + "', "
		
		wQy = wQy + "upddate = '" + str( gVal.STR_Time['TimeDate'] ) + "' "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "'"
		wQy = wQy + " and id = '" + str(inID) + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	# 連ファボカウント更新
	#####################################################
###	def UpdateFavoData_RenFavo( self, inID, inCnt, inBotCnt=None ):
	def UpdateFavoData_RenFavo( self, inID, inCnt ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "UpdateFavoData_RenFavo"
		
		#############################
		# 更新
		wQy = "update tbl_favouser_data set "
		wQy = wQy + "renfavo_cnt = " + str(inCnt) + ", "
###		if inBotCnt!=None :
###			wQy = wQy + "renbot_cnt = " + str(inBotCnt) + ", "
###		
		wQy = wQy + "upddate = '" + str( gVal.STR_Time['TimeDate'] ) + "' "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "'"
		wQy = wQy + " and id = '" + str(inID) + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	# いいね情報：連ファボ一覧
	#####################################################
	def GetFavoData_RenFavoList(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetFavoData_RenFavoList"
		
		#############################
		# ユーザレベルを取得する
		wQy = "select id, screen_name, level_tag, renfavo_cnt, rfavo_date, rfavo_id, rfavo_cnt, rfavo_n_cnt from tbl_favouser_data where "
		wQy = wQy + "twitterid = '" + gVal.STR_UserInfo['Account'] + "'"
		wQy = wQy + " and renfavo_cnt > 0 "
		wQy = wQy + ";"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# 添え字をIDに差し替える
		wARR_RateFavoDate = gVal.OBJ_DB_IF.ChgDataID( wARR_DBData )
		
		wRes['Responce'] = wARR_RateFavoDate
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	# いいね情報：いいね送信
	#####################################################
	def GetFavoData_SendFavo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetFavoData_SendFavo"
		
		wRes['Responce'] = {}
		#############################
		# 今週受信回数が1以上のいいね情報を抽出する
#		wQy = "select send_cnt, rfavo_n_cnt from tbl_favouser_data where "
		wQy = "select * from tbl_favouser_data where "
		wQy = wQy + "twitterid = '" + gVal.STR_UserInfo['Account'] + "' and "
		wQy = wQy + "rfavo_n_cnt > 0 "
		wQy = wQy + ";"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# 添え字をIDに差し替える
		wARR_RateFavoDate = gVal.OBJ_DB_IF.ChgDataID( wARR_DBData )
		
		wRes['Responce'] = wARR_RateFavoDate
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

###	#####################################################
###	# いいね情報：非絡みユーザ一覧
###	#####################################################
###	def UpdateFavoData_UserBList( self ):
###	def UpdateFavoData_UserBList( self, inAutoOnly=False ):
###		#############################
###		# 応答形式の取得
###		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
###		wRes = CLS_OSIF.sGet_Resp()
###		wRes['Class'] = "CLS_DB_IF"
###		wRes['Func']  = "UpdateFavoData_UserBList"
###		
###		#############################
###		# ユーザレベルを取得する
###		wQy = "select id, screen_name, level_tag, myfollow, follower, send_cnt from tbl_favouser_data where "
###		wQy = "select id, screen_name, level_tag, myfollow, follower, send_cnt, renfavo_cnt, renbot_cnt from tbl_favouser_data where "
###		wQy = wQy + "twitterid = '" + gVal.STR_UserInfo['Account'] + "'"
###		wQy = wQy + " and level_tag = 'B-' "
###		wQy = wQy + ";"
###		wQy = wQy + " and ("
###		wQy = wQy + " level_tag = 'G' or "
###		wQy = wQy + " level_tag = 'G+' or "
###		wQy = wQy + " level_tag = 'H' or "
###		wQy = wQy + " level_tag = 'H+' "
###		wQy = wQy + " level_tag = 'G' or level_tag = 'H' "
###		if inAutoOnly==False :
###			wQy = wQy + " or level_tag = 'G+' or level_tag = 'H+' "
###		wQy = wQy + ") ;"
###		
###		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy )
###		if wResDB['Result']!=True :
###			wRes['Reason'] = "Run Query is failed"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		
###		#############################
###		# 辞書型に整形
###		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
###		
###		#############################
###		# 添え字をIDに差し替える
###		wARR_RateFavoDate = gVal.OBJ_DB_IF.ChgDataID( wARR_DBData )
###		
###		wRes['Responce'] = wARR_RateFavoDate
###		#############################
###		# 正常
###		wRes['Result'] = True
###		return wRes

	#####################################################
	# いいね情報：被ブロックユーザ一覧
	#####################################################
	def GetFavoData_BlockList( self ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetFavoData_BlockList"
		
		#############################
		# ユーザレベルを取得する
		wQy = "select id, screen_name from tbl_favouser_data where "
		wQy = wQy + "twitterid = '" + gVal.STR_UserInfo['Account'] + "'"
		wQy = wQy + " and level_tag = 'Z' "
		wQy = wQy + ";"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# 添え字をIDに差し替える
		wARR_RateFavoDate = gVal.OBJ_DB_IF.ChgDataID( wARR_DBData )
		
		wRes['Responce'] = wARR_RateFavoDate
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def UpdateFavoData_SendFavo( self, inARR_ID=[] ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "UpdateFavoData_SendFavo"
		
		for wID in inARR_ID :
			wID = str(wID)
			
			#############################
			# いいね情報を抽出する
			wQy = "select send_cnt from tbl_favouser_data where "
			wQy = wQy + "twitterid = '" + gVal.STR_UserInfo['Account'] + "' and "
			wQy = wQy + "id = '" + str(wID) + "' "
			wQy = wQy + ";"
			
			wResDB = gVal.OBJ_DB_IF.RunQuery( wQy )
			if wResDB['Result']!=True :
				wRes['Reason'] = "Run Query is failed"
				gVal.OBJ_L.Log( "B", wRes )
				continue
			
			#############################
			# 辞書型に整形
			wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
			
			if len(wARR_DBData)!=1 :
				### 1つだけでなければNG（ありえない？）
				wRes['Reason'] = "data is not one: user id=" + str(wID)
				gVal.OBJ_L.Log( "A", wRes )
				continue
			
			#############################
			# カウントアップ
			wCnt = wARR_DBData[0]['send_cnt']
			wCnt += 1
			
			#############################
			# 更新
			wQy = "update tbl_favouser_data set "
			wQy = wQy + "send_cnt = " + str(wCnt) + ", "
			
			wQy = wQy + "upddate = '" + str( gVal.STR_Time['TimeDate'] ) + "' "
			wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "'"
			wQy = wQy + " and id = '" + str(wID) + "' ;"
			
			wResDB = gVal.OBJ_DB_IF.RunQuery( wQy )
			if wResDB['Result']!=True :
				wRes['Reason'] = "Run Query is failed(1)"
				gVal.OBJ_L.Log( "B", wRes )
				continue
		
		#############################
		# 今週の受信回数クリア
		wQy = "update tbl_favouser_data set "
		wQy = wQy + "rfavo_n_cnt = 0 "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "'"
		wQy = wQy + " ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQy )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed(2)"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	# いいね情報：削除
	#####################################################
	def DeleteFavoData(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "DeleteFavoData"
		
		#############################
		# DBのいいね情報取得(IDのみ)
		wQy = "select id from tbl_favouser_data where "
		wQy = wQy + "twitterid = '" + gVal.STR_UserInfo['Account'] + "' and "
		wQy = wQy + "myfollow = False and "
		wQy = wQy + "follower = False "
		wQy = wQy + ";"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed: RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# リスト型に整形
		wARR_DBDataID = gVal.OBJ_DB_IF.ChgList( wResDB['Responce'] )
		
		for wID in wARR_DBDataID :
			wID = str(wID)
			
			#############################
			# DBのいいね情報取得
			wQy = "select * from tbl_favouser_data where "
			wQy = wQy + "twitterid = '" + gVal.STR_UserInfo['Account'] + "' and "
			wQy = wQy + "id = '" + wID + "' "
			wQy = wQy + ";"
			
			wResDB = self.OBJ_DB.RunQuery( wQy )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed: RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			#############################
			# 1個取得できたか
			if len(wResDB['Responce']['Data'])==0 :
				## ないのは正常で返す(ResponceはNoneのまま)
				wRes['Result'] = True
				return wRes
			if len(wResDB['Responce']['Data'])!=1 :
				## 1個ではない
				wRes['Reason'] = "Get data is failed : id=" + str(inID)
				gVal.OBJ_L.Log( "D", wRes )
				return wRes
			
			#############################
			# 辞書型に整形
			wARR_RateFavoData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
			wARR_RateFavoData = wARR_RateFavoData[0]	#1個しかないので添え字を消す
			
			#############################
			# 自動削除禁止ならスキップ
			if wARR_RateFavoData['flg_save']==True :
				continue
			
			#############################
			# ユーザレベル除外
###			if wARR_RateFavoData['level_tag']!="D-" and wARR_RateFavoData['level_tag']!="E-" and wARR_RateFavoData['level_tag']!="H-" and wARR_RateFavoData['level_tag']!="L" and \
###			   wARR_RateFavoData['level_tag']!="Z" and wARR_RateFavoData['level_tag']!="Z-" :
###			if wARR_RateFavoData['level_tag']!="D-" and wARR_RateFavoData['level_tag']!="E-" and wARR_RateFavoData['level_tag']!="H-" :
			if wARR_RateFavoData['level_tag']!="D-" and wARR_RateFavoData['level_tag']!="E-" :
				continue
			
			#############################
			# 削除対象か
			#   いいね受信日といいね送信日が初期値の場合
			#     登録日が期間を過ぎてたら削除
			#   いいね受信日 もしくは いいね送信日 が初期値でない場合
			#     いいね受信日が期間を過ぎてたら削除
			if str( wARR_RateFavoData['rfavo_date'] )==gVal.DEF_TIMEDATE and \
			   str( wARR_RateFavoData['pfavo_date'] )==gVal.DEF_TIMEDATE :
				wCHR_DelTimeDate = str( wARR_RateFavoData['regdate'] )
			else:
				if str( wARR_RateFavoData['rfavo_date'] )!=gVal.DEF_TIMEDATE :
					wCHR_DelTimeDate = str( wARR_RateFavoData['rfavo_date'] )
				else:
					wCHR_DelTimeDate = str( wARR_RateFavoData['pfavo_date'] )
			
			if wARR_RateFavoData['level_tag']=="F" :
				wThreshold = gVal.DEF_STR_TLNUM['forFavoDataDelLevelFSec']
			
###			elif wARR_RateFavoData['level_tag']=="L" or wARR_RateFavoData['level_tag']=="Z" or wARR_RateFavoData['level_tag']=="Z-" :
			elif wARR_RateFavoData['level_tag']=="L" or wARR_RateFavoData['level_tag']=="Z" :
				wThreshold = gVal.DEF_STR_TLNUM['forFavoDataDelHardSec']
			
			else:
				wThreshold = gVal.DEF_STR_TLNUM['forFavoDataDelSec']
			
			wGetLag = CLS_OSIF.sTimeLag( wCHR_DelTimeDate, inThreshold=wThreshold )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==False :
				### 規定以内は除外
				continue
			
			#############################
			# DBから削除
			wQy = "delete from tbl_favouser_data where "
			wQy = wQy + "twitterid = '" + gVal.STR_UserInfo['Account'] + "' and "
			wQy = wQy + "id = '" + wID + "' "
			wQy = wQy + ";"
			
			wResDB = self.OBJ_DB.RunQuery( wQy )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed: RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			gVal.OBJ_L.Log( "N", wRes, "DB: Delete FavoData: " + str( wARR_RateFavoData['screen_name'] ) )
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# 検索ワード
#####################################################
	def GetSearchWord(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetSearchWord"
		
		#############################
		# データベースを取得
		wQy = "select * from tbl_search_word "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return False
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		wARR_Data = {}
		#############################
		# 除外文字データを登録する
		wKeylist = list( wARR_DBData.keys() )
		wListNo = 1
		for wKey in wKeylist :
			wCell = {
				"list_number"	: wListNo,
				"regdate"		: str(wARR_DBData[wKey]['regdate']),
				"upddate"		: str(wARR_DBData[wKey]['upddate']),
				"valid"			: wARR_DBData[wKey]['valid'],
				"word"			: str(wARR_DBData[wKey]['word']),
				"hit_cnt"		: wARR_DBData[wKey]['hit_cnt'],
				"favo_cnt"		: wARR_DBData[wKey]['favo_cnt'],
				"auto_follow"	: wARR_DBData[wKey]['auto_follow']
			}
			wARR_Data.update({ str(wListNo) : wCell })
			wListNo += 1
		
		#############################
		# グローバルに反映
		gVal.ARR_SearchData = wARR_Data
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def SetSearchWord( self, inWord ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetSearchWord"
		
		#############################
		# 入力チェック
		wWord = inWord.replace( "'", "''" )
		
		wFlg_Detect = False
		wKeylist = list( gVal.ARR_SearchData.keys() )
		for wIndex in wKeylist :
			if gVal.ARR_SearchData[wIndex]['word']==wWord :
				wFlg_Detect = True
				break
		if wFlg_Detect==True :
			##失敗
			wRes['Reason'] = "Dual word input: word=" + wWord
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# リスト番号の取得
		wKeylist = list( gVal.ARR_SearchData.keys() )
		wListNo = 1
		for wKey in wKeylist :
			### ダブり登録はスキップ
			if gVal.ARR_SearchData[wKey]['list_number']!=wListNo :
				###決定
				break
			wListNo += 1
		
		#############################
		# 登録データを作成する
		
		wCell = {
			"list_number"	: wListNo,
			"regdate"		: str( gVal.STR_Time['TimeDate'] ),
			"upddate"		: str( gVal.STR_Time['TimeDate'] ),
			"valid"			: True,
			"word"			: wWord,
			"hit_cnt"		: 0,
			"favo_cnt"		: 0,
			"auto_follow"	: False
		}
		
		#############################
		# データベースに登録する
		wQy = "insert into tbl_search_word values ("
		wQy = wQy + "'" + gVal.STR_UserInfo['Account'] + "', "
		wQy = wQy + "'" + str( wCell['regdate'] ) + "', "
		wQy = wQy + "'" + str( wCell['upddate'] ) + "', "
		wQy = wQy + str( wCell['valid'] ) + ", "
		wQy = wQy + "'" + str( wCell['word'] ) + "', "
		wQy = wQy + str( wCell['hit_cnt'] ) + ", "
		wQy = wQy + str( wCell['favo_cnt'] ) + ", "
		wQy = wQy + str( wCell['auto_follow'] ) + " "
		wQy = wQy + ") ;"
		
		#############################
		# クエリの実行
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# グローバルを更新する
		gVal.ARR_SearchData.update({ str(wListNo) : wCell })
		
		wRes['Result'] = True
		return wRes

	#####################################################
	def ValidSearchWord( self, inIndex ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "ValidSearchWord"
		
		wFLG_Valid = gVal.ARR_SearchData[inIndex]['valid']
		#############################
		# 有効/無効の切り替え
		if wFLG_Valid==True :
			wFLG_Valid = False
		else:
			wFLG_Valid = True
		
		wWord = gVal.ARR_SearchData[inIndex]['word']
		#############################
		# データベースを更新する
		wQy = "update tbl_search_word set "
		wQy = wQy + "valid = " + str(wFLG_Valid) + " "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' and "
		wQy = wQy + "word = '" + wWord + "' "
		wQy = wQy + ";"
		
		#############################
		# クエリの実行
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# データ変更
		gVal.ARR_SearchData[inIndex]['valid'] = wFLG_Valid
		
		wRes['Result'] = True
		return wRes

	#####################################################
	def SearchWord_AutoFollow( self, inIndex ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SearchWord_AutoFollow"
		
		wFLG_AutoFollow = gVal.ARR_SearchData[inIndex]['auto_follow']
		#############################
		# 有効/無効の切り替え
		if wFLG_AutoFollow==True :
			wFLG_AutoFollow = False
		else:
			wFLG_AutoFollow = True
		
		wWord = gVal.ARR_SearchData[inIndex]['word']
		#############################
		# データベースを更新する
		wQy = "update tbl_search_word set "
		wQy = wQy + "auto_follow = " + str(wFLG_AutoFollow) + " "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' and "
		wQy = wQy + "word = '" + wWord + "' "
		wQy = wQy + ";"
		
		#############################
		# クエリの実行
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# データ変更
		gVal.ARR_SearchData[inIndex]['auto_follow'] = wFLG_AutoFollow
		
		wRes['Result'] = True
		return wRes

	#####################################################
	def UpdateSearchWord( self, inIndex, inWord=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "UpdateSearchWord"
		
		#############################
		# 入力チェック
		wWord = inWord.replace( "'", "''" )
		
		#############################
		# 検索ワードの設定
		# 被ってるワードがないか
		wKeylist = list( gVal.ARR_SearchData.keys() )
		for wKey in wKeylist :
			if gVal.ARR_SearchData[wKey]['list_number']==inIndex :
				###自分のリストはスキップ
				continue
			
			if gVal.ARR_SearchData[wKey]['word']==inWord :
				##失敗
				wRes['Reason'] = "Dual word input: word=" + inWord
				gVal.OBJ_L.Log( "D", wRes )
				return wRes
		
		#############################
		# データベースを更新する
		wQy = "update tbl_search_word set "
		wQy = wQy + "word = '" + str(gVal.ARR_SearchData[inIndex]['word']) + "' "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' and "
		wQy = wQy + "word = '" + wWord + "' "
		wQy = wQy + ";"
		
		#############################
		# クエリの実行
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# データ変更
		gVal.ARR_SearchData[inIndex]['word'] = inWord
		
		wRes['Result'] = True
		return wRes

	#####################################################
	def CountSearchWord( self, inIndex, inHitCnt=1, inFavoCnt=1 ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "CountSearchWord"
		
		wWord    = gVal.ARR_SearchData[inIndex]['word']
		wHitCnt  = gVal.ARR_SearchData[inIndex]['hit_cnt'] + inHitCnt
		wFavoCnt = gVal.ARR_SearchData[inIndex]['favo_cnt'] + inFavoCnt
		#############################
		# データベースを更新する
		wQy = "update tbl_search_word set "
		wQy = wQy + "hit_cnt = " + str(wHitCnt) + ", "
		wQy = wQy + "favo_cnt = " + str(wFavoCnt) + ", "
		wQy = wQy + "upddate = '" + str( gVal.STR_Time['TimeDate'] ) + "' "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' and "
		wQy = wQy + "word = '" + wWord + "' "
		wQy = wQy + ";"
		
		#############################
		# クエリの実行
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# データ変更
		gVal.ARR_SearchData[inIndex]['upddate'] = str( gVal.STR_Time['TimeDate'] )
		gVal.ARR_SearchData[inIndex]['hit_cnt'] = wHitCnt
		gVal.ARR_SearchData[inIndex]['favo_cnt'] = wFavoCnt
		
		wRes['Result'] = True
		return wRes

	#####################################################
	def ClearSearchWord(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "ClearSearchWord"
		
		#############################
		# カウンタを0クリア
		wQy = "update tbl_search_word set "
		wQy = wQy + "hit_cnt = 0, "
		wQy = wQy + "favo_cnt = 0 "
		wQy = wQy + "upddate = '" + str( gVal.DEF_TIMEDATE ) + "' "
		wQy = wQy + "where twitterid = '" + inUserData['Account'] + "' ;"
		
		#############################
		# クエリの実行
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			CLS_OSIF.sErr( wRes )
			return wRes
		
		wRes['Result'] = True
		return wRes

	#####################################################
	def DeleteSearchWord( self, inIndex ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "DeleteSearchWord"
		
		wWord = gVal.ARR_SearchData[inIndex]['word']
		#############################
		# データベースから削除
		wQy = "delete from tbl_search_word "
		wQy = wQy + "where twitterid = '" + gVal.STR_UserInfo['Account'] + "' and "
		wQy = wQy + "word = '" + wWord + "' "
		wQy = wQy + ";"
		
		#############################
		# クエリの実行
		wResDB = self.OBJ_DB.RunQuery( wQy )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# データ削除
		del gVal.ARR_SearchData[inIndex]
		
		#############################
		# ログ記録
		gVal.OBJ_L.Log( "N", wRes, "DB: Delete SearchWord: index=" + str(inIndex) + " word=" + str( wWord ) )
		
		wRes['Result'] = True
		return wRes



