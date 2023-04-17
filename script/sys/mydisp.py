#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : ディスプレイ表示
#####################################################

from osif import CLS_OSIF
from filectrl import CLS_File
from gval import gVal
#####################################################
class CLS_MyDisp():
#####################################################

#####################################################
# インプリメント処理
#####################################################
	@classmethod
	def sDispInp( cls, inDisp, inLine, inIndex, inData={} ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_MyDisp"
		wRes['Func']  = "sDispInp"
		
		###メイン画面
		if inDisp=="MainConsole" :
			cls.__dispInp_Main( inLine, wRes )
		###システム設定画面
		elif inDisp=="SystemConfigConsole" :
			cls.__dispInp_SystemConfig( inLine, wRes )
		###ユーザ管理画面
		elif inDisp=="UserAdminConsole" :
			cls.__dispInp_UserAdmin( inLine, wRes, inData )
		###キーワードいいね画面
		elif inDisp=="KeywordConsole" :
			cls.__dispInp_Keyword( inLine, wRes, inData )
		###リストいいね設定画面
		elif inDisp=="ListFavoConsole" :
			cls.__dispInp_ListFavo( inLine, wRes, inData )
		###禁止ユーザ画面
		elif inDisp=="ExcUserConsole" :
			cls.__dispInp_ExcUser( inLine, wRes, inData )
		###警告ユーザ管理
		elif inDisp=="CautionConsole" :
			cls.__dispInp_CautionUser( inLine, wRes, inData )
		###非絡みユーザ一覧
		elif inDisp=="UserBConsole" :
			cls.__dispInp_UserB( inLine, wRes, inData )
		
		###トラヒック報告
		elif inDisp=="TrafficReport" :
			cls.__dispInp_TrafficReport( inLine, wRes, inData )
		
		###システム情報画面
		elif inDisp=="SystemViewConsole" :
			cls.__dispInp_SystemView( inLine, wRes, inData )
		else:
			wRes['Reason'] = "Disp name is no: inDisp=" + str(inDisp)
		
		return wRes

	#####################################################
	# メイン画面
	@classmethod
	def __dispInp_Main( cls, inLine, outRes ):
		pRes = outRes
		#############################
		# インプリメント処理
		
		###インプリ：ユーザアカウント
		if "[@USER-ACCOUNT@]"==inLine :
			pRes['Responce'] = "Twitter ID : " + gVal.STR_UserInfo['Account']
		
		#############################
		# 正常
		pRes['Result'] = True
		return

	#####################################################
	# システム設定画面
	@classmethod
	def __dispInp_SystemConfig( cls, inLine, outRes ):
		pRes = outRes
		#############################
		# インプリメント処理
		
		###インプリ：ユーザアカウント
		if "[@USER-ACCOUNT@]"==inLine :
			pRes['Responce'] = "Twitter ID : " + gVal.STR_UserInfo['Account']
		
		#############################
		# 正常
		pRes['Result'] = True
		return

	#####################################################
	# ユーザ管理画面
	@classmethod
	def __dispInp_UserAdmin( cls, inLine, outRes, inData={} ):
		pRes = outRes
		#############################
		# インプリメント処理
		
		###インプリ：対象ユーザ
		if "[@USERADMIN-TWITTER@]"==inLine :
			pRes['Responce'] = "対象ユーザ  @" + inData['screen_name']
		
		elif "[@USERADMIN-TWITTER-ID@]"==inLine :
			pRes['Responce'] = "ユーザID     " + str(inData['id'])
		
		###インプリ：ユーザレベル
		elif "[@USERADMIN-USER_LEVEL@]"==inLine :
			if inData['flg_db_set']==False or inData['level_tag']==gVal.DEF_NOTEXT :
				wStr = ""
			else:
###				pRes['Responce'] = "ユーザレベル: " + str(inData['level_tag'])
				wStr = "ユーザレベル: " + str(inData['level_tag'])
			pRes['Responce'] = wStr
		
		###インプリ：フォロー者
		elif "[@USERADMIN-MYFOLLOW@]"==inLine :
			if inData['myfollow']==True :
				wStr = "〇はい"
			else:
				wStr = "▼いいえ"
			if inData['flg_db_set']==True and inData['myfollow_date']!=gVal.DEF_TIMEDATE :
				wStr = wStr + " [最終フォロー日: " + str( inData['myfollow_date'] ) + "]"
			pRes['Responce'] = "    フォロー中                  : " + wStr
		
		###インプリ：フォロワー
		elif "[@USERADMIN-FOLLOWER@]"==inLine :
			if inData['follower']==True :
				wStr = "〇はい"
			else:
				wStr = "▼いいえ"
			if inData['flg_db_set']==True and inData['follower_date']!=gVal.DEF_TIMEDATE :
				wStr = wStr + " [最終被フォロー: " + str( inData['follower_date'] ) + "]"
			pRes['Responce'] = "    フォロワー                  : " + wStr
		
		###インプリ：鍵アカウント
		elif "[@USERADMIN-PROTECT@]"==inLine :
			if inData['protected']==True :
				wStr = "●はい"
			else:
				wStr = "  いいえ"
			pRes['Responce'] = "    鍵アカウント                : " + wStr
		
		###インプリ：ブロック中
		elif "[@USERADMIN-MYBLOCK@]"==inLine :
			if inData['blocking']==True :
				wStr = "●はい"
			else:
				wStr = "  いいえ"
			pRes['Responce'] = "    ブロック中                  : " + wStr
		
		###インプリ：被ブロック
		elif "[@USERADMIN-BLOCKED@]"==inLine :
			if inData['blocked_by']==True :
				wStr = "●はい"
			else:
				wStr = "  いいえ"
			pRes['Responce'] = "    被ブロック                  : " + wStr
		
		###インプリ：最終いいね受信日
		elif "[@USERADMIN-R_FAVO_DATE@]"==inLine :
###			if inData['flg_db_set']==False or str(inData['rfavo_date'])==gVal.DEF_TIMEDATE or \
###			   inData['rfavo_cnt']==0 :
			if inData['flg_db_set']==False or str(inData['rfavo_date'])==gVal.DEF_TIMEDATE :
				wStr = "－－－"
			else:
###				wStr = str( inData['favo_date'] )
				wStr = str( inData['rfavo_date'] )
			if inData['flg_db_set']==True and inData['rfavo_cnt']>=0 :
				wStr = wStr + " [総計=" +str( inData['rfavo_cnt'] ) + " / 今週=" + str( inData['rfavo_n_cnt'] ) + "]"
			pRes['Responce'] = "    最終いいね受信日            : " + wStr
		
		###インプリ：最終リスト通知日
		elif "[@USERADMIN-LIST_DATE@]"==inLine :
			if inData['flg_db_set']==False or str(inData['list_ind_date'])==gVal.DEF_TIMEDATE :
				wStr = "－－－"
			else:
				wStr = str( inData['list_ind_date'] )
			pRes['Responce'] = "    最終リスト通知日            : " + wStr
		
		###インプリ：最終いいね実施日
		elif "[@USERADMIN-P_FAVO_DATE@]"==inLine :
			if inData['flg_db_set']==False or str(inData['pfavo_date'])==gVal.DEF_TIMEDATE or \
			   inData['pfavo_cnt']==0 :
				wStr = "－－－"
			else:
				wStr = str( inData['pfavo_date'] )
			if inData['flg_db_set']==True and inData['pfavo_cnt']>=0 :
				wStr = wStr + " [総計=" +str( inData['pfavo_cnt'] ) + "]"
			pRes['Responce'] = "    最終いいね実施日            : " + wStr
		
		###インプリ：最終いいね送信日
		elif "[@USERADMIN-SEND_DATE@]"==inLine :
			if inData['flg_db_set']==False or str(inData['send_date'])==gVal.DEF_TIMEDATE or \
			   inData['send_cnt']==0 :
				wStr = "－－－"
			else:
				wStr = str( inData['send_date'] )
			if inData['flg_db_set']==True and inData['send_cnt']>=0 :
				wStr = wStr + " [総計=" +str( inData['send_cnt'] ) + "]"
			pRes['Responce'] = "    最終いいね送信日            : " + wStr
		
		###インプリ：メモ
		elif "[@USERADMIN-MEMO@]"==inLine :
			if inData['flg_db_set']==False or inData['memo']==gVal.DEF_NOTEXT :
				wStr = ""
			else:
				wStr = str( inData['memo'] )
			pRes['Responce'] = wStr
		
		###インプリ：DB情報あり
		elif "[@USERADMIN-EXIST@]"==inLine :
			if inData['flg_db_set']==True :
				wStr = "〇はい"
				if inData['flg_save']==True :
					wStr = wStr + " [〇自動削除禁止]"
			
			else:
				wStr = "▼いいえ"
			pRes['Responce'] = "    DB情報あり                  : " + wStr
		
		###インプリ：DB登録日
		elif "[@USERADMIN-DB_REGDATE@]"==inLine :
			if inData['flg_db_set']==False or \
			   inData['regdate']==None :
				wStr = "－－－"
			else:
				wStr = str( inData['regdate'] )
			pRes['Responce'] = "    DB登録日                    : " + wStr
		
		###インプリ：操作ログ
###		elif "[@USERADMIN-LOG@]"==inLine and len(inData['log'])!=0 :
		elif "[@USERADMIN-LOG@]"==inLine :
			wStr = ""
			if len(inData['log'])==0 :
				wStr = "操作履歴がありません。" + '\n'
			else:
				wKeylist = list(inData['log'].keys() )
				for wIndex in wKeylist :
					wLog = inData['log'][wIndex] + '\n'
					wStr = wStr + wLog
			pRes['Responce'] = wStr
		
		#############################
		# 正常
		pRes['Result'] = True
		return

	#####################################################
	# キーワードいいね画面
	@classmethod
	def __dispInp_Keyword( cls, inLine, outRes, inData={} ):
		pRes = outRes
		#############################
		# インプリメント処理
		
		###インプリ：最大ツイート取得数
		if "[@KEYWORD-MAXSEARCHNUM@]"==inLine :
			pRes['Responce'] = "    最大ツイート取得数: " + str( inData['max_searchnum'] )
		
		###インプリ：記憶ユーザ数
		elif "[@KEYWORD-USERNUM@]"==inLine :
			pRes['Responce'] = "    記憶ユーザ数      : " + str( inData['usernum'] )
		
		###インプリ：抽出ユーザ数
		elif "[@KEYWORD-USERNUM@]"==inLine :
			pRes['Responce'] = "    抽出ユーザ数      : " + str( inData['now_usernum'] )
		
		###インプリ：いいね実行数
		elif "[@KEYWORD-FAVOUSERNUM@]"==inLine :
			pRes['Responce'] = "    いいね実行数      : " + str( inData['favo_usernum'] )
		
		###インプリ：検索データ 一覧
		elif "[@KEYWORD-LIST@]"==inLine :
			pRes['Responce'] = str( inData['list_data'] )
		
		#############################
		# 正常
		pRes['Result'] = True
		return

	#####################################################
	# リストいいね設定画面
	@classmethod
	def __dispInp_ListFavo( cls, inLine, outRes, inData=None ):
		pRes = outRes
		#############################
		# インプリメント処理
		
		###インプリ：リストいいね設定 一覧
		if "[@LISTFAVO_LIST@]"==inLine :
			pRes['Responce'] = inData
		
		#############################
		# 正常
		pRes['Result'] = True
		return

	#####################################################
	# 禁止ユーザ画面
	@classmethod
	def __dispInp_ExcUser( cls, inLine, outRes, inData=None ):
		pRes = outRes
		#############################
		# インプリメント処理
		
		###インプリ：禁止ユーザ 一覧
		if "[@EXCUSER-LIST@]"==inLine :
			pRes['Responce'] = inData
		
		#############################
		# 正常
		pRes['Result'] = True
		return

	#####################################################
	# 警告ユーザ画面
	@classmethod
	def __dispInp_CautionUser( cls, inLine, outRes, inData=None ):
		pRes = outRes
		#############################
		# インプリメント処理
		
		###インプリ：警告ユーザ 一覧
		if "[@CAUTION-LIST@]"==inLine :
			pRes['Responce'] = inData
		
		#############################
		# 正常
		pRes['Result'] = True
		return

	#####################################################
	# 非絡みユーザ一覧
	@classmethod
	def __dispInp_UserB( cls, inLine, outRes, inData=None ):
		pRes = outRes
		#############################
		# インプリメント処理
		
		###インプリ：警告ユーザ 一覧
		if "[@USERB_LIST@]"==inLine :
			pRes['Responce'] = inData
		
		#############################
		# 正常
		pRes['Result'] = True
		return



	#####################################################
	# システム情報画面
	@classmethod
	def __dispInp_SystemView( cls, inLine, outRes, inData={} ):
		pRes = outRes
		#############################
		# インプリメント処理
		
		###インプリ：ユーザアカウント
		if "[@USER-ID@]"==inLine :
			pRes['Responce'] = "Twitter ID : " + str( inData['screen_name'] ) + "(id=" + str( inData['id'] ) + ")"
		
		###インプリ：現在時刻
		elif "[@NOW-TIMEDATE@]"==inLine :
			pRes['Responce'] = "             " + str( inData['now_TimeDate'] )
		
		###インプリ：クライアント名
		elif "[@PRJ-CLIENT-NAME@]"==inLine :
			pRes['Responce'] = "    クライアント名    : " + str( inData['Prj_Client_Name'] )
		
		###インプリ：github
		elif "[@PRJ-GITHUB@]"==inLine :
			pRes['Responce'] = "    github            : " + str( inData['Prj_github'] )
		
		###インプリ：作成者(Admin)
		elif "[@PRJ-ADMIN@]"==inLine :
			pRes['Responce'] = "    作成者(Admin)     : " + str( inData['Prj_Admin'] )
		
		###インプリ：Pythonバージョン
		elif "[@PRJ-PYTHONVER@]"==inLine :
			pRes['Responce'] = "    Pythonバージョン  : " + str( inData['Prj_PythonVer'] )
		
		###インプリ：ホスト名
		elif "[@PRJ-HOSTNAME@]"==inLine :
			pRes['Responce'] = "    ホスト名          : " + str( inData['Prj_HostName'] )
		
		###インプリ：フォロー者数
		elif "[@TWT-MYFOLLOWNUM@]"==inLine :
			pRes['Responce'] = "    フォロー者数      : " + str( inData['Twt_MyFollowNum'] )
		
		###インプリ：フォロワー数
		elif "[@TWT-FOLLOWERNUM@]"==inLine :
			pRes['Responce'] = "    フォロワー数      : " + str( inData['Twt_FollowerNum'] )
		
		###インプリ：いいね数
		elif "[@TWT-FAVORITENUM@]"==inLine :
			pRes['Responce'] = "    いいね数          : " + str( inData['Twt_FavoriteNum'] )
		
		###インプリ：DBユーザ情報数
		elif "[@DB-FAVOUSERNUM@]"==inLine :
			pRes['Responce'] = "    DBユーザ情報数    : " + str( inData['DB_FavoUserNum'] )
		
		###インプリ：DBログ総数
		elif "[@DB-LOGNUM@]"==inLine :
			pRes['Responce'] = "    DBログ総数        : " + str( inData['DB_LogNum'] )
		
		###インプリ：トレンドタグ
		elif "[@SYS-TRENDTAG@]"==inLine :
			wStr = "    トレンドタグ      : "
			if inData['Sys_TrendTag']==None or inData['Sys_TrendTag']=="" :
				wStr = wStr + "(なし)"
			else:
				wStr = wStr + inData['Sys_TrendTag']
			pRes['Responce'] = wStr
		
		###インプリ：質問タグ
		elif "[@SYS-QUESTIONTAG@]"==inLine :
			wStr = "    質問タグ          : "
			if inData['Sys_QuestionTag']==None or inData['Sys_QuestionTag']=="" :
				wStr = wStr + "(なし)"
			else:
				wStr = wStr + inData['Sys_QuestionTag']
			pRes['Responce'] = wStr
		
		###インプリ：VIPタグ
		elif "[@SYS-VIPTAG@]"==inLine :
			wStr = "    VIPタグ           : "
			if inData['Sys_VipTag']==None or inData['Sys_VipTag']=="" :
				wStr = wStr + "(なし)"
			else:
				wStr = wStr + inData['Sys_VipTag']
			pRes['Responce'] = wStr
		
		###インプリ：削除タグ
		elif "[@SYS-DELTAG@]"==inLine :
			wStr = "    削除タグ          : "
			if inData['Sys_DelTag']==None or inData['Sys_DelTag']=="" :
				wStr = wStr + "(なし)"
			else:
				wStr = wStr + inData['Sys_DelTag']
			pRes['Responce'] = wStr
		
		###インプリ：リスト通知
		elif "[@SYS-LISTNAME@]"==inLine :
			wStr = "    リスト通知        : "
			if inData['Sys_ListName']==None or inData['Sys_ListName']=="" :
				wStr = wStr + "無効"
			else:
				wStr = wStr + "有効(list=" + inData['Sys_ListName'] + ")"
			pRes['Responce'] = wStr
		
		###インプリ：自動リムーブ
		elif "[@SYS-AUTOREMOVE@]"==inLine :
			wStr = "    自動リムーブ      : "
			if inData['Sys_AutoRemove']==None or inData['Sys_AutoRemove']=="" :
				wStr = wStr + "無効"
			else:
				wStr = wStr + "有効"
			pRes['Responce'] = wStr
		
		###インプリ：相互フォローリスト
		elif "[@SYS-MLISTNAME@]"==inLine :
			wStr = "    相互フォローリスト: "
			if inData['Sys_mListName']==None or inData['Sys_mListName']=="" :
				wStr = wStr + "無効"
			else:
				wStr = wStr + "有効(list=" + inData['Sys_mListName'] + ")"
			pRes['Responce'] = wStr
		
		###インプリ：片フォロワーリスト
		elif "[@SYS-FLISTNAME@]"==inLine :
			wStr = "    片フォロワーリスト: "
			if inData['Sys_fListName']==None or inData['Sys_fListName']=="" :
				wStr = wStr + "無効"
			else:
				wStr = wStr + "有効(list=" + inData['Sys_fListName'] + ")"
			pRes['Responce'] = wStr
		
		###インプリ：相互いいね停止
		elif "[@SYS-MFVSTOP@]"==inLine :
			wStr = "    相互いいね停止    : "
			if inData['Sys_MFvStop']==False :
				wStr = wStr + "未設定"
			else:
				wStr = wStr + "設定中(設定日時=" + str(inData['Sys_MFvStop_Date']) + ")"
			pRes['Responce'] = wStr
		
		#############################
		# 正常
		pRes['Result'] = True
		return



	#####################################################
	# トラヒック報告
	@classmethod
	def __dispInp_TrafficReport( cls, inLine, outRes, inData={} ):
		pRes = outRes
		#############################
		# インプリメント処理
		
		###インプリデータチェック
		if inLine not in inData :
			pRes['Result'] = True
			return
		
		###インプリ
		pRes['Responce'] = inData[inLine]
		
		#############################
		# 正常
		pRes['Result'] = True
		return



#####################################################
# ディスプレイファイル 読み込み→画面表示
#####################################################
	@classmethod
	def sViewDisp( cls, inDisp, inIndex=-1, inClear=True, inData={} ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_MyDisp"
		wRes['Func']  = "sViewDisp"
		
		#############################
		# ディスプレイファイルの確認
		wKeylist = gVal.DEF_STR_DISPFILE.keys()
		if inDisp not in wKeylist :
			###キーがない(指定ミス)
			wRes['Reason'] = "Display key is not found: inDisp= " + inDisp
			return wRes
		
		if CLS_File.sExist( gVal.DEF_STR_DISPFILE[inDisp] )!=True :
			###ファイルがない...(消した？)
			wRes['Reason'] = "Displayファイルがない: file=" + gVal.DEF_STR_DISPFILE[inDisp]
			return wRes
		
		#############################
		# ディスプレイファイルの読み込み
		wDispFile = []
		if CLS_File.sReadFile( gVal.DEF_STR_DISPFILE[inDisp], outLine=wDispFile, inStrip=False )!=True :
			wRes['Reason'] = "Displayファイルがない(sReadFile): file=" + gVal.DEF_STR_DISPFILE[inDisp]
			return wRes
		
		if len(wDispFile)<=1 :
			wRes['Reason'] = "Displayファイルが空: file=" + gVal.DEF_STR_DISPFILE[inDisp]
			return wRes
		
		#############################
		# 画面クリア(=通常モード時)
		if gVal.FLG_Test_Mode==False and inClear==True :
			CLS_OSIF.sDispClr()
		
		#############################
		# 画面に表示する
		for wLine in wDispFile :
			###コメントはスキップ
			if wLine.find("#")==0 :
				continue
			
			###インプリメント
			wResInp = cls.sDispInp( inDisp, wLine, inIndex, inData )
			if wResInp['Result']!=True :
				wRes['Reason'] = "sDispInp is failed: reason=" + str(wResInp['Reason'])
				return wRes
			if wResInp['Responce']!=None :
				###インプリメントされていれば差し替える
				wLine = wResInp['Responce']
			
			#############################
			# print表示
			CLS_OSIF.sPrn( wLine )
		
		#############################
		# 正常処理
		wRes['Result'] = True
		return wRes

	#####################################################
	@classmethod
	def __get_JPstr_Single( cls, inFLG_Inc ):
		if inFLG_Inc==True :
			wStr = "はい"
		else:
			wStr = "いいえ"
		return wStr


	#####################################################
	@classmethod
	def __get_JPstr_Dual( cls, inFLG_Inc, inFLG_Exc ):
		if inFLG_Inc==True and inFLG_Exc==False :
			wStr = "含める"
		elif inFLG_Inc==False and inFLG_Exc==True :
			wStr = "除外する"
		elif inFLG_Inc==False and inFLG_Exc==False :
			wStr = "無条件"
		else:
			wStr = None
		return wStr



#####################################################
# ヘッダ表示
#####################################################
	@classmethod
	def sViewHeaderDisp( cls, inText, inFLG_Prossessing=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_MyDisp"
		wRes['Func']  = "sViewHeaderDisp"
		
		wStr =        "******************************" + '\n'
		wStr = wStr + inText + '\n'
		wStr = wStr + "******************************" + '\n'
		
		if inFLG_Prossessing==True :
			wStr = wStr + "処理中です。しばらくお待ちください......" + '\n'
		
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 正常
		wRes['Result'] = True
		return



