#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : ぽすぐれユーズ
#####################################################
# 参考：
#   psycopg2
#     https://qiita.com/hoto17296/items/0ca1569d6fa54c7c4732
#
#####################################################
import psycopg2

#####################################################
class CLS_PostgreSQL_Use():
#####################################################
	PostgreSQL_use = ""						#PostgreSQLモジュール実体
	DbStatus = ""
	##	"Init"     : False
	##	"Open"     : False
	##	"Reason"   : None
	##	"Responce" : None
	
	QueryStat = ""
	##	"Result"	: False,
	##	"RunFunc"	: inRunFunc,
	##	"Command"	: None,
	##	"Reason"	: None,
	##	"Responce"	: None,
	##	"Query"		: "None"

	STR_DBdata = {
		"hostname"		:	"",
		"database"		:	"",
		"username"		:	"",
		"password"		:	""
	}

	DEF_MOJI_ENCODE = 'utf-8'				#ファイル文字エンコード



#####################################################
# DB状態取得
#####################################################
	def GetDbStatus(self):
		return self.DbStatus	#返すだけ



#####################################################
# DB状態 初期化
#####################################################
	def __initDbStatus(self):
		self.DbStatus = {
			"Init"     : False,
			"Open"     : False,
			"Reason"   : "DB closed",
			"Responce" : None
		}
		return



#####################################################
# クエリ状態取得
#####################################################
	def GetQueryStat(self):
		return self.QueryStat	#返すだけ



#####################################################
# クエリ状態 初期化
#####################################################
	def __initQueryStat( self, inRunFunc=None ):
		self.QueryStat = {
			"Result"	: False,
			"RunFunc"	: inRunFunc,
			"Command"	: None,
			"Reason"	: None,
			"Responce"	: None,
			"Query"		: "None"
		}
		return



#####################################################
# 初期化
#####################################################
	def __init__(self):
		return



#####################################################
# 接続情報の作成
#####################################################
	def Create( self, inData, inFLG_Close=False ):
		#############################
		# inData構造
		#   = {
		#		"hostname"	:	"",
		#		"database"	:	"",
		#		"username"	:	"",
		#		"password"	:	""
		#	}
		
		#############################
		# パラメータチェック
		if "hostname" not in inData or \
		   "database" not in inData or \
		   "username" not in inData or \
		   "password" not in inData :
			self.DbStatus['Reason'] = "CLS_PostgreSQL_Use: Create: パラメータが足りません: inData=" + str(inData)
			return False	#失敗
		
		#############################
		# DB状態 全初期化
		self.__initDbStatus()
		
		#############################
		# 接続情報の仮セット
		self.STR_DBdata['hostname'] = inData['hostname']
		self.STR_DBdata['database'] = inData['database']
		self.STR_DBdata['username'] = inData['username']
		self.STR_DBdata['password'] = inData['password']
		
		#############################
		# DB接続テスト
		if self.__dbConnect()!=True :
			return False	#失敗
		
		if inFLG_Close==True :
			#############################
			# DB切断
			if self.__dbClose()!=True :
				return False	#失敗
		else :
			self.DbStatus['Open'] = True
		
		#############################
		# 初期化完了
		self.DbStatus['Init'] = True
		return True



#####################################################
# DB接続
#####################################################
	def Connect(self):
		#############################
		# 初期化状態の確認
		if self.DbStatus['Init']!=True :
			self.DbStatus['Reason'] = "CLS_PostgreSQL_Use: Connect: DbStatusが初期化されていません"
			return False
		
		#############################
		# DB接続
		if self.__dbConnect()!=True :
			return False
		
		return True

	#####################################################
	def __dbConnect(self):
		self.DbStatus['Open'] = False
		
		#############################
		# DB接続
		try:
			#############################
			# 接続
			self.PostgreSQL_use = psycopg2.connect( host=self.STR_DBdata['hostname'], database=self.STR_DBdata['database'], user=self.STR_DBdata['username'], password=self.STR_DBdata['password'] )
			
			#############################
			# エンコードの強制設定
			self.PostgreSQL_use.set_client_encoding('utf-8')
		except psycopg2.OperationalError as e:
			self.DbStatus['Reason'] = "CLS_PostgreSQL_Use: __dbConnect: psycopg2 error: " + str(e)
			return False
		
		#############################
		# DB接続完了
		self.DbStatus['Open'] = True
		return True



#####################################################
# DB切断
#####################################################
	def Close(self):
		#############################
		# 接続状態の確認
		if self.DbStatus['Open']!=True :
			self.DbStatus['Reason'] = "CLS_PostgreSQL_Use: Close: DBが接続されていません"
			return False
		
		#############################
		# DB切断
		if self.__dbClose()!=True :
			return False
		
		return True

	#####################################################
	def __dbClose(self):
		#############################
		# DB切断
		try:
			self.PostgreSQL_use.close()
		except psycopg2.OperationalError as e:
			self.DbStatus['Reason'] = "CLS_PostgreSQL_Use: __dbClose: psycopg2 error: " + str(e)
			return False
		
		self.DbStatus['Reason'] = "DB closed"
		self.DbStatus['Open']   = False
		return True



#####################################################
# クエリ実行
#####################################################
	def RunQuery( self, inQuery=None ):
		#############################
		# 状態初期化
		self.__initQueryStat( "RunQuery" )
		
		#############################
		# 接続状態の確認
		if self.DbStatus['Open']!=True :
			self.QueryStat['Reason'] = "DBが接続されていません"
			return False
		
		#############################
		# 実行前チェック
		if inQuery==None :
			self.QueryStat['Reason'] = "None Query"
			return False
		
		#############################
		# コマンド取得
		wCommand = inQuery.split(" ")
		if len( wCommand )<=1 :
			self.QueryStat['Reason'] = "Query is not correct: " + inQuery
			return False
		wCommand = wCommand[0]
		self.QueryStat['Command'] = wCommand
		
		# チェック
		if wCommand!="select" and \
		   wCommand!="create" and \
		   wCommand!="drop"   and \
		   wCommand!="insert" and \
		   wCommand!="delete" and \
		   wCommand!="update" :
			self.QueryStat['Reason'] = "Unknown command: " + inQuery
			return False
		
		#############################
		# クエリ実行
		if wCommand=="select" :
			if self.__runQuerySelect( inQuery )!=True :
				return False
		else :
			if self.__runQueryCommit( inQuery )!=True :
				return False
		
		#############################
		# 正常
		self.QueryStat['Result'] = True
		return True

#############################
	def __runQuerySelect( self, inQuery ):
		with self.PostgreSQL_use.cursor() as wCur :
			try:
				#############################
				# 本実行
				self.QueryStat['Query'] = inQuery	#デバック用記録
				wCur.execute( inQuery )
				
				#############################
				# 結果を格納
				wColum = []
				for wCol in wCur.description :
					wColum.append( wCol.name )
				self.QueryStat['Responce'] = {
					"Collum" : wColum,
					"Data"   : wCur.fetchall()
				}
			
			except psycopg2.OperationalError as e:
				self.QueryStat['Reason'] = "psycopg2.OperationalError(1): " + str(e)
				return False
		
		#############################
		# 正常
		return True

#############################
	def __runQueryCommit( self, inQuery ):
		with self.PostgreSQL_use.cursor() as wCur :
			try:
				#############################
				# 本実行
				self.QueryStat['Query'] = inQuery	#デバック用記録
				wCur.execute( inQuery )
				
				#############################
				# commit
				self.PostgreSQL_use.commit()
			
			except psycopg2.OperationalError as e:
				self.QueryStat['Reason'] = "psycopg2.OperationalError(2): " + str(e)
				return False
		
		#############################
		# 正常
		return True



#####################################################
# クエリ実行  存在チェック
#####################################################
	def RunExist( self, inObjTable=None, inWhere=None ):
		#############################
		# 状態初期化
		self.__initQueryStat( "RunExist" )
		
		#############################
		# 接続状態の確認
		if self.DbStatus['Open']!=True :
			self.QueryStat['Reason'] = "DBが接続されていません"
			return False
		
		#############################
		# 実行前チェック
		if inObjTable==None :
			self.QueryStat['Reason'] = "None Object table"
			return False
		if inWhere==None :
			self.QueryStat['Reason'] = "None Where"
			return False
		
		#############################
		# クエリ作成
		wQuery = "select exists (select * from " + \
					inObjTable + " where " + \
					inWhere + ");"
		
		#############################
		# クエリ実行
		with self.PostgreSQL_use.cursor() as wCur :
			try:
				#############################
				# 本実行
				self.QueryStat['Query'] = wQuery	#デバック用記録
				wCur.execute( wQuery )
				
				#############################
				# 結果を格納
				wRes = wCur.fetchall()
				self.QueryStat['Responce'] = wRes[0][0]
			
			except psycopg2.OperationalError as e:
				self.QueryStat['Reason'] = "psycopg2.OperationalError(3): " + str(e)
				return False
		
		#############################
		# 正常
		self.QueryStat['Result'] = True
		return True



#####################################################
# クエリ実行  テーブル存在チェック
#####################################################
	def RunTblExist( self, inObjTable=None ):
		#############################
		# 状態初期化
		self.__initQueryStat( "RunTblExist" )
		
		#############################
		# 接続状態の確認
		if self.DbStatus['Open']!=True :
			self.QueryStat['Reason'] = "DBが接続されていません"
			return False
		
		#############################
		# 実行前チェック
		if inObjTable==None :
			self.QueryStat['Reason'] = "None Object table"
			return False
		
		#############################
		# クエリ作成
		wQuery = "select * from information_schema.tables where table_name = '" + \
			inObjTable + "'" + \
			" ;"
		
		#############################
		# クエリ実行
		with self.PostgreSQL_use.cursor() as wCur :
			try:
				self.QueryStat['Responce'] = False
				
				#############################
				# 本実行
				self.QueryStat['Query'] = wQuery	#デバック用記録
				wCur.execute( wQuery )
				
				#############################
				# 結果を格納
				wRes = wCur.fetchall()
				if len(wRes)==1 :
					self.QueryStat['Responce'] = True
			
			except psycopg2.OperationalError as e:
				self.QueryStat['Reason'] = "psycopg2.OperationalError(4): " + str(e)
				return False
		
		#############################
		# 正常
		self.QueryStat['Result'] = True
		return True



#####################################################
# クエリ実行  レコード数
#####################################################
	def RunCount( self, inObjTable=None ):
		#############################
		# 状態初期化
		self.__initQueryStat( "RunCount" )
		
		#############################
		# 接続状態の確認
		if self.DbStatus['Open']!=True :
			self.QueryStat['Reason'] = "DBが接続されていません"
			return False
		
		#############################
		# 実行前チェック
		if inObjTable==None :
			self.QueryStat['Reason'] = "None Object table"
			return False
		
		#############################
		# クエリ作成
		wQuery = "select count(*) from " + \
					inObjTable + \
					";"
		
		#############################
		# クエリ実行
		with self.PostgreSQL_use.cursor() as wCur :
			try:
				#############################
				# 本実行
				self.QueryStat['Query'] = wQuery	#デバック用記録
				wCur.execute( wQuery )
				
				#############################
				# 結果を格納
				wRes = wCur.fetchall()
				self.QueryStat['Responce'] = wRes[0][0]
			
			except psycopg2.OperationalError as e:
				self.QueryStat['Reason'] = "psycopg2.OperationalError(5): " + str(e)
				return False
		
		#############################
		# 正常
		self.QueryStat['Result'] = True
		return True



#####################################################
# クエリ結果をリスト型に取りだす
#   ※共通フル取得
#####################################################
	def ChgList( self, inData, outList=[] ):
		if len( inData )==0 :
			return False
		
		wList = outList
		#############################
		# カウント値の取り出し
		for wLineTap in inData :
			wGetTap = []
			for wCel in wLineTap :
				wGetTap.append( wCel )
			wList.extend( wGetTap )
		
		return True



#####################################################
# クエリ結果を辞書型に取りだす
#   ※共通フル取得
#####################################################
	def ChgDict( self, inCollum, inData, outDict={} ):
		if len( inData )==0 :
			return False
		
		wDict = outDict
		wIndex = 0
		#############################
		# カウント値の取り出し
		for wLineTap in inData :
			wGetTap = {}
			wC_Index = 0
			for wCel in wLineTap :
				wGetTap.update({ inCollum[wC_Index] : wCel })
				wC_Index += 1
			
			wDict.update({ wIndex : wGetTap })
			wIndex += 1
		
		return True






## cd /home/starregion/wsgi/strg_run/


##	>>> import psycopg2
##	# コネクション作成
##	>>> conn = psycopg2.connect("dbname=test host=localhost user=postgres")
##	# カーソル作成
##	>>> cur = conn.cursor()
##	# SQLコマンド実行 (今回はテーブル作成)
##	>>> cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
##	# SQLコマンド実行 (プレースホルダー使用。エスケープも勝手にされる)
##	>>> cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))
##	# SQL結果を受け取る
##	>>> cur.execute("SELECT * FROM test;")
##	>>> cur.fetchone()
##	(1, 100, "abc'def")
##	# コミット
##	>>> conn.commit()
##	# クローズ
##	>>> cur.close()
##	>>> conn.close()


####カラム名の取得
## select 
##	* 
## from 
## 	information_schema.columns 
## where 
##	table_catalog='データベース名' 
##	and 
##	table_name='テーブル名' 
## order by 
##	ordinal_position;
##







#####################################################
# HTML作成
#####################################################
def create_HTML( user, dbres ):
	
	wStr = '<!DOCTYPE html>'
	wStr = wStr + '<html>'
	wStr = wStr + '<head>'
	wStr = wStr + '<meta charset="utf-8" />'
	wStr = wStr + '<title>TEST</title>'
	wStr = wStr + '</head>'
	wStr = wStr + '<body>'
	wStr = wStr + user + '<br />'
	wStr = wStr + dbres + '<br />'
	wStr = wStr + '</body></html>'
	
	return wStr



