#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Misskey
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_misskey/
# ::Class    : misskey I/F
#####################################################
import asyncio
import json
import websockets
from misskey import Misskey

from osif import CLS_OSIF
from gval import gVal
from misskey_com import CLS_Misskey_Com


###async def Async_dummy():
###	print("OK")
###	await asyncio.sleep(10)

#####################################################
# 非同期 受信処理
#####################################################
async def Async_Receive():
	#############################
	# 応答形式の取得
	#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
	wRes = CLS_OSIF.sGet_Resp()
	wRes['Class'] = "CLS_Misskey_IF"
	wRes['Func']  = "Async_Receive"
	
##	#############################
##	# ループの表示
##	wLoop = asyncio.get_running_loop()
##	if gVal.FLG_Test==True :
##		CLS_OSIF.sPrn( " now loops: " + str( wLoop ) )
##	
	#############################
	# 受信処理
	async with websockets.connect( gVal.STR_UserInfo['URL'] ) as ws:
		await ws.send(json.dumps({
		   "type": "connect",
		   "body": {
		     "channel": "homeTimeline",
		     "id": "test"
		}
	}))
	
	#############################
	# 受信データの表示
	while True:
###		wData = json.loads(await ws.recv())
		wData = await ws.recv()
		
		### ノート単位に表示する
		if wData['type'] == 'channel':
			if wData['body']['type'] == 'note':
				wNote = wData['body']['body']
				await __async_OnNote( wNote )
		
		### フォローされたら、フォローする
		if wData['body']['type'] == 'followed':
			wUser = wData['body']['body']
			await __async_Followed( wUser )
	
	#############################
	# 完了
	wRes['Result'] = True
	return wRes

#####################################################
# 非同期：ノート単位の表示
#####################################################
async def __async_OnNote( inNote ):
	#############################
	# 応答形式の取得
	#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
	wRes = CLS_OSIF.sGet_Resp()
	wRes['Class'] = "CLS_Misskey_IF"
	wRes['Func']  = "__async_OnNote"
	
	if inNote.get('mentions'):
		if gVal.STR_UserInfo['ID'] in inNote['mentions']:
			self.OBJ_Misskey.notes_create(text='呼んだ？', replyId=inNote['id'])
	
	return

#####################################################
# 非同期：フォローする
#####################################################
async def __async_Followed( inUser ):
	#############################
	# 応答形式の取得
	#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
	wRes = CLS_OSIF.sGet_Resp()
	wRes['Class'] = "CLS_Misskey_IF"
	wRes['Func']  = "__async_Followed"
	
	try:
		self.OBJ_Misskey.following_create( inUser['id'] )
	except:
		pass

	return



#####################################################
class CLS_Misskey_IF() :
#####################################################
	OBJ_Misskey = ""		#misskeyオブジェクト(トークン)

	STR_Status = {				# misskey状態
		"FLG_Con"	: False,	# 接続  True=接続確認済

		"FLG_Rec"	: False,	# 受信処理  True=受信中

###		"FLG_Open"	: False,	# DB状態の返送
###		
###		"Result"	: False,	# Result
###		"Reason"	: None,		# エラー理由
###		"Data"		: None		# 結果応答
		
	}



#####################################################
# Init
#####################################################
	def __init__( self, outRes, parentObj=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Misskey_IF"
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
# misskey接続
#####################################################
	def Connect( self, inAccount, inHost, inToken ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Misskey_IF"
		wRes['Func']  = "Connect"
		
		#############################
		# 入力チェック
		if inToken==None or inToken=="" :
			### 入力エラー
			wRes['Reason'] = "token is invalid"
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		self.STR_Status['FLG_Con'] = False
		#############################
		# misskeyと接続
		#   IDを取得する
		try:
			self.OBJ_Misskey = Misskey( inHost, i=inToken )
			wID = self.OBJ_Misskey.i()['id']
			WS_URL = CLS_Misskey_Com.DEF_MISSKEY_STREAM_URL + str( inToken )
		except ValueError as err :
			### 接続エラー
			wRes['Reason'] = "misskey connect is failed: reason=" + str(err)
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# ユーザ情報の設定
		gVal.STR_UserInfo['ID']   = wID
		gVal.STR_UserInfo['URL']  = WS_URL
		
		#############################
		# 処理表示
		if gVal.FLG_Test==True :
			wStr = "misskey: connect: "
			wStr = wStr + "Account: " + str( gVal.STR_UserInfo['Account'] )
			wStr = wStr + "Host: " + str( gVal.STR_UserInfo['Host'] )
			wStr = wStr + "ID: " + str( gVal.STR_UserInfo['ID'] )
			CLS_OSIF.sPrn( wStr )
		
		self.STR_Status['FLG_Con'] = True
		self.STR_Status['FLG_Rec'] = False
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



	#####################################################
	# 非同期：受信処理 開始
	#####################################################
	def Async_StartReceive(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Misskey_IF"
		wRes['Func']  = "Async_StartReceive"
		
		#############################
		# 受信中か？
		if self.STR_Status['FLG_Rec']==True :
			### 受信中は処理しない
			return wRes
		
		#############################
		# 非同期ループタスクの作成
		
		### new loop
		wNewLoop = asyncio.new_event_loop()
		wLoop = asyncio.set_event_loop( wNewLoop )
		if gVal.FLG_Test==True :
			CLS_OSIF.sPrn( "+new loop: " + str( wNewLoop ) )
		
		### 受信関数コルーチンの起動
		wNewLoop.run_until_complete( Async_Receive() )
		wNewLoop.run_forever()
		
		#############################
		# 受信中
		self.STR_Status['FLG_Rec'] = True
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes

	#####################################################
	# 非同期：受信処理 停止
	#####################################################
	def Async_StopReceive(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Misskey_IF"
		wRes['Func']  = "Async_StartReceive"
		
		#############################
		# 未受信か？
		if self.STR_Status['FLG_Rec']==False :
			### 未受信時は処理しない
			return wRes
		
		#############################
		# 非同期ループタスクの停止
		wLoop = asyncio.get_event_loop()
		wLoop.stop()
		wLoop.close()
		
		#############################
		# 未受信
		self.STR_Status['FLG_Rec'] = False
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes




