#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Misskey
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_misskey/
# ::Class    : Database I/F
#####################################################
from mysql_use import CLS_MySQL_Use

from traffic import CLS_Traffic
from ktime import CLS_TIME
from osif import CLS_OSIF
from gval import gVal
from mysql_com import CLS_MySQL_Com
#####################################################
class CLS_MySQL_IF() :
#####################################################
	OBJ_Parent = ""				# 親クラス実体
	OBJ_MySQL = ""				# DBオブジェクト



#####################################################
# Init
#####################################################
	def __init__( self, outRes, parentObj=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_MySQL_IF"
		wRes['Func']  = "__init__"
		
		pRes = outRes
		if parentObj==None :
			###親クラス実体の未設定
			pRes['Reason'] = "parentObj is none"
			pRes['Result']  = False
		else:
			self.OBJ_Parent = parentObj
			pRes['Result']  = True
		
		return



#####################################################
# DB接続
#####################################################
	def Connect(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_MySQL_IF"
		wRes['Func']  = "Connect"
		
		#############################
		# DB接続
		self.OBJ_MySQL = CLS_MySQL_Use()
		
		self.OBJ_MySQL.Connect( inData=gVal.STR_UserInfo )
		wSubRes = self.GetInfo()
		if wSubRes['Result']!=True :
			###失敗
			wStr = "Function is failed: OBJ_MySQL.Connect: "
			wStr = wStr + "FLG_Open: " + str( wSubRes['Responce']['FLG_Open'] )
			wStr = wStr + " " + str( wSubRes['Responce']['DB_Info'] )
			CLS_OSIF.sErr( wRes )
			
			###DB接続中なら切断する
			if wSubRes['FLG_Open']==True :
				self.Close()
			
			return wRes
		
		#############################
		# 処理表示
		if gVal.FLG_Test==True :
			wStr = "mysql: connect: "
			wStr = wStr + "DB_HOST: " + str( gVal.STR_UserInfo['DB_HOST'] )
			wStr = wStr + "DB_NAME: " + str( gVal.STR_UserInfo['DB_NAME'] )
			wStr = wStr + "DB_USER: " + str( gVal.STR_UserInfo['DB_USER'] )
			CLS_OSIF.sPrn( wStr )
		
		#############################
		# 正常
		wRes['Result'] = True	#正常
		return wRes



#####################################################
# DB切断
#####################################################
	def Close(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_MySQL_IF"
		wRes['Func']  = "Close"
		
		#############################
		# DB切断
		self.OBJ_MySQL.Close()
		
		#############################
		# 処理表示
		if gVal.FLG_Test==True :
			CLS_OSIF.sPrn( "mysql: disconnect" )
		
		#############################
		# 正常
		wRes['Result'] = True	#正常
		return wRes



#####################################################
# DB状態取得
#####################################################
	def GetInfo(self):
		return self.OBJ_MySQL.GetInfo()



#####################################################
# DB情報表示
#####################################################
	def ViewInfo(self):
		
		wFLG_Open = self.OBJ_MySQL.GetInfo()
		
		wStr =        "#############################" + '\n'
		wStr = wStr + "FLG_Open : " + str( wFLG_Open ) + '\n'
		wStr = wStr + '\n'
		wStr = wStr + "DB_HOST  : " + gVal.STR_UserInfo['DB_HOST'] + '\n'
		wStr = wStr + "DB_NAME  : " + gVal.STR_UserInfo['DB_NAME'] + '\n'
		wStr = wStr + "DB_USER  : " + gVal.STR_UserInfo['DB_USER'] + '\n'
		wStr = wStr + "DB_USER  : (ナイチョ) " + '\n'
		wStr = wStr + "#############################" + '\n'
		CLS_OSIF.sPrn( wStr )
		return



#####################################################
# クエリ実行
#####################################################
	def RunQuery( self, inQuery=None, inFLGtraffic=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_MySQL_IF"
		wRes['Func']  = "RunQuery"
		
		#############################
		# 実行結果の返送用
		wRes['Responce'] = {
			"Command"	: None,
			"Commit"	: False,
			"Data"		: []
		}
		
		#############################
		# コマンドの取得
		wSubRes = CLS_OSIF.sRe_Split( " ", inQuery )
		if wSubRes['Result']!=True :
			###失敗
			CLS_OSIF.sErr( "Function is failed: sRe_Split" )
			return wRes
		wCommand = wSubRes['After'][0]
		
		### 小文字化
		wSubRes = CLS_OSIF.sRe_Lower( wCommand )
		if wSubRes['Result']!=True :
			###失敗
			CLS_OSIF.sErr( "Function is failed: sRe_Lower" )
			return wRes
		wCommand = wSubRes['After']
		wRes['Responce']['Command'] = wCommand
		
		#############################
		# 実行
		wResDB = self.OBJ_MySQL.RunQuery( inQuery=inQuery, inCommand=wCommand )
		
		### 結果判定
		wSubRes = self.GetInfo()
		if wSubRes['Result']!=True :
			###失敗
			CLS_OSIF.sErr( "Function is failed: OBJ_MySQL.RunQuery: reason=" + wSubRes['Reason'] )
			return wRes
		
		#############################
		# 抽出コマンド
		if wCommand=="select" :
			if len(wSubRes['Data'])>0:
				wRes['Responce']['Data'] = wSubRes['Data']
		
		#############################
		# ログ記録
		# トラヒック記録
		if inFLGtraffic==True :
			gVal.OBJ_L.Log( "P", wRes, "query= "+inQuery, inID=wCommand )
			
			if wCommand=="create" or \
			   wCommand=="insert" :
				CLS_Traffic.sP( "db_ins" )
			
			elif wCommand=="update" :
				CLS_Traffic.sP( "db_up" )
			
			elif wCommand=="delete" or \
			     wCommand=="drop" :
				CLS_Traffic.sP( "db_del" )
			
			elif wCommand=="select" :
				CLS_Traffic.sP( "db_req" )
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	# 辞書型に整形
	def ChgDict( self, inData ):
		wARR_DBData = {}
		self.OBJ_MySQL.ChgDict( inData['Collum'], inData['Data'], outDict=wARR_DBData )
		return wARR_DBData

	#####################################################
	# リスト型に整形
	def ChgList( self, inData ):
		wARR_DBData = []
		self.OBJ_MySQL.ChgList( inData['Data'], outList=wARR_DBData )
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
	def GetRecordNum( self, inTableName=None ):
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
		
		wResDB = self.OBJ_MySQL.RunQuery( inQuery=inQuery, inCommand="select" )
		
		### 結果判定
		wSubRes = self.GetInfo()
		if wSubRes['Result']!=True :
			###失敗
			CLS_OSIF.sErr( "Function is failed: OBJ_MySQL.RunQuery: reason=" + wSubRes['Reason'] )
			return wRes
		
		#############################
		# レコード数の取り出し
		try:
			wNum = int( wResDB['Responce']['Data'][0][0] )
			wRes['Responce'] = wNum
		except ValueError:
			##失敗
			wRes['Reason'] = "Data is failer"
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# TBL_USER 操作
#####################################################
#####################################################
# TBL_USER：登録
#####################################################
	def USER_Regist( self, inID, inHost, inToken ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_MySQL_IF"
		wRes['Func']  = "USER_Regist"
		
		#############################
		# 時間を取得
		wTD = CLS_TIME.sGet()
		
		#############################
		# 既登録情報の取得
		wQy = "select * from tbl_user where "
		wQy = wQy + "id = '" + str( inID ) + "' ;"
		
		### クエリ実行
		wSubRes = self.RunQuery( inQuery=wQy )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "Function is failed: RunQuery(1)"
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		### 結果の取得
		wSubRes = self.GetInfo()
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "Function is failed: GetInfo(1): reason=" + wSubRes['Reason']
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		wQy = None
		#############################
		# 登録してなければ
		#   新規登録
		if len(wSubRes['Data'])==0 :
			wQy = "insert into tbl_user values ("
			wQy = wQy + "'" + str( inID ) + "',"				# ユーザ(アカウント)
			wQy = wQy + "'" + str( inHost ) + "',"				# アカウントのホスト名
			wQy = wQy + "'" + str( inToken ) + "',"				# misskeyアクセストークン
			wQy = wQy + "'" + str( wTD ) + "',"					# 登録日時
			wQy = wQy + "False,"								# 排他ロック true=ロックON
			wQy = wQy + "'" + str( gVal.DEF_TIMEDATE ) + "',"	# 排他日時
			wQy = wQy + "'" + str( gVal.DEF_TIMEDATE ) + "',"	# 排他獲得日時
			wQy = wQy + "'" + str( gVal.DEF_TIMEDATE ) + "',"	# 排他解除日時
			wQy = wQy + "0 " 									# 自動監視シーケンス
			wQy = wQy + ") ;"
		
		#############################
		# 登録されていればキーを更新する
		elif len(wSubRes['Data'])==1 :
			wQy = "update tbl_user set "
			wQy = wQy + "host = '"  + str( inHost ) + "', "
			wQy = wQy + "token = '" + str( inToken ) + "' "
			wQy = wQy + "where id = '" + str( inID ) + "' ;"
			
		#############################
		# 複数登録されてる？
		else:
			###ありえないルート
			wRes['Reason'] = "USER ID is dual registed: id=" +str(wID)
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		### クエリ実行
		wSubRes = self.RunQuery( inQuery=wQy )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "Function is failed: RunQuery(2)"
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		### 結果の取得
		wSubRes = self.GetInfo()
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "Function is failed: GetInfo(2): reason=" + wSubRes['Reason']
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# ユーザ名の登録
		gVal.STR_UserInfo['Account'] = inID
		gVal.STR_UserInfo['Host']    = inHost
		
		#############################
		# ログに記録する
		gVal.OBJ_L.Log( "SC", wRes, "データ更新: USER ID=" + str( inID ) )
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes

	#####################################################
	# TBL_USER：取得
	#####################################################
###	def USER_Get( self, inID ):
	def USER_Get( self, inID, inHost ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_MySQL_IF"
		wRes['Func']  = "USER_Get"
		
		#############################
		# 既登録情報の取得
		wQy = "select * from tbl_user where "
###		wQy = wQy + "id = '" + inUserData['Account'] + "' ;"
		wQy = wQy + "id = '" + str( inID ) + "' and "
		wQy = wQy + "host = '" + str( inHost ) + "' ;"
		
		### クエリ実行
		wSubRes = self.RunQuery( inQuery=wQy )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "Function is failed: RunQuery"
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		### 結果の取得
		wSubRes = self.GetInfo()
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "Function is failed: GetInfo: reason=" + wSubRes['Reason']
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# 1個以外はありえない
		if len(wSubRes['Data'])!=1 :
			wRes['Reason'] = "Function is failed: User is not exist: id=" + str(inID)
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
###		#############################
###		# 辞書型に整形
###		wData = self.ChgDict( wSubRes['Data'] )
###		
		#############################
		# ユーザ名の登録
		gVal.STR_UserInfo['Account'] = inID
		gVal.STR_UserInfo['Host']    = inHost
		
		wRes['Responce'] = wSubRes['Data'][0]
		#############################
		# =正常
		wRes['Result'] = True
		return wRes



#####################################################
# ログテーブル構築
#####################################################
	def CreateLOG( self, inTimeDate=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_MySQL_IF"
		wRes['Func']  = "CreateLOG"
		
		#############################
		# テーブルのドロップ
		wQy = "drop table if exists " + CLS_MySQL_Com.DEF_MYSQL_LOG_TABLE_NAME
		
		### クエリ実行
		wSubRes = self.RunQuery( inQuery=wQy, inFLGtraffic=False )
		#############################
		# テーブル枠の作成
		wQy = "create table " + CLS_MySQL_Com.DEF_MYSQL_LOG_TABLE_NAME + "("
		wQy = wQy + "account     TEXT  NOT NULL,"		# 記録したアカウント
		wQy = wQy + "regdate     TIMESTAMP,"			# 登録日時
		wQy = wQy + "level       CHAR(2) DEFAULT '-',"	# ログレベル
		wQy = wQy + "log_class   TEXT  NOT NULL,"		# ログクラス
		wQy = wQy + "log_func    TEXT  NOT NULL,"		# ログ関数
		wQy = wQy + "reason      TEXT  NOT NULL,"		# 理由
		wQy = wQy + "id          TEXT "					# 操作ユーザ
		wQy = wQy + " );"
		
		### クエリ実行
		wSubRes = self.RunQuery( inQuery=wQy, inFLGtraffic=False )
		if wSubRes['Result']!=True :
			###失敗
			wStr = "Function is failed: RunQuery"
			CLS_OSIF.sErr( wRes )
			return wRes
		
		### 結果判定
		wSubRes = self.GetInfo()
		if wSubRes['Result']!=True :
			###失敗
			CLS_OSIF.sErr( "Function is failed: OBJ_MySQL.CreateLOG: reason=" + wSubRes['Reason'] )
			return wRes
		
		#############################
		# 正常
		wRes['Result'] = True	#正常
		return wRes



#####################################################
# テーブル構築
#####################################################
	def CreateTable(self):
		self.__create_TBL_USER()
		self.__create_TBL_FOLLOWER()
		self.__create_TBL_EXC_WORD()
		self.__create_TBL_EXC_PROF()
		self.__create_TBL_EXC_USER()
		self.__create_TBL_TRAFFIC()
		return


#####################################################
# テーブル作成: TBL_USER
#####################################################
	def __create_TBL_USER( self, inTBLname="tbl_user" ):
		#############################
		# テーブルのドロップ
		wQy = "drop table if exists " + inTBLname + ";"
		self.RunQuery( inQuery=wQy, inFLGtraffic=False )
		
		#############################
		# テーブル枠の作成
		wQy = "create table " + inTBLname + "("
		wQy = wQy + "id          VARCHAR(64) NOT NULL,"	# ユーザ(アカウント)
		wQy = wQy + "host        TEXT  NOT NULL,"		# アカウントのホスト名
		wQy = wQy + "token       TEXT  NOT NULL,"		# misskeyアクセストークン
		wQy = wQy + "regdate     TIMESTAMP,"			# 登録日時
		wQy = wQy + "locked      BOOL  DEFAULT false,"	# 排他ロック true=ロックON
		wQy = wQy + "lok_date    TIMESTAMP,"			# 排他日時
		wQy = wQy + "get_date    TIMESTAMP,"			# 排他獲得日時
		wQy = wQy + "rel_date    TIMESTAMP,"			# 排他解除日時
		wQy = wQy + "auto_seq    INTEGER DEFAULT 0, "	# 自動監視シーケンス
		wQy = wQy + " PRIMARY KEY ( id ) ) ;"
		
		self.RunQuery( inQuery=wQy, inFLGtraffic=False )
		return



#####################################################
# テーブル作成: TBL_FOLLOWER
#####################################################
	def __create_TBL_FOLLOWER( self, inTBLname="tbl_follower" ):
		#############################
		# テーブルのドロップ
		wQy = "drop table if exists " + inTBLname + ";"
		self.RunQuery( inQuery=wQy, inFLGtraffic=False )
		
		#############################
		# テーブル枠の作成
		wQy = "create table " + inTBLname + "("
		wQy = wQy + "regid        VARCHAR(64) NOT NULL,"# 記録したユーザ(ID)
		wQy = wQy + "regdate      TIMESTAMP,"			# 登録日時
		wQy = wQy + "upddate      TIMESTAMP,"			# 更新日時(最終)
		
		wQy = wQy + "id            TEXT  NOT NULL,"		# Misskey ID(数値)
		wQy = wQy + "host          TEXT  NOT NULL,"		# アカウントのホスト名
		
		wQy = wQy + "follower      BOOL  DEFAULT false,"# フォロワー true=フォロー者
		wQy = wQy + "follower_date TIMESTAMP, "			# フォロー日時
		
		wQy = wQy + "ract_id       TEXT  NOT NULL,"		# リアクション受信(このユーザがいいねした) ツイートID
		wQy = wQy + "ract_date     TIMESTAMP,"			# リアクション受信日時
		wQy = wQy + "ract_cnt      INTEGER DEFAULT 0,"	# リアクション受信回数(総数)
		wQy = wQy + "ract_n_cnt    INTEGER DEFAULT 0,"	# リアクション受信回数(今周)
		
		wQy = wQy + "pact_id       TEXT  NOT NULL,"		# リアクション実施(このユーザのツイート) ツイートID
		wQy = wQy + "pact_date     TIMESTAMP, "			# リアクション送信日時
		wQy = wQy + "pact_cnt      INTEGER DEFAULT 0,"	# リアクション送信回数(総数)
		
		wQy = wQy + "memo          TEXT "				# 自由記載(メモ)
		wQy = wQy + " ) ;"
		
		self.RunQuery( inQuery=wQy, inFLGtraffic=False )
		return



#####################################################
# テーブル作成: TBL_EXC_WORD
#####################################################
	def __create_TBL_EXC_WORD( self, inTBLname="tbl_exc_word" ):
		#############################
		# テーブルのドロップ
		wQy = "drop table if exists " + inTBLname + ";"
		self.RunQuery( inQuery=wQy, inFLGtraffic=False )
		
		#############################
		# テーブル枠の作成
		wQy = "create table " + inTBLname + "("
		wQy = wQy + "regdate     TIMESTAMP,"			# 登録日時
		wQy = wQy + "word        VARCHAR(64) NOT NULL, "# 禁止ワード
		wQy = wQy + "report      BOOL  DEFAULT false,"	# 通報対象か True=対象
		wQy = wQy + " PRIMARY KEY ( word ) ) ;"
		
		self.RunQuery( inQuery=wQy, inFLGtraffic=False )
		return



#####################################################
# テーブル作成: TBL_EXC_PROF
#####################################################
	def __create_TBL_EXC_PROF( self, inTBLname="tbl_exc_prof" ):
		#############################
		# テーブルのドロップ
		wQy = "drop table if exists " + inTBLname + ";"
		self.RunQuery( inQuery=wQy, inFLGtraffic=False )
		
		#############################
		# テーブル枠の作成
		wQy = "create table " + inTBLname + "("
		wQy = wQy + "regdate     TIMESTAMP,"			# 登録日時
		wQy = wQy + "word        VARCHAR(64) NOT NULL, "# 禁止ワード
		wQy = wQy + "report      BOOL  DEFAULT false,"	# 通報対象か True=対象
		wQy = wQy + " PRIMARY KEY ( word ) ) ;"
		
		self.RunQuery( inQuery=wQy, inFLGtraffic=False )
		return



#####################################################
# テーブル作成: TBL_EXC_USER
#####################################################
	def __create_TBL_EXC_USER( self, inTBLname="tbl_exc_user" ):
		#############################
		# テーブルのドロップ
		wQy = "drop table if exists " + inTBLname + ";"
		self.RunQuery( inQuery=wQy, inFLGtraffic=False )
		
		#############################
		# テーブル枠の作成
		wQy = "create table " + inTBLname + "("
		wQy = wQy + "regdate     TIMESTAMP,"			# 登録日時
		wQy = wQy + "id          VARCHAR(64) NOT NULL, "# misskey ID(数値)
		wQy = wQy + "report      BOOL  DEFAULT false,"	# 通報対象 True=対象
		wQy = wQy + "vip         BOOL  DEFAULT false,"	# VIP扱い  True=VIP
		wQy = wQy + "ope         BOOL  DEFAULT false,"	# リアクション監視  True=監視ON
		wQy = wQy + "follow      BOOL  DEFAULT false,"	# フォロー監視(Mainフォローしてるか)  True=監視ON
		wQy = wQy + "rel_date    TIMESTAMP,"			# 禁止解除日時 (noneは自動解除しない)
		wQy = wQy + "memo        TEXT, "				# 自由記載(メモ)
		wQy = wQy + " PRIMARY KEY ( id ) ) ;"
		
		self.RunQuery( inQuery=wQy, inFLGtraffic=False )
		return



#####################################################
# テーブル作成: TBL_TRAFFIC
#####################################################
	def __create_TBL_TRAFFIC( self, inTBLname="tbl_traffic" ):
		#############################
		# テーブルのドロップ
		wQy = "drop table if exists " + inTBLname + ";"
		self.RunQuery( inQuery=wQy, inFLGtraffic=False )
		
		#############################
		# テーブル枠の作成
		wQy = "create table " + inTBLname + "("
		wQy = wQy + "twitterid   TEXT  NOT NULL,"		# Twitter ID(数値)
		wQy = wQy + "regdate     TIMESTAMP,"			# 登録日時
		wQy = wQy + "upddate     TIMESTAMP,"			# 記録日時(更新)
		wQy = wQy + "day         TEXT  NOT NULL,"		# 記録日
		wQy = wQy + "run         INTEGER DEFAULT 0,"	# bot実行回数
		wQy = wQy + "run_time    NUMERIC DEFAULT 0,"	# 実行時間
		
		wQy = wQy + "run_api     INTEGER DEFAULT 0,"	# api実行回数
		wQy = wQy + "run_ope     INTEGER DEFAULT 0,"	# 自動監視実施回数
		
		###### Twittterトラヒック
		wQy = wQy + "timeline    INTEGER DEFAULT 0,"	# タイムライン取得数(ライン数)
		
		wQy = wQy + "myfollow    INTEGER DEFAULT 0,"	# フォロー者数(報告時)
		wQy = wQy + "p_myfollow  INTEGER DEFAULT 0,"	# フォロー実施数
		wQy = wQy + "d_myfollow  INTEGER DEFAULT 0,"	# リムーブ実施数
		
		wQy = wQy + "follower    INTEGER DEFAULT 0,"	# フォロワー数(報告時)
		wQy = wQy + "p_follower  INTEGER DEFAULT 0,"	# フォロワー獲得数
		wQy = wQy + "d_follower  INTEGER DEFAULT 0,"	# 被リムーブ者数
		
		wQy = wQy + "r_reaction  INTEGER DEFAULT 0,"	# リアクション受信回数(総数)
		wQy = wQy + "r_rep       INTEGER DEFAULT 0,"	# リプライ受信回数
		wQy = wQy + "r_retweet   INTEGER DEFAULT 0,"	# リツイート受信回数
		wQy = wQy + "r_iret      INTEGER DEFAULT 0,"	# 引用リツイート受信回数
		wQy = wQy + "r_favo      INTEGER DEFAULT 0,"	# いいね受信回数
		wQy = wQy + "r_in        INTEGER DEFAULT 0,"	# フォロワーからのアクション受信回数
		wQy = wQy + "r_out       INTEGER DEFAULT 0,"	# フォロワー以外からのアクション受信回数
		wQy = wQy + "r_vip       INTEGER DEFAULT 0,"	# VIP監視アクション受信回数
		
		wQy = wQy + "s_run       INTEGER DEFAULT 0,"	# 検索実施数
		wQy = wQy + "s_hit       INTEGER DEFAULT 0,"	# 検索ヒット数
		wQy = wQy + "s_favo      INTEGER DEFAULT 0,"	# 検索時いいね数
		
		wQy = wQy + "favo        INTEGER DEFAULT 0,"	# いいね数
		wQy = wQy + "p_favo      INTEGER DEFAULT 0,"	# いいね実施回数
		wQy = wQy + "d_favo      INTEGER DEFAULT 0,"	# いいね解除回数
		wQy = wQy + "p_tweet     INTEGER DEFAULT 0,"	# ツイート送信回数
		
		###### DBトラヒック
		wQy = wQy + "db_req INTEGER DEFAULT 0,"			# DB select回数
		wQy = wQy + "db_ins INTEGER DEFAULT 0,"			# DB insert回数
		wQy = wQy + "db_up  INTEGER DEFAULT 0,"			# DB update回数
		wQy = wQy + "db_del INTEGER DEFAULT 0 "			# DB delete回数
		wQy = wQy + " ) ;"
		
		self.RunQuery( inQuery=wQy, inFLGtraffic=False )
		return



