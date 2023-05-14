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
#####################################################
class CLS_Misskey_IF() :
#####################################################
	OBJ_Misskey = ""		#misskeyオブジェクト(トークン)

	STR_Status = {				# misskey状態
		"FLG_Con"	: False,	# 接続  True=接続確認済


		"FLG_Open"	: False,	# DB状態の返送
		
		"Result"	: False,	# Result
		"Reason"	: None,		# エラー理由
		"Data"		: None		# 結果応答
		
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
###		gVal.STR_UserInfo['Account'] = inAccount
		gVal.STR_UserInfo['ID']   = wID
###		gVal.STR_UserInfo['Host'] = inHost
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
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



'''
	async def runner():
		async with websockets.connect(WS_URL) as ws:
			await ws.send(json.dumps({
			   "type": "connect",
			   "body": {
			     "channel": "homeTimeline",
			     "id": "test"
			}
		}))
		while True:
			data = json.loads(await ws.recv())
			print(data)



   if data['type'] == 'channel':
    if data['body']['type'] == 'note':
     note = data['body']['body']
     await on_note(note)

    if data['body']['type'] == 'followed':
     user = data['body']['body']
     await on_follow(user)



async def on_note(note):
 if note.get('mentions'):
  if MY_ID in note['mentions']:
   msk.notes_create(text='呼んだ？', replyId=note['id'])



async def on_follow(user):
 try:
  msk.following_create(user['id'])
 except:
  pass



asyncio.get_event_loop().run_until_complete(runner())


'''








