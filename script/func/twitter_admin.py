#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : Twitter監視 管理系
#####################################################

from ktime import CLS_TIME
from osif import CLS_OSIF
from traffic import CLS_Traffic
from htmlif import CLS_HTMLIF
from mydisp import CLS_MyDisp
from gval import gVal
#####################################################
class CLS_TwitterAdmin():
#####################################################
	OBJ_Parent = ""				#親クラス実体
	
	STR_UserAdminInfo = None
	
###	STR_UserBList = {}
###	
###	ARR_CautionList = {}
	DEF_VAL_SLEEP = 10			#Twitter処理遅延（秒）

	DEF_ADMIN_SCORE_LEN = 3



#####################################################
# Init
#####################################################
	def __init__( self, parentObj=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__init__"
		
		if parentObj==None :
			###親クラス実体の未設定
			wRes['Reason'] = "You have not set the parent class entity for parentObj"
			gVal.OBJ_L.Log( "A", wRes )
			return
		
		self.OBJ_Parent = parentObj
		self.GetUserAdminInfo()
		return



#####################################################
# ユーザ管理情報 枠取得
#####################################################
	def GetUserAdminInfo(self):
		
		self.STR_UserAdminInfo = {
			"flg_set"			: False,		# 設定 True=設定済
			
			"id"        		: -1,			# ユーザID
			"name"				: None,			# Twitterユーザ名(日本語)
			"screen_name"		: None,			# Twitterアカウント名(英語)
			"statuses_count"	: -1,
			
			"myfollow"			: False,		# フォロー者
			"follower"			: False,		# フォロワー
			
			"protected"			: False,		# 鍵付き
			"blocking"			: False,		# ブロック
			"blocked_by"		: False,		# 被ブロック
			"excute_by"			: False,		# 禁止ユーザ
			
			"flg_db_set"		: False,		# DB設定 True=DBあり
			"regdate"			: None,
			"upddate"			: None,
			"flg_save"			: False,
			
			"level_tag"			: None,
			
			"send_date"			: None,
			"send_cnt"			: -1,
			
			"rfavo_date"		: None,
			"rfavo_cnt"			: -1,
			"rfavo_n_cnt"		: -1,
			"pfavo_date"		: None,
			"pfavo_cnt"			: -1,
			"list_ind_date"		: None,
			
			"myfollow_date"		: None,
			"follower_date"		: None,
			
			"memo"				: None, 
			"log"				: {}
		}
		return



#####################################################
# ユーザ管理
#####################################################
	def UserAdmin(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "UserAdmin"
		
		#############################
		# コンソールを表示
		while True :
			
			self.STR_UserAdminInfo['flg_set'] = False
			#############################
			# 画面クリア
			CLS_OSIF.sDispClr()
			
			#############################
			# ヘッダ表示
			wStr = "--------------------" + '\n'
			wStr = wStr + " ユーザ管理" + '\n'
			wStr = wStr + "--------------------" + '\n'
			wStr = wStr + "管理をおこないたいユーザのTwitter ID(@なし)を入力してください。" + '\n'
			wStr = wStr + "中止する場合は \q を入力してください" + '\n'
			CLS_OSIF.sPrn( wStr )
			
			#############################
			# 実行の確認
			wTwitterID = CLS_OSIF.sInp( "Twitter ID(@なし)？(\\q=中止)=> " )
			if wTwitterID=="\\q" :
				##キャンセル
				wRes['Result'] = True
				return wRes
			
			#############################
			# 処理中表示
			CLS_OSIF.sPrn( "確認しています。しばらくお待ちください......" )
			
			#############################
			# ユーザ情報を取得する
			wUserinfoRes = self.__get_UserAdmin( wTwitterID )
			if wUserinfoRes['Result']!=True :
				wRes['Reason'] = "__get_UserAdmin is failed: " + wUserinfoRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wUserinfoRes['Responce']==False :
				continue
			
			#############################
			# 管理の本画面を表示する
			while True :
				wWord = self.__view_UserAdmin()
				
				if wWord=="\\q" :
					###終了
					break
				if wWord=="" :
					###未入力は再度入力
					continue
				
				wResSearch = self.__run_UserAdmin( wWord )
				if wResSearch['Result']!=True :
					### 処理失敗
					continue
		
		wRes['Result'] = True
		return wRes

	#####################################################
	# ユーザ管理 画面表示
	#####################################################
	def __view_UserAdmin(self):
		wResDisp = CLS_MyDisp.sViewDisp( inDisp="UserAdminConsole", inIndex=-1, inData=self.STR_UserAdminInfo )
		if wResDisp['Result']==False :
			gVal.OBJ_L.Log( "B", wResDisp )
			return "\\q"	#失敗=強制終了
		
		wWord = CLS_OSIF.sInp( "コマンド？=> " )
		return wWord

	#####################################################
	# ユーザ管理 実行
	#####################################################
	def __run_UserAdmin( self, inWord ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__run_UserAdmin"
		
		#############################
		# コマンド：リムーブする
		if inWord=="\\rm" :
			wRes = self.__run_Remove()
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
		
		#############################
		# コマンド：関係リセット
		elif inWord=="\\rma" :
			wRes = self.__run_Reset()
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
		
###		#############################
###		# コマンド：相互レベル変更
###		elif inWord=="\\ml" :
###			wRes = self.__run_ChangeLevel()
###			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
###		
		#############################
		# コマンド：ブラウザで表示
		elif inWord=="\\p" :
			wRes = self.__view_Profile( self.STR_UserAdminInfo['screen_name'] )
		
		#############################
		# コマンド：VIP設定
		elif inWord=="\\v" :
			wRes = self.__run_UserAdmin_VIP()
		
		#############################
		# コマンド：自動削除禁止
		elif inWord=="\\r" :
			wRes = self.__run_UserAdmin_Save()
		
		#############################
		# コマンド：メモする
		elif inWord=="\\m" :
			wRes = self.__run_UserAdmin_memo()
		
		#############################
		# コマンド：レベル強制変更
		elif inWord=="\\fl" :
			wRes = self.__run_UserAdmin_LevelChange()
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
		
		#############################
		# 不明なコマンド
		else :
			CLS_OSIF.sPrn( "不明なコマンドです" + '\n' )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
		
		return wRes



#####################################################
# リムーブ実行
#####################################################
	def __run_Remove(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__run_Remove"
		
		#############################
		# フォロー中か
		if self.STR_UserAdminInfo['myfollow']!=True :
			CLS_OSIF.sPrn( "そのユーザはフォローしてません" + '\n' )
			return wRes
		
		CLS_OSIF.sPrn( "リムーブ処理をおこなってます。しばらくお待ちください......" )
		#############################
		# リムーブする
		wSubRes = gVal.OBJ_Tw_IF.Remove( self.STR_UserAdminInfo['id'] )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "RelRemove is failed: " + wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			###失敗してもDB削除は継続する
		### Twitter Wait
		CLS_OSIF.sSleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 情報反映
		wSubRes = self.__get_UserAdmin( inScreenName=self.STR_UserAdminInfo['screen_name'] )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "__get_UserAdmin is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常終了
###		gVal.OBJ_L.Log( "R", wRes, "●リムーブ者: " + self.STR_UserAdminInfo['screen_name'] )
		gVal.OBJ_L.Log( "R", wRes, "●リムーブ者: " + self.STR_UserAdminInfo['screen_name'], inID=self.STR_UserAdminInfo['id'] )
		
		wRes['Result'] = True
		return wRes



#####################################################
# 相互レベル変更
#####################################################
###	def __run_ChangeLevel(self):
###		#############################
###		# 応答形式の取得
###		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
###		wRes = CLS_OSIF.sGet_Resp()
###		wRes['Class'] = "CLS_TwitterAdmin"
###		wRes['Func']  = "__run_ChangeLevel"
###		
###		wID = str(self.STR_UserAdminInfo['id'])
###		#############################
###		# 相互フォロー中か
###		if gVal.OBJ_Tw_IF.CheckSubscribeListUser( wID )!=False :
###			CLS_OSIF.sPrn( "そのユーザは変更できません" + '\n' )
###			return wRes
###		
###		#############################
###		# 相互フォロー中か
###		if self.STR_UserAdminInfo['myfollow']==True and \
###		   self.STR_UserAdminInfo['follower']==True and \
###		   gVal.OBJ_Tw_IF.CheckMutualListUser( wID )==True and \
###		   gVal.OBJ_Tw_IF.CheckFollowListUser( wID )==False and \
###		   ( self.STR_UserAdminInfo['level_tag']=="B" or self.STR_UserAdminInfo['level_tag']=="B+" or \
###		     self.STR_UserAdminInfo['level_tag']=="C" or self.STR_UserAdminInfo['level_tag']=="C+" ) :
###			
######			wUserLevel = "G"
###			wUserLevel = "G+"
###		
###		#############################
###		# 片フォロワーか
###		elif self.STR_UserAdminInfo['myfollow']==False and \
###		     self.STR_UserAdminInfo['follower']==True and \
###		     gVal.OBJ_Tw_IF.CheckMutualListUser( wID )==False and \
###		     gVal.OBJ_Tw_IF.CheckFollowListUser( wID )==True and \
###		     self.STR_UserAdminInfo['level_tag']=="E" :
###			
######			wUserLevel = "H"
###			wUserLevel = "H+"
###		
###		#############################
###		# 相互フォロー中 解除か
###		elif self.STR_UserAdminInfo['myfollow']==True and \
###		     self.STR_UserAdminInfo['follower']==True and \
###		     gVal.OBJ_Tw_IF.CheckMutualListUser( wID )==True and \
###		     gVal.OBJ_Tw_IF.CheckFollowListUser( wID )==False and \
###		     ( self.STR_UserAdminInfo['level_tag']=="G" or self.STR_UserAdminInfo['level_tag']=="G+" ) :
###			
###			if self.STR_UserAdminInfo['send_cnt']>=gVal.DEF_STR_TLNUM['LEVEL_B_Cnt'] :
###				wUserLevel = "B+"
###			elif self.STR_UserAdminInfo['send_cnt']>=1 :
###				wUserLevel = "B"
###			else:
###				wUserLevel = "C+"
###		
###		#############################
###		# 片フォロワー 解除か
######		elif self.STR_UserAdminInfo['myfollow']==False and \
######		     self.STR_UserAdminInfo['follower']==True and \
######		     gVal.OBJ_Tw_IF.CheckMutualListUser( wID )==False and \
######		     gVal.OBJ_Tw_IF.CheckFollowListUser( wID )==True and \
###		     self.STR_UserAdminInfo['level_tag']=="H" :
###		elif self.STR_UserAdminInfo['myfollow']==False and \
###		     self.STR_UserAdminInfo['follower']==True and \
###		     gVal.OBJ_Tw_IF.CheckMutualListUser( wID )==False and \
###		     gVal.OBJ_Tw_IF.CheckFollowListUser( wID )==True and \
###		     ( self.STR_UserAdminInfo['level_tag']=="H" or self.STR_UserAdminInfo['level_tag']=="H+" ) :
###			
###			wUserLevel = "E"
###		
###		#############################
###		# 制御不能
###		else:
###			CLS_OSIF.sPrn( "そのユーザは変更できません(2)" + '\n' )
###			return wRes
###		
###		#############################
###		# ユーザレベルの変更の実行
###		wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( self.STR_UserAdminInfo['id'], wUserLevel )
###		if wSubRes['Result']!=True :
###			###失敗
###			wRes['Reason'] = "UpdateFavoData_UserLevel is failed"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		
###		#############################
###		# ユーザ管理へ変更
###		self.STR_UserAdminInfo['level_tag'] = wUserLevel
###		
###		wStr = "レベルタグを変更しました"
###		CLS_OSIF.sPrn( wStr )
###		
###		#############################
###		# 正常終了
###		wRes['Result'] = True
###		return wRes
##
###

#####################################################
# 関係リセット実行
#####################################################
	def __run_Reset(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__run_Reset"
		
		CLS_OSIF.sPrn( "リムーブ処理をおこなってます。しばらくお待ちください......" )
		#############################
		# ブロック＆リムーブする
		wSubRes = gVal.OBJ_Tw_IF.BlockRemove( self.STR_UserAdminInfo['id'] )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "BlockRemove is failed: " + wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			###失敗してもDB削除は継続する
		### Twitter Wait
		CLS_OSIF.sSleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 関係解除= DB削除
		if self.STR_UserAdminInfo['flg_db_set']==True :
			wQuery = "delete from tbl_favouser_data " + \
						"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
						" and id = '" + str(self.STR_UserAdminInfo['id']) + "' ;"
			
			wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
			if wResDB['Result']!=True :
				wRes['Reason'] = "Run Query is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# 情報反映
		wSubRes = self.__get_UserAdmin( inScreenName=self.STR_UserAdminInfo['screen_name'] )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "__get_UserAdmin is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常終了
###		gVal.OBJ_L.Log( "R", wRes, "●関係リセットによるリムーブ: " + self.STR_UserAdminInfo['screen_name'] )
		gVal.OBJ_L.Log( "R", wRes, "●関係リセットによるリムーブ: " + self.STR_UserAdminInfo['screen_name'], inID=self.STR_UserAdminInfo['id'] )
		
		wRes['Result'] = True
		return wRes



#####################################################
# ブラウザ表示
#####################################################
	def __view_Profile( self, inScreenName ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__view_Profile"
		
		#############################
		# ブラウザ表示
		wURL = "https://twitter.com/" + inScreenName
		CLS_HTMLIF.sOpenURL( wURL )
		
		### Twitter Wait
		CLS_OSIF.sSleep( self.DEF_VAL_SLEEP )
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



#####################################################
# VIP設定
#####################################################
	def __run_UserAdmin_VIP(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__run_UserAdmin_VIP"
		
		wLevelTag = self.STR_UserAdminInfo['level_tag']
		#############################
		# ユーザレベルの変更
		if wLevelTag=="A+" and \
		   self.STR_UserAdminInfo['myfollow']==True and self.STR_UserAdminInfo['follower']==True :
			### VIP設定解除
			if self.STR_UserAdminInfo['send_cnt']>=gVal.DEF_STR_TLNUM['LEVEL_B_Cnt'] :
				wLevelTag = "B+"
			elif self.STR_UserAdminInfo['send_cnt']>=1 :
				wLevelTag = "B"
			else:
				wLevelTag = "C+"
		
		elif ( wLevelTag=="B+" or wLevelTag=="B" or wLevelTag=="C+" or wLevelTag=="C" ) and \
		   self.STR_UserAdminInfo['myfollow']==True and self.STR_UserAdminInfo['follower']==True :
			### VIP設定
			wLevelTag = "A+"
		
		elif wLevelTag=="A" :
			### 公式アカウントのため変更不可
			wStr = "レベル A のためVIP設定できません"
			CLS_OSIF.sInp( wStr )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		elif self.STR_UserAdminInfo['myfollow']==False or self.STR_UserAdminInfo['follower']==False :
			### 相互フォローではない
			wStr = "相互フォローでないためVIP設定できません"
			CLS_OSIF.sInp( wStr )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		else:
			### 変更不能のレベル
			wStr = "設定できないレベルのためVIP設定できません"
			CLS_OSIF.sInp( wStr )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# ユーザレベルの変更の実行
		wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( self.STR_UserAdminInfo['id'], wLevelTag )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "UpdateFavoData_UserLevel is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# ユーザ管理へ変更
		self.STR_UserAdminInfo['level_tag'] = wLevelTag
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# 自動削除禁止
#####################################################
	def __run_UserAdmin_Save(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__run_UserAdmin_Save"
		
		#############################
		# DBがなければ終わり
		if self.STR_UserAdminInfo['flg_db_set']==False :
			wStr = "DBがないため設定できません"
			CLS_OSIF.sInp( wStr )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# 実行の確認
		wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_FLG_Save( self.STR_UserAdminInfo['id'] )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "UpdateFavoData_FLG_Save is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wStr = "禁止ユーザを削除しました"
		CLS_OSIF.sInp( wStr )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# メモする
#####################################################
	def __run_UserAdmin_memo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__run_UserAdmin_memo"
		
		#############################
		# コンソールを表示
		wStr = "memoを入力します。" + '\n'
		wStr = wStr + "  \\q=中止 / \\r=メモ削除 / other=memo" + '\n'
		CLS_OSIF.sPrn( wStr )
		wWord = CLS_OSIF.sInp( "  => " )
		if wWord!="\\q" :
			wRes['Result'] = True
			return wRes
		
		elif wWord!="\\r" :
			wWord = gVal.DEF_NOTEXT
		
		#############################
		# 実行の確認
		wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_memo( self.STR_UserAdminInfo['id'], wWord )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "UpdateFavoData_memo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wStr = "禁止ユーザを削除しました"
		CLS_OSIF.sInp( wStr )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# レベル強制変更
#####################################################
	def __run_UserAdmin_LevelChange(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__run_UserAdmin_LevelChange"
		
		#############################
		# DBがなければ終わり
		if self.STR_UserAdminInfo['flg_db_set']==False :
			wStr = "DBがないため設定できません"
			CLS_OSIF.sInp( wStr )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# コンソールを表示
		wStr = "ユーザレベルを変更します。変更後のレベルタグを入力してください。" + '\n'
		wStr = wStr + "  \\q=中止 / other=change" + '\n'
		CLS_OSIF.sPrn( wStr )
		wWord = CLS_OSIF.sInp( "  => " )
		if wWord=="\\q" :
			wStr = "中止しました。" + '\n'
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
		#############################
		# 入力チェック
		if wWord not in gVal.DEF_STR_USER_LEVEL :
			wStr = "対応しないレベルタグのため、変更できませんでした。" + '\n'
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
		#############################
		# ユーザレベルの変更の実行
		wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( self.STR_UserAdminInfo['id'], wWord )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "UpdateFavoData_UserLevel is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# ユーザ管理へ変更
		self.STR_UserAdminInfo['level_tag'] = wWord
		
		wStr = "レベルタグを変更しました"
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# ユーザ情報取得
#####################################################
	def __get_UserAdmin( self, inScreenName ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__get_UserAdmin"
		
		wRes['Responce'] = False
		#############################
		# 退避枠初期化
		self.GetUserAdminInfo()
		
		#############################
		# Twitterからユーザ情報を取得する
		wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inScreenName=inScreenName )
		if wUserInfoRes['Result']!=True :
			### 404エラーか
			if CLS_OSIF.sRe_Search( "404", wUserInfoRes['Reason'] )!=False :
				### ユーザが存在しない
				wRes['Responce'] = False
				wRes['Reason'] = "Twitterに存在しないユーザ"
				wRes['Result'] = True
				return wRes
			
			wRes['Reason'] = "Twitter API Error(GetUserinfo): " + wUserInfoRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### Twitter Wait
		CLS_OSIF.sSleep( self.DEF_VAL_SLEEP )
		
		### IDの取得
		wID = str( wUserInfoRes['Responce']['id'] )
		
		wFLG_DB = False
		wARR_DBData = None
		#############################
		# DBからユーザ情報を取得する(1個)
		wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( wUserInfoRes['Responce'], inFLG_New=False )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetFavoDataOne is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wSubRes['Responce']['Data']!=None :
			### DBにユーザが存在する
			wFLG_DB = True
			wARR_DBData = wSubRes['Responce']['Data']
		
		#############################
		# Twitterからフォロー関係を取得する
		wFollowInfoRes = gVal.OBJ_Tw_IF.GetFollowInfo( wID )
		if wFollowInfoRes['Result']!=True :
			wRes['Reason'] = "Twitter API Error(GetUserinfo): " + wFollowInfoRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 退避に情報を反映する
		
		### Twitter UserInfo
		self.STR_UserAdminInfo['screen_name'] = inScreenName
		self.STR_UserAdminInfo['name']    = str( wUserInfoRes['Responce']['name'] )
		self.STR_UserAdminInfo['id']      = wID
		self.STR_UserAdminInfo['statuses_count'] = str(wUserInfoRes['Responce']['statuses_count'])
		self.STR_UserAdminInfo['protected'] = wUserInfoRes['Responce']['protected']
		
		### Twitter Follow
		self.STR_UserAdminInfo['myfollow'] = wFollowInfoRes['Responce']['following']
		self.STR_UserAdminInfo['follower'] = wFollowInfoRes['Responce']['followed_by']
		self.STR_UserAdminInfo['blocking'] = wFollowInfoRes['Responce']['blocking']
		self.STR_UserAdminInfo['blocked_by'] = wFollowInfoRes['Responce']['blocked_by']
		
		### DB
		if wFLG_DB==True :
			self.STR_UserAdminInfo['regdate']  = str( wARR_DBData['regdate'] )
			self.STR_UserAdminInfo['upddate']  = str( wARR_DBData['upddate'] )
			self.STR_UserAdminInfo['flg_save'] = wARR_DBData['flg_save']
			
			self.STR_UserAdminInfo['level_tag'] = str( wARR_DBData['level_tag'] )
			self.STR_UserAdminInfo['send_date'] = str( wARR_DBData['send_date'] )
			self.STR_UserAdminInfo['send_cnt']  = wARR_DBData['send_cnt']
			
			self.STR_UserAdminInfo['rfavo_date']  = str( wARR_DBData['rfavo_date'] )
			self.STR_UserAdminInfo['rfavo_cnt']   = wARR_DBData['rfavo_cnt']
			self.STR_UserAdminInfo['rfavo_n_cnt'] = wARR_DBData['rfavo_n_cnt']
			self.STR_UserAdminInfo['pfavo_date']  = str( wARR_DBData['pfavo_date'] )
			self.STR_UserAdminInfo['pfavo_cnt']   = wARR_DBData['pfavo_cnt']
			self.STR_UserAdminInfo['list_ind_date'] = str( wARR_DBData['list_ind_date'] )
			self.STR_UserAdminInfo['myfollow_date'] = str( wARR_DBData['myfollow_date'] )
			self.STR_UserAdminInfo['follower_date'] = str( wARR_DBData['follower_date'] )
			
			self.STR_UserAdminInfo['memo'] = str( wARR_DBData['memo'] )
			
			self.STR_UserAdminInfo['flg_db_set'] = True
		
		#############################
		# 操作ログの取得
		self.STR_UserAdminInfo['log'] = {}
		wARR_Log = gVal.OBJ_L.GetLog( wID )
		wKeylist = list( wARR_Log.keys() )
		wCnt = 1
		for wIndex in wKeylist :
			if gVal.DEF_ADMINLOG_POINT<wCnt :
				break
			
			wLog = wARR_Log[wIndex]['regdate'] + "  " + wARR_Log[wIndex]['level'] + " : "
			wLog = wLog + wARR_Log[wIndex]['reason']
			self.STR_UserAdminInfo['log'].update({ wCnt : wLog })
			wCnt += 1
		
		### データセット
		self.STR_UserAdminInfo['flg_set'] = True
		
		#############################
		# 正常
		wRes['Responce'] = True
		wRes['Result'] = True
		return wRes



#####################################################
# 禁止ユーザ
#####################################################
	def ExcuteUser(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "ExcuteUser"
		
		#############################
		# コンソールを表示
		while True :
			
			#############################
			# データ表示
			self.__view_ExcuteUser()
			
			#############################
			# 実行の確認
			wListNumber = CLS_OSIF.sInp( "コマンド？(\\q=中止)=> " )
			if wListNumber=="\\q" :
				wRes['Result'] = True
				return wRes
			
			#############################
			# コマンド処理
			wCommRes = self.__run_ExcuteUser( wListNumber )
			if wCommRes['Result']!=True :
				wRes['Reason'] = "__run_ExcuteUser is failed: " + wCommRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		wRes['Result'] = True
		return wRes

	#####################################################
	# 画面表示
	#####################################################
	def __view_ExcuteUser(self):
		
		wKeylist = list( gVal.ARR_NotReactionUser.keys() )
		wStr = ""
		for wI in wKeylist :
			wStr = wStr + "   : "
			
			### リスト番号
			wListData = str(gVal.ARR_NotReactionUser[wI]['list_number'])
			wListNumSpace = 4 - len( wListData )
			if wListNumSpace>0 :
				wListData = wListData + " " * wListNumSpace
			wStr = wStr + wListData + ": "
			
			### 通報 有効/無効
			if gVal.ARR_NotReactionUser[wI]['vip']==True :
				wStr = wStr + "[－]"
			elif gVal.ARR_NotReactionUser[wI]['report']==True :
				wStr = wStr + "[〇]"
			else:
				wStr = wStr + "[  ]"
			wStr = wStr + "  "
			
			### VIP 有効/無効
			if gVal.ARR_NotReactionUser[wI]['report']==True :
				wStr = wStr + "[－  ]"
			elif gVal.ARR_NotReactionUser[wI]['vip']==True :
				if gVal.ARR_NotReactionUser[wI]['ope']==True :
					wStr = wStr + "[〇監]"
				else:
					wStr = wStr + "[〇  ]"
			else:
				wStr = wStr + "[    ]"
			wStr = wStr + "   "
			
			### フォロー監視 有効/無効
			if gVal.ARR_NotReactionUser[wI]['vip']==False :
				wStr = wStr + "[－]"
			else:
				if gVal.ARR_NotReactionUser[wI]['follow']==True :
					wStr = wStr + "[〇]"
				else:
					wStr = wStr + "[  ]"
			wStr = wStr + "  "
			
			### ユーザ名
			wListData = gVal.ARR_NotReactionUser[wI]['screen_name']
			wStr = wStr + wListData + '\n'
		
		wResDisp = CLS_MyDisp.sViewDisp( inDisp="ExcUserConsole", inIndex=-1, inData=wStr )
		if wResDisp['Result']==False :
			gVal.OBJ_L.Log( "D", wResDisp )
		
		return

	#####################################################
	# コマンド処理
	#####################################################
	def __run_ExcuteUser( self, inWord ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__run_ExcuteUser"
		
		#############################
		# s: 禁止ユーザ追加
		if inWord=="\\s" :
			self.__set_ExcuteUser()
###			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# チェック
		
		wARR_Comm = str(inWord).split("-")
		wCom = None
		if len(wARR_Comm)==1 :
			wNum = wARR_Comm[0]
			wCom = None
		elif len(wARR_Comm)==2 :
			wNum = wARR_Comm[0]
			wCom = wARR_Comm[1]
		else:
			CLS_OSIF.sPrn( "コマンドの書式が違います" + '\n' )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		### 整数か
		try:
			wNum = int(wNum)
		except ValueError:
			CLS_OSIF.sPrn( "LIST番号が整数ではありません" + '\n' )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# リストのインデックス
		wGetIndex = None
		wKeylist = list( gVal.ARR_NotReactionUser.keys() )
		for wID in wKeylist :
			wID = str(wID)
			if gVal.ARR_NotReactionUser[wID]['list_number']==wNum :
				wGetIndex = wID
				break
		if wGetIndex==None :
			CLS_OSIF.sPrn( "LIST番号が範囲外です" + '\n' )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# コマンドの分岐
		
		#############################
		# コマンドなし: 通報の設定変更をする
		if wCom==None :
			wFLG_Update = False
			if gVal.ARR_NotReactionUser[wGetIndex]['report']==False :
				### VIP ONの場合は排他する
				if gVal.ARR_NotReactionUser[wGetIndex]['vip']==True :
					CLS_OSIF.sPrn( "VIP ONのため通報設定にできません" )
					CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
					wRes['Result'] = True
					return wRes
				
				wFLG_Update = True
			
			wSubRes = gVal.OBJ_DB_IF.UpdateExeUser( wGetIndex, inReport=wFLG_Update )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "UpdateExeUser is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
###			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# c: VIP 有効/無効
		elif wCom=="p" :
			wFLG_Update = False
			if gVal.ARR_NotReactionUser[wGetIndex]['vip']==False :
				### 通報 ONの場合は排他する
				if gVal.ARR_NotReactionUser[wGetIndex]['report']==True :
					CLS_OSIF.sPrn( "通報 ONのためVIP設定にできません" )
					CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
					wRes['Result'] = True
					return wRes
				
				### 予約削除の場合は設定不可にする
				if gVal.ARR_NotReactionUser[wGetIndex]['rel_date']!=gVal.DEF_TIMEDATE :
					CLS_OSIF.sPrn( "予約削除中のため設定にできませ" )
					CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
					wRes['Result'] = True
					return wRes
				
				wFLG_Update = True
			else:
				if gVal.ARR_NotReactionUser[wGetIndex]['ope']==True :
					### VIP監視 ONの場合は排他する
					CLS_OSIF.sPrn( "VIP監視 ONのためVIP設定解除できません" )
					CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
					wRes['Result'] = True
					return wRes
			
			wSubRes = gVal.OBJ_DB_IF.UpdateExeUser( wGetIndex, inVIP=wFLG_Update )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "UpdateExeUser is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
###			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# o: VIP監視 有効/無効
		elif wCom=="o" :
			wFLG_Update = False
			if gVal.ARR_NotReactionUser[wGetIndex]['ope']==False :
				if gVal.ARR_NotReactionUser[wGetIndex]['vip']==False :
					### VIP OFFの場合は排他する
					CLS_OSIF.sPrn( "VIP OFFのためVIP監視設定できません" )
					CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
					wRes['Result'] = True
					return wRes
				
				wFLG_Update = True
			
			wSubRes = gVal.OBJ_DB_IF.UpdateExeUser( wGetIndex, inOpe=wFLG_Update )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "UpdateExeUser is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			wRes['Result'] = True
			return wRes
		
		#############################
		# f: フォロー監視 有効/無効
		elif wCom=="f" :
			wFLG_Update = False
			if gVal.ARR_NotReactionUser[wGetIndex]['vip']==False :
				CLS_OSIF.sPrn( "VIP OFFのためVIP監視設定できません" )
				CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
				wRes['Result'] = True
				return wRes
			
			if gVal.ARR_NotReactionUser[wGetIndex]['follow']==False :
				wFLG_Update = True
			
			wSubRes = gVal.OBJ_DB_IF.UpdateExeUser( wGetIndex, inFollow=wFLG_Update )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "UpdateExeUser is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			wRes['Result'] = True
			return wRes
		
		#############################
		# v: 予約削除
		elif wCom=="v" :
			wFLG_Update = False
			if gVal.ARR_NotReactionUser[wGetIndex]['vip']==True :
				### VIP ONの場合は設定できない
				CLS_OSIF.sPrn( "VIP ONのため予約削除できません" )
				CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
				wRes['Result'] = True
				return wRes
			
			CLS_OSIF.sPrn( "予約削除する日数を入力してください。" )
			wDays = CLS_OSIF.sInp( "  \\q=中止 / \\r=解除 / days ? (1-90) => " )
			
			wRelDate = None
			if wDays=="\\q" :
				### 中止
				CLS_OSIF.sPrn( "キャンセルされました。" )
				CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
				wRes['Result'] = True
				return wRes
			
			elif wDays=="\\r" :
				### 解除
				wRelDate = gVal.DEF_TIMEDATE
			
			else:
				### 整数か
				try:
					wDays = int(wDays)
				except ValueError:
					CLS_OSIF.sPrn( "入力が整数ではありません" + '\n' )
					CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
					wRes['Result'] = True
					return wRes
				
				### 範囲内か
				if wDays<=0 or wDays>90 :
					CLS_OSIF.sPrn( "範囲外の数値です" + '\n' )
					CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
					wRes['Result'] = True
					return wRes
				
				### 日数加算
				wSubRes = CLS_OSIF.sAddTimedate_day( str( gVal.STR_Time['TimeDate'] ), wDays )
				if wSubRes['Result']!=True :
					wRes['Reason'] = "sAddTimedate_day failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
				### wSubRes['TimeDate']
				wRelDate = wSubRes['TimeDate']
			
			wFLG_Update = True
			
			wSubRes = gVal.OBJ_DB_IF.UpdateExeUser( wGetIndex, inRelDate=str(wRelDate) )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "UpdateExeUser is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# m: memo
		elif wCom=="m" :
			CLS_OSIF.sPrn( "メモする内容" )
			wMemo = CLS_OSIF.sInp( "  \\q=中止 / \\r=解除 / memo ? => " )
			
			if wMemo=="\\q" :
				### 中止
				CLS_OSIF.sPrn( "キャンセルされました。" )
				CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
				wRes['Result'] = True
				return wRes
			
			elif wMemo=="\\r" :
				### 解除
				wMemo = gVal.DEF_NOTEXT
			
			wFLG_Update = True
			
			wSubRes = gVal.OBJ_DB_IF.UpdateExeUser( wGetIndex, inMemo=wMemo )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "UpdateExeUser is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# d: 禁止ユーザ削除
		elif wCom=="d" :
			self.__delete_ExcuteUser( wGetIndex )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# 範囲外のコマンド
		else:
			CLS_OSIF.sPrn( "コマンドが違います" + '\n' )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		wRes['Result'] = True
		return wRes

	#####################################################
	# 禁止ユーザ追加
	#####################################################
	def __set_ExcuteUser(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__set_ExcuteUser"
		
		#############################
		# コンソールを表示
		wWord = CLS_OSIF.sInp( "禁止ユーザ？=> " )
		if wWord=="" :
			### 未入力は終了
			wRes['Result'] = True
			return wRes
		
		if wWord in gVal.ARR_NotReactionUser :
			### ダブりは終了
			wStr = "既に登録済みのユーザ: screen_user=" + wWord
			CLS_OSIF.sInp( wStr )
			
			wRes['Result'] = True
			return wRes
		
		#############################
		# Twitterからユーザ情報を取得する
		wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inScreenName=wWord )
		if wUserInfoRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetUserinfo is failed"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		wUser = {
			"id"			: str(wUserInfoRes['Responce']['id']),
			"screen_name"	: wWord
		}
		
		#############################
		# 実行の確認
		wSubRes = gVal.OBJ_DB_IF.InsertExeUser( wUser )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "InsertExeUser is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wStr = "〇禁止ユーザを登録: screen_user=" + wWord
		CLS_OSIF.sInp( wStr )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes

	#####################################################
	# 禁止ユーザ削除
	#####################################################
	def __delete_ExcuteUser( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "__delete_ExcuteUser"
		
		#############################
		# コンソールを表示
		wStr = "禁止ユーザ " + str(gVal.ARR_NotReactionUser[inID]['screen_name']) + " を削除します"
		CLS_OSIF.sPrn( wStr )
		wWord = CLS_OSIF.sInp( "  y=YES / other=中止=> " )
		if wWord!="y" :
			wRes['Result'] = True
			return wRes
		
		#############################
		# 実行の確認
		wSubRes = gVal.OBJ_DB_IF.DeleteExeUser( inID )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "DeleteExeUser is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wStr = "禁止ユーザを削除しました"
		CLS_OSIF.sInp( wStr )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# 禁止ユーザ自動削除
#####################################################
	def ExcuteUser_AutoDelete( self, inFLG_FirstDisp=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "ExcuteUser_AutoDelete"
		
		#############################
		# 取得開始の表示
		if inFLG_FirstDisp==True :
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "禁止ユーザ自動削除" )
		
		wKeylist = list( gVal.ARR_NotReactionUser.keys() )
		for wKey in wKeylist :
			#############################
			# 自動削除設定中か
			if str(gVal.ARR_NotReactionUser[wKey]['rel_date'])==gVal.DEF_TIMEDATE :
				### 設定OFFはスキップ
				continue
			
			#############################
			# 予定日が過ぎたか
			wSubRes = CLS_OSIF.sCmpTime( str(gVal.ARR_NotReactionUser[wKey]['rel_date']), inDstTD=str( gVal.STR_Time['TimeDate'] ) )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "sCmpTime is failed: user=" + gVal.ARR_NotReactionUser[wKey]['screen_name']
				gVal.OBJ_L.Log( "B", wRes )
				continue
			if wSubRes['Future']==True :
				###未来時間= 過ぎてないのでスキップ
				continue
			
			# ※予定時間を過ぎたので削除実行
			#############################
			# 実行の確認
			wSubRes = gVal.OBJ_DB_IF.DeleteExeUser( str(gVal.ARR_NotReactionUser[wKey]['id']) )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "DeleteExeUser is failed"
				gVal.OBJ_L.Log( "B", wRes )
				continue
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# 相互いいね停止
#####################################################
	def SetMfvStop(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "SetMfvStop"
		
		#############################
		# 入力画面表示
		wStr = "相互いいね停止の設定をおこないます。" + '\n'
		wStr = wStr + '\n'
		wStr = wStr + "  \\q=キャンセル  /  \\y=停止設定  /  \\n=停止解除" + '\n'
		wStr = wStr + "---------------------------------------" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 入力
		while True :
			#############################
			# 現在の設定の表示
			wStr = "[現在の設定] "
			if gVal.STR_UserInfo['mfvstop']==True :
				wStr = wStr + "● 設定中"
			else:
				wStr = wStr + "〇 未設定"
			wStr = wStr + '\n'
			CLS_OSIF.sPrn( wStr )
			
			wInputName = CLS_OSIF.sInp( "Command ？=> " )
			
			if wInputName=="" :
				CLS_OSIF.sPrn( "コマンドが未入力です" + '\n' )
				continue
			
			elif wInputName=="\\q" :
				# 完了
				wRes['Result'] = True
				return wRes
			
			elif ( gVal.STR_UserInfo['mfvstop']==True and wInputName=="\\y" ) or \
			     ( gVal.STR_UserInfo['mfvstop']==False and wInputName=="\\n" ) :
				continue
			
			###ここまでで入力は完了した
			break
		
		wFLG_Set = False
		#############################
		# 設定値の設定
		if wInputName=="\\y" :
			wFLG_Set = True
		
		#############################
		# DBに設定
		wSubRes = gVal.OBJ_DB_IF.SetMfvStop( inSet=wFLG_Set )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "SetMfvStop is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# トレンドタグ設定
#####################################################
	def SetTrendTag(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "SetTrendTag"
		
		#############################
		# 入力画面表示
		wStr = "トレンドタグの設定をおこないます。" + '\n'
		wStr = wStr + "タグに設定する名前を入力してください。" + '\n'
		wStr = wStr + '\n'
		wStr = wStr + "  \\q=キャンセル  /  \\n=設定解除  /  other=設定値" + '\n'
		wStr = wStr + "---------------------------------------" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 入力
		while True :
			#############################
			# 現在の設定の表示
			wStr = "[現在の設定] "
			wStr = wStr + "トレンドタグ名="
			if gVal.STR_UserInfo['TrendTag']!=gVal.DEF_NOTEXT :
				wStr = wStr + gVal.STR_UserInfo['TrendTag']
			else:
				wStr = wStr + "(設定解除)"
			wStr = wStr + '\n'
			CLS_OSIF.sPrn( wStr )
			
			wInputName = CLS_OSIF.sInp( "Tag Name ？=> " )
			
			if wInputName=="" :
				CLS_OSIF.sPrn( "タグ名かコマンドが未入力です" + '\n' )
				continue
			
			elif wInputName=="\\q" :
				# 完了
				wRes['Result'] = True
				return wRes
			
			###ここまでで入力は完了した
			break
		
		#############################
		# 設定解除の場合
		if wInputName=="\\n" :
			wInputName = gVal.DEF_NOTEXT
		
		#############################
		# DBに設定
		wSubRes = gVal.OBJ_DB_IF.SetTrendTag( inTrendName=wInputName )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "SetListName is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# 質問タグ設定
#####################################################
	def SetQuestionTag(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "SetQuestionTag"
		
		#############################
		# 入力画面表示
		wStr = "質問タグの設定をおこないます。" + '\n'
		wStr = wStr + "タグに設定する名前を入力してください。" + '\n'
		wStr = wStr + '\n'
		wStr = wStr + "  \\q=キャンセル  /  \\n=設定解除  /  other=設定値" + '\n'
		wStr = wStr + "---------------------------------------" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 入力
		while True :
			#############################
			# 現在の設定の表示
			wStr = "[現在の設定] "
			wStr = wStr + "質問タグ名="
			if gVal.STR_UserInfo['QuestionTag']!=gVal.DEF_NOTEXT :
				wStr = wStr + gVal.STR_UserInfo['QuestionTag']
			else:
				wStr = wStr + "(設定解除)"
			wStr = wStr + '\n'
			CLS_OSIF.sPrn( wStr )
			
			wInputName = CLS_OSIF.sInp( "Tag Name ？=> " )
			
			if wInputName=="" :
				CLS_OSIF.sPrn( "タグ名かコマンドが未入力です" + '\n' )
				continue
			
			elif wInputName=="\\q" :
				# 完了
				wRes['Result'] = True
				return wRes
			
			###ここまでで入力は完了した
			break
		
		#############################
		# 設定解除の場合
		if wInputName=="\\n" :
			wInputName = gVal.DEF_NOTEXT
		
		#############################
		# DBに設定
		wSubRes = gVal.OBJ_DB_IF.SetQuestionTag( inQuestionName=wInputName )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "SetQuestionTag is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# VIPタグ設定
#####################################################
	def SetVipTag(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "SetVipTag"
		
		#############################
		# 入力画面表示
		wStr = "VIPタグの設定をおこないます。" + '\n'
		wStr = wStr + "タグに設定する名前を入力してください。" + '\n'
		wStr = wStr + '\n'
		wStr = wStr + "  \\q=キャンセル  /  \\n=設定解除  /  other=設定値" + '\n'
		wStr = wStr + "---------------------------------------" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 入力
		while True :
			#############################
			# 現在の設定の表示
			wStr = "[現在の設定] "
			wStr = wStr + "VIPタグ名="
			if gVal.STR_UserInfo['VipTag']!=gVal.DEF_NOTEXT :
				wStr = wStr + gVal.STR_UserInfo['VipTag']
			else:
				wStr = wStr + "(設定解除)"
			wStr = wStr + '\n'
			CLS_OSIF.sPrn( wStr )
			
			wInputName = CLS_OSIF.sInp( "Tag Name ？=> " )
			
			if wInputName=="" :
				CLS_OSIF.sPrn( "タグ名かコマンドが未入力です" + '\n' )
				continue
			
			elif wInputName=="\\q" :
				# 完了
				wRes['Result'] = True
				return wRes
			
			###ここまでで入力は完了した
			break
		
		#############################
		# 設定解除の場合
		if wInputName=="\\n" :
			wInputName = gVal.DEF_NOTEXT
		
		#############################
		# DBに設定
		wSubRes = gVal.OBJ_DB_IF.SetVipTag( inTagName=wInputName )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "SetVipTag is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# 削除タグ設定
#####################################################
	def SetDelTag(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "SetDelTag"
		
		#############################
		# 入力画面表示
		wStr = "削除タグの設定をおこないます。" + '\n'
		wStr = wStr + "タグに設定する名前を入力してください。" + '\n'
		wStr = wStr + '\n'
		wStr = wStr + "  \\q=キャンセル  /  \\n=設定解除  /  other=設定値" + '\n'
		wStr = wStr + "---------------------------------------" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 入力
		while True :
			#############################
			# 現在の設定の表示
			wStr = "[現在の設定] "
			wStr = wStr + "削除タグ名="
			if gVal.STR_UserInfo['DelTag']!=gVal.DEF_NOTEXT :
				wStr = wStr + gVal.STR_UserInfo['DelTag']
			else:
				wStr = wStr + "(設定解除)"
			wStr = wStr + '\n'
			CLS_OSIF.sPrn( wStr )
			
			wInputName = CLS_OSIF.sInp( "Tag Name ？=> " )
			
			if wInputName=="" :
				CLS_OSIF.sPrn( "タグ名かコマンドが未入力です" + '\n' )
				continue
			
			elif wInputName=="\\q" :
				# 完了
				wRes['Result'] = True
				return wRes
			
			###ここまでで入力は完了した
			break
		
		#############################
		# 設定解除の場合
		if wInputName=="\\n" :
			wInputName = gVal.DEF_NOTEXT
		
		#############################
		# DBに設定
		wSubRes = gVal.OBJ_DB_IF.SetDelTag( inTagName=wInputName )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "SetDelTag is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# リスト通知設定
#####################################################
	def SetListName(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "SetListName"
		
		#############################
		# 入力画面表示
		wStr = "リスト通知の設定をおこないます。" + '\n'
		wStr = wStr + "通知に設定するリスト名を入力してください。" + '\n'
		wStr = wStr + '\n'
		wStr = wStr + "  \\q=キャンセル  /  \\n=設定解除  /  other=設定値" + '\n'
		wStr = wStr + "---------------------------------------" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		wListID = None
		#############################
		# 入力
		while True :
			#############################
			# 現在の設定の表示
			wStr = "[現在の設定] "
			wStr = wStr + "通知リスト名="
			if gVal.STR_UserInfo['ListName']!=gVal.DEF_NOTEXT :
				wStr = wStr + gVal.STR_UserInfo['ListName']
			else:
				wStr = wStr + "(設定解除)"
			wStr = wStr + '\n'
			CLS_OSIF.sPrn( wStr )
			
			wInputName = CLS_OSIF.sInp( "List Name ？=> " )
			
			if wInputName=="" :
				CLS_OSIF.sPrn( "リスト名か解除コマンドが未入力です" + '\n' )
				continue
			
			elif wInputName=="\\q" :
				# 完了
				wRes['Result'] = True
				return wRes
			
			elif wInputName=="\\n" :
				### 設定解除
				break
			
			#############################
			# 名称被りチェック
			if gVal.STR_UserInfo['ListName']==wInputName or \
			   gVal.STR_UserInfo['mListName']==wInputName or \
			   gVal.STR_UserInfo['fListName']==wInputName :
				CLS_OSIF.sPrn( "設定済みリストのため設定できません" + '\n' )
				continue
			
			wFLG_Detect = False
			wKeylist = list( gVal.ARR_ListFavo.keys() )
			for wKey in wKeylist :
				if gVal.ARR_ListFavo[wKey]['screen_name']==gVal.STR_UserInfo['Account'] and \
				   gVal.ARR_ListFavo[wKey]['list_name']==wInputName :
					wFLG_Detect = True
					break
			if wFLG_Detect==True :
				CLS_OSIF.sPrn( "いいねリスト設定済みため設定できません" + '\n' )
				continue
			
			wStr = "Twitterの情報確認中..."
			CLS_OSIF.sPrn( wStr )
			#############################
			# リストがTwitterにあるか確認
			wSubRes = gVal.OBJ_Tw_IF.GetListID( inListName=wInputName )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "GetListID is failed"
				gVal.OBJ_L.Log( "B", wRes )
				continue
			if wSubRes['Responce']==None :
				CLS_OSIF.sPrn( "Twitterにないリストです" + '\n' )
				continue
			
			###ここまでで入力は完了した
			wListID = wSubRes['Responce'] # ListID
			break
		
		#############################
		# 設定解除
		if wInputName=="\\n" :
			wInputName = gVal.DEF_NOTEXT
		
		#############################
		# DBに登録する
		wSubRes = gVal.OBJ_DB_IF.SetListName( inListName=wInputName, inListID=wListID )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "SetListName is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# 自動リムーブ設定
#####################################################
	def SetAutoRemove(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "SetAutoRemove"
		
		#############################
		# 入力画面表示
		wStr = "自動リムーブ設定をおこないます。" + '\n'
		wStr = wStr + "コマンドを入力してください。" + '\n'
		wStr = wStr + '\n'
		wStr = wStr + "  \\a   : 自動リムーブ設定のON / OFF 切り替え" + '\n'
		wStr = wStr + "  \\l   : 相互フォロー、片フォロワーリスト設定" + '\n'
		wStr = wStr + "  \\r   : 相互フォロー、片フォロワーリスト設定解除" + '\n'
		wStr = wStr + "  \\q   : 戻る" + '\n'
		wStr = wStr + "---------------------------------------" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		wMListID   = None
		wMListName = None
		wFListID   = None
		wFListName = None
		#############################
		# 入力
		while True :
			#############################
			# 現在の設定の表示
			wStr = "[現在の設定] "
			wStr = wStr + "自動リムーブ="
			if gVal.STR_UserInfo['AutoRemove']==True :
				wStr = wStr + "〇ON "
			else:
				wStr = wStr + "●OFF "
			wStr = wStr + "リスト 相互="
			wStr = wStr + gVal.STR_UserInfo['mListName']
			wStr = wStr + " 片="
			wStr = wStr + gVal.STR_UserInfo['fListName'] + '\n'
			CLS_OSIF.sPrn( wStr )
			
			#############################
			# コマンド入力
			wInputName = CLS_OSIF.sInp( "   Command ？=> " )
			
			if wInputName=="" :
				continue
			
			elif wInputName=="\\q" :
				# 戻る
				break
			
			#############################
			# \a : 自動リムーブ設定
			elif wInputName=="\\a" :
				wSubRes = gVal.OBJ_DB_IF.SetAutoRemove()
				if wSubRes['Result']!=True :
					wRes['Reason'] = "SetAutoRemove is failed"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			#############################
			# \l : リスト設定
			elif wInputName=="\\l" :
				wMListID   = None
				wMListName = None
				wFListID   = None
				wFListName = None
				
				#############################
				# 相互フォローリスト設定
				wInputName = CLS_OSIF.sInp( "   相互フォローリスト名 ？=> " )
				
				#############################
				# 名称被りチェック
				if gVal.STR_UserInfo['ListName']==wInputName or \
				   gVal.STR_UserInfo['mListName']==wInputName or \
				   gVal.STR_UserInfo['fListName']==wInputName :
					CLS_OSIF.sPrn( "設定済みリストのため設定できません" + '\n' )
					continue
				
				wFLG_Detect = False
				wKeylist = list( gVal.ARR_ListFavo.keys() )
				for wKey in wKeylist :
					if gVal.ARR_ListFavo[wKey]['screen_name']==gVal.STR_UserInfo['Account'] and \
					   gVal.ARR_ListFavo[wKey]['list_name']==wInputName :
						wFLG_Detect = True
						break
				if wFLG_Detect==True :
					CLS_OSIF.sPrn( "いいねリスト設定済みため設定できません" + '\n' )
					continue
				
				wStr = "Twitterの情報確認中..."
				CLS_OSIF.sPrn( wStr )
				### リストがTwitterにあるか確認
				wSubRes = gVal.OBJ_Tw_IF.GetListID( inListName=wInputName )
				if wSubRes['Result']!=True :
					wRes['Reason'] = "GetListID is failed"
					gVal.OBJ_L.Log( "B", wRes )
					continue
				if wSubRes['Responce']==None :
					CLS_OSIF.sPrn( "Twitterにないリストです" + '\n' )
					continue
				wMListID   = wSubRes['Responce'] # ListID
				wMListName = wInputName
				
				#############################
				# 片フォロワーリスト設定
				wInputName = CLS_OSIF.sInp( "   片フォロワーリスト名 ？=> " )
				
				#############################
				# 名称被りチェック
				if gVal.STR_UserInfo['ListName']==wInputName or \
				   gVal.STR_UserInfo['mListName']==wInputName or \
				   gVal.STR_UserInfo['fListName']==wInputName :
					CLS_OSIF.sPrn( "設定済みリストのため設定できません" + '\n' )
					continue
				
				wFLG_Detect = False
				wKeylist = list( gVal.ARR_ListFavo.keys() )
				for wKey in wKeylist :
					if gVal.ARR_ListFavo[wKey]['screen_name']==gVal.STR_UserInfo['Account'] and \
					   gVal.ARR_ListFavo[wKey]['list_name']==wInputName :
						wFLG_Detect = True
						break
				if wFLG_Detect==True :
					CLS_OSIF.sPrn( "いいねリスト設定済みため設定できません" + '\n' )
					continue
				
				wStr = "Twitterの情報確認中..."
				CLS_OSIF.sPrn( wStr )
				### リストがTwitterにあるか確認
				wSubRes = gVal.OBJ_Tw_IF.GetListID( inListName=wInputName )
				if wSubRes['Result']!=True :
					wRes['Reason'] = "GetListID is failed"
					gVal.OBJ_L.Log( "B", wRes )
					continue
				if wSubRes['Responce']==None :
					CLS_OSIF.sPrn( "Twitterにないリストです" + '\n' )
					continue
				wFListID   = wSubRes['Responce'] # ListID
				wFListName = wInputName
				
				wSubRes = gVal.OBJ_DB_IF.SetAutoList(
				   inMListName=wMListName,inFListName=wFListName, 
				   inMListID=wMListID, inFListID=wFListID )
				if wSubRes['Result']!=True :
					wRes['Reason'] = "SetAutoList is failed(set)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			#############################
			# \r : リスト設定解除
			elif wInputName=="\\r" :
				wSubRes = gVal.OBJ_DB_IF.SetAutoList(
				   inMListName=gVal.DEF_NOTEXT,inFListName=gVal.DEF_NOTEXT, 
				   inMListID=gVal.DEF_NOTEXT, inFListID=gVal.DEF_NOTEXT )
				if wSubRes['Result']!=True :
					wRes['Reason'] = "SetAutoList is failed(remove)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# ユーザ自動削除
#####################################################
	def RunAutoUserRemove(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "RunAutoUserRemove"
		
		#############################
		# 実行時間か
		wGetLag = CLS_OSIF.sTimeLag( str( gVal.STR_Time['auto_delete'] ), inThreshold=gVal.DEF_STR_TLNUM['forCheckAutoDeleteSec'] )
		if wGetLag['Result']!=True :
			wRes['Reason'] = "sTimeLag failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wGetLag['Beyond']==False :
			### 規定以内は除外
			wStr = "●自動削除期間外 処理スキップ: 次回処理日時= " + str(wGetLag['RateTime']) + '\n'
			CLS_OSIF.sPrn( wStr )
			wRes['Result'] = True
			return wRes
		
		#############################
		# 入力画面表示
		wStr = "ユーザ自動削除中..."
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# フォロー情報 取得
		wFollowerData = gVal.OBJ_Tw_IF.GetFollowerData()
		
		#############################
		# 以下に該当するユーザをブロックリムーブしていく
		# ・片フォロワー
		# ・ツイート数=0 か 最後のツイートが規定期間外
		wKeylist = list( wFollowerData.keys() )
		for wID in wKeylist :
			wUserID = str(wID)
			
			### フォロー者はスキップ
			if wFollowerData[wID]['myfollow']==True :
				continue
			### フォロワーでない場合はスキップ
			if wFollowerData[wID]['follower']==False :
				continue
			
			wFLG_Detect = False
			#############################
			# Twitterからユーザ情報を取得する
			wUserInfoRes = gVal.OBJ_Tw_IF.GetUserinfo( inScreenName=wFollowerData[wID]['screen_name'] )
			if wUserInfoRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(GetUserinfo): " + wUserInfoRes['Reason'] + " screen_name=" + wFollowerData[wID]['screen_name']
				gVal.OBJ_L.Log( "B", wRes )
				continue
			
			### 鍵垢は対象
			if wUserInfoRes['Responce']['protected']==True :
				wFLG_Detect = True
			else:
			### ツイート数0超の場合
			###   規定期間チェックする
			### ツイート数0の場合
			###   対象確定
				if wFollowerData[wID]['statuses_count']==0 :
					wFLG_Detect = True
				else:
					
					# タイムラインを取得する
					#   最初の1ツイートの日時を最新の活動日とする
					wTweetRes = gVal.OBJ_Tw_IF.GetTL( inTLmode="user", inFLG_Rep=False, inFLG_Rts=True,
						 inID=wID, inCount=1 )
					if wTweetRes['Result']!=True :
						wRes['Reason'] = "Twitter Error: GetTL"
						gVal.OBJ_L.Log( "B", wRes )
						continue
					
					###日時の変換をして、設定
					wTime = CLS_TIME.sTTchg( wRes, "(1)", wTweetRes['Responce'][0]['created_at'] )
					if wTime['Result']!=True :
						continue
					
					wGetLag = CLS_OSIF.sTimeLag( str( wTime['TimeDate'] ), inThreshold=gVal.DEF_STR_TLNUM['forAutoUserRemoveSec'] )
					if wGetLag['Result']!=True :
						wRes['Reason'] = "sTimeLag failed"
						gVal.OBJ_L.Log( "B", wRes )
						continue
					if wGetLag['Beyond']==True :
						### 規定外 =許容外の日数なので対象
						wFLG_Detect = True
			
			if wFLG_Detect==False :
				continue
			
			# ※リムーブ確定
			#############################
			# ブロック→リムーブ実行
			wTweetRes = gVal.OBJ_Tw_IF.BlockRemove( wUserID )
			if wTweetRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error: BlockRemove" + wTweetRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				continue
			
			### ユーザレベル変更
###			wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wUserID, "G-" )
###			wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wUserID, "Z-" )
			wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wUserID, "G-" )
			
			### トラヒック記録（フォロワー減少）
			CLS_Traffic.sP( "d_follower" )
			
			#############################
			# ログに記録
###			gVal.OBJ_L.Log( "R", wRes, "追い出し: " + wFollowerData[wID]['screen_name'] )
			gVal.OBJ_L.Log( "R", wRes, "追い出し: " + wFollowerData[wID]['screen_name'], inID=wID )
			
			wRes['Responce'] = True		#自動リムーブ実行
			#############################
			# DBに反映
			wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_Follower( wUserID, False, False )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "UpdateFavoData_Follower is failed"
				gVal.OBJ_L.Log( "B", wRes )
				continue
		
		#############################
		# 現時間を設定
		wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "auto_delete", gVal.STR_Time['TimeDate'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "SetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		###	gVal.STR_Time['auto_remove']
		
		wStr = "〇自動削除 完了" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# 警告ユーザ追い出し
#####################################################
	def RemoveCautionUser( self, inListNum=-1, inFLR_Recheck=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "RemoveCautionUser"
		
		#############################
		# 個別追い出し指定
		if inListNum>=1 :
			wSubRes = self.__removeCautionUser( inListNum=inListNum )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "__removeCautionUser is failed" + wSubRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		#############################
		# 全追い出し指定
		else:
			#############################
			# 取得開始の表示
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "警告削除処理" )
			
			#############################
			# 警告リストID一覧の作成
			wARR_IndListID = []
			if gVal.STR_UserInfo['ListID']!=gVal.DEF_NOTEXT :
				wARR_IndListID.append( gVal.STR_UserInfo['ListID'] )
			
			if gVal.STR_UserInfo['AutoRemove']==True and \
			   ( gVal.STR_UserInfo['mListID']!=gVal.DEF_NOTEXT or \
			     gVal.STR_UserInfo['fListID']!=gVal.DEF_NOTEXT ) :
				wARR_IndListID.append( gVal.STR_UserInfo['mListID'] )
				wARR_IndListID.append( gVal.STR_UserInfo['fListID'] )
			
			wKeylist = list( gVal.ARR_ListFavo.keys() )
			for wKey in wKeylist :
				if gVal.ARR_ListFavo[wKey]['caution']==True :
					wARR_IndListID.append( gVal.ARR_ListFavo[wKey]['id'] )
			
			wKeylist = list( gVal.ARR_CautionTweet.keys() )
			wListLeng = len( gVal.ARR_CautionTweet )
			wListCnt = 0
			for wListNum in wKeylist :
				
				wFLG_Caution = True	#再チェックなしの場合、警告付き処理にする
				#############################
				# 再チェックが有効なら再チェック
				if inFLR_Recheck==True :
					wUserID = gVal.ARR_CautionTweet[wListNum]['id']
					#############################
					# リストの取得
					wGetListsRes = gVal.OBJ_Tw_IF.GetLists( gVal.ARR_CautionTweet[wListNum]['screen_name'] )
					if wGetListsRes['Result']!=True :
						### エラーでリスト取得できなかったら正常処理できないので
						### 警告は保持するため、処理を抜ける
						wRes['Reason'] = "Twitter API Error(31): Critical Error: " + wGetListsRes['Reason'] + " screen_name=" + gVal.ARR_CautionTweet[wListNum]['screen_name']
						gVal.OBJ_L.Log( "A", wRes )
						return wRes
					wARR_Lists = wGetListsRes['Responce']
					
					#############################
					# 自分のリストを登録しているか
					wFLG_Caution = False
					wKeylist = list( wARR_Lists.keys() )
					for wKey in wKeylist :
						### 自分のリスト以外はスキップ
						if wARR_Lists[wKey]['me']!=True :
							continue
						if str(wARR_Lists[wKey]['id']) in wARR_IndListID :
							wFLG_Caution = True		# 警告リストまだ登録中
							break
						if gVal.OBJ_Tw_IF.CheckFollower( wUserID )==False :
							wFLG_Caution = True		# 非フォロワーのリスト登録中
							break
				
				#############################
				# 警告状態でない場合
				#  =追い出しモードOFFで削除
				if wFLG_Caution==False :
					wSubRes = self.__removeCautionUser( inListNum=wListNum, inFLG_Remove=False )
					if wSubRes['Result']!=True :
						wRes['Reason'] = "__removeCautionUser is failed" + wSubRes['Reason'] + " screen_name=" + gVal.ARR_CautionTweet[wListNum]['screen_name']
						gVal.OBJ_L.Log( "B", wRes )
				
				#############################
				# 警告状態のまま
				else :
					#############################
					# 規定の期間を過ぎたか
					wGetLag = CLS_OSIF.sTimeLag( str( gVal.ARR_CautionTweet[wListNum]['regdate'] ), inThreshold=gVal.DEF_STR_TLNUM['forDeleteCautionTweetSec'] )
					if wGetLag['Result']!=True :
						wRes['Reason'] = "sTimeLag failed"
						gVal.OBJ_L.Log( "B", wRes )
						continue
					if wGetLag['Beyond']==False :
						### 規定内 =許容内の日数なのでスキップ
						
						### まだ警告状態ならスキップする
						wStr = "●警告状態中(期間内): screen_name=" + gVal.ARR_CautionTweet[wListNum]['screen_name']
						CLS_OSIF.sPrn( wStr )
						continue
					else :
						### 規定外
						if gVal.OBJ_Tw_IF.CheckMyFollow( wUserID )==True :
							### フォロー者は自動で追い出さない
							wStr = "●警告状態中(期間外フォロー者): screen_name=" + gVal.ARR_CautionTweet[wListNum]['screen_name']
							CLS_OSIF.sPrn( wStr )
							continue
						else :
							#############################
							# 追い出し
							wSubRes = self.__removeCautionUser( inListNum=wListNum )
							if wSubRes['Result']!=True :
								wRes['Reason'] = "__removeCautionUser is failed" + wSubRes['Reason'] + " screen_name=" + gVal.ARR_CautionTweet[wListNum]['screen_name']
								gVal.OBJ_L.Log( "B", wRes )
				
				wListCnt += 1
				### まだ処理するデータがあるなら
				###   約10秒遅延待
				if wListLeng>wListCnt :
					CLS_OSIF.sSleep(10)
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes

	#####################################################
	def __removeCautionUser( self, inListNum=-1, inFLG_Remove=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "__removeCautionUser"
		
		wUserID = gVal.ARR_CautionTweet[inListNum]['id']
		
		#############################
		# 追い出しモードON
		if inFLG_Remove==True :
			#############################
			# 追い出し中表示
			wStr = "追い出し処理中... : screen_name=" + gVal.ARR_CautionTweet[inListNum]['screen_name']
			CLS_OSIF.sPrn( wStr )
			
			#############################
			# 追い出す
			wBlockRes = gVal.OBJ_Tw_IF.BlockRemove( wUserID )
			if wBlockRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error(BlockRemove): " + wBlockRes['Reason'] + " screen_name=" + gVal.ARR_CautionTweet[inListNum]['screen_name']
				return wRes
			
			### ログに記録
			gVal.OBJ_L.Log( "RC", wRes, "▼リスト登録者 追い出し(手動): screen_name=" + gVal.ARR_CautionTweet[inListNum]['screen_name'], inID=wUserID )
			
			### トラヒック記録（フォロワー減少）
			CLS_Traffic.sP( "d_follower" )
			
			### ユーザレベル変更（いちお設定）
			wUserLevel = "L"
			wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wUserID, wUserLevel )
		
		#############################
		# 追い出しモードOFF
		else :
			#############################
			# DBからいいね情報を取得する(1個)
			wSubRes = gVal.OBJ_DB_IF.GetFavoDataOne( gVal.ARR_CautionTweet[inListNum] )
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "GetFavoDataOne is failed(2)"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			### DB未登録（ありえない）
			if wSubRes['Responce']['Data']==None :
				wRes['Reason'] = "GetFavoDataOne is no data"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wSubRes['Responce']['FLG_New']==True :
				#############################
				# 新規情報の設定
				wSubRes = self.OBJ_Parent.SetNewFavoData( gVal.ARR_CautionTweet[inListNum], wSubRes['Responce']['Data'] )
				if wSubRes['Result']!=True :
					###失敗
					wRes['Reason'] = "SetNewFavoData is failed(2)"
					gVal.OBJ_L.Log( "B", wRes )
					return wRes
			
			wARR_DBData = wSubRes['Responce']['Data']
			
			#############################
			# 相互フォロー中 解除か
			if wARR_DBData['myfollow']==True and wARR_DBData['follower']==True :
				if wARR_DBData['send_cnt']>=gVal.DEF_STR_TLNUM['LEVEL_B_Cnt'] :
					wUserLevel = "B+"
				elif wARR_DBData['send_cnt']>=1 :
					wUserLevel = "B"
				else:
					wUserLevel = "C+"
			
			#############################
			# 片フォロワー 解除か
			elif wARR_DBData['myfollow']==True and wARR_DBData['follower']==False :
				wUserLevel = "D+"
			
			elif wARR_DBData['myfollow']==False and wARR_DBData['follower']==True :
				wUserLevel = "E"
			
			#############################
			# 関連なし
			else :
				wUserLevel = "F"
			
			### ユーザレベル変更
			wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( wUserID, wUserLevel )
		
		#############################
		# Twitterにツイートしていたら、ツイートを削除
		if gVal.ARR_CautionTweet[inListNum]['tweet_id']!="(none)" :
			wTweetRes = gVal.OBJ_Tw_IF.DelTweet( gVal.ARR_CautionTweet[inListNum]['tweet_id'] )
			if wTweetRes['Result']!=True :
				wRes['Reason'] = "Twitter API Error: DelTweet" + wTweetRes['Reason'] + " screen_name=" + gVal.ARR_CautionTweet[inListNum]['screen_name'] + " tweetid=" + gVal.ARR_CautionTweet[inListNum]['tweet_id']
		
		#############################
		# ログに記録
		gVal.OBJ_L.Log( "RC", wRes, "〇警告解除: screen_name=" + gVal.ARR_CautionTweet[inListNum]['screen_name'], inID=wUserID )
		
		#############################
		# DBに反映
		wSubRes = gVal.OBJ_DB_IF.DeleteCautionTweet( inListNum )
		if wSubRes['Result']!=True :
			###失敗
			wRes['Reason'] = "DeleteCautionTweet is failed"
			return wRes
		
		#############################
		# 完了
		wRes['Result'] = True
		return wRes



#####################################################
# 警告ユーザ管理
#####################################################
	def AdminCautionUser(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "AdminCautionUser"
		
		#############################
		# コンソールを表示
		while True :
			
			#############################
			# データ表示
			self.__view_CautionUser()
			
			#############################
			# 実行の確認
			wListNumber = CLS_OSIF.sInp( "コマンド？(\\q=中止)=> " )
			if wListNumber=="\\q" :
				###  終わる
				wRes['Result'] = True
				return wRes
			
			#############################
			# コマンド処理
			wCommRes = self.__run_CautionUser( wListNumber )
			if wCommRes['Result']!=True :
				wRes['Reason'] = "__run_CautionUser is failed: " + wCommRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
		
		wRes['Result'] = True
		return wRes

	#####################################################
	# 画面表示
	#####################################################
	def __view_CautionUser(self):
		
###		self.ARR_CautionList = {}
		wKeylist = list( gVal.ARR_CautionTweet.keys() )
###		wListNum = 1
		wStr = ""
###		for wID in wKeylist :
###			wID = str(wID)
		for wIndex in wKeylist :
			
###			### 編集インデックス用
###			wCellUser = {
###				"id"			: wID,
###				"screen_name"	: gVal.ARR_CautionTweet[wID]['screen_name']
###			}
###			self.ARR_CautionList.update({ wListNum : wCellUser })
###			
			wStr = wStr + "   : "
			
			### リスト番号
###			wListData = str(wListNum)
###			wListNumSpace = 4 - len( wListData )
			wListData = str(gVal.ARR_CautionTweet[wIndex]['list_number'])
			wListNumSpace = 4 - len( str(gVal.ARR_CautionTweet[wIndex]['list_number']) )
			if wListNumSpace>0 :
				wListData = wListData + " " * wListNumSpace
			wStr = wStr + wListData + "  "
			
			### 警告日
###			wListData = str( gVal.ARR_CautionTweet[wID]['regdate'] )
			wListData = str( gVal.ARR_CautionTweet[wIndex]['regdate'] )
			wListData = wListData.split(" ")
			wListData = wListData[0]
			wStr = wStr + wListData + "  "
			
			### ユーザ名（screen_name）
###			wListData = gVal.ARR_CautionTweet[wID]['screen_name']
			wListData = gVal.ARR_CautionTweet[wIndex]['screen_name']
			wListNumSpace = gVal.DEF_SCREEN_NAME_SIZE - len(wListData)
			if wListNumSpace>0 :
				wListData = wListData + " " * wListNumSpace
			wStr = wStr + wListData
			
			wStr = wStr + '\n'
###			wListNum += 1
		
		wResDisp = CLS_MyDisp.sViewDisp( inDisp="CautionConsole", inIndex=-1, inData=wStr )
		if wResDisp['Result']==False :
			gVal.OBJ_L.Log( "D", wResDisp )
		
		return

	#####################################################
	# コマンド処理
	#####################################################
	def __run_CautionUser( self, inWord ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "__run_CautionUser"
		
		#############################
		# rall: 全追い出し
		if inWord=="\\rall" :
			wSubRes = self.RemoveCautionUser()
			if wSubRes['Result']!=True :
				wRes['Reason'] = "RemoveCautionUser is failed(not recheck)"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# rm: 全再チェック＆追い出し
		elif inWord=="\\rm" :
			wSubRes = self.RemoveCautionUser( inFLR_Recheck=True )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "RemoveCautionUser is failed(recheck)"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# チェック
		
		wARR_Comm = str(inWord).split("-")
		wCom = None
		if len(wARR_Comm)==1 :
			wNum = wARR_Comm[0]
			wCom = None
		elif len(wARR_Comm)==2 :
			wNum = wARR_Comm[0]
			wCom = wARR_Comm[1]
		else:
			CLS_OSIF.sPrn( "コマンドの書式が違います" + '\n' )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		### 整数か
		try:
			wNum = int(wNum)
		except ValueError:
			CLS_OSIF.sPrn( "LIST番号が整数ではありません" + '\n' )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
###		if wNum<1 or len(self.ARR_CautionList)<wNum :
###			CLS_OSIF.sPrn( "LIST番号が範囲外です" + '\n' )
###			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
###			wRes['Result'] = True
###			return wRes
		### リストのインデックス
		wKeylist = list( gVal.ARR_CautionTweet.keys() )
		wGetIndex = None
		for wIndex in wKeylist :
			if gVal.ARR_CautionTweet[wIndex]['list_number']==wNum :
###				wGetIndex = str(wIndex)
				wGetIndex = wIndex
				break
		
		if wGetIndex==None :
			CLS_OSIF.sPrn( "LIST番号が範囲外です" + '\n' )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		#############################
		# コマンドの分岐
		
		#############################
		# コマンドなし: 指定の番号のリストの設定変更をする
		if wCom==None :
###			wRes = self.__view_Profile( self.ARR_CautionList[wNum]['screen_name'] )
			wRes = self.__view_Profile( self.ARR_CautionList[wGetIndex]['screen_name'] )
		
		#############################
		# r: 追い出し(手動)
		elif wCom=="r" :
###			wSubRes = self.RemoveCautionUser( inListNum=wNum )
			wSubRes = self.RemoveCautionUser( inListNum=wGetIndex )
			if wSubRes['Result']!=True :
				wRes['Reason'] = "RemoveCautionUser is failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
		
		#############################
		# 範囲外のコマンド
		else:
			CLS_OSIF.sPrn( "コマンドが違います" + '\n' )
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			wRes['Result'] = True
			return wRes
		
		wRes['Result'] = True
		return wRes



#####################################################
# 被ブロックユーザ一覧
#####################################################
	def BlockList(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterFavo"
		wRes['Func']  = "UserBList"
		
		#############################
		# 取得開始の表示
		wResDisp = CLS_MyDisp.sViewHeaderDisp( "被ブロックユーザ一覧" )
		
		#############################
		# 被ブロックユーザ一覧の取得
		wDBRes = gVal.OBJ_DB_IF.GetFavoData_BlockList()
		if wDBRes['Result']!=True :
			wRes['Reason'] = "GetFavoData_BlockList is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		wARR_BlockList = wDBRes['Responce']
		
		wKeylist = list( wARR_BlockList.keys() )
		wStr = ""
		if len(wKeylist)==0 :
			wStr = "(非絡みユーザなし)" + '\n'
		
		#############################
		# 被ブロックユーザ一覧の作成
		else:
			wStr = "--------------------" + '\n'
			
			for wID in wKeylist :
				wID = str(wID)
				
				wStr = wStr + wARR_BlockList[wID]['screen_name'] + "  " + '\n'
		
		#############################
		# 表示
		CLS_OSIF.sPrn( wStr )
		
		wRes['Result'] = True
		return wRes



#####################################################
# 非絡みユーザ一覧
#####################################################
###	def UserBList(self):
###		#############################
###		# 応答形式の取得
###		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
###		wRes = CLS_OSIF.sGet_Resp()
###		wRes['Class'] = "CLS_TwitterFavo"
###		wRes['Func']  = "UserBList"
###		
###		#############################
###		# コンソールを表示
###		while True :
###			
###			#############################
###			# データ表示
###			self.__view_UserBList()
###			
###			#############################
###			# 実行の確認
###			wListNumber = CLS_OSIF.sInp( "コマンド？(\\q=中止)=> " )
###			if wListNumber=="\\q" :
###				###  終わる
###				wRes['Result'] = True
###				return wRes
###			
###			#############################
###			# コマンド処理
###			wCommRes = self.__run_UserBList( wListNumber )
###			if wCommRes['Result']!=True :
###				wRes['Reason'] = "__run_UserBList is failed: " + wCommRes['Reason']
###				gVal.OBJ_L.Log( "B", wRes )
###				return wRes
###		
###		wRes['Result'] = True
###		return wRes
###
###	#####################################################
###	# 画面表示
###	#####################################################
###	def __view_UserBList(self):
###		#############################
###		# 応答形式の取得
###		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
###		wRes = CLS_OSIF.sGet_Resp()
###		wRes['Class'] = "CLS_TwitterFavo"
###		wRes['Func']  = "__view_UserBList"
###		
###		#############################
###		# 非絡みユーザ一覧の取得
###		wUserB_Res = gVal.OBJ_DB_IF.UpdateFavoData_UserBList()
###		if wUserB_Res['Result']!=True :
###			wRes['Reason'] = "UpdateFavoData_UserBList is failed"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		wUserBList = wUserB_Res['Responce']
###		
###		self.STR_UserBList = {}
###		wKeylist = list( wUserBList.keys() )
###		wStr = ""
###		wList_Number = 1
###		if len(wKeylist)==0 :
###			wStr = "(非絡みユーザなし)" + '\n'
###		
###		else:
###			for wIndex in wKeylist :
###				
###				wCell = {
###					"list_number"	: wList_Number,
###					"id"			: wUserBList[wIndex]['id'],
###					"screen_name"	: wUserBList[wIndex]['screen_name'],
###					"level_tag"		: wUserBList[wIndex]['level_tag'],
###					"myfollow"		: wUserBList[wIndex]['myfollow'],
###					"follower"		: wUserBList[wIndex]['follower'],
###					"subs_list"		: gVal.OBJ_Tw_IF.CheckSubscribeListUser( wUserBList[wIndex]['id'] ),
###					"multi_list"	: gVal.OBJ_Tw_IF.CheckMutualListUser( wUserBList[wIndex]['id'] ),
###					"follow_list"	: gVal.OBJ_Tw_IF.CheckFollowListUser( wUserBList[wIndex]['id'] ),
######					"send_cnt"		: wUserBList[wIndex]['send_cnt']
###					"send_cnt"		: wUserBList[wIndex]['send_cnt'],
###					"renfavo_cnt"	: wUserBList[wIndex]['renfavo_cnt'],
###					"renbot_cnt"	: wUserBList[wIndex]['renbot_cnt']
###				}
###				self.STR_UserBList.update({ wList_Number : wCell })
###				
###				wStr = wStr + "   : "
###				
###				### リスト番号
###				wListData = str(wList_Number)
###				wListNumSpace = 4 - len( str(wList_Number) )
###				if wListNumSpace>0 :
###					wListData = wListData + " " * wListNumSpace
###				wStr = wStr + wListData + "  "
###				
###				### ユーザレベル
###				wListData = str(wCell['level_tag'])
###				wListNumSpace = 2 - len( str(wCell['level_tag']) )
###				if wListNumSpace>0 :
###					wListData = wListData + " " * wListNumSpace
###				wStr = wStr + wListData + "  "
###				
###				### 連ファボカウント
###				wListData = str(wCell['renfavo_cnt'])
###				wSpace = self.DEF_ADMIN_SCORE_LEN - len( str(wCell['renfavo_cnt']) )
###				wStr = wStr + wListData + " " * wSpace + "  "
###				
###				### bot判定カウント
###				wListData = str(wCell['renbot_cnt'])
###				wSpace = self.DEF_ADMIN_SCORE_LEN - len( str(wCell['renbot_cnt']) )
###				wStr = wStr + wListData + " " * wSpace + "  "
###				
###				### フォロー者
###				if wCell['myfollow']==True :
###					wStr = wStr + "〇" + "    "
###				else:
###					wStr = wStr + "－" + "    "
###				
###				### フォロワー
###				if wCell['follower']==True :
###					wStr = wStr + "〇" + "    "
###				else:
###					wStr = wStr + "－" + "    "
###				
###				### 相互フォローリスト
###				if wCell['multi_list']==True :
###					wStr = wStr + "〇" + "    "
###				else:
###					wStr = wStr + "－" + "    "
###				
###				### 片フォロワーリスト
###				if wCell['follow_list']==True :
###					wStr = wStr + "〇" + "      "
###				else:
###					wStr = wStr + "－" + "      "
###				
###				### ユーザ名（screen_name）
###				wListData = wCell['screen_name']
###				wStr = wStr + wListData + '\n'
###				
###				wList_Number += 1
###		
###		wResDisp = CLS_MyDisp.sViewDisp( inDisp="UserBConsole", inIndex=-1, inData=wStr )
###		if wResDisp['Result']==False :
###			gVal.OBJ_L.Log( "D", wResDisp )
###		
###		return
###
###	#####################################################
###	# コマンド処理
###	#####################################################
###	def __run_UserBList( self, inWord ):
###		#############################
###		# 応答形式の取得
###		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
###		wRes = CLS_OSIF.sGet_Resp()
###		wRes['Class'] = "CLS_TwitterFavo"
###		wRes['Func']  = "__run_UserBList"
###		
###		#############################
###		# チェック
###		
###		wARR_Comm = str(inWord).split("-")
###		wCom = None
###		if len(wARR_Comm)==1 :
###			wNum = wARR_Comm[0]
###			wCom = None
###		elif len(wARR_Comm)==2 :
###			wNum = wARR_Comm[0]
###			wCom = wARR_Comm[1]
###		else:
###			CLS_OSIF.sPrn( "コマンドの書式が違います" + '\n' )
###			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
###			wRes['Result'] = True
###			return wRes
###		
###		### 整数か
###		try:
###			wNum = int(wNum)
###		except ValueError:
###			CLS_OSIF.sPrn( "LIST番号が整数ではありません" + '\n' )
###			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
###			wRes['Result'] = True
###			return wRes
###		
###		### リストのインデックス
###		wKeylist = list( self.STR_UserBList.keys() )
###		wGetIndex = None
###		for wIndex in wKeylist :
###			if self.STR_UserBList[wIndex]['list_number']==wNum :
###				wGetIndex = str(wIndex)
###				break
###		
###		if wGetIndex==None :
###			CLS_OSIF.sPrn( "LIST番号が範囲外です" + '\n' )
###			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
###			wRes['Result'] = True
###			return wRes
###		wGetIndex = wNum
###		
###		if wGetIndex not in self.STR_UserBList :
###			CLS_OSIF.sPrn( "LIST番号のデータがありません" + '\n' )
###			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
###			wRes['Result'] = True
###			return wRes
###		
###		#############################
###		# コマンドの分岐
###		
###		#############################
###		# コマンドなし: 指定の番号のリストの設定変更をする
###		if wCom==None :
###			#############################
###			# 実行の確認
###			wStr = "ユーザ " +  self.STR_UserBList[wGetIndex]['screen_name'] + " を非絡みから解除します"
###			CLS_OSIF.sPrn( wStr )
###			wListNumber = CLS_OSIF.sInp( "コマンド？(\\y=実行)=> " )
###			if wListNumber!="\\y" :
###				###  終わる
###				wRes['Result'] = True
###				return wRes
###			
###			#############################
###			# 実行
###			wSubRes = self.__run_UserBList_Release( inData=self.STR_UserBList[wGetIndex] )
###			if wSubRes['Result']!=True :
###				wRes['Reason'] = "__run_UserBList_Release is failed"
###				gVal.OBJ_L.Log( "B", wRes )
###				return wRes
###			
###			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
###		
###		#############################
###		# 範囲外のコマンド
###		else:
###			CLS_OSIF.sPrn( "コマンドが違います" + '\n' )
###			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
###			wRes['Result'] = True
###			return wRes
###		
###		wRes['Result'] = True
###		return wRes
###
###	#####################################################
###	def __run_UserBList_Release( self ,inData ):
###		#############################
###		# 応答形式の取得
###		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
###		wRes = CLS_OSIF.sGet_Resp()
###		wRes['Class'] = "CLS_TwitterAdmin"
###		wRes['Func']  = "__run_UserBList_Release"
###		
###		#############################
###		# 登録リストユーザか
###		if inData['subs_list']!=False :
###			CLS_OSIF.sPrn( "そのユーザは変更できません" + '\n' )
###			return wRes
###		
###		wFLG_Rel = False
###		#############################
###		# 相互フォロー中 解除か
###		if inData['myfollow']==True and \
###		   inData['follower']==True and \
###		   inData['multi_list']==True and \
###		   inData['follow_list']==False and \
###		   ( inData['level_tag']=="G" or inData['level_tag']=="G+" ) :
###			
###			if inData['send_cnt']>=gVal.DEF_STR_TLNUM['LEVEL_B_Cnt'] :
###				wUserLevel = "B+"
###			elif inData['send_cnt']>=1 :
###				wUserLevel = "B"
###			else:
###				wUserLevel = "C+"
###			wFLG_Rel = True
###		
###		#############################
###		# 片フォロワー 解除か
###		elif inData['myfollow']==False and \
###		     inData['follower']==True and \
###		     inData['multi_list']==False and \
###		     inData['follow_list']==True and \
###		     ( inData['level_tag']=="H" or inData['level_tag']=="H+" ) :
###			
###			wUserLevel = "E"
###			wFLG_Rel = True
###		
###		#############################
###		# 制御不能
###		else:
###			CLS_OSIF.sPrn( "そのユーザは変更できません" + '\n' )
###			wRes['Result'] = True
###			return wRes
###		
###		#############################
###		# 連ファボカウント クリア
###		if wFLG_Rel==True :
###			wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_RenFavo( inData['id'], 0, 0 )
###			if wSubRes['Result']!=True :
###				###失敗
###				wRes['Reason'] = "UpdateFavoData_RenFavo is failed"
###				gVal.OBJ_L.Log( "B", wRes )
###				return wRes
###		
###		#############################
###		# ユーザレベルの変更の実行
###		wSubRes = gVal.OBJ_DB_IF.UpdateFavoData_UserLevel( inData['id'], wUserLevel )
###		if wSubRes['Result']!=True :
###			###失敗
###			wRes['Reason'] = "UpdateFavoData_UserLevel is failed"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		
###		#############################
###		# 正常終了
###		wRes['Result'] = True
###		return wRes
###
###

#####################################################
# 時間リセット
#####################################################
	def ResetTimeInfo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "ResetTimeInfo"
		
		#############################
		# 実行の確認
		wStr = "全スケジュール時間をリセットします"
		CLS_OSIF.sPrn( wStr )
		wAns = CLS_OSIF.sInp( "y=Yes / other=cancel => " )
		if wAns!="y" :
			###  終わる
			wRes['Result'] = True
			return wRes
		
		wStr = "リセット処理実行中..."
		CLS_OSIF.sPrn( wStr )
		#############################
		# 時間リセット
		wTimeRes = gVal.OBJ_DB_IF.ResetTimeInfo( gVal.STR_UserInfo['Account'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "ResetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# ログ記録
		gVal.OBJ_L.Log( "SC", wRes, "全時間リセット実行" )
		
		wRes['Result'] = True
		return wRes



#####################################################
# スケジュールの表示
#####################################################
	def View_Schedule( self, inFLG_FirstDisp=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "View_Sysinfo"
		
		#############################
		# 取得開始の表示
		if inFLG_FirstDisp==True :
			wResDisp = CLS_MyDisp.sViewHeaderDisp( "スケジュール表示", False )
		
		#############################
		# 自動監視
		wTimeRes = CLS_OSIF.sTimeAddHour( inTimedate=gVal.STR_Time['autorun'], inSec=gVal.DEF_STR_TLNUM['forAutoAllRunSec'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "sTimeAddHour is failed(autorun)"
			gVal.OBJ_L.Log( "A", wTimeRes )
			return wRes
		
		wStr = "自動監視        ：" + str(gVal.STR_Time['autorun'])
		wStr = wStr + "  次回フル監視：" + str(wTimeRes['NextTD'])
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 自動監視シーケンス
		wTimeRes = CLS_OSIF.sTimeAddHour( inTimedate=gVal.STR_Time['autoseq'], inSec=gVal.DEF_STR_TLNUM['forAutoSeqSec'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "sTimeAddHour is failed(autoseq)"
			gVal.OBJ_L.Log( "A", wTimeRes )
			return wRes
		
		wStr = "シーケンス更新  ：" + str(gVal.STR_Time['autorun'])
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# リアクションチェック
		wTimeRes = CLS_OSIF.sTimeAddHour( inTimedate=gVal.STR_Time['reaction'], inSec=gVal.DEF_STR_TLNUM['forReactionSec'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "sTimeAddHour is failed(reaction)"
			gVal.OBJ_L.Log( "A", wTimeRes )
			return wRes
		
		wStr = "リアクション    ：" + str(gVal.STR_Time['reaction'])
		wStr = wStr + "  次回予定    ：" + str(wTimeRes['NextTD'])
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# リストいいね
		wTimeRes = CLS_OSIF.sTimeAddHour( inTimedate=gVal.STR_Time['mffavo'], inSec=gVal.DEF_STR_TLNUM['forListFavoSec'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "sTimeAddHour is failed(mffavo)"
			gVal.OBJ_L.Log( "A", wTimeRes )
			return wRes
		
		wStr = "リストいいね    ：" + str(gVal.STR_Time['mffavo'])
		wStr = wStr + "  次回予定    ：" + str(wTimeRes['NextTD'])
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# リストいいね
		wTimeRes = CLS_OSIF.sTimeAddHour( inTimedate=gVal.STR_Time['flfavo'], inSec=gVal.DEF_STR_TLNUM['forFollowerFavoSec'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "sTimeAddHour is failed(flfavo)"
			gVal.OBJ_L.Log( "A", wTimeRes )
			return wRes
		
		wStr = "フォロワー支援  ：" + str(gVal.STR_Time['flfavo'])
		wStr = wStr + "  次回予定    ：" + str(wTimeRes['NextTD'])
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# リスト通知クリア
		wStr = "リスト通知クリア：" + str(gVal.STR_Time['list_clear'])
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 自動リムーブ
		wTimeRes = CLS_OSIF.sTimeAddHour( inTimedate=gVal.STR_Time['auto_remove'], inSec=gVal.DEF_STR_TLNUM['forCheckAutoRemoveSec'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "sTimeAddHour is failed(auto_remove)"
			gVal.OBJ_L.Log( "A", wTimeRes )
			return wRes
		
		wStr = "自動リムーブ    ：" + str(gVal.STR_Time['auto_remove'])
		wStr = wStr + "  次回予定    ：" + str(wTimeRes['NextTD'])
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 自動リムーブ
		wTimeRes = CLS_OSIF.sTimeAddHour( inTimedate=gVal.STR_Time['send_favo'], inSec=gVal.DEF_VAL_WEEK )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "sTimeAddHour is failed(send_favo)"
			gVal.OBJ_L.Log( "A", wTimeRes )
			return wRes
		
		wStr = "いいね送信      ：" + str(gVal.STR_Time['send_favo'])
		wStr = wStr + "  次回予定    ：" + str(wTimeRes['NextTD'])
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# VIPリアクション
		wTimeRes = CLS_OSIF.sTimeAddHour( inTimedate=gVal.STR_Time['vip_ope'], inSec=gVal.DEF_STR_TLNUM['forVipOperationSec'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "sTimeAddHour is failed(vip_ope)"
			gVal.OBJ_L.Log( "A", wTimeRes )
			return wRes
		
		wStr = "VIPリアクション ：" + str(gVal.STR_Time['vip_ope'])
		wStr = wStr + "  次回予定    ：" + str(wTimeRes['NextTD'])
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 削除ツイート
		wTimeRes = CLS_OSIF.sTimeAddHour( inTimedate=gVal.STR_Time['del_tweet'], inSec=gVal.DEF_STR_TLNUM['forAutoTweetDeleteCycleSec'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "sTimeAddHour is failed(del_tweet)"
			gVal.OBJ_L.Log( "A", wTimeRes )
			return wRes
		
		wStr = "削除ツイート    ：" + str(gVal.STR_Time['del_tweet'])
		wStr = wStr + "  次回予定    ：" + str(wTimeRes['NextTD'])
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 自動削除
		wTimeRes = CLS_OSIF.sTimeAddHour( inTimedate=gVal.STR_Time['auto_delete'], inSec=gVal.DEF_STR_TLNUM['forCheckAutoDeleteSec'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "sTimeAddHour is failed(auto_delete)"
			gVal.OBJ_L.Log( "A", wTimeRes )
			return wRes
		
		wStr = "自動削除        ：" + str(gVal.STR_Time['auto_delete'])
		wStr = wStr + "  次回予定    ：" + str(wTimeRes['NextTD'])
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# タイムラインフォロー
		wTimeRes = CLS_OSIF.sTimeAddHour( inTimedate=gVal.STR_Time['tl_follow'], inSec=gVal.DEF_STR_TLNUM['forTimelineFollowSec'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "sTimeAddHour is failed(tl_follow)"
			gVal.OBJ_L.Log( "A", wTimeRes )
			return wRes
		
		wStr = "TLフォロー      ：" + str(gVal.STR_Time['tl_follow'])
		wStr = wStr + "  次回予定    ：" + str(wTimeRes['NextTD'])
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 自動キーワードいいね
		wTimeRes = CLS_OSIF.sTimeAddHour( inTimedate=gVal.STR_Time['keywordsrch'], inSec=gVal.DEF_STR_TLNUM['forAutoKeywordSearchFavoSec'] )
		if wTimeRes['Result']!=True :
			wRes['Reason'] = "sTimeAddHour is failed(keywordsrch)"
			gVal.OBJ_L.Log( "A", wTimeRes )
			return wRes
		
		wStr = "自動キーワード  ：" + str(gVal.STR_Time['keywordsrch'])
		wStr = wStr + "  次回予定    ：" + str(wTimeRes['NextTD'])
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# システム時刻
		wStr = "システム時刻    ：" + str(gVal.STR_Time['TimeDate']) + '\n'
		CLS_OSIF.sPrn( wStr )
		
		wRes['Result'] = True
		return wRes



#####################################################
# システム情報の表示
#####################################################
	def View_Sysinfo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterAdmin"
		wRes['Func']  = "View_Sysinfo"
		
		wStr = "情報収集中......" + '\n' ;
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# 枠作成
		wSTR_SystemInfo = {
			"now_TimeDate"		: None,
			
			"id"				: str(gVal.STR_UserInfo['id']),
			"screen_name"		: gVal.STR_UserInfo['Account'],
			
			"Prj_Client_Name"	: gVal.STR_SystemInfo['Client_Name'],
			"Prj_github"		: gVal.STR_SystemInfo['github'],
			"Prj_Admin"			: gVal.STR_SystemInfo['Admin'],
			"Prj_PythonVer"		: str( gVal.STR_SystemInfo['PythonVer'] ),
			"Prj_HostName"		: gVal.STR_SystemInfo['HostName'],
			
			"Twt_MyFollowNum"	: 0,
			"Twt_FollowerNum"	: 0,
			"Twt_FavoriteNum"	: 0,
			
			"DB_FavoUserNum"	: 0,
			"DB_LogNum"			: 0,
			
			"Sys_TrendTag"		: gVal.STR_UserInfo['TrendTag'],
			"Sys_QuestionTag"	: gVal.STR_UserInfo['QuestionTag'],
			"Sys_ListName"		: gVal.STR_UserInfo['ListName'],
			"Sys_AutoRemove"	: gVal.STR_UserInfo['AutoRemove'],
			"Sys_mListName"		: gVal.STR_UserInfo['mListName'],
###			"Sys_fListName"		: gVal.STR_UserInfo['fListName']
			"Sys_fListName"		: gVal.STR_UserInfo['fListName'],
			"Sys_VipTag"		: gVal.STR_UserInfo['VipTag'],
			"Sys_DelTag"		: gVal.STR_UserInfo['DelTag'],
			
			"Sys_MFvStop"		: gVal.STR_UserInfo['mfvstop'],
			"Sys_MFvStop_Date"	: gVal.STR_UserInfo['mfvstop_date']
		}
		
		#############################
		# 時間の取得
		wTDRes = CLS_TIME.sGet( wRes, "(1)" )
		wSTR_SystemInfo['now_TimeDate'] = str( wTDRes['TimeDate'] )
		
		#############################
		# フォロー一覧 取得
		wFollowRes = gVal.OBJ_Tw_IF.GetFollowerID()
		wSTR_SystemInfo['Twt_MyFollowNum'] = len( wFollowRes['MyFollowID'] )
		wSTR_SystemInfo['Twt_FollowerNum'] = len( wFollowRes['FollowerID'] )
		
		#############################
		# ふぁぼ一覧 取得
		wFavoRes = gVal.OBJ_Tw_IF.GetFavoData()
		wSTR_SystemInfo['Twt_FavoriteNum'] = len( wFavoRes )
		
		#############################
		# いいねDBレコード数の取得
		wDBRes = gVal.OBJ_DB_IF.GetRecordNum( "tbl_favouser_data" )
		if wDBRes['Result']!=True :
			wRes['Reason'] = "GetRecordNum is failed(tbl_favouser_data)"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wSTR_SystemInfo['DB_FavoUserNum'] = wDBRes['Responce']
		
		#############################
		# ログDBレコード数の取得
		wDBRes = gVal.OBJ_DB_IF.GetRecordNum( "tbl_log_data" )
		if wDBRes['Result']!=True :
			wRes['Reason'] = "GetRecordNum is failed(tbl_log_data)"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wSTR_SystemInfo['DB_LogNum'] = wDBRes['Responce']
		
		#############################
		# 画面表示
		wResDisp = CLS_MyDisp.sViewDisp( inDisp="SystemViewConsole", inIndex=-1, inData=wSTR_SystemInfo )
		if wResDisp['Result']==False :
			gVal.OBJ_L.Log( "B", wResDisp )
			return wRes
		
		#############################
		# 正常終了
		wRes['Result'] = True
		return wRes



