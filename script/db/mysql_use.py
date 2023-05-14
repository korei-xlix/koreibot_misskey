#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Misskey
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_misskey/
# ::Class    : MySQL use
#####################################################
# 前提モジュール
#   mysql-connector-python
#####################################################
import mysql.connector

from mysql_com import CLS_MySQL_Com
#####################################################
class CLS_MySQL_Use() :
#####################################################
	OBJ_MySQL = ""				# DBオブジェクト
	OBJ_MySQL_cur = ""			# DBカーソル
	FLG_MySQL_Open = False		# DB接続  True=接続中、False=未接続

	STR_Status = {				# DB状態
		"FLG_Open"	: False,	# DB状態の返送
		
		"Result"	: False,	# Result
		"Reason"	: None,		# エラー理由
		"Data"		: None		# 結果応答
		
	}



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
		# inData / DB_Info 構造
		#   = {
		#		"DB_HOST"	:	None,
		#		"DB_NAME"	:	None,
		#		"DB_USER"	:	None,
		#		"DB_PASS"	:	None
		#	}
		
		self.STR_Status['Result'] = False
		#############################
		# 入力チェック
		if "DB_HOST" not in inData or \
		   "DB_NAME" not in inData or \
		   "DB_USER" not in inData or \
		   "DB_PASS" not in inData :
			
			### NG
			self.STR_Status['Reason'] = "input is failer: " + str(inData)
			return
		
		#############################
		# 接続中はNG
		if self.FLG_MySQL_Open==True :
			self.STR_Status['Reason'] = "db is connected"
			return
		
		#############################
		# MySQLに接続する
		try:
			wSubRes = mysql.connector.connect(
				host     = inData['DB_HOST'],
				user     = inData['DB_USER'],
				password = inData['DB_PASS'],
				database = inData['DB_NAME'],
				charset  = CLS_MySQL_Com.DEF_MYSQL_MOJI_ENCODE
			)
			
		except ValueError as err :
			### NG
			self.STR_Status['Reason'] = "db connect exception: reason=" + str( err )
			return False
		
		### 結果
		if not wSubRes.is_connected() :
			self.STR_Status['Reason'] = "db connect is failer"
		
		self.OBJ_MySQL = wSubRes
		
		#############################
		# カーソル取得
		self.OBJ_MySQL_cur = self.OBJ_MySQL.cursor( dictionary=True )
		
		#############################
		# 接続
		self.FLG_MySQL_Open = True
		
		#############################
		# 正常処理
		self.STR_Status['Result'] = True
		return



#####################################################
# DB切断
#####################################################
	def Close(self):
		self.OBJ_MySQL_cur.close()
		self.OBJ_MySQL.close()
		self.FLG_MySQL_Open = False
		return



#####################################################
# DB状態取得
#####################################################
	def GetInfo(self):
		self.STR_Status['FLG_Open'] = self.FLG_MySQL_Open
		return self.STR_Status



#####################################################
# クエリ実行
#####################################################
	def RunQuery( self, inQuery=None, inCommand=None ):
		
		self.STR_Status['Result'] = False
		#############################
		# クエリ実行＆コミット
		try:
			self.OBJ_MySQL_cur.execute( inQuery )
			if inCommand=="create" or \
			   inCommand=="insert" or \
			   inCommand=="update" or \
			   inCommand=="delete" or \
			   inCommand=="drop" :
				self.OBJ_MySQL.commit()
			
			#############################
			# selectの場合、結果を返送する
			elif inCommand=="select" :
				self.STR_Status['Data'] = []
				wData = self.OBJ_MySQL_cur.fetchall()
				if wData!=None :
					self.STR_Status['Data'] = wData
		
		except ValueError as err :
			### NG
			self.STR_Status['Reason'] = "this querry run is failer: " + str( inQuery )
			return False
		
		#############################
		# 正常処理
		self.STR_Status['Result'] = True
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
