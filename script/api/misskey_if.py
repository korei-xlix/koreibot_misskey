#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Misskey
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_misskey/
# ::Class    : misskey I/F
#####################################################
from kbhit import *

import asyncio
import json
import websockets
from misskey import Misskey

from osif import CLS_OSIF
from gval import gVal
from misskey_com import CLS_Misskey_Com


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
	
	wSubRes = CLS_OSIF.sGet_Resp()
	wSubRes['Class'] = "CLS_Misskey_IF"
	wSubRes['Func']  = "Async_Receive"
	
###	#############################
###	# ループの表示
###	wLoop = asyncio.get_running_loop()
###	if gVal.FLG_Test==True :
###		CLS_OSIF.sPrn( " now loops: " + str( wLoop ) )
###	
	#############################
	# 受信開始
	if gVal.FLG_Test==True :
		CLS_OSIF.sPrn( "loop start: Async Receive" )
	
	#############################
	# キー受け付け準備
	atexit.register(set_normal_term)
	set_curses_term()
	
	#############################
	# 受信処理
	async with websockets.connect( gVal.STR_UserInfo['URL'] ) as ws:
		await ws.send(json.dumps({
		   "type": "connect",
		   "body": {
		     "channel": "localTimeline",
###		     "id": "test"
			}
		}))
		
		while True:
			#############################
			# 何かキーが推されたら停止ON
			if kbhit():
##				key = getch()   # 1文字取得
				if gVal.FLG_Test==True :
					CLS_OSIF.sPrn( "rec: Stop commans" )
				CLS_Misskey_Com.STR_Status['FLG_RecEnd'] = True
			
			#############################
			# 停止ON
			if CLS_Misskey_Com.STR_Status['FLG_RecEnd']==True :
				break
			
			#############################
			# データ受信
			await __async_Receive( ws, wSubRes )
			if wSubRes['Result']!=True :
				continue
			
			wData = wSubRes['Responce']
			
			#############################
			# 受信振り分け
			
			### ノート単位に表示する
			if wData['type'] == 'channel':
				if wData['body']['type'] == 'note' and \
				   wData['body']['body']['text'] != None:
					wNote = wData['body']['body']
					await __async_OnNote( wNote )
			
			### フォローされたら、フォローする
			if wData['body']['type'] == 'followed':
				wUser = wData['body']['body']
				await __async_Followed( wUser )
	
	#############################
	# ループ停止
	await __async_StopReceive()
	
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
	
	#############################
	# ノート情報の整理
	wSTR_Note = {
		"id"	: str( inNote['user']['username'] ),
		"host"	: str( inNote['user']['host'] ),
		"name"	: str( inNote['user']['name'] ),
		
		"text"	: str( inNote['text'] ),
		"date"	: str( inNote['createdAt'] ),
		
		"isBot"	: str( inNote['user']['isBot'] ),
		"onlineStatus"	: str( inNote['user']['onlineStatus'] ),

		"renoteCount"	: str( inNote['renoteCount'] ),
		"repliesCount"	: str( inNote['repliesCount'] ),
		"reactions"	: str( inNote['reactions'] ),
	}
	
	#############################
	# ツイート表示
	wStr = wSTR_Note['name'] + "(" + wSTR_Note['id'] + "@" + wSTR_Note['host'] + ")" + '\n'
	wStr = wStr + wSTR_Note['text'] + '\n'
	wStr = wStr + wSTR_Note['date'] + '\n'
	wStr = wStr + "******************************" + '\n'
	CLS_OSIF.sPrn( wStr )
	
	#############################
	# メンションに対し返信
	if inNote.get('mentions'):
		if gVal.STR_UserInfo['ID'] in inNote['mentions']:
			CLS_Misskey_Com.OBJ_Misskey.notes_create(text='呼んだ？', replyId=inNote['id'])
	
	return

#####################################################
# 非同期：データ受信
#####################################################
async def __async_Receive( inWebSock, outRes ):
	#############################
	# 応答形式の取得
	#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
	pRes = outRes
	pRes['Class'] = "CLS_Misskey_IF"
	pRes['Func']  = "__async_Receive"
	
	try:
		wData = json.loads(await inWebSock.recv())
		pRes['Responce']  = wData
		pRes['Result'] = True
	except:
		pRes['Reason']  = "__async_Receive is exception"
		pass
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
		CLS_Misskey_Com.OBJ_Misskey.following_create( inUser['id'] )
	except:
		pass

	return



#####################################################
# 非同期：受信処理 停止
#####################################################
async def __async_StopReceive():
	#############################
	# 応答形式の取得
	#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
	wRes = CLS_OSIF.sGet_Resp()
	wRes['Class'] = "CLS_Misskey_IF"
	wRes['Func']  = "__async_StopReceive"
	
	#############################
	# 非同期ループタスクの停止
	wLoop = asyncio.get_event_loop()
	wLoop.stop()
#	wLoop.close()
	
	#############################
	# 未受信
	CLS_Misskey_Com.STR_Status['FLG_Rec'] = False
	
	### 表示
	if gVal.FLG_Test==True :
		CLS_OSIF.sPrn( "loop end: Async Receive" )
	
	#############################
	# 完了
	wRes['Result'] = True
	return wRes


#####################################################
# Class
#####################################################
class CLS_Misskey_IF() :
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
		
		CLS_Misskey_Com.STR_Status['FLG_Con'] = False
		#############################
		# misskeyと接続
		#   IDを取得する
		try:
			CLS_Misskey_Com.OBJ_Misskey = Misskey( inHost, i=inToken )
			wID = CLS_Misskey_Com.OBJ_Misskey.i()['id']
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
		
		CLS_Misskey_Com.STR_Status['FLG_Con'] = True
		CLS_Misskey_Com.STR_Status['FLG_Rec'] = False
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
		
###		#############################
###		# 受信停止中か？
###		if CLS_Misskey_Com.STR_Status['FLG_RecEnd']==True :
###			### 受信中は処理しない
###			return wRes
###		
		#############################
		# 受信中か？
		if CLS_Misskey_Com.STR_Status['FLG_Rec']==True :
			### 受信中は処理しない
			return wRes
		### 受信中
		CLS_Misskey_Com.STR_Status['FLG_Rec'] = True
		
		#############################
		# 受信停止OFF
		CLS_Misskey_Com.STR_Status['FLG_RecEnd'] = False
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
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# ノート送信
#####################################################
	def SendNote( self, inText ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Misskey_IF"
		wRes['Func']  = "SendNote"
		
		#############################
		# ノート送信
		try:
			CLS_Misskey_Com.OBJ_Misskey.notes_create( text=inText )
		except:
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



